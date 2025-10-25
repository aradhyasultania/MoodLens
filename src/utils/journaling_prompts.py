"""
Journaling Prompts for MoodLens Guided Check-in
Directed questions designed to help users express their emotional state through writing
"""

class JournalingPrompts:
    def __init__(self):
        # Initial screening questions to determine emotional direction
        self.screening_questions = [
            {
                'id': 'energy_screening',
                'question': 'On a scale of 1-10, how would you rate your current energy level?',
                'type': 'scale',
                'follow_up_category': 'energy_based'
            },
            {
                'id': 'mood_screening',
                'question': 'Which word best describes your overall mood right now?',
                'type': 'single_choice',
                'options': ['uplifted', 'neutral', 'down', 'mixed', 'overwhelmed'],
                'follow_up_category': 'mood_based'
            },
            {
                'id': 'stress_screening',
                'question': 'How much stress are you feeling right now?',
                'type': 'single_choice',
                'options': ['none', 'a little', 'moderate', 'high', 'overwhelming'],
                'follow_up_category': 'stress_based'
            }
        ]
        
        # Directed journaling prompts based on screening results
        self.journaling_prompts = {
            'energy_based': {
                'high_energy': [
                    {
                        'id': 'high_energy_1',
                        'question': 'What is energizing you right now? Describe the source of this energy.',
                        'prompt_type': 'reflective',
                        'expected_emotions': ['excited', 'motivated', 'enthusiastic', 'confident']
                    },
                    {
                        'id': 'high_energy_2',
                        'question': 'How does this energy feel in your body? What physical sensations are you noticing?',
                        'prompt_type': 'body_awareness',
                        'expected_emotions': ['energized', 'alert', 'ready', 'powerful']
                    },
                    {
                        'id': 'high_energy_3',
                        'question': 'What would you like to do with this energy? What feels most important right now?',
                        'prompt_type': 'action_oriented',
                        'expected_emotions': ['determined', 'focused', 'ambitious', 'hopeful']
                    }
                ],
                'low_energy': [
                    {
                        'id': 'low_energy_1',
                        'question': 'What feels heavy or draining right now? What is weighing on you?',
                        'prompt_type': 'reflective',
                        'expected_emotions': ['tired', 'exhausted', 'overwhelmed', 'burdened']
                    },
                    {
                        'id': 'low_energy_2',
                        'question': 'How long have you been feeling this way? What might have contributed to this?',
                        'prompt_type': 'temporal',
                        'expected_emotions': ['fatigued', 'drained', 'disappointed', 'frustrated']
                    },
                    {
                        'id': 'low_energy_3',
                        'question': 'What would help you feel more energized? What do you need right now?',
                        'prompt_type': 'solution_focused',
                        'expected_emotions': ['hopeful', 'motivated', 'grateful', 'optimistic']
                    }
                ]
            },
            'mood_based': {
                'uplifted': [
                    {
                        'id': 'uplifted_1',
                        'question': 'What is bringing you joy or satisfaction right now? Describe what feels good.',
                        'prompt_type': 'positive_focus',
                        'expected_emotions': ['happy', 'content', 'grateful', 'pleased']
                    },
                    {
                        'id': 'uplifted_2',
                        'question': 'How does this positive feeling show up in your body and thoughts?',
                        'prompt_type': 'embodied',
                        'expected_emotions': ['light', 'open', 'warm', 'expansive']
                    }
                ],
                'down': [
                    {
                        'id': 'down_1',
                        'question': 'What is making you feel down? Describe what feels difficult or painful.',
                        'prompt_type': 'emotional_exploration',
                        'expected_emotions': ['sad', 'disappointed', 'hurt', 'lonely']
                    },
                    {
                        'id': 'down_2',
                        'question': 'How does this sadness or disappointment feel in your body?',
                        'prompt_type': 'body_awareness',
                        'expected_emotions': ['heavy', 'tight', 'empty', 'aching']
                    },
                    {
                        'id': 'down_3',
                        'question': 'What would comfort you right now? What do you need to feel supported?',
                        'prompt_type': 'needs_focused',
                        'expected_emotions': ['cared_for', 'understood', 'safe', 'hopeful']
                    }
                ],
                'mixed': [
                    {
                        'id': 'mixed_1',
                        'question': 'Describe the different emotions you\'re experiencing right now. What feels conflicting?',
                        'prompt_type': 'complex_emotions',
                        'expected_emotions': ['confused', 'torn', 'ambivalent', 'uncertain']
                    },
                    {
                        'id': 'mixed_2',
                        'question': 'What situations or thoughts are creating these mixed feelings?',
                        'prompt_type': 'situational',
                        'expected_emotions': ['conflicted', 'torn', 'unsure', 'complex']
                    }
                ],
                'overwhelmed': [
                    {
                        'id': 'overwhelmed_1',
                        'question': 'What feels like too much right now? What is overwhelming you?',
                        'prompt_type': 'stress_identification',
                        'expected_emotions': ['overwhelmed', 'stressed', 'anxious', 'pressured']
                    },
                    {
                        'id': 'overwhelmed_2',
                        'question': 'How does this overwhelm feel in your body? What physical sensations do you notice?',
                        'prompt_type': 'body_awareness',
                        'expected_emotions': ['tense', 'restless', 'tight', 'scattered']
                    },
                    {
                        'id': 'overwhelmed_3',
                        'question': 'What would help you feel more grounded and centered right now?',
                        'prompt_type': 'grounding',
                        'expected_emotions': ['calm', 'centered', 'focused', 'peaceful']
                    }
                ]
            },
            'stress_based': {
                'high_stress': [
                    {
                        'id': 'high_stress_1',
                        'question': 'What specific situations or thoughts are causing you stress right now?',
                        'prompt_type': 'stress_source',
                        'expected_emotions': ['anxious', 'worried', 'pressured', 'stressed']
                    },
                    {
                        'id': 'high_stress_2',
                        'question': 'How is this stress affecting your body? Describe any tension or discomfort.',
                        'prompt_type': 'physical_stress',
                        'expected_emotions': ['tense', 'restless', 'tight', 'uncomfortable']
                    },
                    {
                        'id': 'high_stress_3',
                        'question': 'What coping strategies have helped you in similar situations before?',
                        'prompt_type': 'coping_exploration',
                        'expected_emotions': ['hopeful', 'resourceful', 'confident', 'prepared']
                    }
                ],
                'moderate_stress': [
                    {
                        'id': 'moderate_stress_1',
                        'question': 'What challenges are you facing that feel manageable but still present?',
                        'prompt_type': 'challenge_identification',
                        'expected_emotions': ['concerned', 'focused', 'determined', 'cautious']
                    },
                    {
                        'id': 'moderate_stress_2',
                        'question': 'How are you currently handling these challenges? What\'s working?',
                        'prompt_type': 'strategy_assessment',
                        'expected_emotions': ['confident', 'competent', 'resourceful', 'hopeful']
                    }
                ]
            }
        }
        
        # Voice analysis prompts - standardized phrases for voice characteristic analysis
        self.voice_prompts = [
            {
                'id': 'voice_prompt_1',
                'text': 'The quick brown fox jumps over the lazy dog.',
                'purpose': 'neutral_baseline',
                'analysis_focus': ['pitch_stability', 'speech_rate', 'voice_clarity']
            },
            {
                'id': 'voice_prompt_2',
                'text': 'I feel calm and peaceful right now.',
                'purpose': 'emotional_expression',
                'analysis_focus': ['emotional_tone', 'voice_warmth', 'relaxation_indicators']
            },
            {
                'id': 'voice_prompt_3',
                'text': 'Today has been challenging but I\'m managing.',
                'purpose': 'stress_expression',
                'analysis_focus': ['stress_indicators', 'voice_tension', 'emotional_load']
            },
            {
                'id': 'voice_prompt_4',
                'text': 'I\'m excited about what\'s coming next.',
                'purpose': 'positive_expression',
                'analysis_focus': ['energy_level', 'voice_brightness', 'enthusiasm_indicators']
            }
        ]
        
        # Welcome and encouragement messages
        self.welcome_messages = [
            "Let's take a moment to check in with how you're feeling",
            "I'm here to help you explore your current emotional state",
            "Take your time to reflect and share what's on your mind",
            "Let's discover together what you're experiencing right now",
            "This is a safe space to express your feelings"
        ]
        
        self.encouragement_messages = [
            "Thank you for sharing that with me",
            "Your honesty helps me understand you better",
            "That's really helpful to know",
            "I appreciate you taking the time to reflect",
            "Thank you for being open about your experience"
        ]
        
        self.transition_messages = [
            "Now let's explore this a bit deeper",
            "I'd like to understand more about this",
            "Let's dive a little deeper into this feeling",
            "Can you tell me more about this?",
            "I'm curious to learn more about your experience"
        ]
    
    def get_screening_questions(self):
        """Get all screening questions"""
        return self.screening_questions
    
    def get_journaling_prompts(self, category, subcategory):
        """Get journaling prompts based on screening results"""
        if category in self.journaling_prompts and subcategory in self.journaling_prompts[category]:
            return self.journaling_prompts[category][subcategory]
        return []
    
    def get_voice_prompts(self):
        """Get standardized voice analysis prompts"""
        return self.voice_prompts
    
    def get_random_welcome(self):
        """Get a random welcome message"""
        import random
        return random.choice(self.welcome_messages)
    
    def get_random_encouragement(self):
        """Get a random encouragement message"""
        import random
        return random.choice(self.encouragement_messages)
    
    def get_random_transition(self):
        """Get a random transition message"""
        import random
        return random.choice(self.transition_messages)
    
    def determine_follow_up_category(self, screening_responses):
        """Determine which journaling prompts to use based on screening responses"""
        # Analyze screening responses to determine emotional direction
        energy_score = screening_responses.get('energy_screening', 5)
        mood_response = screening_responses.get('mood_screening', 'neutral')
        stress_response = screening_responses.get('stress_screening', 'moderate')
        
        # Determine primary category based on responses
        if energy_score >= 7:
            return 'energy_based', 'high_energy'
        elif energy_score <= 4:
            return 'energy_based', 'low_energy'
        elif mood_response in ['uplifted', 'down', 'mixed', 'overwhelmed']:
            return 'mood_based', mood_response
        elif stress_response in ['high', 'overwhelming']:
            return 'stress_based', 'high_stress'
        elif stress_response in ['moderate', 'a little']:
            return 'stress_based', 'moderate_stress'
        else:
            return 'mood_based', 'neutral'
    
    def analyze_journaling_response(self, response_text, expected_emotions):
        """Analyze journaling response for emotional indicators"""
        # This would be used by the text analyzer to understand the emotional content
        # of the journaling responses
        return {
            'text': response_text,
            'expected_emotions': expected_emotions,
            'length': len(response_text),
            'has_emotional_words': any(emotion in response_text.lower() for emotion in expected_emotions)
        }

# Test the journaling prompts system
if __name__ == "__main__":
    prompts = JournalingPrompts()
    
    print("MoodLens Journaling Prompts System")
    print("=" * 50)
    print(f"Welcome message: {prompts.get_random_welcome()}")
    print()
    
    print("Screening Questions:")
    for question in prompts.get_screening_questions():
        print(f"- {question['question']}")
    print()
    
    # Test follow-up determination
    test_responses = {
        'energy_screening': 8,
        'mood_screening': 'uplifted',
        'stress_screening': 'moderate'
    }
    
    category, subcategory = prompts.determine_follow_up_category(test_responses)
    print(f"Based on responses, using: {category} -> {subcategory}")
    
    follow_up_prompts = prompts.get_journaling_prompts(category, subcategory)
    print(f"\nFollow-up prompts ({len(follow_up_prompts)} prompts):")
    for prompt in follow_up_prompts:
        print(f"- {prompt['question']}")
    
    print(f"\nVoice analysis prompts ({len(prompts.get_voice_prompts())} prompts):")
    for prompt in prompts.get_voice_prompts():
        print(f"- \"{prompt['text']}\" (focus: {', '.join(prompt['analysis_focus'])})")
