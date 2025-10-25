import numpy as np
from advanced_text_analysis import AdvancedTextEmotionAnalyzer
from advanced_face_analysis import AdvancedFaceEmotionAnalyzer
from advanced_voice_analysis import AdvancedVoiceEmotionAnalyzer

class AdvancedEmotionFusionSystem:
    def __init__(self):
        print("🧠 Initializing Advanced MoodLens Fusion System...")
        
        # Initialize all analyzers
        self.text_analyzer = AdvancedTextEmotionAnalyzer()
        self.face_analyzer = AdvancedFaceEmotionAnalyzer()
        self.voice_analyzer = AdvancedVoiceEmotionAnalyzer()
        
        # Define unified emotion categories for actionable recommendations
        self.unified_categories = {
            'stressed': {
                'description': 'High stress, pressure, overwhelm',
                'recommendation': self._stress_recommendation
            },
            'anxious': {
                'description': 'Worry, nervousness, anticipatory fear',
                'recommendation': self._anxiety_recommendation
            },
            'frustrated': {
                'description': 'Anger, annoyance, irritation',
                'recommendation': self._frustration_recommendation
            },
            'sad': {
                'description': 'Sadness, disappointment, low mood',
                'recommendation': self._sadness_recommendation
            },
            'overwhelmed': {
                'description': 'Too much to handle, confusion, chaos',
                'recommendation': self._overwhelm_recommendation
            },
            'positive': {
                'description': 'Joy, excitement, happiness, satisfaction',
                'recommendation': self._positive_recommendation
            },
            'calm': {
                'description': 'Neutral, peaceful, balanced',
                'recommendation': self._calm_recommendation
            }
        }
        
        print("✅ Advanced Fusion System ready!")
    
    def weighted_fusion(self, modality_results):
        """Advanced fusion using weighted probabilities based on confidence - OPTIMIZED VERSION"""
        valid_results = []
        
        for modality, data in modality_results.items():
            if data is not None:
                # Handle different data structures from each modality
                cluster_scores = None
                
                if modality == 'text' and 'cluster_scores' in data:
                    cluster_scores = data['cluster_scores']
                elif modality == 'face' and 'cluster_scores' in data:
                    cluster_scores = data['cluster_scores']  
                elif modality == 'voice' and 'cluster_scores' in data:
                    cluster_scores = data['cluster_scores']
                else:
                    # Try to create cluster_scores if not present
                    cluster_scores = self._create_cluster_scores(modality, data)
                
                if cluster_scores:
                    # Weight by overall confidence/quality of the analysis
                    weight = self._calculate_modality_weight(modality, data)
                    valid_results.append((modality, cluster_scores, weight))
        
        if not valid_results:
            return None
        
        # Combine weighted scores
        all_categories = set()
        for _, cluster_scores, _ in valid_results:
            all_categories.update(cluster_scores.keys())
        
        fused_scores = {}
        for category in all_categories:
            weighted_sum = 0
            total_weight = 0
            
            for modality, cluster_scores, weight in valid_results:
                if category in cluster_scores:
                    weighted_sum += cluster_scores[category] * weight
                    total_weight += weight
            
            if total_weight > 0:
                fused_scores[category] = weighted_sum / total_weight
            else:
                fused_scores[category] = 0
        
        # Find dominant emotion safely
        if fused_scores:
            try:
                top_category = max(fused_scores.items(), key=lambda x: x[1])
            except (ValueError, TypeError) as e:
                print(f"Error finding top category: {e}")
                top_category = ("calm", 0.5)
        else:
            top_category = ("calm", 0.5)
        
        # Calculate fusion confidence
        fusion_confidence = self._calculate_fusion_confidence(valid_results, top_category[0])
        
        # Assess fusion quality
        fusion_quality = self._assess_fusion_quality(valid_results, fusion_confidence)
        
        return {
            'dominant_emotion': top_category[0],
            'confidence': fusion_confidence,
            'all_scores': fused_scores,
            'modalities_used': [modality for modality, _, _ in valid_results],
            'fusion_method': 'weighted_probability',
            'fusion_quality': fusion_quality,
            'modality_details': self._get_modality_details(valid_results)
        }
    
    def _create_cluster_scores(self, modality, data):
        """Create cluster scores if not present in data structure"""
        try:
            if modality == 'text':
                # Use existing cluster mapping
                return data.get('cluster_scores', {'calm': 0.5})
            elif modality == 'face':
                # Map face emotions to clusters
                if 'actionable_category' in data:
                    category = data['actionable_category']
                    confidence = data.get('category_confidence', 0.5)
                    return {category: confidence}
            elif modality == 'voice':
                # Use existing cluster mapping or create from actionable category
                if 'actionable_category' in data:
                    category = data['actionable_category']
                    confidence = data.get('category_confidence', 0.5)
                    return {category: confidence}
            
            # Fallback
            return {'calm': 0.5}
            
        except Exception as e:
            print(f"Error creating cluster scores for {modality}: {e}")
            return {'calm': 0.5}
    
    def _calculate_modality_weight(self, modality, data):
        """Calculate reliability weight for each modality"""
        base_weights = {
            'text': 1.0,     # Text is usually most reliable
            'voice': 0.8,    # Voice can be noisy
            'face': 0.7      # Face analysis can be affected by lighting
        }
        
        weight = base_weights.get(modality, 0.5)
        
        try:
            # Adjust weight based on confidence/quality indicators
            if modality == 'voice' and data.get('stress_analysis'):
                # Higher weight if stress indicators are clear
                if data['stress_analysis'].get('stress_likelihood', 0) > 0.5:
                    weight += 0.2
            
            if modality == 'face' and 'ensemble_info' in data:
                # Higher weight if multiple models agree
                if 'ensemble' in data['ensemble_info'].lower():
                    weight += 0.1
            
            # Boost weight for high-confidence results
            confidence = data.get('category_confidence', 0) or data.get('confidence', 0)
            if confidence > 0.7:
                weight += 0.1
        
        except Exception as e:
            print(f"Error calculating weight for {modality}: {e}")
        
        return min(weight, 1.0)  # Cap at 1.0
    
    def _calculate_fusion_confidence(self, valid_results, dominant_emotion):
        """Calculate overall confidence in the fused result"""
        try:
            # Count how many modalities agree with the dominant emotion
            agreement_count = 0
            total_modalities = len(valid_results)
            
            for modality, cluster_scores, weight in valid_results:
                if dominant_emotion in cluster_scores and cluster_scores[dominant_emotion] > 0.3:
                    agreement_count += 1
            
            # Base confidence from agreement
            agreement_confidence = agreement_count / total_modalities if total_modalities > 0 else 0
            
            # Boost if high-quality modalities agree
            quality_boost = 0
            for modality, cluster_scores, weight in valid_results:
                if (dominant_emotion in cluster_scores and 
                    cluster_scores[dominant_emotion] > 0.5 and 
                    weight > 0.8):
                    quality_boost += 0.1
            
            return min(agreement_confidence + quality_boost, 1.0)
            
        except Exception as e:
            print(f"Error calculating fusion confidence: {e}")
            return 0.5
    
    def _assess_fusion_quality(self, valid_results, fusion_confidence):
        """Assess the overall quality of the fusion analysis"""
        try:
            quality_score = 0
            
            # Number of modalities
            modality_count = len(valid_results)
            if modality_count >= 3:
                quality_score += 2
            elif modality_count >= 2:
                quality_score += 1
            
            # Confidence level
            if fusion_confidence > 0.8:
                quality_score += 2
            elif fusion_confidence > 0.6:
                quality_score += 1
            
            # Individual modality quality
            high_quality_modalities = 0
            for modality, _, weight in valid_results:
                if weight > 0.8:
                    high_quality_modalities += 1
            
            if high_quality_modalities >= 2:
                quality_score += 1
            
            if quality_score >= 4:
                return 'high'
            elif quality_score >= 2:
                return 'medium'
            elif quality_score >= 1:
                return 'low'
            else:
                return 'very_low'
                
        except Exception as e:
            print(f"Error assessing fusion quality: {e}")
            return 'unknown'
    
    def _get_modality_details(self, valid_results):
        """Get detailed information about each modality used"""
        details = {}
        for modality, cluster_scores, weight in valid_results:
            details[modality] = {
                'weight': weight,
                'top_category': max(cluster_scores.items(), key=lambda x: x[1])[0] if cluster_scores else 'unknown',
                'confidence': max(cluster_scores.values()) if cluster_scores else 0
            }
        return details
    
    def complete_analysis(self, include_face=True, include_voice=True, include_text=True):
        """Run complete multimodal emotion analysis - BULLETPROOFED VERSION"""
        print("\n" + "="*80)
        print("🏭 ADVANCED MOODLENS - COMPLETE EMOTIONAL ANALYSIS")
        print("="*80)
        print("Analyzing your emotions across multiple dimensions:")
        print("😐 Facial expressions → micro-expressions, stress indicators")
        print("🎤 Voice patterns → tone, pace, stress in speech")
        print("💭 Emotional content → nuanced feelings, context")
        print("="*80)
        
        modality_results = {}
        
        # Face Analysis
        if include_face:
            print("\n👁️ FACIAL EXPRESSION ANALYSIS")
            print("-" * 40)
            try:
                face_result = self.face_analyzer.analyze_complete_face(take_photo=True)
                if face_result:
                    modality_results['face'] = face_result
                    print(f"✅ Face: {face_result['actionable_category']} ({face_result['category_confidence']:.1%})")
                    print(f"💭 Top emotions: {', '.join([f'{e}:{p:.1%}' for e, p in face_result['top_emotions'][:3]])}")
                else:
                    print("❌ Face analysis failed")
            except Exception as e:
                print(f"❌ Face analysis error: {e}")
        
        # Voice Analysis
        if include_voice:
            print("\n🎤 VOICE & SPEECH ANALYSIS")
            print("-" * 40)
            try:
                voice_result = self.voice_analyzer.analyze_complete_voice(record_new=True)
                if voice_result:
                    modality_results['voice'] = voice_result
                    print(f"✅ Voice: {voice_result['actionable_category']} ({voice_result['category_confidence']:.1%})")
                    if voice_result['spoken_text']:
                        print(f"💬 You said: '{voice_result['spoken_text'][:100]}...'")
                    if voice_result['stress_analysis']:
                        print(f"📊 Stress likelihood: {voice_result['stress_analysis']['stress_likelihood']:.1%}")
                else:
                    print("❌ Voice analysis failed")
            except Exception as e:
                print(f"❌ Voice analysis error: {e}")
        
        # Text Analysis
        if include_text:
            print("\n💭 TEXT/THOUGHT ANALYSIS")
            print("-" * 40)
            user_text = input("💭 Describe your current feelings/situation (or press Enter to skip): ").strip()
            
            if user_text:
                try:
                    text_result = self.text_analyzer.analyze_complete(user_text)
                    if text_result:
                        modality_results['text'] = text_result
                        print(f"✅ Text: {text_result['actionable_category']} ({text_result['category_confidence']:.1%})")
                        print(f"📊 Top emotions: {', '.join([f'{e}:{p:.1%}' for e, p in text_result['top_emotions'][:3]])}")
                    else:
                        print("❌ Text analysis failed")
                except Exception as e:
                    print(f"❌ Text analysis error: {e}")
            else:
                print("⏭️ Text analysis skipped")
        
        # Advanced Fusion
        print("\n🧠 ADVANCED FUSION ANALYSIS")
        print("=" * 50)
        
        try:
            fusion_result = self.weighted_fusion(modality_results)
            
            if fusion_result:
                print(f"🎯 DOMINANT EMOTION: {fusion_result['dominant_emotion'].upper()}")
                print(f"📊 Fusion Confidence: {fusion_result['confidence']:.1%}")
                print(f"🔧 Modalities Used: {', '.join(fusion_result['modalities_used'])}")
                print(f"⚡ Method: {fusion_result['fusion_method']}")
                
                print("\n📈 All Emotional Categories:")
                for category, score in sorted(fusion_result['all_scores'].items(), key=lambda x: x[1], reverse=True):
                    if score > 0.1:  # Only show significant scores
                        print(f"   {category}: {score:.1%}")
                
                # Generate personalized recommendation
                recommendation = self._generate_personalized_recommendation(
                    fusion_result, modality_results
                )
                
                print("\n💡 PERSONALIZED RECOMMENDATION:")
                print("=" * 50)
                print(recommendation)
                
                return fusion_result, modality_results, recommendation
            
            else:
                print("❌ Fusion analysis failed - no valid modality results")
                return None, modality_results, "Unable to provide recommendations due to analysis failure"
        
        except Exception as e:
            print(f"❌ Fusion system error: {e}")
            return None, modality_results, "Unable to provide recommendations due to system error"
    
    def _generate_personalized_recommendation(self, fusion_result, modality_results):
        """Generate contextual recommendations based on fusion analysis"""
        try:
            dominant_emotion = fusion_result['dominant_emotion']
            confidence = fusion_result['confidence']
            
            # Get base recommendation
            if dominant_emotion in self.unified_categories:
                base_rec = self.unified_categories[dominant_emotion]['recommendation']()
            else:
                base_rec = "Take a moment for self-reflection."
            
            # Add context-specific adjustments
            context_additions = []
            
            # High confidence = more specific advice
            if confidence > 0.8:
                context_additions.append("(High confidence - this analysis is very reliable)")
            elif confidence < 0.4:
                context_additions.append("(Lower confidence - consider multiple check-ins throughout the day)")
            
            # Modality-specific insights
            if 'voice' in modality_results and modality_results['voice']:
                voice_data = modality_results['voice']
                if voice_data.get('stress_analysis', {}).get('stress_likelihood', 0) > 0.6:
                    context_additions.append("Your voice shows significant stress patterns - prioritize relaxation techniques")
            
            if 'face' in modality_results and modality_results['face']:
                face_data = modality_results['face']
                if face_data.get('actionable_category') == 'stressed':
                    context_additions.append("Facial tension detected - consider gentle face/neck stretches")
            
            if 'text' in modality_results and modality_results['text']:
                text_data = modality_results['text']
                if 'overwhelm' in text_data.get('actionable_category', ''):
                    context_additions.append("Your words suggest feeling overwhelmed - break tasks into smaller steps")
            
            # Combine base recommendation with context
            full_recommendation = base_rec
            if context_additions:
                full_recommendation += "\n\nAdditional Insights:\n" + "\n".join(f"• {addition}" for addition in context_additions)
            
            return full_recommendation
            
        except Exception as e:
            print(f"Error generating recommendation: {e}")
            return "Take some time for self-care and reflection."
    
    # Recommendation functions for each emotional category
    def _stress_recommendation(self):
        return """STRESS MANAGEMENT PROTOCOL:

1. IMMEDIATE (next 2 minutes):
   • 4-7-8 breathing: Inhale 4, hold 7, exhale 8 (repeat 3x)
   • Progressive muscle release: tense and release shoulder muscles

2. SHORT-TERM (next 30 minutes):
   • Take a 10-minute walk, preferably outdoors
   • Listen to calming music or nature sounds
   • Stretch your neck, shoulders, and back

3. PLANNING:
   • Identify the specific stressor causing this feeling
   • Write down 3 actionable steps you can take today
   • Consider what you can delegate or postpone"""
    
    def _anxiety_recommendation(self):
        return """ANXIETY RELIEF PROTOCOL:

1. GROUNDING (next 5 minutes):
   • 5-4-3-2-1 technique: Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste
   • Place feet flat on floor, hands on your lap, breathe slowly

2. COGNITIVE RESET:
   • Write down your specific worry
   • Ask: "Is this worry about something I can control right now?"
   • If yes: make a small action plan. If no: practice letting it go

3. SELF-SOOTHING:
   • Make yourself a warm drink
   • Call a supportive friend or family member
   • Engage in a familiar, comforting activity"""
    
    def _frustration_recommendation(self):
        return """FRUSTRATION PROCESSING PROTOCOL:

1. IMMEDIATE RELEASE (next 5 minutes):
   • Physical release: Do 10 jumping jacks or push-ups
   • Vocal release: Go somewhere private and say/yell what's frustrating you
   • Writing release: Write your frustrations on paper (you can throw it away after)

2. PERSPECTIVE SHIFT:
   • What specifically triggered this frustration?
   • What would you advise a friend in this situation?
   • Is this frustration pointing to something that needs to change?

3. CONSTRUCTIVE ACTION:
   • If possible, address the root cause directly
   • Set a boundary if someone crossed yours
   • Practice self-compassion - frustration is human and valid"""
    
    def _sadness_recommendation(self):
        return """SADNESS SUPPORT PROTOCOL:

1. GENTLE ACKNOWLEDGMENT:
   • It's okay to feel sad - this emotion has important information
   • Allow yourself to feel this without judgment
   • Sadness often means something matters to you

2. NURTURING ACTIVITIES (choose what feels right):
   • Take a warm bath or shower
   • Watch something that usually comforts you
   • Journal about what you're feeling
   • Reach out to someone who cares about you

3. GENTLE MOVEMENT:
   • Go for a slow walk
   • Do gentle stretching
   • Consider what your body needs right now"""
    
    def _overwhelm_recommendation(self):
        return """OVERWHELM ORGANIZATION PROTOCOL:

1. BRAIN DUMP (next 10 minutes):
   • Write down EVERYTHING on your mind
   • Don't organize yet - just get it all out
   • Include tasks, worries, thoughts, everything

2. CATEGORIZE & PRIORITIZE:
   • Sort into: Urgent/Important, Important/Not Urgent, etc.
   • Pick only 3 things to focus on today
   • Put the rest in a "later" list

3. SIMPLIFY & DELEGATE:
   • What can you say no to?
   • What can you delegate to others?
   • What perfectionist standards can you lower?
   • Remember: Done is better than perfect"""
    
    def _positive_recommendation(self):
        return """POSITIVE ENERGY AMPLIFICATION:

1. SAVOR THIS MOMENT:
   • Take a mental snapshot of how you feel right now
   • Share this positive feeling with someone you care about
   • Write down what's going well in your life

2. PRODUCTIVE CHANNELING:
   • This is great energy for creative projects
   • Consider tackling a task you've been putting off
   • Use this mood to plan something you're excited about

3. GRATITUDE PRACTICE:
   • Write down 3 specific things you're grateful for
   • Acknowledge your own role in creating this positive feeling
   • Consider how you can maintain this energy"""
    
    def _calm_recommendation(self):
        return """CALM MAINTENANCE PROTOCOL:

1. APPRECIATE THIS BALANCE:
   • This calm state is valuable - notice how it feels
   • This is a good time for reflection and planning
   • Your nervous system is in a healthy, regulated state

2. PRODUCTIVE CALM ACTIVITIES:
   • Organize or plan upcoming projects
   • Have meaningful conversations
   • Learn something new that interests you
   • Engage in mindful activities

3. MAINTAIN EQUILIBRIUM:
   • Notice what contributed to this calm feeling
   • Consider how to incorporate more of these factors into your routine
   • Use this clarity to make important decisions"""

# Test the complete advanced system
if __name__ == "__main__":
    print("Starting Advanced MoodLens System...")
    
    system = AdvancedEmotionFusionSystem()
    
    print("\nWelcome to Advanced MoodLens!")
    print("This system provides nuanced emotional analysis beyond basic emotions.")
    print("We'll detect complex states like stress, anxiety, overwhelm, and provide personalized guidance.")
    
    # Run complete analysis
    fusion_result, modality_results, recommendation = system.complete_analysis(
        include_face=True,
        include_voice=True, 
        include_text=True
    )
    
    if fusion_result:
        print(f"\nAnalysis Complete! Your emotional state: {fusion_result['dominant_emotion']} ({fusion_result['confidence']:.1%} confidence)")
    else:
        print("\nAnalysis incomplete - please try again with different modalities")