"""
Simplified Emotion Detector for MoodLens
Combines guided questions, face analysis, and voice tone into unified emotion detection
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import os
from datetime import datetime

class UnifiedEmotionDetector:
    def __init__(self):
        print("🧠 Initializing Unified Emotion Detector...")
        
        # Simplified emotion categories
        self.emotions = {
            'anxious': {
                'name': 'Anxious/Worried',
                'emoji': '😰',
                'description': 'Racing thoughts, tension, worry',
                'indicators': ['racing_thoughts', 'tension', 'worry', 'high_energy']
            },
            'sad': {
                'name': 'Sad/Down', 
                'emoji': '😢',
                'description': 'Low energy, withdrawn, tearful',
                'indicators': ['low_energy', 'withdrawn', 'tearful', 'crying']
            },
            'frustrated': {
                'name': 'Frustrated/Angry',
                'emoji': '😤', 
                'description': 'Tense, irritable, ready to explode',
                'indicators': ['tense', 'irritable', 'screaming', 'action_needed']
            },
            'overwhelmed': {
                'name': 'Overwhelmed',
                'emoji': '😫',
                'description': 'Too much, stuck, can\'t cope',
                'indicators': ['stuck_thoughts', 'too_much', 'cant_cope', 'racing_thoughts']
            },
            'calm': {
                'name': 'Calm/Peaceful',
                'emoji': '😌',
                'description': 'Relaxed, balanced, content',
                'indicators': ['relaxed', 'flowing_thoughts', 'neutral', 'balanced']
            },
            'happy': {
                'name': 'Happy/Energized',
                'emoji': '😊',
                'description': 'High energy, positive, excited',
                'indicators': ['high_energy', 'laughing', 'positive', 'better_mood']
            },
            'neutral': {
                'name': 'Neutral/Flat',
                'emoji': '😐',
                'description': 'Numb, disconnected, empty',
                'indicators': ['numb', 'nothing_feeling', 'same_mood', 'disconnected']
            },
            'tired': {
                'name': 'Tired/Drained',
                'emoji': '😴',
                'description': 'Exhausted, depleted, need rest',
                'indicators': ['low_energy', 'rest_needed', 'exhausted', 'drained']
            }
        }
        
        # Question scoring weights
        self.question_weights = {
            'energy_level': {
                'high': {'happy': 0.8, 'anxious': 0.3, 'frustrated': 0.2},
                'moderate': {'calm': 0.7, 'neutral': 0.3},
                'low': {'sad': 0.7, 'tired': 0.8, 'overwhelmed': 0.3, 'neutral': 0.2}
            },
            'thoughts': {
                'racing': {'anxious': 0.8, 'overwhelmed': 0.9, 'frustrated': 0.3},
                'flowing': {'calm': 0.9, 'happy': 0.5},
                'stuck': {'overwhelmed': 0.9, 'sad': 0.6, 'neutral': 0.2}
            },
            'physical': {
                'tense': {'anxious': 0.8, 'frustrated': 0.7, 'overwhelmed': 0.6},
                'neutral': {'calm': 0.6, 'neutral': 0.5},
                'relaxed': {'calm': 0.9, 'happy': 0.4}
            },
            'worry': {
                'nothing': {'calm': 0.8, 'happy': 0.5, 'neutral': 0.2},
                'few_things': {'anxious': 0.5, 'overwhelmed': 0.4},
                'a_lot': {'anxious': 0.8, 'overwhelmed': 0.9}
            },
            'feeling_like': {
                'crying': {'sad': 0.9, 'overwhelmed': 0.6},
                'screaming': {'frustrated': 0.9, 'overwhelmed': 0.4, 'anxious': 0.3},
                'laughing': {'happy': 0.9, 'calm': 0.5},
                'nothing': {'neutral': 0.7, 'overwhelmed': 0.4, 'calm': 0.2, 'sad': 0.2, 'tired': 0.2}
            },
            'mood_comparison': {
                'better': {'happy': 0.8, 'calm': 0.4},
                'same': {'neutral': 0.5, 'calm': 0.4},
                'worse': {'sad': 0.7, 'anxious': 0.5, 'overwhelmed': 0.4, 'tired': 0.3}
            },
            'need_most': {
                'company': {'sad': 0.6, 'anxious': 0.3},
                'rest': {'tired': 0.9, 'overwhelmed': 0.5, 'calm': 0.3},
                'focus': {'anxious': 0.5, 'overwhelmed': 0.6},
                'action': {'frustrated': 0.8, 'overwhelmed': 0.3, 'anxious': 0.3}
            }
        }
        
        # Input weights for final scoring
        self.input_weights = {
            'questions': 0.7,  # Primary signal
            'face': 0.2,       # Supporting evidence  
            'voice': 0.1       # Additional context
        }
        
        print("✅ Unified Emotion Detector ready!")
    
    def detect_emotion(self, initial_responses: Dict, journaling_responses: Dict, face_data: Optional[Dict] = None, voice_data: Optional[Dict] = None) -> Dict:
        """
        Main emotion detection function that combines all inputs
        
        Args:
            initial_responses: Dict of initial categorization answers
            journaling_responses: Dict of journaling responses
            face_data: Optional face analysis results
            voice_data: Optional voice analysis results
            
        Returns:
            Dict with emotion, confidence, indicators, and actions
        """
        try:
            # Calculate emotion scores from each input
            initial_scores = self._score_initial_responses(initial_responses)
            journaling_scores = self._score_journaling_responses(journaling_responses)
            face_scores = self._score_face(face_data) if face_data else {}
            voice_scores = self._score_voice(voice_data) if voice_data else {}
            
            # Combine scores with weights
            final_scores = self._combine_scores(initial_scores, journaling_scores, face_scores, voice_scores)
            
            # Find dominant emotion
            dominant_emotion = max(final_scores.items(), key=lambda x: x[1])
            
            # Calculate confidence
            confidence = self._calculate_confidence(final_scores, dominant_emotion)
            
            # Get indicators
            indicators = self._get_indicators(initial_responses, journaling_responses, face_data, voice_data, dominant_emotion[0])
            
            # Get actions
            actions = self._get_actions_for_emotion(dominant_emotion[0])
            
            return {
                'emotion': dominant_emotion[0],
                'emotion_name': self.emotions[dominant_emotion[0]]['name'],
                'emotion_emoji': self.emotions[dominant_emotion[0]]['emoji'],
                'confidence': confidence,
                'description': self.emotions[dominant_emotion[0]]['description'],
                'indicators': indicators,
                'immediate_actions': actions['immediate'],
                'short_term_actions': actions['short_term'],
                'all_scores': final_scores,
                'analysis_details': {
                    'initial_scores': initial_scores,
                    'journaling_scores': journaling_scores,
                    'face_scores': face_scores,
                    'voice_scores': voice_scores
                }
            }
            
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return self._get_fallback_result()
    
    def _score_initial_responses(self, responses: Dict) -> Dict[str, float]:
        """Score emotions based on initial categorization responses"""
        scores = {emotion: 0.0 for emotion in self.emotions.keys()}
        
        for question, answer in responses.items():
            if question in self.question_weights and answer in self.question_weights[question]:
                weights = self.question_weights[question][answer]
                for emotion, weight in weights.items():
                    scores[emotion] += weight
        
        # Normalize scores to 0-1 range
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1
        for emotion in scores:
            scores[emotion] = scores[emotion] / max_score
            
        return scores
    
    def _score_journaling_responses(self, responses: Dict) -> Dict[str, float]:
        """Score emotions based on journaling responses using text analysis"""
        scores = {emotion: 0.0 for emotion in self.emotions.keys()}
        
        if not responses:
            return scores
        
        # Keywords and phrases that indicate specific emotions
        emotion_keywords = {
            'anxious': [
                'worried', 'anxious', 'nervous', 'stressed', 'panic', 'fear', 'scared',
                'racing thoughts', 'can\'t stop thinking', 'overwhelming', 'tense',
                'heart racing', 'sweating', 'shaking', 'restless'
            ],
            'sad': [
                'sad', 'depressed', 'down', 'hopeless', 'empty', 'lonely', 'crying',
                'tears', 'grief', 'loss', 'disappointed', 'hurt', 'broken', 'heavy',
                'can\'t get out of bed', 'no energy', 'worthless'
            ],
            'frustrated': [
                'frustrated', 'angry', 'mad', 'irritated', 'annoyed', 'furious',
                'rage', 'explosive', 'can\'t take it', 'fed up', 'sick of',
                'want to scream', 'punch something', 'so angry'
            ],
            'overwhelmed': [
                'overwhelmed', 'too much', 'can\'t cope', 'drowning', 'stuck',
                'paralyzed', 'frozen', 'don\'t know where to start', 'everything at once',
                'too many things', 'can\'t handle', 'breaking down'
            ],
            'calm': [
                'calm', 'peaceful', 'relaxed', 'centered', 'balanced', 'serene',
                'content', 'at ease', 'comfortable', 'breathing easy', 'quiet mind',
                'peaceful', 'tranquil', 'grounded'
            ],
            'happy': [
                'happy', 'joyful', 'excited', 'energized', 'positive', 'optimistic',
                'grateful', 'blessed', 'lucky', 'amazing', 'wonderful', 'fantastic',
                'smiling', 'laughing', 'celebrating'
            ],
            'neutral': [
                'okay', 'fine', 'neutral', 'nothing', 'empty', 'numb', 'flat',
                'don\'t feel anything', 'meh', 'whatever', 'indifferent', 'bored'
            ],
            'tired': [
                'tired', 'exhausted', 'drained', 'fatigued', 'worn out', 'burned out',
                'no energy', 'can\'t keep going', 'need rest', 'sleepy', 'lethargic',
                'running on empty', 'depleted'
            ]
        }
        
        # Analyze each journaling response
        for question_id, response_text in responses.items():
            if not response_text or not response_text.strip():
                continue
                
            response_lower = response_text.lower()
            
            # Score based on keyword matches
            for emotion, keywords in emotion_keywords.items():
                for keyword in keywords:
                    if keyword in response_lower:
                        scores[emotion] += 1.0
        
        # Normalize scores to 0-1 range
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1
        for emotion in scores:
            scores[emotion] = scores[emotion] / max_score
            
        return scores
    
    def _score_face(self, face_data: Dict) -> Dict[str, float]:
        """Score emotions based on face analysis"""
        if not face_data or 'cluster_scores' not in face_data:
            return {emotion: 0.0 for emotion in self.emotions.keys()}
        
        face_scores = face_data['cluster_scores']
        
        # Map face emotions to our simplified categories
        mapping = {
            'stressed': 'anxious',
            'anxious': 'anxious', 
            'frustrated': 'frustrated',
            'sad': 'sad',
            'overwhelmed': 'overwhelmed',
            'positive': 'happy',
            'calm': 'calm',
            'energized': 'happy'
        }
        
        scores = {emotion: 0.0 for emotion in self.emotions.keys()}
        
        for face_emotion, score in face_scores.items():
            if face_emotion in mapping:
                mapped_emotion = mapping[face_emotion]
                scores[mapped_emotion] += score
        
        # Normalize
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1
        for emotion in scores:
            scores[emotion] = scores[emotion] / max_score
            
        return scores
    
    def _score_voice(self, voice_data: Dict) -> Dict[str, float]:
        """Score emotions based on voice analysis"""
        if not voice_data or 'cluster_scores' not in voice_data:
            return {emotion: 0.0 for emotion in self.emotions.keys()}
        
        voice_scores = voice_data['cluster_scores']
        
        # Map voice emotions to our simplified categories
        mapping = {
            'stressed': 'anxious',
            'anxious': 'anxious',
            'frustrated': 'frustrated', 
            'sad': 'sad',
            'overwhelmed': 'overwhelmed',
            'positive': 'happy',
            'calm': 'calm',
            'energized': 'happy'
        }
        
        scores = {emotion: 0.0 for emotion in self.emotions.keys()}
        
        for voice_emotion, score in voice_scores.items():
            if voice_emotion in mapping:
                mapped_emotion = mapping[voice_emotion]
                scores[mapped_emotion] += score
        
        # Normalize
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1
        for emotion in scores:
            scores[emotion] = scores[emotion] / max_score
            
        return scores
    
    def _combine_scores(self, initial_scores: Dict, journaling_scores: Dict, face_scores: Dict, voice_scores: Dict) -> Dict[str, float]:
        """Combine scores from all inputs with appropriate weights"""
        final_scores = {emotion: 0.0 for emotion in self.emotions.keys()}
        
        for emotion in self.emotions.keys():
            # Weighted combination - journaling gets higher weight as it's more detailed
            final_scores[emotion] = (
                initial_scores.get(emotion, 0) * 0.3 +  # Initial categorization
                journaling_scores.get(emotion, 0) * 0.4 +  # Journaling responses
                face_scores.get(emotion, 0) * 0.2 +  # Face analysis
                voice_scores.get(emotion, 0) * 0.1   # Voice analysis
            )
        
        return final_scores
    
    def _calculate_confidence(self, scores: Dict, dominant_emotion: Tuple) -> float:
        """Calculate confidence in the dominant emotion"""
        emotion, score = dominant_emotion
        
        # Base confidence from score strength
        confidence = score
        
        # Boost confidence if there's clear separation from second-best
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_scores) >= 2:
            second_best = sorted_scores[1][1]
            separation = score - second_best
            
            # More aggressive boosting for clear winners
            if separation > 0.3:
                confidence += 0.35  # Strong boost for clear winner
            elif separation > 0.15:
                confidence += separation * 0.5  # Medium boost
            else:
                confidence += separation * 0.2  # Small boost for close call
        
        # Penalize if score is too low (means nothing was very strong)
        if score < 0.3:
            confidence *= 0.7  # Reduce confidence for weak signals
        elif score > 0.6:
            confidence = min(confidence + 0.15, 1.0)  # Bonus for strong signals
        
        return min(confidence, 1.0)
    
    def _get_indicators(self, initial_responses: Dict, journaling_responses: Dict, face_data: Dict, voice_data: Dict, emotion: str) -> List[str]:
        """Get human-readable indicators for why this emotion was detected"""
        indicators = []
        
        # Initial response indicators
        if initial_responses.get('thoughts') == 'racing' and emotion in ['anxious', 'overwhelmed']:
            indicators.append("Your thoughts are racing")
        if initial_responses.get('energy_level') == 'low' and emotion in ['sad', 'tired']:
            indicators.append("Your energy feels low")
        if initial_responses.get('physical') == 'tense' and emotion in ['anxious', 'frustrated']:
            indicators.append("You feel physically tense")
        if initial_responses.get('feeling_like') == 'crying' and emotion == 'sad':
            indicators.append("You feel like crying")
        if initial_responses.get('feeling_like') == 'screaming' and emotion == 'frustrated':
            indicators.append("You feel like screaming")
        if initial_responses.get('feeling_like') == 'laughing' and emotion == 'happy':
            indicators.append("You feel like laughing")
        
        # Journaling response indicators
        if journaling_responses:
            for question_id, response_text in journaling_responses.items():
                if response_text and len(response_text.strip()) > 10:  # Substantial response
                    # Look for emotion-specific keywords in responses
                    response_lower = response_text.lower()
                    if emotion == 'anxious' and any(word in response_lower for word in ['worried', 'nervous', 'stressed', 'panic']):
                        indicators.append("Your writing shows signs of worry")
                    elif emotion == 'sad' and any(word in response_lower for word in ['sad', 'down', 'hopeless', 'empty']):
                        indicators.append("Your writing reflects sadness")
                    elif emotion == 'frustrated' and any(word in response_lower for word in ['angry', 'mad', 'frustrated', 'irritated']):
                        indicators.append("Your writing shows frustration")
                    elif emotion == 'overwhelmed' and any(word in response_lower for word in ['overwhelmed', 'too much', 'can\'t cope']):
                        indicators.append("Your writing indicates feeling overwhelmed")
                    break  # Only use one journaling indicator
        
        # Face-based indicators
        if face_data and face_data.get('actionable_category') == emotion:
            indicators.append("Your facial expression shows this emotion")
        
        # Voice-based indicators
        if voice_data and voice_data.get('actionable_category') == emotion:
            indicators.append("Your voice tone indicates this emotion")
        
        return indicators[:3]  # Limit to top 3 indicators
    
    def _get_actions_for_emotion(self, emotion: str) -> Dict[str, List[Dict]]:
        """Get immediate and short-term actions for the detected emotion"""
        actions = {
            'anxious': {
                'immediate': [
                    {'action': '3 Deep Breaths', 'type': 'breathing', 'duration': '2 min'},
                    {'action': '5-4-3-2-1 Grounding', 'type': 'grounding', 'duration': '3 min'},
                    {'action': 'Quick Body Scan', 'type': 'mindfulness', 'duration': '2 min'}
                ],
                'short_term': [
                    {'action': 'Take a 10-minute walk', 'type': 'movement', 'duration': '10 min'},
                    {'action': 'Write down your worries', 'type': 'journaling', 'duration': '15 min'},
                    {'action': 'Text a supportive friend', 'type': 'social', 'duration': '5 min'}
                ]
            },
            'sad': {
                'immediate': [
                    {'action': 'Gentle Self-Hug', 'type': 'self-care', 'duration': '1 min'},
                    {'action': 'Listen to Comforting Music', 'type': 'audio', 'duration': '5 min'},
                    {'action': 'Look at Happy Photos', 'type': 'visual', 'duration': '3 min'}
                ],
                'short_term': [
                    {'action': 'Take a warm shower', 'type': 'self-care', 'duration': '15 min'},
                    {'action': 'Call someone you love', 'type': 'social', 'duration': '20 min'},
                    {'action': 'Do something creative', 'type': 'expression', 'duration': '30 min'}
                ]
            },
            'frustrated': {
                'immediate': [
                    {'action': '10 Jumping Jacks', 'type': 'movement', 'duration': '1 min'},
                    {'action': 'Scream into Pillow', 'type': 'release', 'duration': '30 sec'},
                    {'action': 'Write Frustrations Down', 'type': 'journaling', 'duration': '3 min'}
                ],
                'short_term': [
                    {'action': 'Go for a run or workout', 'type': 'movement', 'duration': '30 min'},
                    {'action': 'Talk to someone about it', 'type': 'social', 'duration': '20 min'},
                    {'action': 'Do something productive', 'type': 'action', 'duration': '45 min'}
                ]
            },
            'overwhelmed': {
                'immediate': [
                    {'action': 'Brain Dump Everything', 'type': 'journaling', 'duration': '5 min'},
                    {'action': 'Pick Just ONE Thing', 'type': 'focus', 'duration': '2 min'},
                    {'action': 'Take 5 Deep Breaths', 'type': 'breathing', 'duration': '2 min'}
                ],
                'short_term': [
                    {'action': 'Make a simple to-do list', 'type': 'organization', 'duration': '10 min'},
                    {'action': 'Say no to one thing', 'type': 'boundaries', 'duration': '5 min'},
                    {'action': 'Ask for help', 'type': 'social', 'duration': '15 min'}
                ]
            },
            'calm': {
                'immediate': [
                    {'action': 'Savor This Moment', 'type': 'mindfulness', 'duration': '2 min'},
                    {'action': 'Gentle Stretching', 'type': 'movement', 'duration': '5 min'},
                    {'action': 'Gratitude Practice', 'type': 'mindfulness', 'duration': '3 min'}
                ],
                'short_term': [
                    {'action': 'Plan something you enjoy', 'type': 'planning', 'duration': '20 min'},
                    {'action': 'Have a meaningful conversation', 'type': 'social', 'duration': '30 min'},
                    {'action': 'Do something creative', 'type': 'expression', 'duration': '45 min'}
                ]
            },
            'happy': {
                'immediate': [
                    {'action': 'Share Your Joy', 'type': 'social', 'duration': '2 min'},
                    {'action': 'Dance or Move', 'type': 'movement', 'duration': '3 min'},
                    {'action': 'Write Down What\'s Good', 'type': 'journaling', 'duration': '3 min'}
                ],
                'short_term': [
                    {'action': 'Do something fun', 'type': 'enjoyment', 'duration': '30 min'},
                    {'action': 'Help someone else', 'type': 'service', 'duration': '20 min'},
                    {'action': 'Plan more good things', 'type': 'planning', 'duration': '15 min'}
                ]
            },
            'neutral': {
                'immediate': [
                    {'action': 'Check In With Body', 'type': 'mindfulness', 'duration': '2 min'},
                    {'action': 'Do Something Small', 'type': 'action', 'duration': '5 min'},
                    {'action': 'Connect With Someone', 'type': 'social', 'duration': '3 min'}
                ],
                'short_term': [
                    {'action': 'Try something new', 'type': 'exploration', 'duration': '30 min'},
                    {'action': 'Reflect on your needs', 'type': 'journaling', 'duration': '20 min'},
                    {'action': 'Do something meaningful', 'type': 'purpose', 'duration': '45 min'}
                ]
            },
            'tired': {
                'immediate': [
                    {'action': 'Rest Your Eyes', 'type': 'rest', 'duration': '3 min'},
                    {'action': 'Drink Water', 'type': 'self-care', 'duration': '1 min'},
                    {'action': 'Gentle Stretching', 'type': 'movement', 'duration': '2 min'}
                ],
                'short_term': [
                    {'action': 'Take a nap', 'type': 'rest', 'duration': '20 min'},
                    {'action': 'Go to bed early', 'type': 'rest', 'duration': '8 hours'},
                    {'action': 'Reduce commitments', 'type': 'boundaries', 'duration': '10 min'}
                ]
            }
        }
        
        return actions.get(emotion, {
            'immediate': [{'action': 'Take a deep breath', 'type': 'breathing', 'duration': '1 min'}],
            'short_term': [{'action': 'Check in with yourself', 'type': 'mindfulness', 'duration': '10 min'}]
        })
    
    def _get_fallback_result(self) -> Dict:
        """Return a safe fallback result if detection fails"""
        return {
            'emotion': 'neutral',
            'emotion_name': 'Neutral/Flat',
            'emotion_emoji': '😐',
            'confidence': 0.5,
            'description': 'Unable to determine emotion clearly',
            'indicators': ['Analysis incomplete'],
            'immediate_actions': [{'action': 'Take a deep breath', 'type': 'breathing', 'duration': '1 min'}],
            'short_term_actions': [{'action': 'Check in with yourself', 'type': 'mindfulness', 'duration': '10 min'}],
            'all_scores': {'neutral': 0.5},
            'analysis_details': {}
        }

# Test the emotion detector
if __name__ == "__main__":
    detector = UnifiedEmotionDetector()
    
    # Test with sample responses
    test_initial_responses = {
        'energy_level': 'low',
        'thoughts': 'stuck', 
        'physical': 'tense',
        'feeling_like': 'crying'
    }
    
    test_journaling_responses = {
        'sad_1': 'I feel really down today, everything seems hopeless',
        'sad_2': 'My body feels heavy and I have no energy',
        'sad_3': 'I wish someone understood how empty I feel inside',
        'sad_4': 'Usually talking to friends helps but I feel too sad to reach out'
    }
    
    result = detector.detect_emotion(test_initial_responses, test_journaling_responses)
    print(f"Detected emotion: {result['emotion_emoji']} {result['emotion_name']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Indicators: {', '.join(result['indicators'])}")
    print(f"Immediate actions: {[a['action'] for a in result['immediate_actions']]}")

