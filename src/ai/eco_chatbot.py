"""
EcoBuddy AI Chatbot - Main chatbot engine
Integrates intent detection, response generation, and context management.
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import uuid

from .chat_intents import IntentDetector
from .response_generator import ResponseGenerator
from .context_manager import ContextManager

logger = logging.getLogger(__name__)


class EcoChatbot:
    """
    Main chatbot engine for EcoBuddy AI.
    Handles user interactions, intent detection, and response generation.
    """
    
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.response_generator = ResponseGenerator(self.intent_detector)
        self.context_manager = ContextManager()
        self.session_id = str(uuid.uuid4())
        self.user_data = {}
        self.is_active = True
        
        logger.info(f"EcoChatbot initialized with session: {self.session_id}")
    
    def set_user_data(self, user_data: Dict[str, Any]):
        """
        Set user data for personalized responses.
        
        Args:
            user_data: User data dictionary
        """
        self.user_data = user_data
        self.response_generator.set_user_data(user_data)
        
        # Update context with user data
        if user_data.get('user_id'):
            self.context_manager.update_user_context(
                user_data['user_id'],
                'user_data',
                user_data
            )
        
        logger.info(f"User data set for chatbot: {user_data.get('user_id', 'unknown')}")
    
    def process_message(
        self,
        message: str,
        user_id: str = None,
        user_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and generate a response.
        
        Args:
            message: User message
            user_id: Optional user ID
            user_data: Optional user data
        
        Returns:
            Response dictionary with message and metadata
        """
        start_time = datetime.now()
        
        # Update user data if provided
        if user_data:
            self.set_user_data(user_data)
        
        # Use provided user_id or fallback
        user_id = user_id or self.user_data.get('user_id', 'guest')
        
        # Check if conversation is stale and reset context if needed
        if self.context_manager.is_conversation_stale(user_id):
            self.context_manager.clear_conversation(user_id)
            logger.info(f"Cleared stale conversation for user: {user_id}")
        
        # Get conversation context
        context = self.context_manager.get_user_context(user_id)
        
        # Detect intent
        intent_result = self.intent_detector.detect_intent(message)
        
        # Check for context switch
        if self.context_manager.detect_context_switch(user_id, intent_result.intent):
            self.context_manager.set_topic_focus(user_id, intent_result.intent)
            logger.info(f"Context switch detected for user {user_id}: {intent_result.intent}")
        
        # Generate response
        response_text, response_metadata = self.response_generator.generate_response(
            message,
            user_id
        )
        
        # Add to conversation history
        self.context_manager.add_to_conversation(
            user_id,
            message,
            response_text,
            intent_result.intent
        )
        
        # Get follow-up suggestions
        suggestions = self.context_manager.get_follow_up_suggestions(user_id)
        
        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Build response
        result = {
            'success': True,
            'message': response_text,
            'intent': intent_result.intent,
            'confidence': intent_result.confidence,
            'session_id': self.session_id,
            'response_time_ms': round(response_time, 2),
            'follow_up_suggestions': suggestions[:3],
            'requires_action': response_metadata.get('requires_data', False),
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def get_conversation_history(self, user_id: str = None) -> List[Dict[str, Any]]:
        """
        Get conversation history for a user.
        
        Args:
            user_id: Optional user ID
        
        Returns:
            List of conversation entries
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        return self.context_manager.get_conversation(user_id)
    
    def get_user_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Get user context.
        
        Args:
            user_id: Optional user ID
        
        Returns:
            User context dictionary
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        return self.context_manager.get_user_context(user_id)
    
    def clear_conversation(self, user_id: str = None):
        """
        Clear conversation history for a user.
        
        Args:
            user_id: Optional user ID
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        self.context_manager.clear_conversation(user_id)
        logger.info(f"Cleared conversation for user: {user_id}")
    
    def get_conversation_summary(self, user_id: str = None) -> Dict[str, Any]:
        """
        Get conversation summary for a user.
        
        Args:
            user_id: Optional user ID
        
        Returns:
            Conversation summary
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        return self.context_manager.get_conversation_summary(user_id)
    
    def get_conversation_stats(self, user_id: str = None) -> Dict[str, Any]:
        """
        Get conversation statistics for a user.
        
        Args:
            user_id: Optional user ID
        
        Returns:
            Conversation statistics
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        return self.context_manager.get_conversation_stats(user_id)
    
    def get_follow_up_suggestions(self, user_id: str = None) -> List[str]:
        """
        Get follow-up suggestions for a user.
        
        Args:
            user_id: Optional user ID
        
        Returns:
            List of suggestions
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        return self.context_manager.get_follow_up_suggestions(user_id)
    
    def get_engagement_score(self, user_id: str = None) -> float:
        """
        Get user engagement score.
        
        Args:
            user_id: Optional user ID
        
        Returns:
            Engagement score (0-1)
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        return self.context_manager.get_user_engagement_score(user_id)
    
    def get_intent_distribution(self, user_id: str = None) -> Dict[str, int]:
        """
        Get intent distribution for a user.
        
        Args:
            user_id: Optional user ID
        
        Returns:
            Intent distribution dictionary
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        return self.context_manager.get_topic_distribution(user_id)
    
    def get_topic_focus(self, user_id: str = None) -> Optional[str]:
        """
        Get current topic focus for a user.
        
        Args:
            user_id: Optional user ID
        
        Returns:
            Topic focus string
        """
        user_id = user_id or self.user_data.get('user_id', 'guest')
        return self.context_manager.get_topic_focus(user_id)
    
    def get_intents(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all available intents.
        
        Returns:
            Dictionary of intents
        """
        intents = {}
        for name, intent in self.intent_detector.intents.items():
            intents[name] = {
                'keywords': intent.keywords,
                'patterns': intent.patterns,
                'responses': intent.responses,
                'requires_data': intent.requires_data
            }
        return intents
    
    def get_session_info(self) -> Dict[str, Any]:
        """
        Get session information.
        
        Returns:
            Session info dictionary
        """
        return {
            'session_id': self.session_id,
            'is_active': self.is_active,
            'created_at': datetime.now().isoformat(),
            'user_data_available': bool(self.user_data),
            'user_id': self.user_data.get('user_id', 'guest') if self.user_data else None
        }
    
    def reset_chatbot(self):
        """Reset the chatbot state."""
        self.session_id = str(uuid.uuid4())
        self.user_data = {}
        self.response_generator.clear_history()
        logger.info(f"Chatbot reset. New session: {self.session_id}")
    
    def get_common_questions(self) -> List[Dict[str, str]]:
        """
        Get list of common questions for the chatbot.
        
        Returns:
            List of question-answer pairs
        """
        return [
            {
                'question': 'What is my carbon footprint?',
                'answer': 'I can show you your carbon footprint based on your latest assessment. Would you like to see it?'
            },
            {
                'question': 'How can I reduce my footprint?',
                'answer': 'I can give you personalized tips based on your lifestyle. Try using public transport, reducing electricity usage, and eating more plant-based meals!'
            },
            {
                'question': 'What is Eco Score?',
                'answer': 'Eco Score is a measure of your sustainability from 0-100. Higher is better! It\'s calculated based on your carbon footprint, energy usage, and lifestyle choices.'
            },
            {
                'question': 'Give me eco-tips',
                'answer': 'I have plenty of tips! 🌱 From saving water to reducing waste, I can help you live more sustainably.'
            },
            {
                'question': 'What challenges are available?',
                'answer': 'I have daily, weekly, and monthly challenges to help you build sustainable habits. Want to see today\'s challenges?'
            },
            {
                'question': 'How to save water?',
                'answer': 'Great question! 💧 Take shorter showers, fix leaks, use water-efficient appliances, and collect rainwater for gardening.'
            },
            {
                'question': 'How to reduce waste?',
                'answer': '♻️ Reduce, reuse, recycle! Start by avoiding single-use plastics, composting organic waste, and buying products with minimal packaging.'
            },
            {
                'question': 'How to save energy at home?',
                'answer': '⚡ Switch to LED bulbs, turn off unused appliances, use energy-efficient devices, and consider installing solar panels!'
            }
        ]
    
    def handle_feedback(self, user_id: str, feedback: str, rating: int) -> Dict[str, Any]:
        """
        Handle user feedback on the chatbot.
        
        Args:
            user_id: User ID
            feedback: User feedback text
            rating: Rating (1-5)
        
        Returns:
            Feedback result
        """
        logger.info(f"Feedback received from user {user_id}: rating {rating}")
        
        return {
            'success': True,
            'message': 'Thank you for your feedback! 🙏 It helps me improve.',
            'rating': rating,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }