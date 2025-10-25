"""
MoodLens Simplified Flask App
Guided emotional wellness companion with unified emotion detection
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
from datetime import datetime
import base64
import io
from PIL import Image

# Import core modules
from src.core.emotion_detector import UnifiedEmotionDetector
from src.core.question_prompts import QuestionPrompts
from src.core.recommendation_engine import RecommendationEngine
from src.core.pattern_tracker import PatternTracker

# Import analysis modules for background processing
try:
    from src.analysis.advanced_face_analysis import AdvancedFaceEmotionAnalyzer
    from src.analysis.voice_tone_analyzer import VoiceToneAnalyzer
    FACE_ANALYZER_AVAILABLE = True
    VOICE_ANALYZER_AVAILABLE = True
except ImportError:
    print("⚠️ Advanced analyzers not available, using simplified mode")
    FACE_ANALYZER_AVAILABLE = False
    VOICE_ANALYZER_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'moodlens_simplified_secret_key_2024'

# Initialize components
emotion_detector = UnifiedEmotionDetector()
question_prompts = QuestionPrompts()
recommendation_engine = RecommendationEngine()
pattern_tracker = PatternTracker()

# Initialize analyzers if available
face_analyzer = None
voice_analyzer = None

if FACE_ANALYZER_AVAILABLE:
    try:
        face_analyzer = AdvancedFaceEmotionAnalyzer()
        print("✅ Face analyzer loaded")
    except Exception as e:
        print(f"❌ Face analyzer failed to load: {e}")
        face_analyzer = None

if VOICE_ANALYZER_AVAILABLE:
    try:
        voice_analyzer = VoiceToneAnalyzer()
        print("✅ Voice tone analyzer loaded")
    except Exception as e:
        print(f"❌ Voice tone analyzer failed to load: {e}")
        voice_analyzer = None

@app.route('/')
def index():
    """Main check-in page"""
    return render_template('check_in.html')

@app.route('/api/questions')
def get_questions():
    """Get initial categorization questions"""
    questions = question_prompts.get_initial_questions()
    return jsonify({
        'questions': questions,
        'welcome_message': question_prompts.get_random_welcome(),
        'total_questions': question_prompts.get_initial_question_count()
    })

@app.route('/api/journaling-prompts', methods=['POST'])
def get_journaling_prompts():
    """Get journaling prompts based on initial responses"""
    try:
        data = request.get_json()
        initial_responses = data.get('responses', {})
        
        # Determine emotion category
        emotion_category = question_prompts.determine_emotion_category(initial_responses)
        
        # Get journaling prompts for that category
        journaling_prompts = question_prompts.get_journaling_prompts(emotion_category)
        
        return jsonify({
            'emotion_category': emotion_category,
            'journaling_prompts': journaling_prompts,
            'total_prompts': len(journaling_prompts)
        })
        
    except Exception as e:
        print(f"Error getting journaling prompts: {e}")
        return jsonify({'error': 'Failed to get journaling prompts'}), 500

@app.route('/api/voice-prompts')
def get_voice_prompts():
    """Get voice analysis prompts"""
    prompts = question_prompts.get_voice_prompts()
    return jsonify({
        'voice_prompts': prompts,
        'total_prompts': len(prompts)
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion from initial responses, journaling, and optional face/voice data"""
    try:
        data = request.get_json()
        initial_responses = data.get('initial_responses', {})
        journaling_responses = data.get('journaling_responses', {})
        face_image_data = data.get('face_image', None)
        voice_audio_data = data.get('voice_audio', None)
        
        # Validate initial responses
        for question_id, response in initial_responses.items():
            if not question_prompts.validate_initial_response(question_id, response):
                return jsonify({'error': f'Invalid response for {question_id}'}), 400
        
        # Process face data if provided
        face_data = None
        if face_image_data and face_analyzer:
            try:
                # Decode base64 image
                image_data = base64.b64decode(face_image_data.split(',')[1])
                image = Image.open(io.BytesIO(image_data))
                
                # Save temporary image
                temp_path = 'temp_face.jpg'
                image.save(temp_path)
                
                # Analyze face
                face_result = face_analyzer.analyze_complete_face(temp_path)
                face_data = face_result
                
                # Clean up
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            except Exception as e:
                print(f"Face analysis error: {e}")
                face_data = None
        
        # Process voice data if provided
        voice_data = None
        if voice_audio_data and voice_analyzer:
            try:
                # Decode base64 audio
                audio_data = base64.b64decode(voice_audio_data.split(',')[1])
                
                # Save temporary audio
                temp_path = 'temp_voice.wav'
                with open(temp_path, 'wb') as f:
                    f.write(audio_data)
                
                # Analyze voice tone characteristics
                voice_result = voice_analyzer.analyze_complete_voice(temp_path)
                voice_data = voice_result
                
                # Clean up
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            except Exception as e:
                print(f"Voice tone analysis error: {e}")
                voice_data = None
        
        # Detect emotion using unified detector
        emotion_result = emotion_detector.detect_emotion(
            initial_responses,
            journaling_responses,
            face_data, 
            voice_data
        )
        
        # Add pattern tracking
        pattern_tracker.add_check_in(emotion_result, {**initial_responses, **journaling_responses})
        
        # Format actions for UI
        immediate_actions = []
        for action in emotion_result['immediate_actions']:
            formatted_action = recommendation_engine.format_action_for_ui(action)
            immediate_actions.append(formatted_action)
        
        short_term_actions = []
        for action in emotion_result['short_term_actions']:
            formatted_action = recommendation_engine.format_action_for_ui(action)
            short_term_actions.append(formatted_action)
        
        # Prepare response
        response = {
            'emotion': emotion_result['emotion'],
            'emotion_name': emotion_result['emotion_name'],
            'emotion_emoji': emotion_result['emotion_emoji'],
            'confidence': emotion_result['confidence'],
            'description': emotion_result['description'],
            'indicators': emotion_result['indicators'],
            'immediate_actions': immediate_actions,
            'short_term_actions': short_term_actions,
            'analysis_details': {
                'initial_questions_used': len(initial_responses),
                'journaling_responses_used': len(journaling_responses),
                'face_analyzed': face_data is not None,
                'voice_analyzed': voice_data is not None,
                'confidence_level': 'high' if emotion_result['confidence'] > 0.7 else 'medium' if emotion_result['confidence'] > 0.5 else 'low'
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({'error': 'Analysis failed'}), 500

@app.route('/api/action/<action_name>')
def get_action_details(action_name):
    """Get detailed information about a specific action"""
    try:
        action_details = recommendation_engine.get_action_details(action_name)
        action_type_info = recommendation_engine.get_action_type_info(action_details['type'])
        
        return jsonify({
            'name': action_name,
            'type': action_details['type'],
            'type_name': action_type_info['name'],
            'type_icon': action_type_info['icon'],
            'duration': action_details['duration'],
            'instructions': action_details['instructions'],
            'audio_guide': action_details['audio_guide'],
            'difficulty': action_details['difficulty'],
            'description': action_type_info['description']
        })
        
    except Exception as e:
        print(f"Error getting action details: {e}")
        return jsonify({'error': 'Action not found'}), 404

@app.route('/api/audio-script/<script_type>')
def get_audio_script(script_type):
    """Get audio script for guided exercises"""
    try:
        if script_type == 'breathing':
            script = recommendation_engine.get_breathing_audio_script()
        elif script_type == 'grounding':
            script = recommendation_engine.get_grounding_audio_script()
        elif script_type == 'body_scan':
            script = recommendation_engine.get_body_scan_audio_script()
        else:
            return jsonify({'error': 'Script type not found'}), 404
        
        return jsonify({
            'script': script,
            'type': script_type
        })
        
    except Exception as e:
        print(f"Error getting audio script: {e}")
        return jsonify({'error': 'Script not found'}), 404

@app.route('/api/patterns')
def get_patterns():
    """Get emotional pattern summary"""
    try:
        days = request.args.get('days', 7, type=int)
        summary = pattern_tracker.get_pattern_summary(days)
        return jsonify(summary)
        
    except Exception as e:
        print(f"Error getting patterns: {e}")
        return jsonify({'error': 'Patterns not available'}), 500

@app.route('/api/emergency')
def get_emergency_resources():
    """Get emergency resources"""
    try:
        resources = recommendation_engine.get_emergency_resources()
        return jsonify(resources)
        
    except Exception as e:
        print(f"Error getting emergency resources: {e}")
        return jsonify({'error': 'Resources not available'}), 500

@app.route('/history')
def history():
    """Pattern history page"""
    return render_template('history.html')

@app.route('/results')
def results():
    """Results page"""
    return render_template('results.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'system': 'MoodLens Simplified',
        'components': {
            'emotion_detector': True,
            'question_prompts': True,
            'recommendation_engine': True,
            'pattern_tracker': True,
            'face_analyzer': face_analyzer is not None,
            'voice_analyzer': voice_analyzer is not None
        }
    })

if __name__ == '__main__':
    print("🧠 Starting MoodLens Simplified...")
    print("=" * 50)
    print("✨ Guided Emotional Wellness Companion")
    print("📱 Web interface: http://localhost:5001")
    print("🔍 Health check: http://localhost:5001/health")
    print("=" * 50)
    
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(host='0.0.0.0', port=5001, debug=True)

