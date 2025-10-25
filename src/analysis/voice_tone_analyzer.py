"""
Voice Tone Analyzer for MoodLens
Analyzes voice characteristics (pitch, tone, nervousness) from exact prompts
"""

import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf
import os
from typing import Dict, List, Optional, Tuple
import json

class VoiceToneAnalyzer:
    def __init__(self):
        print("🎤 Initializing Voice Tone Analyzer...")
        
        # Voice characteristics we'll analyze
        self.voice_characteristics = {
            'pitch': {
                'name': 'Pitch Level',
                'description': 'How high or low your voice sounds',
                'indicators': {
                    'high': 'Elevated pitch may indicate stress or anxiety',
                    'normal': 'Normal pitch range suggests calmness',
                    'low': 'Lower pitch may indicate sadness or fatigue'
                }
            },
            'pitch_variation': {
                'name': 'Pitch Variation',
                'description': 'How much your pitch changes while speaking',
                'indicators': {
                    'high': 'High variation may indicate emotional intensity',
                    'normal': 'Normal variation suggests balanced emotional state',
                    'low': 'Low variation may indicate flat affect or depression'
                }
            },
            'speech_rate': {
                'name': 'Speech Rate',
                'description': 'How fast or slow you speak',
                'indicators': {
                    'fast': 'Fast speech may indicate anxiety or excitement',
                    'normal': 'Normal rate suggests calmness',
                    'slow': 'Slow speech may indicate sadness or fatigue'
                }
            },
            'volume': {
                'name': 'Volume Level',
                'description': 'How loud or quiet you speak',
                'indicators': {
                    'loud': 'Loud speech may indicate frustration or excitement',
                    'normal': 'Normal volume suggests balanced state',
                    'quiet': 'Quiet speech may indicate sadness or withdrawal'
                }
            },
            'tremor': {
                'name': 'Voice Tremor',
                'description': 'Shakiness or instability in your voice',
                'indicators': {
                    'high': 'High tremor may indicate nervousness or anxiety',
                    'normal': 'Normal stability suggests calmness',
                    'low': 'Very stable voice'
                }
            },
            'breathiness': {
                'name': 'Breathiness',
                'description': 'How much breath is audible in your voice',
                'indicators': {
                    'high': 'High breathiness may indicate stress or fatigue',
                    'normal': 'Normal breathiness',
                    'low': 'Low breathiness suggests strong voice'
                }
            }
        }
        
        # Emotion mapping based on voice characteristics
        self.emotion_mapping = {
            'anxious': {
                'pitch': 'high',
                'pitch_variation': 'high',
                'speech_rate': 'fast',
                'volume': 'normal',
                'tremor': 'high',
                'breathiness': 'high'
            },
            'sad': {
                'pitch': 'low',
                'pitch_variation': 'low',
                'speech_rate': 'slow',
                'volume': 'quiet',
                'tremor': 'normal',
                'breathiness': 'normal'
            },
            'frustrated': {
                'pitch': 'high',
                'pitch_variation': 'high',
                'speech_rate': 'fast',
                'volume': 'loud',
                'tremor': 'normal',
                'breathiness': 'normal'
            },
            'overwhelmed': {
                'pitch': 'high',
                'pitch_variation': 'high',
                'speech_rate': 'fast',
                'volume': 'normal',
                'tremor': 'high',
                'breathiness': 'high'
            },
            'calm': {
                'pitch': 'normal',
                'pitch_variation': 'normal',
                'speech_rate': 'normal',
                'volume': 'normal',
                'tremor': 'low',
                'breathiness': 'low'
            },
            'happy': {
                'pitch': 'high',
                'pitch_variation': 'high',
                'speech_rate': 'fast',
                'volume': 'loud',
                'tremor': 'low',
                'breathiness': 'low'
            },
            'neutral': {
                'pitch': 'normal',
                'pitch_variation': 'normal',
                'speech_rate': 'normal',
                'volume': 'normal',
                'tremor': 'normal',
                'breathiness': 'normal'
            },
            'tired': {
                'pitch': 'low',
                'pitch_variation': 'low',
                'speech_rate': 'slow',
                'volume': 'quiet',
                'tremor': 'normal',
                'breathiness': 'high'
            }
        }
        
        print("✅ Voice Tone Analyzer ready!")
    
    def record_voice_prompt(self, prompt_text: str, instruction: str, duration: int = 5) -> str:
        """Record user saying a specific prompt"""
        try:
            print(f"\n📝 Please say: \"{prompt_text}\"")
            print(f"💡 {instruction}")
            print(f"🎙️ Recording for {duration} seconds...")
            
            # Record audio
            sample_rate = 22050
            audio_data = sd.rec(int(duration * sample_rate), 
                              samplerate=sample_rate, 
                              channels=1, 
                              dtype='float64')
            sd.wait()  # Wait until recording is finished
            
            # Save audio
            filename = f"voice_prompt_{len(prompt_text)}.wav"
            sf.write(filename, audio_data, sample_rate)
            
            print("✅ Recording complete!")
            return filename
            
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return None
    
    def analyze_voice_characteristics(self, audio_file: str) -> Dict:
        """Analyze voice characteristics from audio file"""
        try:
            if not os.path.exists(audio_file):
                return self._get_fallback_analysis()
            
            # Load audio
            y, sr = librosa.load(audio_file, sr=22050)
            
            if len(y) == 0:
                return self._get_fallback_analysis()
            
            # Extract voice characteristics
            characteristics = {}
            
            # Pitch analysis
            pitch = self._analyze_pitch(y, sr)
            characteristics['pitch'] = pitch
            
            # Pitch variation
            pitch_variation = self._analyze_pitch_variation(y, sr)
            characteristics['pitch_variation'] = pitch_variation
            
            # Speech rate
            speech_rate = self._analyze_speech_rate(y, sr)
            characteristics['speech_rate'] = speech_rate
            
            # Volume
            volume = self._analyze_volume(y)
            characteristics['volume'] = volume
            
            # Tremor
            tremor = self._analyze_tremor(y, sr)
            characteristics['tremor'] = tremor
            
            # Breathiness
            breathiness = self._analyze_breathiness(y, sr)
            characteristics['breathiness'] = breathiness
            
            return {
                'characteristics': characteristics,
                'analysis_quality': 'high' if len(y) > sr * 2 else 'medium',
                'audio_duration': len(y) / sr
            }
            
        except Exception as e:
            print(f"Error analyzing voice characteristics: {e}")
            return self._get_fallback_analysis()
    
    def _analyze_pitch(self, y: np.ndarray, sr: int) -> str:
        """Analyze average pitch level"""
        try:
            # Extract pitch using librosa
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr, threshold=0.1)
            
            # Get non-zero pitches
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if not pitch_values:
                return 'normal'
            
            avg_pitch = np.mean(pitch_values)
            
            # Categorize pitch
            if avg_pitch > 200:  # Hz
                return 'high'
            elif avg_pitch < 120:
                return 'low'
            else:
                return 'normal'
                
        except Exception as e:
            print(f"Pitch analysis error: {e}")
            return 'normal'
    
    def _analyze_pitch_variation(self, y: np.ndarray, sr: int) -> str:
        """Analyze pitch variation"""
        try:
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr, threshold=0.1)
            
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if len(pitch_values) < 2:
                return 'normal'
            
            # Calculate coefficient of variation
            mean_pitch = np.mean(pitch_values)
            std_pitch = np.std(pitch_values)
            cv = std_pitch / mean_pitch if mean_pitch > 0 else 0
            
            if cv > 0.3:
                return 'high'
            elif cv < 0.1:
                return 'low'
            else:
                return 'normal'
                
        except Exception as e:
            print(f"Pitch variation analysis error: {e}")
            return 'normal'
    
    def _analyze_speech_rate(self, y: np.ndarray, sr: int) -> str:
        """Analyze speech rate"""
        try:
            # Detect onsets (speech events)
            onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
            
            if len(onsets) < 2:
                return 'normal'
            
            # Calculate average time between onsets
            intervals = np.diff(onsets)
            avg_interval = np.mean(intervals)
            
            # Categorize speech rate
            if avg_interval < 0.3:  # Fast speech
                return 'fast'
            elif avg_interval > 0.8:  # Slow speech
                return 'slow'
            else:
                return 'normal'
                
        except Exception as e:
            print(f"Speech rate analysis error: {e}")
            return 'normal'
    
    def _analyze_volume(self, y: np.ndarray) -> str:
        """Analyze volume level"""
        try:
            # Calculate RMS energy
            rms = librosa.feature.rms(y=y)[0]
            avg_rms = np.mean(rms)
            
            # Categorize volume
            if avg_rms > 0.1:
                return 'loud'
            elif avg_rms < 0.03:
                return 'quiet'
            else:
                return 'normal'
                
        except Exception as e:
            print(f"Volume analysis error: {e}")
            return 'normal'
    
    def _analyze_tremor(self, y: np.ndarray, sr: int) -> str:
        """Analyze voice tremor"""
        try:
            # Extract pitch and look for rapid variations
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr, threshold=0.1)
            
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if len(pitch_values) < 10:
                return 'normal'
            
            # Calculate tremor as rapid pitch variations
            pitch_diff = np.abs(np.diff(pitch_values))
            tremor_score = np.mean(pitch_diff) / np.mean(pitch_values) if np.mean(pitch_values) > 0 else 0
            
            if tremor_score > 0.15:
                return 'high'
            elif tremor_score < 0.05:
                return 'low'
            else:
                return 'normal'
                
        except Exception as e:
            print(f"Tremor analysis error: {e}")
            return 'normal'
    
    def _analyze_breathiness(self, y: np.ndarray, sr: int) -> str:
        """Analyze breathiness in voice"""
        try:
            # Calculate spectral centroid (brightness)
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            avg_centroid = np.mean(spectral_centroids)
            
            # Calculate zero crossing rate (noise indicator)
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            avg_zcr = np.mean(zcr)
            
            # Breathiness is indicated by low spectral centroid and high ZCR
            breathiness_score = avg_zcr - (avg_centroid / 10000)
            
            if breathiness_score > 0.1:
                return 'high'
            elif breathiness_score < 0.05:
                return 'low'
            else:
                return 'normal'
                
        except Exception as e:
            print(f"Breathiness analysis error: {e}")
            return 'normal'
    
    def map_voice_to_emotion(self, characteristics: Dict) -> Dict:
        """Map voice characteristics to emotion scores"""
        try:
            emotion_scores = {emotion: 0.0 for emotion in self.emotion_mapping.keys()}
            
            # Score each emotion based on how well characteristics match
            for emotion, expected_chars in self.emotion_mapping.items():
                score = 0.0
                total_chars = 0
                
                for char_name, expected_value in expected_chars.items():
                    if char_name in characteristics:
                        actual_value = characteristics[char_name]
                        total_chars += 1
                        
                        if actual_value == expected_value:
                            score += 1.0
                        elif self._is_similar(actual_value, expected_value):
                            score += 0.5
                
                if total_chars > 0:
                    emotion_scores[emotion] = score / total_chars
            
            # Find dominant emotion
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            
            return {
                'emotion_scores': emotion_scores,
                'dominant_emotion': dominant_emotion[0],
                'confidence': dominant_emotion[1],
                'characteristics': characteristics
            }
            
        except Exception as e:
            print(f"Error mapping voice to emotion: {e}")
            return self._get_fallback_emotion_mapping()
    
    def _is_similar(self, actual: str, expected: str) -> bool:
        """Check if two characteristic values are similar"""
        similarity_map = {
            'high': ['normal'],
            'normal': ['high', 'low'],
            'low': ['normal']
        }
        
        return expected in similarity_map.get(actual, [])
    
    def _get_fallback_analysis(self) -> Dict:
        """Return fallback analysis if voice analysis fails"""
        return {
            'characteristics': {
                'pitch': 'normal',
                'pitch_variation': 'normal',
                'speech_rate': 'normal',
                'volume': 'normal',
                'tremor': 'normal',
                'breathiness': 'normal'
            },
            'analysis_quality': 'low',
            'audio_duration': 0
        }
    
    def _get_fallback_emotion_mapping(self) -> Dict:
        """Return fallback emotion mapping"""
        return {
            'emotion_scores': {'neutral': 0.5},
            'dominant_emotion': 'neutral',
            'confidence': 0.5,
            'characteristics': {}
        }
    
    def analyze_complete_voice(self, audio_file: str) -> Dict:
        """Complete voice analysis pipeline"""
        try:
            # Analyze voice characteristics
            analysis = self.analyze_voice_characteristics(audio_file)
            
            # Map to emotions
            emotion_mapping = self.map_voice_to_emotion(analysis['characteristics'])
            
            # Combine results
            return {
                'voice_characteristics': analysis['characteristics'],
                'emotion_scores': emotion_mapping['emotion_scores'],
                'dominant_emotion': emotion_mapping['dominant_emotion'],
                'confidence': emotion_mapping['confidence'],
                'analysis_quality': analysis['analysis_quality'],
                'audio_duration': analysis['audio_duration'],
                'actionable_category': emotion_mapping['dominant_emotion']
            }
            
        except Exception as e:
            print(f"Error in complete voice analysis: {e}")
            return {
                'voice_characteristics': {},
                'emotion_scores': {'neutral': 0.5},
                'dominant_emotion': 'neutral',
                'confidence': 0.5,
                'analysis_quality': 'low',
                'audio_duration': 0,
                'actionable_category': 'neutral'
            }

# Test the voice tone analyzer
if __name__ == "__main__":
    analyzer = VoiceToneAnalyzer()
    
    print("Voice Tone Analyzer Test")
    print("=" * 40)
    
    # Test with a sample audio file if it exists
    test_file = "test_voice.wav"
    if os.path.exists(test_file):
        result = analyzer.analyze_complete_voice(test_file)
        print(f"Voice characteristics: {result['voice_characteristics']}")
        print(f"Dominant emotion: {result['dominant_emotion']}")
        print(f"Confidence: {result['confidence']:.1%}")
    else:
        print("No test audio file found. Run with actual audio to test.")
        print("\nVoice characteristics analyzed:")
        for char, info in analyzer.voice_characteristics.items():
            print(f"- {info['name']}: {info['description']}")
