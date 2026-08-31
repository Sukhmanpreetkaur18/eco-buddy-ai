"""
AI module for EcoBuddy AI
Contains chatbot, intent detection, and response generation.
"""

from .eco_chatbot import EcoChatbot
from .chat_intents import IntentDetector
from .response_generator import ResponseGenerator
from .context_manager import ContextManager

__all__ = [
    'EcoChatbot',
    'IntentDetector',
    'ResponseGenerator',
    'ContextManager'
]