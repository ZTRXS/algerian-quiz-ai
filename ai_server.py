# ai_server.py - SMARTER AI
from flask import Flask, request, jsonify
import random
import json
from datetime import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class AlgerianQuizAI:
    def __init__(self):
        self.all_wilayas = [
            "أدرار", "الشلف", "الأغواط", "أم البواقي", "باتنة", "بجاية", "بسكرة", "بشار", "البليدة", "البويرة",
            "تمنراست", "تبسة", "تلمسان", "تيارت", "تيزي وزو", "الجزائر", "الجلفة", "جيجل", "سطيف", "سعيدة",
            "سكيكدة", "سيدي بلعباس", "عنابة", "قالمة", "قسنطينة", "المدية", "مستغانم", "المسيلة", "معسكر", "ورقلة",
            "وهران", "البيض", "إليزي", "برج بوعريريج", "بومرداس", "الطارف", "تندوف", "تيسمسيلت", "الوادي", "خنشلة",
            "سوق أهراس", "تيبازة", "ميلة", "عين الدفلى", "النعامة", "عين تموشنت", "غرداية", "غليزان", "تيميمون", "برج البحري",
            "أولاد جلال", "بني عباس", "عين صالح", "عين قزام", "تقرت", "جانت", "المغير", "المنيعة", "الرويبة"
        ]
        
        # REAL WILAYA INFORMATION
        self.wilaya_info = {
            "وهران": {
                "موقع": "شمال غرب الجزائر على ساحل البحر المتوسط",
                "مساحة": "2,121 كم²",
                "سكان": "1.6 مليون نسمة",
                "معالم": "قصر الباي، حجرة بائيس، شاطئ مداغ، المرفأ",
                "اقتصاد": "ميناء مهم، صناعات مختلفة، سياحة",
                "شخصية": "مرح، اجتماعي، يحب الفنون والموسيقى"
            },
            "الجزائر": {
                "موقع": "شمال الجزائر على ساحل البحر المتوسط",
                "مساحة": "273 كم²", 
                "سكان": "3.9 مليون نسمة",
                "معالم": "القصبة، كنيسة السيدة الإفريقية، مقام الشهيد",
                "اقتصاد": "عاصمة اقتصادية، ميناء، خدمات",
                "شخصية": "طموح، منظم، يحب الحياة العصرية"
            },
            "قسنطينة": {
                "موقع": "شمال شرق الجزائر في المنطقة الداخلية",
                "مساحة": "2,288 كم²",
                "سكان": "1.0 مليون نسمة", 
                "معالم": "جسور قسنطينة، قصر أحمد باي، وادي الرمال",
                "اقتصاد": "تعليم، صناعات خفيفة، سياحة",
                "شخصية": "فيلسوف، مفكر، يحب التاريخ والأدب"
            },
            "تيزي وزو": {
                "موقع": "شمال الجزائر في منطقة القبائل",
                "مساحة": "3,568 كم²",
                "سكان": "1.3 مليون نسمة",
                "معالم": "جبال جرجرة، غابات، تراث ثقافي غني",
                "اقتصاد": "زراعة، صناعات تقليدية، سياحة جبلية",
                "شخصية": "متجذر في التقاليد، عائلي، يحب الطبيعة"
            },
            "عنابة": {
                "موقع": "شمال شرق الجزائر على ساحل البحر المتوسط",
                "مساحة": "1,439 كم²",
                "سكان": "640 ألف نسمة",
                "معالم": "شواطئ جميلة، ميناء، مواقع تاريخية",
                "اقتصاد": "ميناء، صناعات، سياحة شاطئية",
                "شخصية": "هادئ، يحب الجمال الطبيعي، اجتماعي"
            },
            "باتنة": {
                "موقع": "شمال شرق الجزائر في الأوراس",
                "مساحة": "12,192 كم²", 
                "سكان": "1.1 مليون نسمة",
                "معالم": "جبال الأوراس، شلالات، مواقع أثرية",
                "اقتصاد": "زراعة، تربية المواشي، مناجم",
                "شخصية": "قوي، صادق، متصل بالطبيعة"
            },
            "سطيف": {
                "موقع": "شمال الجزائر في الهضاب العليا",
                "مساحة": "6,504 كم²",
                "سكان": "1.5 مليون نسمة",
                "معالم": "الحديقة الوطنية، مواقع تاريخية، فنادق",
                "اقتصاد": "زراعة، صناعات، تجارة",
                "شخصية": "متوازن، عملي، يحب التنوع"
            },
            "تلمسان": {
                "موقع": "شمال غرب الجزائر قرب الحدود المغربية",
                "مساحة": "9,061 كم²",
                "سكان": "950 ألف نسمة",
                "معالم": "مسجد تلمسان، القلعة، المناظر الطبيعية",
                "اقتصاد": "زراعة، صناعات تقليدية، سياحة",
                "شخصية": "راقي، يحب التاريخ، فني"
            }
        }
        
        # MUCH MORE VARIETY IN QUESTIONS
        self.question_templates = [
            # Lifestyle questions
            {"text": "ما هو نشاطك المفضل في العطلة؟", "category": "lifestyle"},
            {"text": "كيف تحب أن تقضي وقت فراغك؟", "category": "lifestyle"},
            {"text": "ما هو مكانك المفضل للاسترخاء؟", "category": "lifestyle"},
            {"text": "ما الذي يجعلك تشعر بالسعادة؟", "category": "lifestyle"},
            
            # Personality questions  
            {"text": "كيف تتعامل مع الضغوط؟", "category": "personality"},
            {"text": "ما هو أسلوبك في حل المشاكل؟", "category": "personality"},
            {"text": "كيف تتخذ القرارات المهمة؟", "category": "personality"},
            {"text": "ما هي صفتك الأبرز؟", "category": "personality"},
            
            # Social questions
            {"text": "كيف تفضل قضاء الوقت مع الآخرين؟", "category": "social"},
            {"text": "ما هو نوع التجمعات المفضل لديك؟", "category": "social"},
            {"text": "كيف تبني علاقاتك مع الناس؟", "category": "social"},
            {"text": "ما هو دورك في المجموعة؟", "category": "social"},
            
            # Adventure questions
            {"text": "ما هو نوع المغامرة المثالية لك؟", "category": "adventure"},
            {"text": "كيف تستمتع باكتشاف أماكن جديدة؟", "category": "adventure"},
            {"text": "ما هو التحدي الذي تود تجربته؟", "category": "adventure"},
            {"text": "ما الذي يثير فضولك؟", "category": "adventure"},
            
            # Food questions
            {"text": "ما هو طبقك الجزائري المفضل؟", "category": "food"},
            {"text": "كيف تفضل تناول وجباتك؟", "category": "food"},
            {"text": "ما هو المذاق المفضل لديك؟", "category": "food"},
            {"text": "أين تحب تناول الطعام؟", "category": "food"}
        ]
        
        # MUCH MORE VARIETY IN OPTIONS
        self.option_templates = [
            # Beach/Sea options
            {"text": "السباحة في البحر", "emoji": "🌊", "category": "beach"},
            {"text": "رياضات مائية", "emoji": "🏄", "category": "beach"},
            {"text": "شاطئ ورياضة", "emoji": "🏖️", "category": "beach"},
            {"text": "صيد بحري", "emoji": "🎣", "category": "beach"},
            
            # Mountain options
            {"text": "تسلق الجبال", "emoji": "⛰️", "category": "mountain"},
            {"text": "التخييم في الطبيعة", "emoji": "🏕️", "category": "mountain"},
            {"text": "استكشاف الغابات", "emoji": "🌲", "category": "mountain"},
            {"text": "رياضة مشي الجبال", "emoji": "🥾", "category": "mountain"},
            
            # City options
            {"text": "استكشاف المدن", "emoji": "🏙️", "category": "city"},
            {"text": "زيارة المتاحف", "emoji": "🏛️", "category": "city"},
            {"text": "التسوق في الأسواق", "emoji": "🛍️", "category": "city"},
            {"text": "مقاهي وحدائق", "emoji": "☕", "category": "city"},
            
            # Family options
            {"text": "وقت مع العائلة", "emoji": "👨‍👩‍👧‍👦", "category": "family"},
            {"text": "مناسبات عائلية", "emoji": "🎉", "category": "family"},
            {"text": "طبخ عائلي", "emoji": "🍲", "category": "family"},
            {"text": "رحلات عائلية", "emoji": "🚗", "category": "family"},
            
            # Friends options
            {"text": "حفلات مع الأصدقاء", "emoji": "🎊", "category": "friends"},
            {"text": "رياضة جماعية", "emoji": "⚽", "category": "friends"},
            {"text": "سهرات ودردشات", "emoji": "💬", "category": "friends"},
            {"text": "مشاريع مع الأصدقاء", "emoji": "🤝", "category": "friends"},
            
            # Adventure options
            {"text": "اكتشاف أماكن جديدة", "emoji": "🧭", "category": "adventure"},
            {"text": "رياضات متطرفة", "emoji": "🚵", "category": "adventure"},
            {"text": "رحلات برية", "emoji": "🗺️", "category": "adventure"},
            {"text": "تحديات شخصية", "emoji": "💪", "category": "adventure"},
            
            # Creative options
            {"text": "فنون وإبداع", "emoji": "🎨", "category": "creative"},
            {"text": "موسيقى وغناء", "emoji": "🎵", "category": "creative"},
            {"text": "كتابة وأدب", "emoji": "📖", "category": "creative"},
            {"text": "تصميم وحرف", "emoji": "✂️", "category": "creative"},
            
            # Relax options
            {"text": "قراءة واسترخاء", "emoji": "📚", "category": "relax"},
            {"text": "تأمل وهدوء", "emoji": "🧘", "category": "relax"},
            {"text": "عطلة استجمام", "emoji": "😴", "category": "relax"},
            {"text": "أنشطة هادئة", "emoji": "🕯️", "category": "relax"}
        ]

    def generate_unique_questions(self, user_id):
        """Generate COMPLETELY unique questions every time"""
        # Use timestamp + user_id for true randomness
        random.seed(datetime.now().timestamp() + hash(user_id))
        
        print(f"🎯 Generating questions for user: {user_id}")
        
        # Shuffle all questions and pick 4 unique ones
        shuffled_questions = self.question_templates.copy()
        random.shuffle(shuffled_questions)
        selected_questions = shuffled_questions[:4]
        
        questions = []
        for i, template in enumerate(selected_questions):
            question_id = f"q{i+1}_{int(datetime.now().timestamp())}_{random.randint(1000,9999)}"
            
            # Generate unique options for this question
            options = self.generate_unique_options()
            
            questions.append({
                "id": question_id,
                "text": template["text"],
                "category": template["category"],
                "options": options
            })
            
            print(f"📝 Generated question {i+1}: {template['text']}")
        
        print(f"✅ Generated {len(questions)} unique questions")
        return questions

    def generate_unique_options(self):
        """Generate COMPLETELY unique options"""
        # Shuffle all options and pick 4 unique ones
        shuffled_options = self.option_templates.copy()
        random.shuffle(shuffled_options)
        selected_options = shuffled_options[:4]
        
        # Get unique wilayas for these options
        shuffled_wilayas = self.all_wilayas.copy()
        random.shuffle(shuffled_wilayas)
        
        options = []
        for i, option_template in enumerate(selected_options):
            wilaya = shuffled_wilayas[i % len(shuffled_wilayas)]
            
            options.append({
                "text": option_template["text"],
                "emoji": option_template["emoji"],
                "wilaya": wilaya,
                "category": option_template["category"]
            })
        
        print(f"🎲 Generated {len(options)} unique options with wilayas: {[opt['wilaya'] for opt in options]}")
        return options

    def calculate_result(self, answers):
        """Calculate result with true randomness and return full info"""
        print(f"🧮 Calculating result for answers: {answers}")
        
        if not answers:
            wilaya = random.choice(self.all_wilayas)
            print(f"🎲 No answers, random wilaya: {wilaya}")
            return self.get_wilaya_full_info(wilaya)
        
        # Count wilaya votes
        wilaya_counts = {}
        for wilaya in answers.values():
            wilaya_counts[wilaya] = wilaya_counts.get(wilaya, 0) + 1
        
        print(f"📊 Wilaya counts: {wilaya_counts}")
        
        # Find most common wilaya(s)
        max_count = max(wilaya_counts.values())
        most_common = [w for w, count in wilaya_counts.items() if count == max_count]
        
        # If tie, pick randomly
        result_wilaya = random.choice(most_common)
        print(f"🏆 Result wilaya: {result_wilaya}")
        
        return self.get_wilaya_full_info(result_wilaya)

    def get_wilaya_full_info(self, wilaya_name):
        """Get complete information about a wilaya"""
        if wilaya_name in self.wilaya_info:
            info = self.wilaya_info[wilaya_name]
            return {
                "wilaya": wilaya_name,
                "info": info,
                "personality": self.generate_personality_description(wilaya_name, info)
            }
        else:
            # Fallback for wilayas without specific info
            return {
                "wilaya": wilaya_name,
                "info": {
                    "موقع": "منطقة جزائرية جميلة",
                    "مساحة": "متنوعة",
                    "سكان": "مختلف",
                    "معالم": "تراث وتاريخ غني",
                    "اقتصاد": "متنوع",
                    "شخصية": "فريدة ومميزة"
                },
                "personality": f"أنت من {wilaya_name}! 🌟 شخصيتك فريدة تجمع بين أصالة الجزائر وحداثتها. أنت تمثل التنوع والثراء الثقافي الذي تتميز به هذه الولاية."
            }

    def generate_personality_description(self, wilaya_name, info):
        """Generate unique personality description based on wilaya"""
        personalities = [
            f"أنت من {wilaya_name}! 🎉 {info['شخصية']} تمتاز بالطاقة الإيجابية والحب للحياة.",
            f"تهانينا! أنت {wilaya_name}! 🌟 {info['شخصية']} تحب التواصل مع الآخرين وتبني علاقات قوية.",
            f"واو! أنت {wilaya_name}! 💫 {info['شخصية']} لديك حكمة وتفكير عميق في الحياة.",
            f"مذهل! أنت {wilaya_name}! ✨ {info['شخصية']} تمتلك روحاً مغامرة وحباً للاستكشاف."
        ]
        return random.choice(personalities)

