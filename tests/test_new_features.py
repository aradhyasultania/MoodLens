#!/usr/bin/env python3
"""
Test script for MoodLens Journaling and Voice Characteristics System
Demonstrates the new directed journaling prompts and voice characteristic analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from journaling_prompts import JournalingPrompts
from advanced_voice_analysis import AdvancedVoiceEmotionAnalyzer

def test_journaling_system():
    """Test the journaling prompts system"""
    print("🧠 TESTING JOURNALING SYSTEM")
    print("=" * 50)
    
    prompts = JournalingPrompts()
    
    # Test screening questions
    print("\n📋 Screening Questions:")
    screening_questions = prompts.get_screening_questions()
    for i, question in enumerate(screening_questions, 1):
        print(f"{i}. {question['question']}")
        if question['type'] == 'single_choice':
            print(f"   Options: {', '.join(question['options'])}")
        print()
    
    # Test follow-up determination
    print("🎯 Testing Follow-up Determination:")
    test_responses = {
        'energy_screening': 8,
        'mood_screening': 'uplifted',
        'stress_screening': 'moderate'
    }
    
    print(f"Screening responses: {test_responses}")
    category, subcategory = prompts.determine_follow_up_category(test_responses)
    print(f"Determined category: {category} -> {subcategory}")
    
    # Get journaling prompts
    journaling_prompts_list = prompts.get_journaling_prompts(category, subcategory)
    print(f"\n📝 Journaling Prompts ({len(journaling_prompts_list)} prompts):")
    for i, prompt in enumerate(journaling_prompts_list, 1):
        print(f"{i}. {prompt['question']}")
        print(f"   Type: {prompt['prompt_type']}")
        print(f"   Expected emotions: {', '.join(prompt['expected_emotions'])}")
        print()
    
    # Test voice prompts
    print("🎤 Voice Analysis Prompts:")
    voice_prompts = prompts.get_voice_prompts()
    for i, prompt in enumerate(voice_prompts, 1):
        print(f"{i}. \"{prompt['text']}\"")
        print(f"   Purpose: {prompt['purpose']}")
        print(f"   Analysis focus: {', '.join(prompt['analysis_focus'])}")
        print()

def test_voice_characteristics():
    """Test the voice characteristics analysis"""
    print("\n🎤 TESTING VOICE CHARACTERISTICS ANALYSIS")
    print("=" * 50)
    
    analyzer = AdvancedVoiceEmotionAnalyzer()
    
    # Test voice prompts
    voice_prompts = [
        "The quick brown fox jumps over the lazy dog.",
        "I feel calm and peaceful right now.",
        "Today has been challenging but I'm managing.",
        "I'm excited about what's coming next."
    ]
    
    print("🎙️ Voice Analysis Prompts:")
    for i, prompt in enumerate(voice_prompts, 1):
        print(f"{i}. \"{prompt}\"")
    print()
    
    print("📊 This would analyze:")
    print("   🎵 Pitch patterns and stability")
    print("   🗣️ Speech rate and rhythm") 
    print("   😰 Stress indicators and tension")
    print("   🎭 Emotional tone and warmth")
    print("   💪 Confidence level")
    print("   🔥 Voice warmth")
    print()
    
    print("⚠️ Note: This requires actual audio recording to test fully")
    print("   Run the analyzer.analyze_voice_characteristics() method")
    print("   with microphone access to see full results")

def demonstrate_workflow():
    """Demonstrate the complete workflow"""
    print("\n🔄 COMPLETE WORKFLOW DEMONSTRATION")
    print("=" * 50)
    
    prompts = JournalingPrompts()
    
    print("1. 📋 User answers screening questions:")
    screening_responses = {
        'energy_screening': 3,  # Low energy
        'mood_screening': 'down',
        'stress_screening': 'high'
    }
    print(f"   Responses: {screening_responses}")
    
    print("\n2. 🎯 System determines follow-up category:")
    category, subcategory = prompts.determine_follow_up_category(screening_responses)
    print(f"   Category: {category} -> {subcategory}")
    
    print("\n3. 📝 System provides directed journaling prompts:")
    journaling_prompts_list = prompts.get_journaling_prompts(category, subcategory)
    print(f"   {len(journaling_prompts_list)} prompts provided")
    for prompt in journaling_prompts_list[:2]:  # Show first 2
        print(f"   - {prompt['question']}")
    
    print("\n4. ✍️ User writes journaling responses")
    print("   (These would be analyzed by the text analyzer)")
    
    print("\n5. 🎤 User records voice characteristics:")
    voice_prompts = prompts.get_voice_prompts()
    print(f"   {len(voice_prompts)} standardized phrases to say")
    for prompt in voice_prompts[:2]:  # Show first 2
        print(f"   - \"{prompt['text']}\"")
    
    print("\n6. 🔍 System analyzes voice characteristics:")
    print("   - Pitch stability")
    print("   - Speech rate")
    print("   - Voice tension")
    print("   - Emotional tone")
    print("   - Stress level")
    
    print("\n7. 🧠 Combined analysis provides:")
    print("   - Overall emotional state")
    print("   - Personalized recommendations")
    print("   - Actionable insights")

if __name__ == "__main__":
    print("MoodLens Journaling & Voice Characteristics Test")
    print("=" * 60)
    
    try:
        test_journaling_system()
        test_voice_characteristics()
        demonstrate_workflow()
        
        print("\n✅ All tests completed successfully!")
        print("\n🚀 To use the full system:")
        print("   1. Run: python moodlens_api.py")
        print("   2. Visit: http://localhost:5001")
        print("   3. Use the new journaling and voice analysis features")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
