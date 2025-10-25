"""
Recommendation Engine for MoodLens
Provides action-focused guidance and immediate interventions
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class RecommendationEngine:
    def __init__(self):
        print("💡 Initializing Recommendation Engine...")
        
        # Action categories with detailed implementations
        self.action_types = {
            'breathing': {
                'name': 'Breathing Exercise',
                'icon': '🫁',
                'description': 'Guided breathing techniques'
            },
            'grounding': {
                'name': 'Grounding Technique', 
                'icon': '🌍',
                'description': 'Present-moment awareness exercises'
            },
            'mindfulness': {
                'name': 'Mindfulness Practice',
                'icon': '🧘',
                'description': 'Mindful awareness activities'
            },
            'movement': {
                'name': 'Physical Movement',
                'icon': '🏃',
                'description': 'Body-based interventions'
            },
            'journaling': {
                'name': 'Journaling',
                'icon': '📝',
                'description': 'Written reflection and expression'
            },
            'social': {
                'name': 'Social Connection',
                'icon': '👥',
                'description': 'Human connection activities'
            },
            'self-care': {
                'name': 'Self-Care',
                'icon': '🛁',
                'description': 'Personal care activities'
            },
            'audio': {
                'name': 'Audio Therapy',
                'icon': '🎵',
                'description': 'Sound-based interventions'
            },
            'visual': {
                'name': 'Visual Therapy',
                'icon': '👁️',
                'description': 'Visual stimulation activities'
            },
            'release': {
                'name': 'Emotional Release',
                'icon': '💥',
                'description': 'Safe emotional expression'
            },
            'focus': {
                'name': 'Focus Exercise',
                'icon': '🎯',
                'description': 'Attention and concentration'
            },
            'organization': {
                'name': 'Organization',
                'icon': '📋',
                'description': 'Structuring and planning'
            },
            'boundaries': {
                'name': 'Boundary Setting',
                'icon': '🚧',
                'description': 'Protecting personal limits'
            },
            'rest': {
                'name': 'Rest & Recovery',
                'icon': '😴',
                'description': 'Physical and mental rest'
            },
            'enjoyment': {
                'name': 'Fun & Enjoyment',
                'icon': '🎉',
                'description': 'Pleasurable activities'
            },
            'service': {
                'name': 'Service to Others',
                'icon': '🤝',
                'description': 'Helping and giving'
            },
            'planning': {
                'name': 'Planning',
                'icon': '📅',
                'description': 'Future-oriented activities'
            },
            'exploration': {
                'name': 'Exploration',
                'icon': '🔍',
                'description': 'Discovery and learning'
            },
            'purpose': {
                'name': 'Purpose & Meaning',
                'icon': '⭐',
                'description': 'Meaningful activities'
            },
            'action': {
                'name': 'Action',
                'icon': '⚡',
                'description': 'Active engagement'
            }
        }
        
        # Detailed action implementations
        self.action_implementations = {
            '3 Deep Breaths': {
                'type': 'breathing',
                'duration': '2 min',
                'instructions': [
                    "Sit comfortably and close your eyes",
                    "Breathe in slowly for 4 counts",
                    "Hold your breath for 4 counts", 
                    "Breathe out slowly for 6 counts",
                    "Repeat 3 times",
                    "Notice how you feel"
                ],
                'audio_guide': True,
                'difficulty': 'easy'
            },
            '5-4-3-2-1 Grounding': {
                'type': 'grounding',
                'duration': '3 min',
                'instructions': [
                    "Name 5 things you can see",
                    "Name 4 things you can touch",
                    "Name 3 things you can hear",
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste",
                    "Take a deep breath and notice you're here"
                ],
                'audio_guide': True,
                'difficulty': 'easy'
            },
            'Quick Body Scan': {
                'type': 'mindfulness',
                'duration': '2 min',
                'instructions': [
                    "Start at the top of your head",
                    "Notice any tension or sensations",
                    "Move down to your shoulders",
                    "Check your chest and breathing",
                    "Notice your stomach area",
                    "Feel your legs and feet",
                    "Take a deep breath"
                ],
                'audio_guide': True,
                'difficulty': 'easy'
            },
            '10 Jumping Jacks': {
                'type': 'movement',
                'duration': '1 min',
                'instructions': [
                    "Stand with feet together",
                    "Jump up spreading legs shoulder-width apart",
                    "Raise arms overhead",
                    "Jump back to starting position",
                    "Repeat 10 times",
                    "Notice your increased energy"
                ],
                'audio_guide': False,
                'difficulty': 'easy'
            },
            'Scream into Pillow': {
                'type': 'release',
                'duration': '30 sec',
                'instructions': [
                    "Find a pillow or soft surface",
                    "Take a deep breath",
                    "Let out a loud scream into the pillow",
                    "Repeat 2-3 times",
                    "Notice the release of tension"
                ],
                'audio_guide': False,
                'difficulty': 'easy'
            },
            'Gentle Self-Hug': {
                'type': 'self-care',
                'duration': '1 min',
                'instructions': [
                    "Cross your arms over your chest",
                    "Give yourself a gentle hug",
                    "Feel the warmth and comfort",
                    "Take slow, deep breaths",
                    "Notice the feeling of self-compassion"
                ],
                'audio_guide': True,
                'difficulty': 'easy'
            },
            'Listen to Comforting Music': {
                'type': 'audio',
                'duration': '5 min',
                'instructions': [
                    "Choose calming, familiar music",
                    "Put on headphones if possible",
                    "Close your eyes and listen",
                    "Let the music wash over you",
                    "Notice any emotions that arise"
                ],
                'audio_guide': False,
                'difficulty': 'easy'
            },
            'Look at Happy Photos': {
                'type': 'visual',
                'duration': '3 min',
                'instructions': [
                    "Open your photo gallery",
                    "Find photos of happy memories",
                    "Look at each photo for 30 seconds",
                    "Remember how you felt in that moment",
                    "Let the positive feelings fill you"
                ],
                'audio_guide': False,
                'difficulty': 'easy'
            },
            'Brain Dump Everything': {
                'type': 'journaling',
                'duration': '5 min',
                'instructions': [
                    "Get a pen and paper",
                    "Write down everything on your mind",
                    "Don't worry about grammar or structure",
                    "Keep writing until you feel empty",
                    "Notice the mental clarity"
                ],
                'audio_guide': False,
                'difficulty': 'easy'
            },
            'Pick Just ONE Thing': {
                'type': 'focus',
                'duration': '2 min',
                'instructions': [
                    "Look at your to-do list or responsibilities",
                    "Choose just ONE thing to focus on",
                    "Write it down clearly",
                    "Commit to doing only that one thing",
                    "Feel the relief of simplification"
                ],
                'audio_guide': False,
                'difficulty': 'easy'
            }
        }
        
        # Emergency resources
        self.emergency_resources = {
            'crisis_text_line': {
                'name': 'Crisis Text Line',
                'number': 'Text HOME to 741741',
                'description': 'Free, 24/7 crisis support via text',
                'url': 'https://www.crisistextline.org'
            },
            'national_suicide_prevention': {
                'name': 'National Suicide Prevention Lifeline',
                'number': '988',
                'description': 'Free, 24/7 suicide prevention support',
                'url': 'https://suicidepreventionlifeline.org'
            },
            'mental_health_america': {
                'name': 'Mental Health America',
                'number': '1-800-273-8255',
                'description': 'Mental health resources and support',
                'url': 'https://www.mhanational.org'
            },
            'immediate_help': {
                'name': 'Emergency Services',
                'number': '911',
                'description': 'For immediate life-threatening emergencies',
                'url': None
            }
        }
        
        print("✅ Recommendation Engine ready!")
    
    def get_action_details(self, action_name: str) -> Dict:
        """Get detailed information about a specific action"""
        return self.action_implementations.get(action_name, {
            'type': 'general',
            'duration': '5 min',
            'instructions': ['Take a moment to breathe and center yourself'],
            'audio_guide': False,
            'difficulty': 'easy'
        })
    
    def get_action_type_info(self, action_type: str) -> Dict:
        """Get information about an action type"""
        return self.action_types.get(action_type, {
            'name': 'General Activity',
            'icon': '⭐',
            'description': 'A helpful activity'
        })
    
    def get_emergency_resources(self) -> Dict:
        """Get emergency resources"""
        return self.emergency_resources
    
    def format_action_for_ui(self, action: Dict) -> Dict:
        """Format an action for display in the UI"""
        action_details = self.get_action_details(action['action'])
        action_type_info = self.get_action_type_info(action_details['type'])
        
        return {
            'name': action['action'],
            'type': action_details['type'],
            'type_name': action_type_info['name'],
            'type_icon': action_type_info['icon'],
            'duration': action['duration'],
            'instructions': action_details['instructions'],
            'audio_guide': action_details['audio_guide'],
            'difficulty': action_details['difficulty'],
            'description': action_type_info['description']
        }
    
    def get_breathing_audio_script(self) -> List[str]:
        """Get script for breathing exercise audio guide"""
        return [
            "Welcome to your breathing exercise. Find a comfortable position.",
            "Close your eyes if that feels comfortable.",
            "We'll breathe together for three cycles.",
            "Breathe in slowly... one... two... three... four...",
            "Hold your breath... one... two... three... four...",
            "Breathe out slowly... one... two... three... four... five... six...",
            "That's one cycle. Let's do two more.",
            "Breathe in slowly... one... two... three... four...",
            "Hold your breath... one... two... three... four...",
            "Breathe out slowly... one... two... three... four... five... six...",
            "One more cycle.",
            "Breathe in slowly... one... two... three... four...",
            "Hold your breath... one... two... three... four...",
            "Breathe out slowly... one... two... three... four... five... six...",
            "Take a moment to notice how you feel.",
            "Thank you for taking this time for yourself."
        ]
    
    def get_grounding_audio_script(self) -> List[str]:
        """Get script for grounding exercise audio guide"""
        return [
            "Welcome to the 5-4-3-2-1 grounding exercise.",
            "This will help you feel more present and centered.",
            "Let's start with what you can see.",
            "Look around and name 5 things you can see.",
            "Take your time with each one.",
            "Now, notice 4 things you can touch.",
            "Feel the texture, temperature, and sensation of each.",
            "Next, listen for 3 things you can hear.",
            "Notice both near and far sounds.",
            "Now, notice 2 things you can smell.",
            "Take a gentle breath in through your nose.",
            "Finally, notice 1 thing you can taste.",
            "It might be the taste in your mouth right now.",
            "Take a deep breath and notice that you are here, in this moment.",
            "You are safe and present."
        ]
    
    def get_body_scan_audio_script(self) -> List[str]:
        """Get script for body scan audio guide"""
        return [
            "Welcome to your body scan exercise.",
            "This will help you connect with your body and release tension.",
            "Start by finding a comfortable position.",
            "Close your eyes and take a deep breath.",
            "Begin at the top of your head.",
            "Notice any sensations there - tension, warmth, or anything else.",
            "Move your attention to your forehead.",
            "Notice any tightness or relaxation.",
            "Now your eyes and the muscles around them.",
            "Let them soften and relax.",
            "Move to your jaw.",
            "Notice if it's clenched or relaxed.",
            "Let your jaw drop slightly.",
            "Now your shoulders.",
            "Notice if they're tense or relaxed.",
            "Let them drop and relax.",
            "Move to your chest.",
            "Notice your breathing.",
            "Feel your chest rise and fall.",
            "Now your stomach area.",
            "Notice any sensations there.",
            "Move to your legs.",
            "Feel the weight of your legs.",
            "Finally, notice your feet.",
            "Feel them connected to the ground.",
            "Take a deep breath and notice how your whole body feels.",
            "Thank you for taking this time for yourself."
        ]
    
    def save_check_in(self, emotion_data: Dict, user_responses: Dict) -> str:
        """Save a check-in session to history"""
        try:
            # Create history directory if it doesn't exist
            history_dir = "check_in_history"
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{history_dir}/check_in_{timestamp}.json"
            
            # Prepare data to save
            check_in_data = {
                'timestamp': datetime.now().isoformat(),
                'emotion': emotion_data['emotion'],
                'emotion_name': emotion_data['emotion_name'],
                'confidence': emotion_data['confidence'],
                'indicators': emotion_data['indicators'],
                'user_responses': user_responses,
                'immediate_actions': emotion_data['immediate_actions'],
                'short_term_actions': emotion_data['short_term_actions']
            }
            
            # Save to file
            with open(filename, 'w') as f:
                json.dump(check_in_data, f, indent=2)
            
            return filename
            
        except Exception as e:
            print(f"Error saving check-in: {e}")
            return None
    
    def load_check_in_history(self, limit: int = 10) -> List[Dict]:
        """Load recent check-in history"""
        try:
            history_dir = "check_in_history"
            if not os.path.exists(history_dir):
                return []
            
            # Get all check-in files
            files = [f for f in os.listdir(history_dir) if f.startswith('check_in_') and f.endswith('.json')]
            files.sort(reverse=True)  # Most recent first
            
            # Load recent check-ins
            check_ins = []
            for filename in files[:limit]:
                filepath = os.path.join(history_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        check_in_data = json.load(f)
                        check_ins.append(check_in_data)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
            
            return check_ins
            
        except Exception as e:
            print(f"Error loading check-in history: {e}")
            return []

# Test the recommendation engine
if __name__ == "__main__":
    engine = RecommendationEngine()
    
    print("MoodLens Recommendation Engine")
    print("=" * 40)
    
    # Test action details
    action = {'action': '3 Deep Breaths', 'type': 'breathing', 'duration': '2 min'}
    formatted = engine.format_action_for_ui(action)
    print(f"Action: {formatted['name']}")
    print(f"Type: {formatted['type_icon']} {formatted['type_name']}")
    print(f"Duration: {formatted['duration']}")
    print(f"Instructions: {formatted['instructions'][:2]}...")
    print()
    
    # Test emergency resources
    resources = engine.get_emergency_resources()
    print("Emergency Resources:")
    for key, resource in resources.items():
        print(f"- {resource['name']}: {resource['number']}")

