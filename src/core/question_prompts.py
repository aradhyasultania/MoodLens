"""
Question Prompts for MoodLens Guided Check-in
Initial categorization questions followed by directed journaling prompts
"""

class QuestionPrompts:
    def __init__(self):
        # Initial categorization questions (MCQ to determine emotion category)
        self.initial_questions = [
            {
                'id': 'energy_level',
                'question': 'Right now, my energy level feels:',
                'options': [
                    {'value': 'high', 'text': '⚡ High', 'emoji': '⚡'},
                    {'value': 'moderate', 'text': '😌 Moderate', 'emoji': '😌'},
                    {'value': 'low', 'text': '😴 Low', 'emoji': '😴'}
                ],
                'category': 'physical'
            },
            {
                'id': 'thoughts',
                'question': 'My thoughts are:',
                'options': [
                    {'value': 'racing', 'text': '🌪️ Racing', 'emoji': '🌪️'},
                    {'value': 'flowing', 'text': '🌊 Flowing', 'emoji': '🌊'},
                    {'value': 'stuck', 'text': '🧊 Stuck', 'emoji': '🧊'}
                ],
                'category': 'mental'
            },
            {
                'id': 'physical',
                'question': 'Physically, I feel:',
                'options': [
                    {'value': 'tense', 'text': '😰 Tense', 'emoji': '😰'},
                    {'value': 'neutral', 'text': '😐 Neutral', 'emoji': '😐'},
                    {'value': 'relaxed', 'text': '😌 Relaxed', 'emoji': '😌'}
                ],
                'category': 'physical'
            },
            {
                'id': 'feeling_like',
                'question': 'I feel most like:',
                'options': [
                    {'value': 'crying', 'text': '😢 Crying', 'emoji': '😢'},
                    {'value': 'screaming', 'text': '😤 Screaming', 'emoji': '😤'},
                    {'value': 'laughing', 'text': '😊 Laughing', 'emoji': '😊'},
                    {'value': 'nothing', 'text': '😶 Nothing', 'emoji': '😶'}
                ],
                'category': 'emotional'
            }
        ]
        
        # Directed journaling prompts based on emotion category
        self.journaling_prompts = {
            'anxious': [
                {
                    'id': 'anxious_1',
                    'question': 'What specific thoughts are racing through your mind right now?',
                    'placeholder': 'Type whatever comes to mind...',
                    'category': 'thoughts'
                },
                {
                    'id': 'anxious_2', 
                    'question': 'What are you most worried about today?',
                    'placeholder': 'Describe what\'s making you feel worried...',
                    'category': 'worries'
                },
                {
                    'id': 'anxious_3',
                    'question': 'Where do you feel tension in your body?',
                    'placeholder': 'Describe any physical sensations...',
                    'category': 'physical'
                },
                {
                    'id': 'anxious_4',
                    'question': 'What would help you feel more calm right now?',
                    'placeholder': 'What do you think you need?',
                    'category': 'needs'
                }
            ],
            'sad': [
                {
                    'id': 'sad_1',
                    'question': 'What\'s making you feel sad or down today?',
                    'placeholder': 'Describe what\'s contributing to these feelings...',
                    'category': 'triggers'
                },
                {
                    'id': 'sad_2',
                    'question': 'How is this sadness showing up in your body?',
                    'placeholder': 'Describe any physical sensations...',
                    'category': 'physical'
                },
                {
                    'id': 'sad_3',
                    'question': 'What do you wish someone understood about how you\'re feeling?',
                    'placeholder': 'What would you want others to know?',
                    'category': 'expression'
                },
                {
                    'id': 'sad_4',
                    'question': 'What usually helps you feel better when you\'re sad?',
                    'placeholder': 'Think of things that have helped before...',
                    'category': 'coping'
                }
            ],
            'frustrated': [
                {
                    'id': 'frustrated_1',
                    'question': 'What\'s frustrating you most right now?',
                    'placeholder': 'Describe what\'s making you feel frustrated...',
                    'category': 'triggers'
                },
                {
                    'id': 'frustrated_2',
                    'question': 'How is this frustration showing up in your body?',
                    'placeholder': 'Describe any physical sensations...',
                    'category': 'physical'
                },
                {
                    'id': 'frustrated_3',
                    'question': 'What do you wish you could do about this situation?',
                    'placeholder': 'What action would you like to take?',
                    'category': 'action'
                },
                {
                    'id': 'frustrated_4',
                    'question': 'What\'s preventing you from feeling better about this?',
                    'placeholder': 'What obstacles do you see?',
                    'category': 'barriers'
                }
            ],
            'overwhelmed': [
                {
                    'id': 'overwhelmed_1',
                    'question': 'What feels like too much right now?',
                    'placeholder': 'Describe what\'s overwhelming you...',
                    'category': 'triggers'
                },
                {
                    'id': 'overwhelmed_2',
                    'question': 'What thoughts keep getting stuck in your head?',
                    'placeholder': 'Describe any repetitive or stuck thoughts...',
                    'category': 'thoughts'
                },
                {
                    'id': 'overwhelmed_3',
                    'question': 'What would it look like if things felt manageable?',
                    'placeholder': 'Describe what manageable would feel like...',
                    'category': 'vision'
                },
                {
                    'id': 'overwhelmed_4',
                    'question': 'What\'s one small thing you could do to feel less overwhelmed?',
                    'placeholder': 'Think of something small and doable...',
                    'category': 'action'
                }
            ],
            'calm': [
                {
                    'id': 'calm_1',
                    'question': 'What\'s contributing to this sense of calm?',
                    'placeholder': 'Describe what\'s helping you feel peaceful...',
                    'category': 'sources'
                },
                {
                    'id': 'calm_2',
                    'question': 'How does this calm feeling show up in your body?',
                    'placeholder': 'Describe the physical sensations of calm...',
                    'category': 'physical'
                },
                {
                    'id': 'calm_3',
                    'question': 'What would you like to do with this peaceful energy?',
                    'placeholder': 'How would you like to use this calm feeling?',
                    'category': 'intention'
                },
                {
                    'id': 'calm_4',
                    'question': 'What helps you maintain this sense of balance?',
                    'placeholder': 'What practices or habits support this?',
                    'category': 'maintenance'
                }
            ],
            'happy': [
                {
                    'id': 'happy_1',
                    'question': 'What\'s making you feel happy or energized today?',
                    'placeholder': 'Describe what\'s bringing you joy...',
                    'category': 'sources'
                },
                {
                    'id': 'happy_2',
                    'question': 'How is this happiness showing up in your body?',
                    'placeholder': 'Describe the physical sensations of joy...',
                    'category': 'physical'
                },
                {
                    'id': 'happy_3',
                    'question': 'What would you like to do with this positive energy?',
                    'placeholder': 'How would you like to channel this happiness?',
                    'category': 'intention'
                },
                {
                    'id': 'happy_4',
                    'question': 'Who would you like to share this good feeling with?',
                    'placeholder': 'Think of people who would appreciate this...',
                    'category': 'connection'
                }
            ],
            'neutral': [
                {
                    'id': 'neutral_1',
                    'question': 'What does this neutral feeling feel like to you?',
                    'placeholder': 'Describe what neutral means for you right now...',
                    'category': 'experience'
                },
                {
                    'id': 'neutral_2',
                    'question': 'What\'s happening around you that might be contributing to this?',
                    'placeholder': 'Describe your current environment or situation...',
                    'category': 'context'
                },
                {
                    'id': 'neutral_3',
                    'question': 'What would you like to feel instead?',
                    'placeholder': 'What emotion would you prefer right now?',
                    'category': 'preference'
                },
                {
                    'id': 'neutral_4',
                    'question': 'What might help you feel more connected or engaged?',
                    'placeholder': 'What could help you feel more alive?',
                    'category': 'engagement'
                }
            ],
            'tired': [
                {
                    'id': 'tired_1',
                    'question': 'What\'s contributing to this feeling of exhaustion?',
                    'placeholder': 'Describe what\'s draining your energy...',
                    'category': 'sources'
                },
                {
                    'id': 'tired_2',
                    'question': 'How does this tiredness show up in your body?',
                    'placeholder': 'Describe the physical sensations of fatigue...',
                    'category': 'physical'
                },
                {
                    'id': 'tired_3',
                    'question': 'What would true rest look like for you right now?',
                    'placeholder': 'Describe what rest would feel like...',
                    'category': 'needs'
                },
                {
                    'id': 'tired_4',
                    'question': 'What\'s preventing you from getting the rest you need?',
                    'placeholder': 'What obstacles are in the way?',
                    'category': 'barriers'
                }
            ]
        }
        
        # Voice analysis prompts - exact lines to say
        self.voice_prompts = [
            {
                'id': 'voice_1',
                'text': 'The quick brown fox jumps over the lazy dog.',
                'instruction': 'Please read this sentence naturally, as you would normally speak.',
                'analysis_focus': 'natural_speech_patterns'
            },
            {
                'id': 'voice_2', 
                'text': 'I am feeling okay today.',
                'instruction': 'Say this sentence as if you\'re telling a friend how you feel.',
                'analysis_focus': 'emotional_expression'
            },
            {
                'id': 'voice_3',
                'text': 'Everything will be alright.',
                'instruction': 'Say this sentence as if you\'re trying to reassure yourself.',
                'analysis_focus': 'self_reassurance'
            }
        ]
        
        # Welcome messages
        self.welcome_messages = [
            "Let's check in with how you're feeling right now",
            "Take a moment to connect with yourself",
            "How are you doing today?",
            "Let's explore what you're experiencing",
            "Time for a gentle emotional check-in"
        ]
        
        # Encouraging messages during the process
        self.encouragement_messages = [
            "Thank you for sharing that",
            "That's helpful to know",
            "I appreciate your honesty",
            "That makes sense",
            "Thank you for being open"
        ]
        
        # Analysis messages
        self.analysis_messages = [
            "Taking a moment to understand what you're experiencing...",
            "Reflecting on your responses...",
            "Processing your emotional state...",
            "Analyzing your feelings...",
            "Understanding your current state..."
        ]
    
    def get_initial_questions(self) -> list:
        """Get initial categorization questions"""
        return self.initial_questions
    
    def get_initial_question_count(self) -> int:
        """Get number of initial questions"""
        return len(self.initial_questions)
    
    def get_journaling_prompts(self, emotion_category: str) -> list:
        """Get journaling prompts for a specific emotion category"""
        return self.journaling_prompts.get(emotion_category, [])
    
    def get_voice_prompts(self) -> list:
        """Get voice analysis prompts"""
        return self.voice_prompts
    
    def determine_emotion_category(self, initial_responses: dict) -> str:
        """Determine emotion category based on initial responses"""
        try:
            # Scoring system for initial responses
            scores = {
                'anxious': 0,
                'sad': 0,
                'frustrated': 0,
                'overwhelmed': 0,
                'calm': 0,
                'happy': 0,
                'neutral': 0,
                'tired': 0
            }
            
            # Energy level scoring
            energy = initial_responses.get('energy_level', 'moderate')
            if energy == 'high':
                scores['happy'] += 2
                scores['anxious'] += 1
            elif energy == 'low':
                scores['sad'] += 2
                scores['tired'] += 2
                scores['neutral'] += 1
            
            # Thoughts scoring
            thoughts = initial_responses.get('thoughts', 'flowing')
            if thoughts == 'racing':
                scores['anxious'] += 2
                scores['overwhelmed'] += 1
            elif thoughts == 'stuck':
                scores['overwhelmed'] += 2
                scores['sad'] += 1
            
            # Physical scoring
            physical = initial_responses.get('physical', 'neutral')
            if physical == 'tense':
                scores['anxious'] += 2
                scores['frustrated'] += 1
            elif physical == 'relaxed':
                scores['calm'] += 2
            
            # Feeling scoring
            feeling = initial_responses.get('feeling_like', 'nothing')
            if feeling == 'crying':
                scores['sad'] += 3
                scores['overwhelmed'] += 1
            elif feeling == 'screaming':
                scores['frustrated'] += 3
                scores['anxious'] += 1
            elif feeling == 'laughing':
                scores['happy'] += 3
            elif feeling == 'nothing':
                scores['neutral'] += 2
                scores['tired'] += 1
            
            # Find highest scoring emotion
            max_score = max(scores.values())
            if max_score == 0:
                return 'neutral'
            
            # Return emotion with highest score
            for emotion, score in scores.items():
                if score == max_score:
                    return emotion
            
            return 'neutral'
            
        except Exception as e:
            print(f"Error determining emotion category: {e}")
            return 'neutral'
    
    def validate_initial_response(self, question_id: str, response: str) -> bool:
        """Validate if a response is valid for an initial question"""
        question = next((q for q in self.initial_questions if q['id'] == question_id), None)
        if not question:
            return False
        
        valid_values = [option['value'] for option in question['options']]
        return response in valid_values
    
    def get_random_welcome(self) -> str:
        """Get a random welcome message"""
        import random
        return random.choice(self.welcome_messages)
    
    def get_random_encouragement(self) -> str:
        """Get a random encouragement message"""
        import random
        return random.choice(self.encouragement_messages)
    
    def get_random_analysis_message(self) -> str:
        """Get a random analysis message"""
        import random
        return random.choice(self.analysis_messages)

