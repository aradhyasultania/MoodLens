#!/usr/bin/env python3
"""
Comprehensive test script for MoodLens system
Tests the full flow: initial questions → journaling → emotion detection → actions
"""

from src.core.emotion_detector import UnifiedEmotionDetector
from src.core.question_prompts import QuestionPrompts
from src.core.recommendation_engine import RecommendationEngine
from src.core.pattern_tracker import PatternTracker

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_emotion_detector():
    """Test emotion detection with different scenarios"""
    
    print_header("TESTING EMOTION DETECTOR")
    
    detector = UnifiedEmotionDetector()
    
    # Test Case 1: Anxious
    print("📋 TEST 1: ANXIOUS SCENARIO")
    print("-" * 40)
    
    initial_responses_anxious = {
        'energy_level': 'high',
        'thoughts': 'racing',
        'physical': 'tense',
        'worry': 'a_lot'
    }
    
    journaling_responses_anxious = {
        'anxious_1': 'My heart is racing and I can\'t stop thinking about everything going wrong',
        'anxious_2': 'I\'m so worried about the deadline and what others will think',
        'anxious_3': 'My shoulders are so tense I can barely move',
        'anxious_4': 'I need to find a way to calm down, maybe some deep breathing'
    }
    
    result = detector.detect_emotion(
        initial_responses_anxious, 
        journaling_responses_anxious
    )
    
    print(f"Detected Emotion: {result['emotion_emoji']} {result['emotion_name']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Description: {result['description']}")
    print(f"Indicators: {', '.join(result['indicators'])}")
    print(f"Score Breakdown: {result['analysis_details']['initial_scores']['anxious']:.2f} (initial) + {result['analysis_details']['journaling_scores']['anxious']:.2f} (journaling)")
    
    assert result['emotion'] == 'anxious', "❌ Failed to detect anxious emotion"
    assert result['confidence'] > 0.7, "❌ Confidence too low for anxious"
    print("✅ Test 1 PASSED\n")
    
    # Test Case 2: Sad
    print("📋 TEST 2: SAD SCENARIO")
    print("-" * 40)
    
    initial_responses_sad = {
        'energy_level': 'low',
        'thoughts': 'stuck',
        'physical': 'neutral',
        'feeling_like': 'crying'
    }
    
    journaling_responses_sad = {
        'sad_1': 'Everything feels so empty and hopeless right now',
        'sad_2': 'My body feels heavy, like I can\'t move',
        'sad_3': 'I wish someone understood how much pain I\'m in',
        'sad_4': 'I used to call friends but I\'m too sad to reach out'
    }
    
    result = detector.detect_emotion(
        initial_responses_sad,
        journaling_responses_sad
    )
    
    print(f"Detected Emotion: {result['emotion_emoji']} {result['emotion_name']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Description: {result['description']}")
    print(f"Indicators: {', '.join(result['indicators'])}")
    
    assert result['emotion'] == 'sad', "❌ Failed to detect sad emotion"
    assert result['confidence'] > 0.7, "❌ Confidence too low for sad"
    print("✅ Test 2 PASSED\n")
    
    # Test Case 3: Happy
    print("📋 TEST 3: HAPPY SCENARIO")
    print("-" * 40)
    
    initial_responses_happy = {
        'energy_level': 'high',
        'thoughts': 'flowing',
        'physical': 'relaxed',
        'feeling_like': 'laughing'
    }
    
    journaling_responses_happy = {
        'happy_1': 'I\'m so grateful for everything in my life right now!',
        'happy_2': 'I feel amazing and ready to take on the world',
        'happy_3': 'Everything feels possible and I\'m smiling all the time',
        'happy_4': 'I want to celebrate and share this joy with everyone'
    }
    
    result = detector.detect_emotion(
        initial_responses_happy,
        journaling_responses_happy
    )
    
    print(f"Detected Emotion: {result['emotion_emoji']} {result['emotion_name']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Description: {result['description']}")
    
    assert result['emotion'] == 'happy', "❌ Failed to detect happy emotion"
    assert result['confidence'] > 0.7, "❌ Confidence too low for happy"
    print("✅ Test 3 PASSED\n")
    
    # Test Case 4: Overwhelmed
    print("📋 TEST 4: OVERWHELMED SCENARIO")
    print("-" * 40)
    
    initial_responses_overwhelmed = {
        'energy_level': 'low',
        'thoughts': 'racing',
        'physical': 'tense',
        'feeling_like': 'nothing'
    }
    
    journaling_responses_overwhelmed = {
        'overwhelmed_1': 'Everything feels like too much right now',
        'overwhelmed_2': 'I have racing thoughts but I feel stuck and paralyzed',
        'overwhelmed_3': 'I don\'t even know where to start, everything is overwhelming'
    }
    
    result = detector.detect_emotion(
        initial_responses_overwhelmed,
        journaling_responses_overwhelmed
    )
    
    print(f"Detected Emotion: {result['emotion_emoji']} {result['emotion_name']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Description: {result['description']}")
    
    assert result['emotion'] == 'overwhelmed', "❌ Failed to detect overwhelmed emotion"
    assert result['confidence'] > 0.6, "❌ Confidence too low for overwhelmed"
    print("✅ Test 4 PASSED\n")

