from transformers import pipeline
import torch
import numpy as np
import hashlib
import json
import os
from typing import Dict, List, Tuple, Optional

class AdvancedTextEmotionAnalyzer:
    def __init__(self):
        print("🧠 Loading optimized emotion models...")
        
        # Device management for better performance
        self.device = 0 if torch.cuda.is_available() else -1
        device_name = "GPU" if self.device == 0 else "CPU"
        print(f"📱 Using {device_name} for inference")
        
        # Cache for repeated analyses
        self.cache = {}
        self.cache_file = "text_emotion_cache.json"
        self._load_cache()
        
        # GoEmotions model - 27 nuanced emotions
        try:
            self.goemotions_model = pipeline(
                "text-classification",
                model="SamLowe/roberta-base-go_emotions",
                top_k=None,
                device=self.device,
                max_length=512,  # Better token handling
                truncation=True
            )
            print("✅ GoEmotions model loaded!")
        except Exception as e:
            print(f"❌ GoEmotions failed: {e}")
            self.goemotions_model = None
        
        # Backup basic model
        try:
            self.basic_model = pipeline(
                "text-classification", 
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None,
                device=self.device,
                max_length=512,
                truncation=True
            )
            print("✅ Basic text model loaded!")
        except Exception as e:
            print(f"❌ Basic model failed: {e}")
            self.basic_model = None
        
        # Fallback simple model for extreme cases
        try:
            self.simple_model = pipeline(
                "sentiment-analysis",
                device=self.device
            )
            print("✅ Simple sentiment model loaded!")
        except Exception as e:
            print(f"❌ Simple model failed: {e}")
            self.simple_model = None
    
    def _load_cache(self):
        """Load cached results from disk"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
                print(f"📦 Loaded {len(self.cache)} cached analyses")
        except Exception as e:
            print(f"Cache load error: {e}")
            self.cache = {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
        except Exception as e:
            print(f"Cache save error: {e}")
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for better analysis"""
        if not text:
            return ""
        
        # Basic cleaning
        text = text.strip()
        
        # Truncate if too long (keep most important part)
        if len(text) > 500:
            # Keep first 200 and last 200 characters
            text = text[:200] + " ... " + text[-200:]
        
        return text
    
    def analyze_nuanced_emotions(self, text):
        """Analyze text for 27 nuanced emotions - OPTIMIZED VERSION"""
        if not text or not text.strip():
            return {'neutral': 1.0}, "empty"
        
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Check cache first
        cache_key = self._get_cache_key(processed_text)
        if cache_key in self.cache:
            print("📦 Using cached result")
            return self.cache[cache_key]['emotions'], self.cache[cache_key]['model']
        
        if not self.goemotions_model:
            return self._fallback_analysis(processed_text)
    
        try:
            results = self.goemotions_model(processed_text)
            emotion_probs = {}
            
            # Use the EXACT logic that worked in debug test
            if isinstance(results, list) and len(results) > 0:
                if isinstance(results[0], list):
                    emotions_list = results[0]  # Nested structure
                else:
                    emotions_list = results     # Flat structure
                
                for emotion_data in emotions_list:
                    if isinstance(emotion_data, dict) and 'label' in emotion_data and 'score' in emotion_data:
                        emotion = emotion_data['label']
                        probability = emotion_data['score']
                        emotion_probs[emotion] = probability
            
            # Cache the result
            self.cache[cache_key] = {
                'emotions': emotion_probs,
                'model': 'goemotions'
            }
            self._save_cache()
            
            return emotion_probs, "goemotions"
            
        except Exception as e:
            print(f"GoEmotions error: {e}")
            return self._fallback_analysis(processed_text)
    
    def _fallback_analysis(self, text):
        """Fallback to basic emotions with multiple levels"""
        if not text or not text.strip():
            return {'neutral': 1.0}, "empty"
        
        # Try basic model first
        if self.basic_model:
            try:
                results = self.basic_model(text)
                emotion_probs = {}
                
                if isinstance(results, list) and len(results) > 0:
                    if isinstance(results[0], list):
                        emotions_list = results[0]
                    else:
                        emotions_list = results
                    
                    for emotion_data in emotions_list:
                        if isinstance(emotion_data, dict) and 'label' in emotion_data and 'score' in emotion_data:
                            emotion = emotion_data['label']
                            probability = emotion_data['score']
                            emotion_probs[emotion] = probability
                
                return emotion_probs, "basic"
                
            except Exception as e:
                print(f"Basic model failed: {e}")
        
        # Try simple sentiment as last resort
        if self.simple_model:
            try:
                result = self.simple_model(text)
                if isinstance(result, list):
                    result = result[0]
                
                # Convert sentiment to emotion
                label = result['label'].lower()
                score = result['score']
                
                if label == 'positive':
                    emotion_probs = {'joy': score, 'optimism': score * 0.7}
                elif label == 'negative':
                    emotion_probs = {'sadness': score, 'anger': score * 0.6}
                else:
                    emotion_probs = {'neutral': score}
                
                return emotion_probs, "sentiment"
                
            except Exception as e:
                print(f"Sentiment model failed: {e}")
        
        # Ultimate fallback
        return {'neutral': 1.0}, "dummy"
    
    def get_top_emotions(self, emotion_probs, top_k=3):
        """Get top K emotions - BULLETPROOF VERSION"""
        if not emotion_probs:
            return [('neutral', 1.0)]
        
        try:
            # Convert to list of tuples and sort
            items = list(emotion_probs.items())
            sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
            return sorted_items[:top_k]
        except Exception as e:
            print(f"Error in get_top_emotions: {e}")
            return [('neutral', 1.0)]
    
    def map_to_actionable_categories(self, emotion_probs):
        """Map to actionable categories - IMPROVED VERSION"""
        if not emotion_probs:
            return {'calm': 1.0}
        
        try:
            # Enhanced emotion clusters with better coverage
            emotion_clusters = {
                'stressed': [
                    'nervousness', 'anxiety', 'fear', 'disappointment', 'confusion',
                    'embarrassment', 'remorse', 'grief', 'disapproval'
                ],
                'anxious': [
                    'nervousness', 'anxiety', 'fear', 'confusion', 'embarrassment'
                ],
                'overwhelmed': [
                    'confusion', 'nervousness', 'anxiety', 'sadness', 'disappointment',
                    'embarrassment', 'remorse'
                ],
                'frustrated': [
                    'anger', 'annoyance', 'disapproval', 'disappointment', 'remorse'
                ],
                'sad': [
                    'sadness', 'disappointment', 'grief', 'remorse', 'embarrassment'
                ],
                'positive': [
                    'joy', 'excitement', 'optimism', 'pride', 'gratitude', 'love',
                    'admiration', 'amusement', 'approval', 'caring', 'desire', 'relief'
                ],
                'calm': [
                    'neutral', 'realization', 'approval', 'relief', 'caring'
                ],
                'energized': [
                    'excitement', 'joy', 'pride', 'admiration', 'optimism', 'desire'
                ]
            }
            
            cluster_scores = {}
            for cluster_name, emotion_list in emotion_clusters.items():
                score = 0.0
                count = 0
                for emotion in emotion_list:
                    if emotion in emotion_probs:
                        score += emotion_probs[emotion]
                        count += 1
                
                # Normalize by count to avoid bias toward clusters with more emotions
                if count > 0:
                    cluster_scores[cluster_name] = score / count
                else:
                    cluster_scores[cluster_name] = 0.0
            
            # Ensure we have at least one category
            if not any(score > 0 for score in cluster_scores.values()):
                cluster_scores['calm'] = 1.0
            
            return cluster_scores
        except Exception as e:
            print(f"Error in map_to_actionable_categories: {e}")
            return {'calm': 1.0}
    
    def analyze_complete(self, text):
        """Complete analysis - OPTIMIZED VERSION"""
        if not text or not text.strip():
            return {
                'text': '',
                'model_used': 'none',
                'all_emotions': {'neutral': 1.0},
                'top_emotions': [('neutral', 1.0)],
                'actionable_category': 'calm',
                'category_confidence': 1.0,
                'cluster_scores': {'calm': 1.0},
                'analysis_quality': 'empty_input'
            }
        
        try:
            # Step 1: Get emotions
            emotion_probs, model_used = self.analyze_nuanced_emotions(text)
            
            # Step 2: Get top emotions
            top_emotions = self.get_top_emotions(emotion_probs, top_k=5)
            
            # Step 3: Get cluster scores
            cluster_scores = self.map_to_actionable_categories(emotion_probs)
            
            # Step 4: Find top cluster
            if cluster_scores:
                top_cluster_name = max(cluster_scores.keys(), key=lambda k: cluster_scores[k])
                top_cluster_score = cluster_scores[top_cluster_name]
            else:
                top_cluster_name = 'calm'
                top_cluster_score = 1.0
            
            # Step 5: Assess analysis quality
            analysis_quality = self._assess_analysis_quality(emotion_probs, model_used, top_cluster_score)
            
            return {
                'text': text,
                'model_used': model_used,
                'all_emotions': emotion_probs,
                'top_emotions': top_emotions,
                'actionable_category': top_cluster_name,
                'category_confidence': top_cluster_score,
                'cluster_scores': cluster_scores,
                'analysis_quality': analysis_quality
            }
        
        except Exception as e:
            print(f"Error in analyze_complete: {e}")
            return {
                'text': text,
                'model_used': 'error',
                'all_emotions': {'neutral': 1.0},
                'top_emotions': [('neutral', 1.0)],
                'actionable_category': 'calm',
                'category_confidence': 1.0,
                'cluster_scores': {'calm': 1.0},
                'analysis_quality': 'error'
            }
    
    def _assess_analysis_quality(self, emotion_probs, model_used, confidence):
        """Assess the quality of the analysis"""
        try:
            if model_used == 'goemotions':
                return 'high'
            elif model_used == 'basic':
                return 'medium'
            elif model_used == 'sentiment':
                return 'low'
            elif confidence > 0.7:
                return 'high'
            elif confidence > 0.4:
                return 'medium'
            else:
                return 'low'
        except:
            return 'unknown'

# Test
if __name__ == "__main__":
    analyzer = AdvancedTextEmotionAnalyzer()
    result = analyzer.analyze_complete("I'm feeling really anxious about tomorrow")
    print(f"Model: {result['model_used']}")
    print(f"Category: {result['actionable_category']}")
    print(f"Top emotions: {result['top_emotions'][:3]}")