# Test the question prompts
if __name__ == "__main__":
    prompts = QuestionPrompts()
    
    print("MoodLens Question Prompts - New Design")
    print("=" * 50)
    print(f"Initial questions: {prompts.get_initial_question_count()}")
    print(f"Welcome message: {prompts.get_random_welcome()}")
    print()
    
    print("Initial Categorization Questions:")
    for i, question in enumerate(prompts.get_initial_questions()):
        print(f"{i+1}. {question['question']}")
        for option in question['options']:
            print(f"   {option['text']}")
        print()
    
    # Test emotion category determination
    test_responses = {
        'energy_level': 'low',
        'thoughts': 'stuck',
        'physical': 'tense',
        'feeling_like': 'crying'
    }
    
    category = prompts.determine_emotion_category(test_responses)
    print(f"Test responses lead to category: {category}")
    
    # Show journaling prompts for that category
    journaling = prompts.get_journaling_prompts(category)
    print(f"\nJournaling prompts for {category}:")
    for i, prompt in enumerate(journaling):
        print(f"{i+1}. {prompt['question']}")
        print(f"   Placeholder: {prompt['placeholder']}")
        print()
    
    # Show voice prompts
    voice_prompts = prompts.get_voice_prompts()
    print("Voice Analysis Prompts:")
    for i, prompt in enumerate(voice_prompts):
        print(f"{i+1}. \"{prompt['text']}\"")
        print(f"   Instruction: {prompt['instruction']}")
        print(f"   Focus: {prompt['analysis_focus']}")
        print()