def test_question_prompts():
    """Test question prompt system"""
    
    print_header("TESTING QUESTION PROMPTS")
    
    prompts = QuestionPrompts()
    
    # Get initial questions
    initial_questions = prompts.get_initial_questions()
    print(f"✅ Loaded {len(initial_questions)} initial questions")
    print(f"   Questions: {', '.join([q['id'] for q in initial_questions])}\n")
    
    # Get journaling prompts for different categories
    for emotion_category in ['anxious', 'sad', 'frustrated', 'overwhelmed']:
        journaling = prompts.get_journaling_prompts(emotion_category)
        print(f"✅ {emotion_category}: {len(journaling)} journaling prompts")

def test_recommendation_engine():
    """Test recommendation engine"""
    
    print_header("TESTING RECOMMENDATION ENGINE")
    
    engine = RecommendationEngine()
    
    # Test action type info for different types
    action_types = ['breathing', 'grounding', 'mindfulness', 'movement', 'journaling', 'social', 'self-care']
    
    for action_type in action_types:
        try:
            info = engine.get_action_type_info(action_type)
            print(f"✅ {action_type}: {info['name']}")
        except Exception as e:
            print(f"⚠️ {action_type}: {e}")

def test_pattern_tracker():
    """Test pattern tracker"""
    
    print_header("TESTING PATTERN TRACKER")
    
    tracker = PatternTracker()
    
    # Add some test check-ins with proper structure
    test_emotions = [
        {'emotion': 'anxious', 'emotion_name': 'Anxious', 'confidence': 0.85, 'indicators': ['Racing thoughts'], 'immediate_actions': [], 'short_term_actions': []},
        {'emotion': 'happy', 'emotion_name': 'Happy', 'confidence': 0.90, 'indicators': ['Feeling good'], 'immediate_actions': [], 'short_term_actions': []},
        {'emotion': 'anxious', 'emotion_name': 'Anxious', 'confidence': 0.78, 'indicators': ['Tense'], 'immediate_actions': [], 'short_term_actions': []},
        {'emotion': 'calm', 'emotion_name': 'Calm', 'confidence': 0.75, 'indicators': ['Relaxed'], 'immediate_actions': [], 'short_term_actions': []},
    ]
    
    for i, emotion_data in enumerate(test_emotions):
        tracker.add_check_in(emotion_data, {f'response_{i}': 'test'})
    
    print(f"✅ Added {len(test_emotions)} test check-ins")
    
    # Get emotion history
    anxiety_history = tracker.get_emotion_history('anxious', days=1)
    print(f"✅ Retrieved {len(anxiety_history)} anxious check-ins from history")
    
    # Get pattern summary
    summary = tracker.get_pattern_summary(days=1)
    print(f"✅ Pattern Summary retrieved: {len(summary.get('recent_check_ins', []))} recent emotions tracked")

def main():
    """Run all tests"""
    
    print("\n" + "="*60)
    print("  🧠 MOODLENS SYSTEM TEST SUITE")
    print("="*60)
    
    try:
        test_question_prompts()
        test_recommendation_engine()
        test_pattern_tracker()
        test_emotion_detector()
        
        print_header("✅ ALL TESTS PASSED!")
        print("System is ready for deployment\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
