from transformers import pipeline
import cv2
from PIL import Image
import numpy as np
import torch
import os
import time
from typing import Dict, List, Tuple, Optional

class AdvancedFaceEmotionAnalyzer:
    def __init__(self):
        print("👁️ Loading optimized face emotion models...")
        
        # Device management
        self.device = 0 if torch.cuda.is_available() else -1
        device_name = "GPU" if self.device == 0 else "CPU"
        print(f"📱 Using {device_name} for face analysis")
        
        # Multiple face emotion models for better coverage
        self.models = {}
        
        # Model 1: Primary face emotion model
        try:
            self.models['primary'] = pipeline(
                "image-classification",
                model="trpakov/vit-face-expression",
                top_k=None,
                device=self.device
            )
            print("✅ Primary face model loaded")
        except Exception as e:
            print(f"❌ Primary model failed: {e}")
        
        # Model 2: Backup emotion model
        try:
            self.models['backup'] = pipeline(
                "image-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None,
                device=self.device
            )
            print("✅ Backup face model loaded")
        except Exception as e:
            print(f"❌ Backup model failed: {e}")
        
        # Model 3: Simple sentiment fallback
        try:
            self.models['sentiment'] = pipeline(
                "sentiment-analysis",
                device=self.device
            )
            print("✅ Sentiment fallback loaded")
        except Exception as e:
            print(f"❌ Sentiment model failed: {e}")
        
        # Face detection for validation
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            print("✅ Face detection loaded")
        except Exception as e:
            print(f"❌ Face detection failed: {e}")
            self.face_cascade = None
    
    def capture_face(self, show_preview=True, max_attempts=3):
        """Capture face from webcam with validation and quality checks"""
        print("📸 Preparing camera for emotion detection...")
        
        for attempt in range(max_attempts):
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"❌ Camera not accessible (attempt {attempt + 1})")
                if attempt < max_attempts - 1:
                    time.sleep(1)
                    continue
                return None, "Camera not accessible"
            
            # Set camera properties for better quality
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
            cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
            
            print("📷 Camera ready! Position yourself well-lit, facing camera")
            print("⏱️ Taking photo in 3 seconds...")
            
            # Let camera stabilize and user get ready
            for i in range(90):  # 3 seconds at 30fps
                ret, frame = cap.read()
                if show_preview and i % 10 == 0:  # Show countdown
                    countdown = 3 - (i // 30)
                    if countdown > 0:
                        print(f"{countdown}...")
            
            # Take the actual photo
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                print(f"❌ Failed to capture photo (attempt {attempt + 1})")
                if attempt < max_attempts - 1:
                    time.sleep(1)
                    continue
                return None, "Failed to capture photo"
            
            # Validate image quality
            quality_check = self._validate_image_quality(frame)
            if not quality_check['valid']:
                print(f"⚠️ Image quality issue: {quality_check['reason']} (attempt {attempt + 1})")
                if attempt < max_attempts - 1:
                    print("🔄 Retrying capture...")
                    time.sleep(1)
                    continue
            
            # Save high-quality image
            timestamp = int(time.time())
            filename = f"face_analysis_hq_{timestamp}.jpg"
            cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            # Show captured image briefly
            if show_preview:
                cv2.imshow("Captured Face", frame)
                cv2.waitKey(1000)  # Show for 1 second
                cv2.destroyAllWindows()
            
            print(f"✅ High-quality photo saved: {filename}")
            return filename, "success"
        
        return None, "Failed after multiple attempts"
    
    def _validate_image_quality(self, frame):
        """Validate image quality for face analysis"""
        try:
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Check if face is detected
            if self.face_cascade:
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                if len(faces) == 0:
                    return {'valid': False, 'reason': 'No face detected'}
                elif len(faces) > 1:
                    return {'valid': False, 'reason': 'Multiple faces detected'}
            
            # Check brightness (avoid too dark or too bright)
            brightness = np.mean(gray)
            if brightness < 50:
                return {'valid': False, 'reason': 'Image too dark'}
            elif brightness > 200:
                return {'valid': False, 'reason': 'Image too bright'}
            
            # Check contrast
            contrast = np.std(gray)
            if contrast < 20:
                return {'valid': False, 'reason': 'Low contrast'}
            
            # Check blur (Laplacian variance)
            blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
            if blur_score < 100:
                return {'valid': False, 'reason': 'Image too blurry'}
            
            return {'valid': True, 'reason': 'Good quality'}
            
        except Exception as e:
            return {'valid': False, 'reason': f'Validation error: {e}'}
    
    def analyze_face_probabilities(self, image_path):
        """Analyze face with probability distributions from multiple models"""
        try:
            image = Image.open(image_path)
            
            all_results = {}
            
            for model_name, model in self.models.items():
                if model is None:  # Skip dummy models
                    continue
                    
                try:
                    results = model(image)
                    
                    # Handle both list and single result formats
                    emotion_probs = {}
                    if isinstance(results, list):
                        for emotion_data in results:
                            emotion = emotion_data['label'].lower()
                            probability = emotion_data['score']
                            emotion_probs[emotion] = probability
                    else:
                        # Single result format
                        emotion = results['label'].lower()
                        probability = results['score']
                        emotion_probs[emotion] = probability
                    
                    all_results[model_name] = emotion_probs
                    
                except Exception as e:
                    print(f"Model {model_name} failed: {e}")
                    all_results[model_name] = None
            
            return all_results
            
        except Exception as e:
            print(f"Image loading error: {e}")
            return {}
    
    def ensemble_face_emotions(self, model_results):
        """Combine results from multiple face models with weighted averaging"""
        valid_results = {k: v for k, v in model_results.items() if v is not None}
        
        if not valid_results:
            return None, "All models failed"
        
        if len(valid_results) == 1:
            model_name, results = next(iter(valid_results.items()))
            return results, f"Single model: {model_name}"
        
        # Weighted averaging based on model reliability
        model_weights = {
            'primary': 1.0,
            'backup': 0.8,
            'sentiment': 0.5
        }
        
        # Collect all emotions
        all_emotions = set()
        for results in valid_results.values():
            all_emotions.update(results.keys())
        
        ensemble_probs = {}
        total_weight = 0
        
        for emotion in all_emotions:
            weighted_sum = 0
            emotion_weight = 0
            
            for model_name, results in valid_results.items():
                weight = model_weights.get(model_name, 0.5)
                if emotion in results:
                    weighted_sum += results[emotion] * weight
                    emotion_weight += weight
            
            if emotion_weight > 0:
                ensemble_probs[emotion] = weighted_sum / emotion_weight
                total_weight += emotion_weight
        
        # Normalize probabilities
        if total_weight > 0:
            for emotion in ensemble_probs:
                ensemble_probs[emotion] = ensemble_probs[emotion] / total_weight * len(valid_results)
        
        return ensemble_probs, f"Ensemble of {len(valid_results)} models"
    
    def map_face_to_actionable(self, emotion_probs):
        """Map facial emotions to actionable stress/anxiety categories - IMPROVED VERSION"""
        try:
            # Enhanced face-specific emotion mapping
            face_clusters = {
                'stressed': [
                    'angry', 'fear', 'disgust', 'sad', 'confusion', 'disappointment',
                    'embarrassment', 'remorse', 'grief', 'disapproval'
                ],
                'anxious': [
                    'fear', 'confusion', 'embarrassment', 'nervousness', 'anxiety'
                ],
                'frustrated': [
                    'angry', 'disgust', 'disapproval', 'annoyance', 'disappointment'
                ],
                'sad': [
                    'sad', 'disappointment', 'grief', 'remorse', 'embarrassment'
                ],
                'overwhelmed': [
                    'confusion', 'fear', 'disappointment', 'embarrassment', 'remorse'
                ],
                'positive': [
                    'happy', 'joy', 'surprise', 'excitement', 'optimism', 'pride',
                    'gratitude', 'love', 'admiration', 'amusement', 'approval'
                ],
                'calm': [
                    'neutral', 'realization', 'approval', 'relief', 'caring'
                ],
                'energized': [
                    'excitement', 'joy', 'pride', 'admiration', 'optimism'
                ]
            }
            
            cluster_scores = {}
            for cluster, emotions in face_clusters.items():
                cluster_score = 0.0
                count = 0
                for emotion in emotions:
                    if emotion in emotion_probs:
                        cluster_score += emotion_probs[emotion]
                        count += 1
                
                # Normalize by count to avoid bias
                if count > 0:
                    cluster_scores[cluster] = cluster_score / count
                else:
                    cluster_scores[cluster] = 0.0
            
            # Ensure we have at least one category
            if not any(score > 0 for score in cluster_scores.values()):
                cluster_scores['calm'] = 1.0
            
            return cluster_scores
            
        except Exception as e:
            print(f"Error in map_face_to_actionable: {e}")
            return {'calm': 1.0}
    
    def analyze_complete_face(self, take_photo=True, image_path=None):
        """Complete face analysis with probabilities and actionable insights - OPTIMIZED VERSION"""
        
        # Check if we have any working models
        working_models = [k for k, v in self.models.items() if v is not None]
        if not working_models:
            return None, "No working face models available"
        
        if take_photo:
            image_path, status = self.capture_face()
            if image_path is None:
                return None, status
        elif image_path is None:
            return None, "No image provided"
        
        print("🔍 Analyzing facial expressions...")
        
        try:
            # Get probabilities from all models
            model_results = self.analyze_face_probabilities(image_path)
            
            if not model_results:
                return None, "Failed to analyze image"
            
            # Ensemble the results
            emotion_probs, ensemble_info = self.ensemble_face_emotions(model_results)
            
            if emotion_probs is None:
                return None, ensemble_info
            
            # Map to actionable categories
            cluster_scores = self.map_face_to_actionable(emotion_probs)
            top_cluster = max(cluster_scores.items(), key=lambda x: x[1])
            
            # Get top individual emotions
            top_emotions = sorted(emotion_probs.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Assess analysis quality
            analysis_quality = self._assess_face_analysis_quality(emotion_probs, ensemble_info, top_cluster[1])
            
            return {
                'image_path': image_path,
                'ensemble_info': ensemble_info,
                'all_emotions': emotion_probs,
                'top_emotions': top_emotions,
                'actionable_category': top_cluster[0],
                'category_confidence': top_cluster[1],
                'cluster_scores': cluster_scores,
                'model_results': model_results,
                'analysis_quality': analysis_quality
            }
            
        except Exception as e:
            print(f"Face analysis error: {e}")
            return None, f"Analysis failed: {e}"
    
    def _assess_face_analysis_quality(self, emotion_probs, ensemble_info, confidence):
        """Assess the quality of face analysis"""
        try:
            if 'Ensemble' in ensemble_info and confidence > 0.6:
                return 'high'
            elif 'Single model' in ensemble_info and confidence > 0.5:
                return 'medium'
            elif confidence > 0.3:
                return 'low'
            else:
                return 'very_low'
        except:
            return 'unknown'

# Test the advanced face analyzer
if __name__ == "__main__":
    analyzer = AdvancedFaceEmotionAnalyzer()
    
    print("\n" + "="*60)
    print("ADVANCED FACE EMOTION ANALYSIS")
    print("="*60)
    
    result = analyzer.analyze_complete_face(take_photo=True)
    
    if result:
        print(f"Image: {result['image_path']}")
        print(f"Analysis: {result['ensemble_info']}")
        print(f"Top Category: {result['actionable_category']} ({result['category_confidence']:.2%})")
        
        print("\nTop Facial Emotions:")
        for emotion, prob in result['top_emotions']:
            print(f"   {emotion}: {prob:.2%}")
        
        print("\nActionable Categories:")
        for category, score in sorted(result['cluster_scores'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {category}: {score:.2%}")
    else:
        print("Face analysis failed")