"""
Context management for the AI Eco-Chatbot
Maintains conversation context, user preferences, and session state.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import hashlib
from collections import deque


class ContextManager:
    """
    Manages conversation context, user preferences, and session data.
    """
    
    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.conversations: Dict[str, deque] = {}
        self.user_contexts: Dict[str, Dict[str, Any]] = {}
        self.session_data: Dict[str, Dict[str, Any]] = {}
        self.topic_focus: Dict[str, str] = {}
        self.last_interaction: Dict[str, datetime] = {}
        self.preferences: Dict[str, Dict[str, Any]] = {}
        
    def get_conversation(self, user_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a user."""
        if user_id not in self.conversations:
            self.conversations[user_id] = deque(maxlen=self.max_history)
        return list(self.conversations[user_id])
    
    def add_to_conversation(self, user_id: str, user_message: str, bot_response: str, intent: str = ""):
        """Add a message pair to conversation history."""
        if user_id not in self.conversations:
            self.conversations[user_id] = deque(maxlen=self.max_history)
        
        entry = {
            'user_message': user_message,
            'bot_response': bot_response,
            'intent': intent,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id
        }
        self.conversations[user_id].append(entry)
        self.last_interaction[user_id] = datetime.now()
    
    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get the current context for a user."""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {}
        return self.user_contexts[user_id]
    
    def update_user_context(self, user_id: str, key: str, value: Any):
        """Update a specific context key for a user."""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {}
        self.user_contexts[user_id][key] = value
    
    def set_topic_focus(self, user_id: str, topic: str):
        """Set the current topic focus for a user."""
        self.topic_focus[user_id] = topic
    
    def get_topic_focus(self, user_id: str) -> Optional[str]:
        """Get the current topic focus for a user."""
        return self.topic_focus.get(user_id)
    
    def get_session_data(self, user_id: str) -> Dict[str, Any]:
        """Get session data for a user."""
        if user_id not in self.session_data:
            self.session_data[user_id] = {}
        return self.session_data[user_id]
    
    def update_session_data(self, user_id: str, key: str, value: Any):
        """Update session data for a user."""
        if user_id not in self.session_data:
            self.session_data[user_id] = {}
        self.session_data[user_id][key] = value
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences."""
        if user_id not in self.preferences:
            self.preferences[user_id] = {
                'eco_goals': [],
                'interests': [],
                'preferred_topics': [],
                'notification_enabled': True,
                'language': 'en',
                'measurement_unit': 'metric'
            }
        return self.preferences[user_id]
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences."""
        if user_id not in self.preferences:
            self.preferences[user_id] = {}
        self.preferences[user_id].update(preferences)
    
    def get_last_intent(self, user_id: str) -> Optional[str]:
        """Get the last intent for a user."""
        conversation = self.get_conversation(user_id)
        if conversation:
            return conversation[-1].get('intent', '')
        return None
    
    def is_conversation_stale(self, user_id: str, timeout_minutes: int = 30) -> bool:
        """Check if a conversation is stale."""
        if user_id not in self.last_interaction:
            return True
        elapsed = datetime.now() - self.last_interaction[user_id]
        return elapsed > timedelta(minutes=timeout_minutes)
    
    def clear_conversation(self, user_id: str):
        """Clear conversation history for a user."""
        if user_id in self.conversations:
            self.conversations[user_id].clear()
        if user_id in self.user_contexts:
            self.user_contexts[user_id] = {}
        if user_id in self.topic_focus:
            del self.topic_focus[user_id]
    
    def get_conversation_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of the conversation."""
        conversation = self.get_conversation(user_id)
        if not conversation:
            return {
                'total_messages': 0,
                'avg_response_time': 0,
                'top_intents': {},
                'duration_minutes': 0
            }
        
        # Calculate statistics
        total = len(conversation)
        intents = {}
        for entry in conversation:
            intent = entry.get('intent', 'unknown')
            intents[intent] = intents.get(intent, 0) + 1
        
        # Get time range
        first_time = datetime.fromisoformat(conversation[0]['timestamp'])
        last_time = datetime.fromisoformat(conversation[-1]['timestamp'])
        duration = (last_time - first_time).total_seconds() / 60
        
        # Get top intents
        top_intents = sorted(intents.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_messages': total,
            'avg_response_time': 0,  # Not tracking this yet
            'top_intents': dict(top_intents),
            'duration_minutes': round(duration, 1),
            'last_message': conversation[-1]['user_message'],
            'current_topic': self.get_topic_focus(user_id)
        }
    
    def detect_context_switch(self, user_id: str, new_intent: str) -> bool:
        """Detect if the user has switched topics."""
        last_intent = self.get_last_intent(user_id)
        if not last_intent:
            return False
        return last_intent != new_intent
    
    def get_follow_up_suggestions(self, user_id: str) -> List[str]:
        """Get follow-up suggestions based on context."""
        conversation = self.get_conversation(user_id)
        if not conversation:
            return [
                "🌱 Ask me about your carbon footprint",
                "💡 Get personalized eco tips",
                "🏆 See today's eco-challenges",
                "📊 Check your Eco Score"
            ]
        
        last_intent = conversation[-1].get('intent', '')
        suggestions = {
            'carbon_footprint': [
                "📊 How can I reduce my carbon footprint?",
                "🌍 Compare my footprint to average",
                "📈 Track my footprint progress"
            ],
            'eco_score': [
                "⭐ How can I improve my Eco Score?",
                "🏆 What's the highest Eco Score?",
                "📊 See my score history"
            ],
            'reduce_footprint': [
                "🚲 Which transport is most sustainable?",
                "⚡ How to save energy at home?",
                "🥗 What's the most eco-friendly diet?"
            ],
            'challenges': [
                "🏆 Give me more challenges",
                "🔥 What's my current streak?",
                "🎯 Harder challenges please"
            ],
            'water': [
                "💧 How to save water at home?",
                "🚿 What uses the most water?",
                "🌿 Water-saving garden tips"
            ],
            'waste': [
                "♻️ What can I recycle?",
                "🗑️ How to reduce food waste?",
                "🌱 Composting tips"
            ],
            'energy': [
                "⚡ Best energy saving tips",
                "☀️ How to go solar?",
                "💡 Energy efficient appliances"
            ],
            'transport': [
                "🚗 Electric vs hybrid cars",
                "🚲 Benefits of cycling",
                "🚌 Public transport options"
            ],
            'diet': [
                "🥗 Plant-based diet benefits",
                "🌱 Sustainable food choices",
                "🍽️ Meal planning tips"
            ]
        }
        
        return suggestions.get(last_intent, [
            "🌱 Ask me about your carbon footprint",
            "💡 Get personalized eco tips",
            "🏆 See today's eco-challenges",
            "📊 Check your Eco Score"
        ])
    
    def get_user_engagement_score(self, user_id: str) -> float:
        """Calculate user engagement score based on conversation history."""
        conversation = self.get_conversation(user_id)
        if not conversation:
            return 0.0
        
        total = len(conversation)
        # Factor 1: Message count
        count_score = min(total / 10, 1.0)
        
        # Factor 2: Intent variety
        intents = {}
        for entry in conversation:
            intent = entry.get('intent', 'unknown')
            intents[intent] = intents.get(intent, 0) + 1
        variety_score = min(len(intents) / 5, 1.0)
        
        # Factor 3: Recency
        if self.last_interaction.get(user_id):
            hours = (datetime.now() - self.last_interaction[user_id]).total_seconds() / 3600
            recency_score = max(0, 1 - (hours / 168))  # 7 days window
        
        # Weighted average
        return round(
            (count_score * 0.4) +
            (variety_score * 0.3) +
            (recency_score * 0.3),
            2
        )
    
    def get_topic_distribution(self, user_id: str) -> Dict[str, int]:
        """Get topic distribution for a user."""
        conversation = self.get_conversation(user_id)
        distribution = {}
        for entry in conversation:
            intent = entry.get('intent', 'unknown')
            distribution[intent] = distribution.get(intent, 0) + 1
        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
    
    def get_conversation_flow(self, user_id: str) -> List[Dict[str, Any]]:
        """Get conversation flow with intent transitions."""
        conversation = self.get_conversation(user_id)
        flow = []
        previous_intent = None
        
        for entry in conversation:
            current_intent = entry.get('intent', 'unknown')
            flow.append({
                'message': entry['user_message'],
                'intent': current_intent,
                'timestamp': entry['timestamp'],
                'transition': f"{previous_intent} -> {current_intent}" if previous_intent else "start"
            })
            previous_intent = current_intent
        
        return flow
    
    def get_conversation_stats(self, user_id: str) -> Dict[str, Any]:
        """Get detailed conversation statistics."""
        conversation = self.get_conversation(user_id)
        if not conversation:
            return {
                'total_messages': 0,
                'unique_intents': 0,
                'avg_words_per_message': 0,
                'duration_minutes': 0,
                'message_frequency': 'daily'
            }
        
        total_words = sum(len(entry['user_message'].split()) for entry in conversation)
        intents = {}
        for entry in conversation:
            intent = entry.get('intent', 'unknown')
            intents[intent] = intents.get(intent, 0) + 1
        
        return {
            'total_messages': len(conversation),
            'unique_intents': len(intents),
            'avg_words_per_message': round(total_words / len(conversation), 1),
            'avg_response_length': round(
                sum(len(entry['bot_response']) for entry in conversation) / len(conversation),
                1
            ),
            'top_intent': max(intents.items(), key=lambda x: x[1])[0] if intents else 'none',
            'intent_distribution': intents
        }