# Initialize AI
quiz_ai = AlgerianQuizAI()

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        
        print(f"🚀 Received quiz generation request from user: {user_id}")
        
        questions = quiz_ai.generate_unique_questions(user_id)
        
        response = {
            'success': True,
            'questions': questions,
            'timestamp': datetime.now().isoformat(),
            'message': 'تم توليد أسئلة فريدة باستخدام الذكاء الاصطناعي!',
            'debug': {
                'user_id': user_id,
                'questions_count': len(questions),
                'categories': [q['category'] for q in questions]
            }
        }
        
        print(f"✅ Sending response with {len(questions)} questions")
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Error generating quiz: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/calculate-result', methods=['POST'])
def calculate_result():
    try:
        data = request.json
        answers = data.get('answers', {})
        
        print(f"🧮 Received result calculation request with {len(answers)} answers")
        
        result = quiz_ai.calculate_result(answers)
        
        response = {
            'success': True,
            'result': result,
            'debug': {
                'answers_count': len(answers),
                'calculated_wilaya': result['wilaya']
            }
        }
        
        print(f"✅ Sending result: {result['wilaya']}")
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Error calculating result: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'AI Algerian Quiz Server is running! 🚀',
        'wilayas_count': len(quiz_ai.all_wilayas),
        'questions_variety': len(quiz_ai.question_templates),
        'options_variety': len(quiz_ai.option_templates),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'Algerian Quiz AI Server - Enhanced Version',
        'features': [
            'True random question generation',
            'Real wilaya information', 
            'Personality-based results',
            'Enhanced variety system'
        ],
        'endpoints': {
            'generate_quiz': 'POST /api/generate-quiz',
            'calculate_result': 'POST /api/calculate-result',
            'health': 'GET /api/health'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Algerian Quiz AI Server on port {port}")
    print(f"📊 Loaded {len(quiz_ai.all_wilayas)} wilayas")
    print(f"❓ Loaded {len(quiz_ai.question_templates)} question templates") 
    print(f"🎯 Loaded {len(quiz_ai.option_templates)} option templates")
    app.run(host='0.0.0.0', port=port, debug=False)
