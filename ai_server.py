from flask import Flask, request, jsonify, send_from_directory
import random
import json
from datetime import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows your website to connect to the AI

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
        
        self.question_patterns = {
            "weekend": ["ما هو عطلة نهاية الأسبوع المثالية بالنسبة لك؟", "كيف تحب أن تقضي عطلة نهاية الأسبوع؟"],
            "food": ["ما هو طعامك المفضل؟", "أي وجبة تفضل؟"],
            "personality": ["كيف تتعامل مع المشاكل؟", "ما هو أسلوبك في الحياة؟"],
            "travel": ["ما هي عطلتك المثالية؟", "أين تحب أن تسافر؟"],
            "hobbies": ["ما هي هوايتك المفضلة؟", "كيف تقضي وقت فراغك؟"],
            "social": ["كيف تقضي أمسياتك؟", "ما هو نمطك الاجتماعي؟"]
        }
        
        self.option_patterns = {
            "beach": ["يوم على الشاطئ", "السباحة في البحر", "نزهة شاطئية"],
            "shopping": ["التسوق في المولات", "شراء الملابس", "تسوق مع الأصدقاء"],
            "mountains": ["تسلق الجبال", "نزهة جبلية", "التخييم في الجبال"],
            "family": ["الاسترخاء مع العائلة", "وجبة عائلية", "وقت عائلي هادئ"],
            "friends": ["الخروج مع الأصدقاء", "حفلة مع الأصدقاء", "نشاط جماعي"],
            "adventure": ["مغامرة جديدة", "اكتشاف أماكن جديدة", "تحدي جديد"]
        }
        
        self.emojis = ["🏖️", "🛍️", "🏔️", "☕", "👨‍👩‍👧‍👦", "😂", "📝", "🧘", "🎵", "🍕"]

    def generate_unique_questions(self, user_id):
        """Generate completely unique questions every time"""
        random.seed(datetime.now().timestamp() + hash(user_id))
        
        questions = []
        
        for i in range(4):
            category = random.choice(list(self.question_patterns.keys()))
            question_text = random.choice(self.question_patterns[category])
            options = self.generate_unique_options()
            
            questions.append({
                "id": f"q{i+1}_{int(datetime.now().timestamp())}",
                "text": question_text,
                "options": options
            })
        
        return questions

    def generate_unique_options(self):
        """Generate unique options with random wilayas"""
        options = []
        used_wilayas = set()
        
        for i in range(4):
            available_wilayas = [w for w in self.all_wilayas if w not in used_wilayas]
            if not available_wilayas:
                available_wilayas = self.all_wilayas.copy()
                used_wilayas.clear()
            
            wilaya = random.choice(available_wilayas)
            used_wilayas.add(wilaya)
            
            option_type = random.choice(list(self.option_patterns.keys()))
            option_text = random.choice(self.option_patterns[option_type])
            emoji = random.choice(self.emojis)
            
            options.append({
                "text": option_text,
                "emoji": emoji,
                "wilaya": wilaya
            })
        
        return options

    def calculate_result(self, answers):
        """Calculate result with true randomness"""
        if not answers:
            return random.choice(self.all_wilayas)
        
        wilaya_counts = {}
        for wilaya in answers.values():
            wilaya_counts[wilaya] = wilaya_counts.get(wilaya, 0) + 1
        
        max_count = max(wilaya_counts.values())
        most_common = [w for w, count in wilaya_counts.items() if count == max_count]
        
        return random.choice(most_common)

# Initialize AI
quiz_ai = AlgerianQuizAI()

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        
        questions = quiz_ai.generate_unique_questions(user_id)
        
        return jsonify({
            'success': True,
            'questions': questions,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/calculate-result', methods=['POST'])
def calculate_result():
    try:
        data = request.json
        answers = data.get('answers', {})
        
        result = quiz_ai.calculate_result(answers)
        
        return jsonify({
            'success': True,
            'result_wilaya': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'AI Algerian Quiz Server is running! 🚀',
        'wilayas_count': len(quiz_ai.all_wilayas),
        'timestamp': datetime.now().isoformat()
    })

# Home page
@app.route('/')
def home():
    return jsonify({
        'message': 'Algerian Quiz AI Server',
        'endpoints': {
            'generate_quiz': 'POST /api/generate-quiz',
            'calculate_result': 'POST /api/calculate-result',
            'health': 'GET /api/health'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)