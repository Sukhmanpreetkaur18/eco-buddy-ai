"""
Intent detection for the AI Eco-Chatbot
Identifies user intent from messages and routes to appropriate handlers.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Intent:
    """Data class for an intent."""
    name: str
    keywords: List[str]
    patterns: List[str]
    responses: List[str]
    fallback: Optional[str] = None
    requires_data: bool = False
    priority: int = 0


@dataclass
class IntentResult:
    """Result of intent detection."""
    intent: str
    confidence: float
    extracted_data: Dict[str, Any]
    matched_keyword: str = ""


class IntentDetector:
    """
    Detects user intent from messages using keyword matching and pattern recognition.
    """
    
    def __init__(self):
        self.intents = self._load_intents()
        self.context = {}
    
    def _load_intents(self) -> Dict[str, Intent]:
        """Load all intents with keywords, patterns, and responses."""
        return {
            'greeting': Intent(
                name='greeting',
                keywords=['hi', 'hello', 'hey', 'greetings', 'good morning', 'good evening', 'howdy'],
                patterns=[r'^(hi|hello|hey|greetings|howdy)\s*$'],
                responses=[
                    "🌱 Hello! I'm your EcoBuddy AI assistant. How can I help you today?",
                    "👋 Hi there! Ready to make the planet greener? I'm here to help!",
                    "🌟 Welcome back! What eco-friendly thing can I assist you with today?"
                ]
            ),
            'carbon_footprint': Intent(
                name='carbon_footprint',
                keywords=['footprint', 'carbon footprint', 'my footprint', 'carbon emissions', 'co2'],
                patterns=[r'what (is|are) my (carbon )?footprint', r'how (much|many) co2'],
                responses=[
                    "🌍 Let me check your carbon footprint! 📊",
                    "📈 Your carbon footprint is an important metric. Here's what I found:",
                    "🌱 Based on your recent assessments, here's your carbon footprint:"
                ],
                requires_data=True,
                priority=2
            ),
            'eco_score': Intent(
                name='eco_score',
                keywords=['eco score', 'score', 'my score', 'sustainability score', 'rating'],
                patterns=[r'what (is )?my eco score', r'how (good|bad) (is )?my eco score'],
                responses=[
                    "⭐ Your Eco Score is a measure of your sustainability. Let me check:",
                    "🏆 Here's your current Eco Score based on your assessments:"
                ],
                requires_data=True,
                priority=2
            ),
            'reduce_footprint': Intent(
                name='reduce_footprint',
                keywords=['reduce', 'lower', 'decrease', 'improve', 'footprint tips', 'how to reduce'],
                patterns=[r'how (can|do) i reduce (my )?carbon', r'ways to (reduce|lower) footprint'],
                responses=[
                    "💡 Here are some personalized tips to reduce your carbon footprint:",
                    "🌱 Great question! Here's what you can do:",
                    "📋 Based on your profile, I recommend these actions:"
                ],
                requires_data=True,
                priority=3
            ),
            'challenges': Intent(
                name='challenges',
                keywords=['challenge', 'challenges', 'eco challenge', 'daily challenge'],
                patterns=[r'what (are )?(the )?challenges', r'show (me )?challenges'],
                responses=[
                    "🏆 Here are today's eco-challenges for you:",
                    "🎯 Ready for some challenges? Here's what I have:"
                ],
                priority=1
            ),
            'water': Intent(
                name='water',
                keywords=['water', 'water footprint', 'save water', 'water usage'],
                patterns=[r'how (much )?water (do|am) i use', r'water (footprint|usage)'],
                responses=[
                    "💧 Let me check your water footprint information:",
                    "🚿 Here's your water usage breakdown:"
                ],
                requires_data=True,
                priority=2
            ),
            'waste': Intent(
                name='waste',
                keywords=['waste', 'recycle', 'recycling', 'compost', 'trash'],
                patterns=[r'how to (reduce|manage) waste', r'waste (reduction|management)'],
                responses=[
                    "♻️ Great question! Here's how you can reduce waste:",
                    "🗑️ Let me help you with waste management tips:"
                ]
            ),
            'energy': Intent(
                name='energy',
                keywords=['energy', 'electricity', 'power', 'solar', 'renewable'],
                patterns=[r'energy (usage|consumption|saving)', r'how to save energy'],
                responses=[
                    "⚡ Here are some energy-saving tips for you:",
                    "💡 Let me help you reduce your energy consumption:"
                ]
            ),
            'transport': Intent(
                name='transport',
                keywords=['transport', 'travel', 'commute', 'drive', 'car', 'bike', 'walk'],
                patterns=[r'how to (reduce|lower) transport emissions', r'sustainable (transport|travel)'],
                responses=[
                    "🚗 Here are some sustainable transport options:",
                    "🚲 Let me help you reduce your travel emissions:"
                ]
            ),
            'diet': Intent(
                name='diet',
                keywords=['diet', 'food', 'plant-based', 'vegetarian', 'vegan', 'meat'],
                patterns=[r'sustainable (diet|food)', r'how to eat (sustainable|eco-friendly)'],
                responses=[
                    "🥗 Here are some sustainable diet tips:",
                    "🌿 Let me help you make eco-friendly food choices:"
                ]
            ),
            'help': Intent(
                name='help',
                keywords=['help', 'what can you do', 'capabilities', 'features'],
                patterns=[r'what can you do', r'help me', r'how do you work'],
                responses=[
                    "🤖 I'm your EcoBuddy AI assistant! I can help you with:",
                    "📋 Here's what I can do for you:"
                ]
            ),
            'thanks': Intent(
                name='thanks',
                keywords=['thanks', 'thank you', 'thankyou', 'thx', 'appreciate', 'great'],
                patterns=[r'^thanks?$', r'thank you', r'thx', r'appreciate'],
                responses=[
                    "🌱 You're welcome! Happy to help you on your eco-journey! 🌿",
                    "💚 My pleasure! Keep making sustainable choices! 🌎",
                    "🌟 Anytime! Together we can make a difference! 💪"
                ]
            ),
            'goodbye': Intent(
                name='goodbye',
                keywords=['bye', 'goodbye', 'see you', 'later', 'exit', 'quit', 'good night'],
                patterns=[r'^(bye|goodbye|quit|exit|see you)\s*$'],
                responses=[
                    "👋 Goodbye! Keep being eco-friendly! 🌱",
                    "🌿 See you later! Remember, every small action counts! 💚",
                    "🌟 Take care! I'm always here to help with your eco-journey! 🌍"
                ]
            ),
            'joke': Intent(
                name='joke',
                keywords=['joke', 'funny', 'laugh', 'humor', 'tell me a joke'],
                patterns=[r'tell (me )?a joke', r'make me laugh'],
                responses=[
                    "🌱 Why don't scientists trust atoms? Because they make up everything! 😄",
                    "💡 What's an environmentalist's favorite type of music? Solar! ☀️",
                    "🌳 Why do trees look suspicious? They're always up to something shady! 🌲"
                ]
            ),
            'quiz': Intent(
                name='quiz',
                keywords=['quiz', 'test', 'knowledge', 'trivia', 'question'],
                patterns=[r'(take|give me) a quiz', r'sustainability (quiz|test)'],
                responses=[
                    "📝 Here's a quick sustainability quiz for you:",
                    "🧠 Test your eco-knowledge with this quiz:"
                ]
            ),
            'tips': Intent(
                name='tips',
                keywords=['tip', 'tips', 'advice', 'suggestion', 'recommendation', 'how to'],
                patterns=[r'give me (some )?tips', r'eco (tips|advice)'],
                responses=[
                    "💡 Here are some eco-tips for you:",
                    "🌿 Here's some advice to help you be more sustainable:"
                ]
            ),
            'default': Intent(
                name='default',
                keywords=[],
                patterns=[],
                responses=[
                    "🌱 I'm not sure I understand. Can you rephrase that?",
                    "🤔 I didn't quite get that. Try asking about carbon footprint, eco score, or sustainability tips!",
                    "💭 Hmm, I'm still learning! Can you ask me something about sustainability?"
                ],
                fallback="default"
            )
        }
    
    def detect_intent(self, message: str) -> IntentResult:
        """
        Detect intent from a user message.
        
        Args:
            message: User's message
        
        Returns:
            IntentResult with detected intent and confidence
        """
        message_lower = message.lower().strip()
        
        # Check each intent
        best_intent = None
        best_confidence = 0.0
        matched_keyword = ""
        extracted_data = {}
        
        for intent_name, intent in self.intents.items():
            confidence = 0.0
            keyword_match = ""
            
            # Check keywords
            for keyword in intent.keywords:
                if keyword in message_lower:
                    confidence += 0.3
                    keyword_match = keyword
                    break
            
            # Check patterns
            for pattern in intent.patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    confidence += 0.5
                    break
            
            # Boost confidence for exact matches
            if message_lower in [k for k in intent.keywords]:
                confidence += 0.2
            
            # Update best intent
            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = intent_name
                matched_keyword = keyword_match
        
        # Extract data from message
        extracted_data = self._extract_data(message, best_intent)
        
        # If no intent found or confidence too low, use default
        if best_intent is None or best_confidence < 0.3:
            best_intent = 'default'
            best_confidence = 0.5
        
        return IntentResult(
            intent=best_intent,
            confidence=min(best_confidence, 1.0),
            extracted_data=extracted_data,
            matched_keyword=matched_keyword
        )
    
    def _extract_data(self, message: str, intent: str) -> Dict[str, Any]:
        """
        Extract relevant data from message.
        
        Args:
            message: User message
            intent: Detected intent
        
        Returns:
            Dictionary of extracted data
        """
        data = {}
        message_lower = message.lower()
        
        # Extract numbers (for amounts, quantities)
        numbers = re.findall(r'\d+\.?\d*', message)
        if numbers:
            data['numbers'] = [float(n) for n in numbers]
        
        # Extract units (kg, km, kWh, etc.)
        units = re.findall(r'\d+\.?\d*\s*(kg|km|kwh|lbs|miles|hours|days)', message_lower)
        if units:
            data['units'] = units
        
        # Extract time periods
        time_periods = ['today', 'yesterday', 'this week', 'this month', 'this year', 'daily', 'weekly', 'monthly']
        for period in time_periods:
            if period in message_lower:
                data['time_period'] = period
                break
        
        return data
    
    def get_response(self, intent_name: str) -> str:
        """
        Get a random response for an intent.
        
        Args:
            intent_name: Name of the intent
        
        Returns:
            Response string
        """
        intent = self.intents.get(intent_name)
        if intent and intent.responses:
            import random
            return random.choice(intent.responses)
        
        return self.intents['default'].responses[0]
    
    def get_intent(self, intent_name: str) -> Optional[Intent]:
        """Get an intent by name."""
        return self.intents.get(intent_name)