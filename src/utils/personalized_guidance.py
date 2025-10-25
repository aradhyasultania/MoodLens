import json
import datetime
from typing import Dict, List, Any, Optional

class PersonalizedGuidanceEngine:
    def __init__(self):
        """Initialize the guidance system with adaptive recommendations"""
        
        # User preference tracking (in real app, this would be in a database)
        self.user_preferences = {
            'preferred_techniques': [],
            'technique_effectiveness': {},
            'personality_type': None,
            'stress_triggers': [],
            'successful_strategies': []
        }
        
        # Technique database with multiple options per emotion
        self.technique_database = {
            'stressed': {
                'breathing': [
                    {'name': '4-7-8 Breathing', 'duration': '2 minutes', 'effectiveness': 'high'},
                    {'name': 'Box Breathing', 'duration': '3 minutes', 'effectiveness': 'high'},
                    {'name': 'Belly Breathing', 'duration': '5 minutes', 'effectiveness': 'medium'}
                ],
                'physical': [
                    {'name': 'Progressive Muscle Relaxation', 'duration': '10 minutes', 'effectiveness': 'high'},
                    {'name': 'Quick Shoulder Stretches', 'duration': '2 minutes', 'effectiveness': 'medium'},
                    {'name': 'Desk Yoga', 'duration': '5 minutes', 'effectiveness': 'medium'}
                ],
                'cognitive': [
                    {'name': 'Priority Matrix', 'duration': '10 minutes', 'effectiveness': 'high'},
                    {'name': 'Stress Journal', 'duration': '15 minutes', 'effectiveness': 'medium'},
                    {'name': 'Reality Check Questions', 'duration': '5 minutes', 'effectiveness': 'medium'}
                ]
            },
            'anxious': {
                'grounding': [
                    {'name': '5-4-3-2-1 Grounding', 'duration': '5 minutes', 'effectiveness': 'high'},
                    {'name': 'Body Scan', 'duration': '10 minutes', 'effectiveness': 'high'},
                    {'name': 'Mindful Breathing', 'duration': '7 minutes', 'effectiveness': 'medium'}
                ],
                'cognitive': [
                    {'name': 'Worry Time Scheduling', 'duration': '15 minutes', 'effectiveness': 'high'},
                    {'name': 'Anxiety Thought Record', 'duration': '20 minutes', 'effectiveness': 'high'},
                    {'name': 'What-If Scenario Planning', 'duration': '15 minutes', 'effectiveness': 'medium'}
                ]
            }
        }
        
        # Context-aware modifiers
        self.context_modifiers = {
            'time_of_day': {
                'morning': {'energy_boost': True, 'gentle_start': True},
                'afternoon': {'energy_reset': True, 'productivity_focus': True},
                'evening': {'wind_down': True, 'reflection': True},
                'night': {'calm_only': True, 'low_energy': True}
            },
            'confidence_level': {
                'high': {'advanced_techniques': True, 'longer_duration': True},
                'medium': {'standard_techniques': True, 'guided_options': True},
                'low': {'simple_techniques': True, 'short_duration': True}
            }
        }
    
    def generate_personalized_recommendations(self, 
                                           emotion: str, 
                                           confidence: float,
                                           modality_data: Dict,
                                           user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate personalized recommendations - BULLETPROOFED VERSION"""
        
        try:
            current_time = datetime.datetime.now().hour
            time_context = self._get_time_context(current_time)
            
            # Initialize with safe defaults
            recommendations = {
                'primary_emotion': emotion or 'neutral',
                'confidence_level': self._categorize_confidence(confidence),
                'time_context': time_context,
                'immediate_actions': [],
                'short_term_strategies': [],
                'long_term_suggestions': [],
                'personalization_notes': [],
                'follow_up_questions': []
            }
            
            # Generate immediate actions (next 5 minutes)
            try:
                immediate = self._generate_immediate_actions(emotion, confidence, modality_data, time_context)
                recommendations['immediate_actions'] = immediate
            except Exception as e:
                print(f"Error generating immediate actions: {e}")
                recommendations['immediate_actions'] = [
                    {
                        'action': 'Take 3 deep breaths',
                        'duration': '1 minute',
                        'instructions': 'Breathe slowly and focus on the present moment',
                        'why': 'Helps activate your body\'s relaxation response'
                    }
                ]
            
            # Generate short-term strategies (next 30 minutes to 2 hours)
            try:
                short_term = self._generate_short_term_strategies(emotion, confidence, modality_data)
                recommendations['short_term_strategies'] = short_term
            except Exception as e:
                print(f"Error generating short-term strategies: {e}")
                recommendations['short_term_strategies'] = [
                    {
                        'name': 'Self-Check-In',
                        'duration': '10 minutes',
                        'description': 'Take time to assess your current needs and feelings'
                    }
                ]
            
            # Generate long-term suggestions (ongoing patterns)
            try:
                long_term = self._generate_long_term_suggestions(emotion, modality_data)
                recommendations['long_term_suggestions'] = long_term
            except Exception as e:
                print(f"Error generating long-term suggestions: {e}")
                recommendations['long_term_suggestions'] = [
                    "Consider keeping a mood journal to track emotional patterns",
                    "Practice regular stress-reduction techniques",
                    "Maintain healthy sleep and exercise habits"
                ]
            
            # Add personalization based on analysis details
            try:
                personalization = self._add_personalization_notes(modality_data, confidence)
                recommendations['personalization_notes'] = personalization
            except Exception as e:
                print(f"Error generating personalization notes: {e}")
                recommendations['personalization_notes'] = ["Analysis completed successfully"]
            
            # Generate follow-up questions for learning
            try:
                follow_up = self._generate_follow_up_questions(emotion)
                recommendations['follow_up_questions'] = follow_up
            except Exception as e:
                print(f"Error generating follow-up questions: {e}")
                recommendations['follow_up_questions'] = ["How are you feeling right now?"]
            
            return recommendations
        
        except Exception as e:
            print(f"Error in generate_personalized_recommendations: {e}")
            # Return minimal safe recommendations
            return {
                'primary_emotion': 'neutral',
                'confidence_level': 'medium',
                'time_context': 'general',
                'immediate_actions': [
                    {
                        'action': 'Take a moment to breathe',
                        'duration': '1 minute',
                        'instructions': 'Focus on your breathing',
                        'why': 'Helps center yourself'
                    }
                ],
                'short_term_strategies': [
                    {
                        'name': 'Self-reflection',
                        'duration': '10 minutes',
                        'description': 'Check in with yourself'
                    }
                ],
                'long_term_suggestions': ["Practice regular self-care"],
                'personalization_notes': ["Recommendations generated"],
                'follow_up_questions': ["How are you feeling?"]
            }
    
    def _get_time_context(self, hour: int) -> str:
        """Determine time context for appropriate recommendations"""
        try:
            if 5 <= hour < 12:
                return 'morning'
            elif 12 <= hour < 17:
                return 'afternoon'  
            elif 17 <= hour < 22:
                return 'evening'
            else:
                return 'night'
        except:
            return 'general'
    
    def _categorize_confidence(self, confidence: float) -> str:
        """Categorize confidence for recommendation complexity"""
        try:
            if confidence >= 0.7:
                return 'high'
            elif confidence >= 0.4:
                return 'medium'
            else:
                return 'low'
        except:
            return 'medium'
    
    def _generate_immediate_actions(self, emotion: str, confidence: float, 
                                  modality_data: Dict, time_context: str) -> List[Dict]:
        """Generate immediate actionable steps"""
        actions = []
        
        try:
            # Breathing techniques (almost always appropriate)
            if emotion in ['stressed', 'anxious', 'overwhelmed']:
                actions.append({
                    'action': 'Take 3 deep, slow breaths',
                    'duration': '1 minute',
                    'instructions': 'Breathe in for 4 counts, hold for 4, exhale for 6. Focus only on your breath.',
                    'why': 'Activates your parasympathetic nervous system to reduce stress response'
                })
            
            # Modality-specific immediate actions
            if modality_data and isinstance(modality_data, dict):
                if 'voice' in modality_data and modality_data['voice']:
                    voice_data = modality_data['voice']
                    if (voice_data.get('stress_analysis', {}).get('stress_likelihood', 0) > 0.6):
                        actions.append({
                            'action': 'Lower and slow your voice',
                            'duration': '2 minutes',
                            'instructions': 'Speak more slowly and in a lower tone for the next few minutes.',
                            'why': 'Your voice analysis shows stress patterns - conscious voice modulation can help'
                        })
                
                if 'face' in modality_data and modality_data['face']:
                    face_data = modality_data['face']
                    if face_data.get('actionable_category') == 'stressed':
                        actions.append({
                            'action': 'Relax your facial muscles',
                            'duration': '30 seconds',
                            'instructions': 'Gently massage your temples, unclench your jaw, and soften your forehead.',
                            'why': 'Facial tension was detected - releasing it can reduce overall stress'
                        })
            
            # Time-appropriate actions
            if time_context == 'morning' and emotion == 'anxious':
                actions.append({
                    'action': 'Ground yourself for the day',
                    'duration': '3 minutes',
                    'instructions': 'Plant your feet firmly on the ground, name your top 3 priorities for today.',
                    'why': 'Morning anxiety often comes from overwhelming thoughts about the day ahead'
                })
            elif time_context == 'night' and emotion in ['stressed', 'overwhelmed']:
                actions.append({
                    'action': 'Brain dump for tomorrow',
                    'duration': '5 minutes',
                    'instructions': 'Write down everything on your mind on paper. Tell your brain you\'ll deal with it tomorrow.',
                    'why': 'Evening stress often comes from unfinished mental loops'
                })
        
        except Exception as e:
            print(f"Error in immediate actions generation: {e}")
            actions.append({
                'action': 'Take a deep breath',
                'duration': '1 minute',
                'instructions': 'Focus on breathing slowly',
                'why': 'Helps calm the nervous system'
            })
        
        return actions[:3] if actions else [actions[0] if actions else {
            'action': 'Pause and breathe',
            'duration': '1 minute',
            'instructions': 'Take a moment to center yourself',
            'why': 'Provides immediate grounding'
        }]
    
    def _generate_short_term_strategies(self, emotion: str, confidence: float, 
                                      modality_data: Dict) -> List[Dict]:
        """Generate strategies for the next 30 minutes to 2 hours"""
        strategies = []
        
        try:
            base_strategies = {
                'stressed': [
                    {'name': 'Priority Reset', 'duration': '15 minutes', 
                     'description': 'List everything causing stress, then identify the top 3 you can actually control today'},
                    {'name': 'Movement Break', 'duration': '20 minutes',
                     'description': 'Take a walk, do stretches, or engage in any physical activity that feels good'}
                ],
                'anxious': [
                    {'name': 'Worry Window', 'duration': '20 minutes',
                     'description': 'Set aside specific time to fully worry, then practice letting go when time is up'},
                    {'name': 'Social Connection', 'duration': '15 minutes',
                     'description': 'Reach out to someone supportive - even a brief chat can shift perspective'}
                ],
                'overwhelmed': [
                    {'name': 'Single-Task Focus', 'duration': '45 minutes',
                     'description': 'Choose ONE task and work on only that. Use timer and take breaks every 15 minutes'},
                    {'name': 'Simplification Review', 'duration': '30 minutes',
                     'description': 'Go through your to-do list and eliminate, delegate, or postpone half of it'}
                ],
                'sad': [
                    {'name': 'Gentle Self-Care', 'duration': '30 minutes',
                     'description': 'Do something nurturing for yourself - warm drink, comfort show, or call a friend'},
                    {'name': 'Emotion Processing', 'duration': '20 minutes',
                     'description': 'Journal about your feelings or just sit with them without trying to fix anything'}
                ]
            }
            
            if emotion and emotion in base_strategies:
                strategies.extend(base_strategies[emotion])
            else:
                # Default strategies
                strategies.extend([
                    {'name': 'Self-Assessment', 'duration': '10 minutes',
                     'description': 'Check in with your physical and emotional needs'},
                    {'name': 'Mindful Activity', 'duration': '15 minutes',
                     'description': 'Engage in an activity that brings you into the present moment'}
                ])
            
            # Add confidence-based modifications
            if confidence < 0.5:
                strategies.append({
                    'name': 'Multiple Check-ins',
                    'duration': 'ongoing',
                    'description': 'Since analysis confidence was lower, check in with yourself every hour today'
                })
            
        except Exception as e:
            print(f"Error generating short-term strategies: {e}")
            strategies = [
                {'name': 'Self-reflection', 'duration': '15 minutes',
                 'description': 'Take time to understand your current emotional state'}
            ]
        
        return strategies[:4]  # Limit to top 4 strategies
    
    def _generate_long_term_suggestions(self, emotion: str, modality_data: Dict) -> List[str]:
        """Generate long-term pattern suggestions"""
        suggestions = []
        
        try:
            # Pattern-based suggestions
            if emotion in ['stressed', 'overwhelmed']:
                suggestions.extend([
                    "Consider tracking when stress peaks during your day/week to identify patterns",
                    "Explore time management techniques like time-blocking or the Pomodoro Technique",
                    "Practice saying 'no' to commitments that don't align with your priorities"
                ])
            
            if emotion == 'anxious':
                suggestions.extend([
                    "Consider mindfulness or meditation practice for daily anxiety management",
                    "Keep an anxiety trigger journal to identify patterns",
                    "Practice uncertainty tolerance exercises when you're feeling calm"
                ])
            
            if emotion == 'sad':
                suggestions.extend([
                    "Consider talking to a counselor or therapist if sadness persists",
                    "Build a support network of trusted friends and family",
                    "Engage in activities that give you a sense of purpose and meaning"
                ])
            
            # Modality-specific long-term suggestions
            if modality_data and isinstance(modality_data, dict):
                if 'voice' in modality_data and modality_data['voice']:
                    voice_data = modality_data['voice']
                    if voice_data.get('stress_analysis', {}).get('stress_likelihood', 0) > 0.5:
                        suggestions.append("Your voice patterns suggest chronic stress - consider stress management coaching or therapy")
                
                # Multi-modal agreement
                emotion_matches = sum(1 for m in modality_data.values() 
                                    if m and m.get('actionable_category') == emotion)
                if emotion_matches >= 2:
                    suggestions.append(f"Multiple analysis methods detected {emotion} - consider this a reliable signal to prioritize {emotion} management")
            
            # Default suggestions if none added
            if not suggestions:
                suggestions.extend([
                    "Practice regular self-care and stress management",
                    "Maintain healthy sleep, nutrition, and exercise habits",
                    "Consider professional support if emotional challenges persist"
                ])
        
        except Exception as e:
            print(f"Error generating long-term suggestions: {e}")
            suggestions = [
                "Practice regular self-care",
                "Monitor your emotional patterns",
                "Seek support when needed"
            ]
        
        return suggestions[:3]  # Limit to top 3 long-term suggestions
    
    def _add_personalization_notes(self, modality_data: Dict, confidence: float) -> List[str]:
        """Add personalized notes based on analysis details"""
        notes = []
        
        try:
            if modality_data and isinstance(modality_data, dict):
                # Multi-modal agreement notes
                modalities_used = [k for k, v in modality_data.items() if v is not None]
                if len(modalities_used) >= 2:
                    notes.append(f"Analysis used {len(modalities_used)} methods ({', '.join(modalities_used)}) for comprehensive assessment")
                
                # Confidence-based notes
                if confidence > 0.8:
                    notes.append("High confidence analysis - these recommendations are well-tailored to your current state")
                elif confidence < 0.4:
                    notes.append("Lower confidence analysis - try different techniques and see what resonates")
                
                # Specific modality insights
                if 'voice' in modality_data and modality_data['voice']:
                    voice_data = modality_data['voice']
                    if voice_data.get('spoken_text'):
                        notes.append("Your own words were analyzed along with voice tone for more accurate results")
                
                if 'face' in modality_data and modality_data['face']:
                    notes.append("Facial expression analysis included - your non-verbal communication was considered")
            
            # Default note if none added
            if not notes:
                notes.append("Analysis completed using available data")
        
        except Exception as e:
            print(f"Error generating personalization notes: {e}")
            notes = ["Recommendations generated based on your input"]
        
        return notes
    
    def _generate_follow_up_questions(self, emotion: str) -> List[str]:
        """Generate questions to help the system learn and improve recommendations"""
        
        try:
            base_questions = [
                "Which of these recommendations feels most doable right now?",
                "Have you noticed this emotional pattern before?",
                "What usually helps when you feel this way?"
            ]
            
            emotion_specific = {
                'stressed': [
                    "What specific stressor is most prominent today?",
                    "Do you feel more mentally or physically stressed?",
                    "Is this stress about something specific or more general?"
                ],
                'anxious': [
                    "Is this anxiety about something specific or more general worry?",
                    "Do you feel this anxiety more in your body or your thoughts?",
                    "What's one small thing you can control in this situation?"
                ],
                'overwhelmed': [
                    "What's contributing most to feeling overwhelmed right now?",
                    "Are you overwhelmed by tasks, emotions, or decisions?",
                    "What would need to change for you to feel more manageable?"
                ]
            }
            
            questions = base_questions.copy()
            if emotion and emotion in emotion_specific:
                questions.extend(emotion_specific[emotion])
        
        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
            questions = [
                "How are you feeling right now?",
                "What would be most helpful for you?",
                "Which approach feels right for you?"
            ]
        
        return questions[:4]  # Limit to 4 questions

# Test the fixed personalized guidance system
if __name__ == "__main__":
    guidance_engine = PersonalizedGuidanceEngine()
    
    # Example usage with safer data handling
    sample_modality_data = {
        'face': {
            'actionable_category': 'stressed',
            'category_confidence': 0.75,
            'top_emotions': [('angry', 0.4), ('fear', 0.3), ('neutral', 0.2)]
        },
        'voice': {
            'actionable_category': 'stressed', 
            'category_confidence': 0.65,
            'stress_analysis': {'stress_likelihood': 0.7},
            'spoken_text': "I have so much to do and not enough time"
        },
        'text': {
            'actionable_category': 'overwhelmed',
            'category_confidence': 0.80,
            'top_emotions': [('anxiety', 0.5), ('nervousness', 0.3), ('disappointment', 0.2)]
        }
    }
    
    try:
        recommendations = guidance_engine.generate_personalized_recommendations(
            emotion='stressed',
            confidence=0.73,
            modality_data=sample_modality_data
        )
        
        print("PERSONALIZED GUIDANCE EXAMPLE")
        print("="*60)
        print(f"Primary Emotion: {recommendations['primary_emotion']}")
        print(f"Confidence Level: {recommendations['confidence_level']}")
        print(f"Time Context: {recommendations['time_context']}")
        
        print("\nIMMEDIATE ACTIONS (next 5 minutes):")
        for i, action in enumerate(recommendations['immediate_actions'], 1):
            print(f"{i}. {action['action']} ({action['duration']})")
            print(f"   Instructions: {action['instructions']}")
            print(f"   Why: {action['why']}\n")
        
        print("SHORT-TERM STRATEGIES (next 30 minutes - 2 hours):")
        for i, strategy in enumerate(recommendations['short_term_strategies'], 1):
            print(f"{i}. {strategy['name']} ({strategy['duration']})")
            print(f"   {strategy['description']}\n")
        
        print("LONG-TERM SUGGESTIONS:")
        for i, suggestion in enumerate(recommendations['long_term_suggestions'], 1):
            print(f"{i}. {suggestion}")
        
        print(f"\nPERSONALIZATION NOTES:")
        for note in recommendations['personalization_notes']:
            print(f"• {note}")
        
        print(f"\nFOLLOW-UP QUESTIONS:")
        for question in recommendations['follow_up_questions']:
            print(f"• {question}")
    
    except Exception as e:
        print(f"Test failed with error: {e}")