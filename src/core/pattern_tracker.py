"""
Pattern Tracker for MoodLens
Tracks emotional patterns and provides insights over time
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class PatternTracker:
    def __init__(self):
        print("📊 Initializing Pattern Tracker...")
        
        self.history_file = "emotional_patterns.json"
        self.patterns = self._load_patterns()
        
        print("✅ Pattern Tracker ready!")
    
    def _load_patterns(self) -> Dict:
        """Load existing pattern data"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            else:
                return {
                    'check_ins': [],
                    'emotion_counts': {},
                    'daily_patterns': {},
                    'weekly_patterns': {},
                    'triggers': {},
                    'insights': []
                }
        except Exception as e:
            print(f"Error loading patterns: {e}")
            return {
                'check_ins': [],
                'emotion_counts': {},
                'daily_patterns': {},
                'weekly_patterns': {},
                'triggers': {},
                'insights': []
            }
    
    def _save_patterns(self):
        """Save pattern data to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving patterns: {e}")
    
    def add_check_in(self, emotion_data: Dict, user_responses: Dict):
        """Add a new check-in to the pattern tracking"""
        try:
            timestamp = datetime.now()
            
            check_in = {
                'timestamp': timestamp.isoformat(),
                'date': timestamp.strftime('%Y-%m-%d'),
                'time': timestamp.strftime('%H:%M'),
                'day_of_week': timestamp.strftime('%A'),
                'hour': timestamp.hour,
                'emotion': emotion_data['emotion'],
                'emotion_name': emotion_data['emotion_name'],
                'confidence': emotion_data['confidence'],
                'indicators': emotion_data['indicators'],
                'user_responses': user_responses
            }
            
            # Add to check-ins
            self.patterns['check_ins'].append(check_in)
            
            # Update emotion counts
            emotion = emotion_data['emotion']
            if emotion not in self.patterns['emotion_counts']:
                self.patterns['emotion_counts'][emotion] = 0
            self.patterns['emotion_counts'][emotion] += 1
            
            # Update daily patterns
            date_str = timestamp.strftime('%Y-%m-%d')
            if date_str not in self.patterns['daily_patterns']:
                self.patterns['daily_patterns'][date_str] = []
            self.patterns['daily_patterns'][date_str].append(emotion)
            
            # Update weekly patterns
            week_start = timestamp - timedelta(days=timestamp.weekday())
            week_str = week_start.strftime('%Y-W%U')
            if week_str not in self.patterns['weekly_patterns']:
                self.patterns['weekly_patterns'][week_str] = []
            self.patterns['weekly_patterns'][week_str].append(emotion)
            
            # Extract triggers from responses
            self._extract_triggers(user_responses, emotion)
            
            # Generate insights
            self._generate_insights()
            
            # Save patterns
            self._save_patterns()
            
        except Exception as e:
            print(f"Error adding check-in: {e}")
    
    def _extract_triggers(self, responses: Dict, emotion: str):
        """Extract potential triggers from user responses"""
        try:
            # Map responses to potential triggers
            trigger_mapping = {
                'energy_level': {
                    'low': 'fatigue',
                    'high': 'overstimulation'
                },
                'thoughts': {
                    'racing': 'mental_overload',
                    'stuck': 'feeling_trapped'
                },
                'physical': {
                    'tense': 'physical_stress',
                    'relaxed': 'physical_comfort'
                },
                'worry': {
                    'a_lot': 'high_stress',
                    'nothing': 'low_stress'
                },
                'need_most': {
                    'rest': 'burnout',
                    'action': 'restlessness',
                    'company': 'loneliness'
                }
            }
            
            for question, answer in responses.items():
                if question in trigger_mapping and answer in trigger_mapping[question]:
                    trigger = trigger_mapping[question][answer]
                    
                    if trigger not in self.patterns['triggers']:
                        self.patterns['triggers'][trigger] = {}
                    
                    if emotion not in self.patterns['triggers'][trigger]:
                        self.patterns['triggers'][trigger][emotion] = 0
                    
                    self.patterns['triggers'][trigger][emotion] += 1
                    
        except Exception as e:
            print(f"Error extracting triggers: {e}")
    
    def _generate_insights(self):
        """Generate insights from pattern data"""
        try:
            insights = []
            
            # Most common emotion
            if self.patterns['emotion_counts']:
                most_common = max(self.patterns['emotion_counts'].items(), key=lambda x: x[1])
                insights.append({
                    'type': 'most_common_emotion',
                    'text': f"You've felt {most_common[0]} most often ({most_common[1]} times)",
                    'priority': 'medium'
                })
            
            # Time patterns
            if len(self.patterns['check_ins']) >= 3:
                hour_emotions = defaultdict(list)
                for check_in in self.patterns['check_ins'][-10:]:  # Last 10 check-ins
                    hour = int(check_in['hour'])
                    hour_emotions[hour].append(check_in['emotion'])
                
                # Find patterns in hours
                for hour, emotions in hour_emotions.items():
                    if len(emotions) >= 2:
                        most_common_hour_emotion = Counter(emotions).most_common(1)[0]
                        if most_common_hour_emotion[1] >= 2:
                            time_period = self._get_time_period(hour)
                            insights.append({
                                'type': 'time_pattern',
                                'text': f"You often feel {most_common_hour_emotion[0]} during {time_period}",
                                'priority': 'low'
                            })
            
            # Trigger patterns
            for trigger, emotions in self.patterns['triggers'].items():
                if len(emotions) >= 2:
                    most_common_trigger_emotion = max(emotions.items(), key=lambda x: x[1])
                    if most_common_trigger_emotion[1] >= 2:
                        insights.append({
                            'type': 'trigger_pattern',
                            'text': f"When you experience {trigger}, you often feel {most_common_trigger_emotion[0]}",
                            'priority': 'high'
                        })
            
            # Recent trend
            if len(self.patterns['check_ins']) >= 3:
                recent_emotions = [ci['emotion'] for ci in self.patterns['check_ins'][-3:]]
                if len(set(recent_emotions)) == 1:
                    insights.append({
                        'type': 'recent_trend',
                        'text': f"You've been feeling {recent_emotions[0]} consistently",
                        'priority': 'medium'
                    })
            
            self.patterns['insights'] = insights[-10:]  # Keep last 10 insights
            
        except Exception as e:
            print(f"Error generating insights: {e}")
    
    def _get_time_period(self, hour: int) -> str:
        """Convert hour to time period"""
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def get_pattern_summary(self, days: int = 7) -> Dict:
        """Get a summary of patterns over the last N days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d')
            
            # Filter recent check-ins
            recent_check_ins = [
                ci for ci in self.patterns['check_ins']
                if ci['date'] >= cutoff_str
            ]
            
            if not recent_check_ins:
                return {
                    'total_check_ins': 0,
                    'emotion_summary': {},
                    'insights': [],
                    'recommendations': []
                }
            
            # Emotion summary
            emotion_counts = Counter(ci['emotion'] for ci in recent_check_ins)
            total_check_ins = len(recent_check_ins)
            
            emotion_summary = {}
            for emotion, count in emotion_counts.items():
                emotion_summary[emotion] = {
                    'count': count,
                    'percentage': round((count / total_check_ins) * 100, 1)
                }
            
            # Get relevant insights
            relevant_insights = [
                insight for insight in self.patterns['insights']
                if insight['priority'] in ['high', 'medium']
            ]
            
            # Generate recommendations based on patterns
            recommendations = self._generate_recommendations(emotion_summary, recent_check_ins)
            
            return {
                'total_check_ins': total_check_ins,
                'emotion_summary': emotion_summary,
                'insights': relevant_insights[-5:],  # Last 5 insights
                'recommendations': recommendations,
                'time_range': f"Last {days} days"
            }
            
        except Exception as e:
            print(f"Error getting pattern summary: {e}")
            return {
                'total_check_ins': 0,
                'emotion_summary': {},
                'insights': [],
                'recommendations': []
            }
    
    def _generate_recommendations(self, emotion_summary: Dict, recent_check_ins: List[Dict]) -> List[str]:
        """Generate recommendations based on patterns"""
        recommendations = []
        
        try:
            # Most common emotion recommendations
            if emotion_summary:
                most_common_emotion = max(emotion_summary.items(), key=lambda x: x[1]['count'])
                emotion = most_common_emotion[0]
                percentage = most_common_emotion[1]['percentage']
                
                if percentage >= 50:  # If feeling one emotion 50%+ of the time
                    if emotion == 'anxious':
                        recommendations.append("Consider daily stress management techniques")
                    elif emotion == 'sad':
                        recommendations.append("You might benefit from talking to someone")
                    elif emotion == 'overwhelmed':
                        recommendations.append("Try breaking tasks into smaller steps")
                    elif emotion == 'tired':
                        recommendations.append("Consider your sleep schedule and rest needs")
            
            # Frequency recommendations
            total_check_ins = len(recent_check_ins)
            if total_check_ins >= 5:
                recommendations.append("Great job checking in regularly!")
            elif total_check_ins >= 2:
                recommendations.append("Consider checking in daily for better insights")
            else:
                recommendations.append("Try checking in more often to build patterns")
            
            # Time-based recommendations
            if recent_check_ins:
                recent_times = [ci['hour'] for ci in recent_check_ins[-3:]]
                avg_hour = sum(recent_times) / len(recent_times)
                
                if avg_hour < 10:
                    recommendations.append("You tend to check in early - consider evening reflection too")
                elif avg_hour > 18:
                    recommendations.append("You check in late - morning check-ins might help start your day")
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
        
        return recommendations[:3]  # Limit to 3 recommendations
    
    def get_emotion_history(self, emotion: str, days: int = 30) -> List[Dict]:
        """Get history of a specific emotion"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d')
            
            emotion_history = [
                ci for ci in self.patterns['check_ins']
                if ci['emotion'] == emotion and ci['date'] >= cutoff_str
            ]
            
            return emotion_history
            
        except Exception as e:
            print(f"Error getting emotion history: {e}")
            return []
    
    def get_weekly_summary(self) -> Dict:
        """Get summary of this week's patterns"""
        try:
            # Get current week
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_str = week_start.strftime('%Y-W%U')
            
            # Get this week's emotions
            week_emotions = self.patterns['weekly_patterns'].get(week_str, [])
            
            if not week_emotions:
                return {
                    'week': week_str,
                    'total_check_ins': 0,
                    'emotion_counts': {},
                    'most_common': None
                }
            
            emotion_counts = Counter(week_emotions)
            most_common = emotion_counts.most_common(1)[0] if emotion_counts else None
            
            return {
                'week': week_str,
                'total_check_ins': len(week_emotions),
                'emotion_counts': dict(emotion_counts),
                'most_common': most_common[0] if most_common else None
            }
            
        except Exception as e:
            print(f"Error getting weekly summary: {e}")
            return {
                'week': 'unknown',
                'total_check_ins': 0,
                'emotion_counts': {},
                'most_common': None
            }

# Test the pattern tracker
if __name__ == "__main__":
    tracker = PatternTracker()
    
    print("MoodLens Pattern Tracker")
    print("=" * 40)
    
    # Test with sample data
    sample_emotion_data = {
        'emotion': 'anxious',
        'emotion_name': 'Anxious/Worried',
        'confidence': 0.75,
        'indicators': ['racing thoughts', 'tension']
    }
    
    sample_responses = {
        'energy_level': 'high',
        'thoughts': 'racing',
        'physical': 'tense',
        'worry': 'a_lot'
    }
    
    # Add sample check-in
    tracker.add_check_in(sample_emotion_data, sample_responses)
    
    # Get pattern summary
    summary = tracker.get_pattern_summary()
    print(f"Total check-ins: {summary['total_check_ins']}")
    print(f"Emotion summary: {summary['emotion_summary']}")
    print(f"Insights: {len(summary['insights'])}")
    print(f"Recommendations: {summary['recommendations']}")

