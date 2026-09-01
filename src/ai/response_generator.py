"""
Response generation for the AI Eco-Chatbot
Generates personalized, context-aware responses based on user intent and data.
"""

import random
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import re

from .chat_intents import IntentDetector, IntentResult


class ResponseGenerator:
    """
    Generates personalized responses based on user intent, context, and user data.
    """
    
    def __init__(self, intent_detector: IntentDetector = None):
        self.intent_detector = intent_detector or IntentDetector()
        self.user_data = {}
        self.conversation_history = []
        self.context = {}
        
        # Response templates
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, List[str]]:
        """Load response templates for different contexts."""
        return {
            'greeting': [
                "🌱 Hello! I'm your EcoBuddy AI assistant. How can I help you today?",
                "👋 Hi there! Ready to make the planet greener? I'm here to help!",
                "🌟 Welcome back! What eco-friendly thing can I assist you with today?",
                "🌿 Hello! It's great to see you again. Let's save the planet together! 💚",
                "👋 Hey there! I'm here to help you with all things sustainability! 🌍"
            ],
            'carbon_footprint': {
                'high': [
                    "🌍 Your carbon footprint is currently {footprint:.1f} kg CO₂, which is above average. Here are some ways to reduce it:",
                    "📈 Your footprint of {footprint:.1f} kg CO₂ is quite high. Let's work on reducing it together!",
                    "⚠️ At {footprint:.1f} kg CO₂, your footprint needs attention. Try these tips:"
                ],
                'medium': [
                    "🌱 Your carbon footprint is {footprint:.1f} kg CO₂. You're doing okay, but there's room for improvement!",
                    "📊 Your footprint is {footprint:.1f} kg CO₂. Some small changes could make a big difference!",
                    "🌿 At {footprint:.1f} kg CO₂, you're on the right track. Here's how to do even better:"
                ],
                'low': [
                    "🎉 Great work! Your carbon footprint is {footprint:.1f} kg CO₂, which is below average!",
                    "🌟 Amazing! At {footprint:.1f} kg CO₂, your footprint is impressively low!",
                    "🏆 You're an eco-champion! Your footprint of {footprint:.1f} kg CO₂ is outstanding!"
                ]
            },
            'eco_score': {
                'high': [
                    "⭐ Your Eco Score is {score}/100 - Outstanding! You're a sustainability superstar! 🌟",
                    "🏆 Excellent work! Your Eco Score of {score}/100 puts you in the top tier!",
                    "🎉 Amazing! With {score}/100, you're leading the way in sustainability!"
                ],
                'medium': [
                    "🌱 Your Eco Score is {score}/100 - Good progress! Keep going!",
                    "📊 At {score}/100, you're on the right track. Here's how to improve:",
                    "🌿 A score of {score}/100 shows you're making good choices. Let's get you higher!"
                ],
                'low': [
                    "📈 Your Eco Score is {score}/100 - There's room for improvement. Let me help!",
                    "🌱 At {score}/100, we can work together to boost your sustainability.",
                    "💡 A score of {score}/100 means there's opportunity to grow. Here's how:"
                ]
            },
            'reduce_tips': [
                "💡 Here are 5 ways to reduce your carbon footprint:\n1. {tip1}\n2. {tip2}\n3. {tip3}\n4. {tip4}\n5. {tip5}",
                "🌿 Try these eco-friendly tips to lower your impact:\n• {tip1}\n• {tip2}\n• {tip3}\n• {tip4}\n• {tip5}",
                "📋 Based on your profile, here are personalized recommendations:\n✓ {tip1}\n✓ {tip2}\n✓ {tip3}\n✓ {tip4}\n✓ {tip5}"
            ],
            'challenges': [
                "🏆 Here are today's eco-challenges:\n🎯 {challenge1}\n🎯 {challenge2}\n🎯 {challenge3}",
                "🔥 Ready for some fun? Try these challenges today:\n✅ {challenge1}\n✅ {challenge2}\n✅ {challenge3}",
                "🌟 Daily eco-challenges:\n⭐ {challenge1}\n⭐ {challenge2}\n⭐ {challenge3}"
            ],
            'water': [
                "💧 Your water footprint:\n🚿 Shower: {shower}L\n🧺 Laundry: {laundry}L\n🍽️ Dishes: {dishes}L\n🚽 Toilet: {toilet}L\n🌿 Gardening: {garden}L\n\nTotal: {total}L",
                "🚿 Water usage breakdown:\n• Showers: {shower}L\n• Laundry: {laundry}L\n• Dishes: {dishes}L\n• Toilet: {toilet}L\n• Garden: {garden}L\n\nTotal: {total}L"
            ],
            'waste': [
                "♻️ Waste reduction tips:\n1. {tip1}\n2. {tip2}\n3. {tip3}\n4. {tip4}",
                "🗑️ Here's how to reduce your waste:\n✓ {tip1}\n✓ {tip2}\n✓ {tip3}\n✓ {tip4}",
                "🌱 Sustainable waste management:\n• {tip1}\n• {tip2}\n• {tip3}\n• {tip4}"
            ],
            'energy': [
                "⚡ Energy saving tips:\n💡 {tip1}\n🔌 {tip2}\n☀️ {tip3}\n🌡️ {tip4}",
                "💡 Reduce your energy consumption:\n• {tip1}\n• {tip2}\n• {tip3}\n• {tip4}",
                "🌿 Energy efficiency tips:\n✅ {tip1}\n✅ {tip2}\n✅ {tip3}\n✅ {tip4}"
            ],
            'transport': [
                "🚗 Sustainable transport options:\n🚲 {tip1}\n🚌 {tip2}\n🚶 {tip3}\n🚆 {tip4}",
                "🌿 Reduce transport emissions:\n• {tip1}\n• {tip2}\n• {tip3}\n• {tip4}",
                "🚀 Green commuting tips:\n✅ {tip1}\n✅ {tip2}\n✅ {tip3}\n✅ {tip4}"
            ],
            'diet': [
                "🥗 Sustainable diet tips:\n🌱 {tip1}\n🥑 {tip2}\n🍅 {tip3}\n🌾 {tip4}",
                "🌿 Eco-friendly eating:\n• {tip1}\n• {tip2}\n• {tip3}\n• {tip4}",
                "🍽️ Reduce your food footprint:\n✅ {tip1}\n✅ {tip2}\n✅ {tip3}\n✅ {tip4}"
            ],
            'help': [
                "🤖 I can help you with:\n🌍 Carbon footprint tracking\n⭐ Eco Score monitoring\n💡 Sustainability tips\n🎯 Daily challenges\n💧 Water footprint\n♻️ Waste management\n⚡ Energy saving\n🚗 Sustainable transport\n🥗 Eco-friendly diet\nAsk me anything!",
                "📋 Here are my capabilities:\n• Track your carbon footprint\n• Monitor your Eco Score\n• Give personalized tips\n• Suggest daily challenges\n• Calculate water footprint\n• Provide waste reduction tips\n• Share energy saving advice\n• Recommend sustainable transport\n• Suggest eco-friendly diet"
            ],
            'thanks': [
                "🌱 You're welcome! Keep making sustainable choices! 💚",
                "💚 My pleasure! Together we can make a difference! 🌍",
                "🌟 Anytime! Every small action counts towards a greener planet! 🌿"
            ],
            'goodbye': [
                "👋 Goodbye! Keep being eco-friendly! 🌱",
                "🌿 See you later! Remember, every small action counts! 💚",
                "🌟 Take care! I'm always here to help with your eco-journey! 🌍"
            ],
            'joke': [
                "🌱 Why don't scientists trust atoms? Because they make up everything! 😄",
                "💡 What's an environmentalist's favorite type of music? Solar! ☀️",
                "🌳 Why do trees look suspicious? They're always up to something shady! 🌲",
                "♻️ What do you call a recycling champion? A can-do person! 🥫",
                "🌊 What did the ocean say to the beach? Nothing, it just waved! 👋"
            ],
            'quiz': [
                "📝 Test your eco-knowledge!\n1. How much CO₂ does a tree absorb per year?\n2. What's the most sustainable transport?\n3. Which diet has the lowest carbon footprint?\n\nReply with your answers!",
                "🧠 Eco Quiz:\n1. What is the average carbon footprint per person?\n2. How can you reduce water usage?\n3. Which energy source is renewable?\n\nAnswer me! 🌿"
            ],
            'tips': [
                "💡 Quick eco-tips:\n🌱 {tip1}\n💧 {tip2}\n♻️ {tip3}\n⚡ {tip4}\n🚗 {tip5}",
                "🌿 Here are some tips for a greener life:\n• {tip1}\n• {tip2}\n• {tip3}\n• {tip4}\n• {tip5}"
            ],
            'default': [
                "🌱 I'm not sure I understand. Can you rephrase that?",
                "🤔 I didn't quite get that. Try asking about carbon footprint, eco score, or sustainability tips!",
                "💭 Hmm, I'm still learning! Can you ask me something about sustainability?",
                "🌿 I'm not sure about that. I can help with carbon footprint, eco score, recycling, energy saving, and more!",
                "🤖 I didn't understand. Try asking me about eco-friendly topics!"
            ]
        }
    
    def set_user_data(self, user_data: Dict[str, Any]):
        """Set user data for personalized responses."""
        self.user_data = user_data
    
    def generate_response(self, message: str, user_id: str = None) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a response for a user message.
        
        Args:
            message: User message
            user_id: Optional user ID
        
        Returns:
            Tuple of (response_text, response_metadata)
        """
        # Detect intent
        intent_result = self.intent_detector.detect_intent(message)
        
        # Generate response based on intent
        response = self._generate_by_intent(intent_result, message)
        
        # Add to conversation history
        self.conversation_history.append({
            'user': message,
            'response': response,
            'intent': intent_result.intent,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate metadata
        metadata = {
            'intent': intent_result.intent,
            'confidence': intent_result.confidence,
            'requires_data': self.intent_detector.get_intent(intent_result.intent).requires_data if self.intent_detector.get_intent(intent_result.intent) else False,
            'timestamp': datetime.now().isoformat()
        }
        
        return response, metadata
    
    def _generate_by_intent(self, intent_result: IntentResult, message: str) -> str:
        """
        Generate response based on detected intent.
        
        Args:
            intent_result: Detected intent
            message: Original message
        
        Returns:
            Generated response
        """
        intent_name = intent_result.intent
        
        if intent_name == 'carbon_footprint':
            return self._generate_footprint_response()
        
        elif intent_name == 'eco_score':
            return self._generate_eco_score_response()
        
        elif intent_name == 'reduce_footprint':
            return self._generate_reduce_response()
        
        elif intent_name == 'challenges':
            return self._generate_challenges_response()
        
        elif intent_name == 'water':
            return self._generate_water_response()
        
        elif intent_name == 'waste':
            return self._generate_waste_response()
        
        elif intent_name == 'energy':
            return self._generate_energy_response()
        
        elif intent_name == 'transport':
            return self._generate_transport_response()
        
        elif intent_name == 'diet':
            return self._generate_diet_response()
        
        elif intent_name == 'help':
            return self._generate_help_response()
        
        elif intent_name == 'thanks':
            return self._generate_thanks_response()
        
        elif intent_name == 'goodbye':
            return self._generate_goodbye_response()
        
        elif intent_name == 'joke':
            return self._generate_joke_response()
        
        elif intent_name == 'quiz':
            return self._generate_quiz_response()
        
        elif intent_name == 'tips':
            return self._generate_tips_response()
        
        elif intent_name == 'greeting':
            return self._generate_greeting_response()
        
        else:
            return self._generate_default_response()
    
    def _generate_greeting_response(self) -> str:
        """Generate greeting response."""
        return random.choice(self.templates['greeting'])
    
    def _generate_footprint_response(self) -> str:
        """Generate carbon footprint response."""
        footprint = self.user_data.get('footprint', 0)
        
        if footprint <= 0:
            return "🌱 I don't have your carbon footprint data yet. Please complete an assessment first! 📊"
        
        if footprint > 5000:
            level = 'high'
        elif footprint > 2000:
            level = 'medium'
        else:
            level = 'low'
        
        template = random.choice(self.templates['carbon_footprint'][level])
        response = template.format(footprint=footprint)
        
        if level == 'high':
            response += "\n\n💡 Try reducing your transport emissions and electricity usage."
        elif level == 'medium':
            response += "\n\n🌱 Small changes like using public transport can make a big difference!"
        else:
            response += "\n\n🎉 Keep up the great work! You're an eco-champion!"
        
        return response
    
    def _generate_eco_score_response(self) -> str:
        """Generate eco score response."""
        score = self.user_data.get('eco_score', 0)
        
        if score <= 0:
            return "⭐ I don't have your Eco Score yet. Complete an assessment to get your score!"
        
        if score >= 80:
            level = 'high'
        elif score >= 50:
            level = 'medium'
        else:
            level = 'low'
        
        template = random.choice(self.templates['eco_score'][level])
        response = template.format(score=score)
        
        if level == 'low':
            response += "\n\n💡 Check out my tips to improve your score!"
        elif level == 'medium':
            response += "\n\n🌱 You're on the right track. Keep going!"
        else:
            response += "\n\n🏆 You're a sustainability superstar!"
        
        return response
    
    def _generate_reduce_response(self) -> str:
        """Generate reduce footprint response."""
        tips = [
            "🚲 Use public transport or cycle instead of driving",
            "⚡ Switch to LED bulbs and turn off unused appliances",
            "🥗 Eat more plant-based meals",
            "♻️ Reduce, reuse, and recycle",
            "💧 Save water by taking shorter showers",
            "☀️ Use renewable energy sources",
            "🌳 Plant trees and support reforestation",
            "🛍️ Avoid single-use plastics",
            "📉 Track your progress with regular assessments",
            "🌿 Compost organic waste"
        ]
        
        template = random.choice(self.templates['reduce_tips'])
        selected_tips = random.sample(tips, 5)
        
        return template.format(
            tip1=selected_tips[0],
            tip2=selected_tips[1],
            tip3=selected_tips[2],
            tip4=selected_tips[3],
            tip5=selected_tips[4]
        )
    
    def _generate_challenges_response(self) -> str:
        """Generate challenges response."""
        challenges = [
            "🌱 Take a 10-minute walk instead of driving",
            "🚿 Reduce shower time by 2 minutes",
            "♻️ Sort and recycle all waste today",
            "💡 Turn off all unused electronics",
            "🥗 Eat one plant-based meal",
            "🚲 Bike or walk to your nearest destination",
            "💧 Fix any leaking taps",
            "📊 Complete a carbon footprint assessment",
            "🌳 Plant a tree or donate to a tree-planting charity",
            "📉 Reduce plastic usage by 50%"
        ]
        
        template = random.choice(self.templates['challenges'])
        selected = random.sample(challenges, 3)
        
        return template.format(
            challenge1=selected[0],
            challenge2=selected[1],
            challenge3=selected[2]
        )
    
    def _generate_water_response(self) -> str:
        """Generate water footprint response."""
        shower = random.randint(30, 80)
        laundry = random.randint(40, 100)
        dishes = random.randint(10, 30)
        toilet = random.randint(20, 50)
        garden = random.randint(10, 40)
        total = shower + laundry + dishes + toilet + garden
        
        template = random.choice(self.templates['water'])
        
        return template.format(
            shower=shower,
            laundry=laundry,
            dishes=dishes,
            toilet=toilet,
            garden=garden,
            total=total
        )
    
    def _generate_waste_response(self) -> str:
        """Generate waste response."""
        tips = [
            "Use reusable bags when shopping",
            "Compost organic waste",
            "Recycle paper, plastic, glass, and metal",
            "Avoid single-use plastics",
            "Buy products with minimal packaging",
            "Repair items instead of replacing them",
            "Donate unwanted items instead of throwing away",
            "Choose products made from recycled materials"
        ]
        
        template = random.choice(self.templates['waste'])
        selected = random.sample(tips, 4)
        
        return template.format(
            tip1=selected[0],
            tip2=selected[1],
            tip3=selected[2],
            tip4=selected[3]
        )
    
    def _generate_energy_response(self) -> str:
        """Generate energy response."""
        tips = [
            "Switch to LED light bulbs",
            "Turn off electronics when not in use",
            "Use energy-efficient appliances",
            "Install solar panels",
            "Use a programmable thermostat",
            "Insulate your home properly",
            "Use natural light during the day",
            "Wash clothes in cold water",
            "Air dry clothes instead of using a dryer",
            "Unplug chargers when not in use"
        ]
        
        template = random.choice(self.templates['energy'])
        selected = random.sample(tips, 4)
        
        return template.format(
            tip1=selected[0],
            tip2=selected[1],
            tip3=selected[2],
            tip4=selected[3]
        )
    
    def _generate_transport_response(self) -> str:
        """Generate transport response."""
        tips = [
            "Use public transport like buses and trains",
            "Cycle or walk for short distances",
            "Carpool with colleagues or friends",
            "Switch to an electric or hybrid vehicle",
            "Plan trips efficiently to reduce driving",
            "Use video calls instead of traveling",
            "Maintain your vehicle for better efficiency",
            "Consider using a bike-sharing service"
        ]
        
        template = random.choice(self.templates['transport'])
        selected = random.sample(tips, 4)
        
        return template.format(
            tip1=selected[0],
            tip2=selected[1],
            tip3=selected[2],
            tip4=selected[3]
        )
    
    def _generate_diet_response(self) -> str:
        """Generate diet response."""
        tips = [
            "Eat more plant-based meals",
            "Reduce meat consumption",
            "Choose locally sourced food",
            "Buy seasonal produce",
            "Reduce food waste",
            "Compost food scraps",
            "Choose organic products",
            "Grow your own vegetables"
        ]
        
        template = random.choice(self.templates['diet'])
        selected = random.sample(tips, 4)
        
        return template.format(
            tip1=selected[0],
            tip2=selected[1],
            tip3=selected[2],
            tip4=selected[3]
        )
    
    def _generate_help_response(self) -> str:
        """Generate help response."""
        return random.choice(self.templates['help'])
    
    def _generate_thanks_response(self) -> str:
        """Generate thanks response."""
        return random.choice(self.templates['thanks'])
    
    def _generate_goodbye_response(self) -> str:
        """Generate goodbye response."""
        return random.choice(self.templates['goodbye'])
    
    def _generate_joke_response(self) -> str:
        """Generate joke response."""
        return random.choice(self.templates['joke'])
    
    def _generate_quiz_response(self) -> str:
        """Generate quiz response."""
        return random.choice(self.templates['quiz'])
    
    def _generate_tips_response(self) -> str:
        """Generate tips response."""
        tips = [
            "🌱 Plant a tree every month",
            "💧 Fix leaking taps immediately",
            "♻️ Recycle all paper and plastic",
            "⚡ Switch to renewable energy",
            "🚲 Bike to work once a week",
            "🥗 Have one meat-free day per week",
            "📊 Track your carbon footprint regularly",
            "🌳 Support reforestation projects",
            "🛍️ Bring your own bags to shops",
            "☀️ Use solar-powered devices"
        ]
        
        template = random.choice(self.templates['tips'])
        selected = random.sample(tips, 5)
        
        return template.format(
            tip1=selected[0],
            tip2=selected[1],
            tip3=selected[2],
            tip4=selected[3],
            tip5=selected[4]
        )
    
    def _generate_default_response(self) -> str:
        """Generate default response."""
        return random.choice(self.templates['default'])
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.context = {}