"""
Chat Widget Component for EcoBuddy AI
Provides a chat interface for the AI Eco-Chatbot.
"""

import streamlit as st
import time
from typing import Optional, Dict, Any, List
from datetime import datetime
import random

from src.ai.eco_chatbot import EcoChatbot


class ChatWidget:
    """
    Chat widget component for displaying and interacting with the EcoChatbot.
    """
    
    @staticmethod
    def render(
        user_id: Optional[str] = None,
        user_data: Optional[Dict[str, Any]] = None,
        placeholder: Optional[str] = "Ask me about sustainability...",
        height: int = 400
    ):
        """
        Render the chat widget.
        
        Args:
            user_id: User ID for the chat session
            user_data: User data for personalized responses
            placeholder: Placeholder text for input
            height: Height of the chat container
        """
        # Initialize chatbot
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = EcoChatbot()
        
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        
        if user_id and user_data:
            st.session_state.chatbot.set_user_data(user_data)
        
        # Chat CSS
        st.markdown("""
        <style>
            .chat-container {
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 16px;
                height: {height}px;
                overflow-y: auto;
                background: #f8fafc;
                margin-bottom: 12px;
            }
            .chat-message {
                display: flex;
                margin-bottom: 12px;
                animation: fadeIn 0.3s ease;
            }
            .chat-message.user {
                justify-content: flex-end;
            }
            .chat-message.bot {
                justify-content: flex-start;
            }
            .chat-bubble {
                max-width: 80%;
                padding: 12px 16px;
                border-radius: 12px;
                font-size: 14px;
                line-height: 1.6;
                word-wrap: break-word;
            }
            .chat-bubble.user {
                background: #3b82f6;
                color: white;
                border-bottom-right-radius: 4px;
            }
            .chat-bubble.bot {
                background: white;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-bottom-left-radius: 4px;
            }
            .chat-bubble.bot .bot-icon {
                margin-right: 8px;
            }
            .chat-bubble .timestamp {
                font-size: 10px;
                opacity: 0.6;
                margin-top: 4px;
                display: block;
            }
            .typing-indicator {
                display: flex;
                gap: 4px;
                padding: 8px 12px;
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                width: 50px;
            }
            .typing-indicator span {
                width: 8px;
                height: 8px;
                background: #94a3b8;
                border-radius: 50%;
                animation: typing 1.4s infinite;
            }
            .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
            .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-8px); }
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .quick-replies {
                display: flex;
                gap: 6px;
                flex-wrap: wrap;
                margin-top: 8px;
            }
            .quick-reply-btn {
                background: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 4px 12px;
                font-size: 12px;
                color: #1e293b;
                cursor: pointer;
                transition: all 0.2s;
            }
            .quick-reply-btn:hover {
                background: #dbeafe;
                border-color: #3b82f6;
            }
            .chat-footer {
                display: flex;
                gap: 8px;
                align-items: center;
            }
            .chat-footer .stTextInput {
                flex: 1;
            }
            .chat-footer .stButton {
                flex: 0;
            }
        </style>
        """.format(height=height), unsafe_allow_html=True)
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display messages
            for msg in st.session_state.chat_messages:
                is_user = msg.get('type') == 'user'
                avatar = "👤" if is_user else "🌱"
                
                if is_user:
                    st.markdown(f"""
                    <div class="chat-message user">
                        <div class="chat-bubble user">
                            {msg['content']}
                            <span class="timestamp">{msg.get('timestamp', '')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="chat-bubble bot">
                            <span class="bot-icon">{avatar}</span>
                            {msg['content']}
                            <span class="timestamp">{msg.get('timestamp', '')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Typing indicator
            if st.session_state.get('is_typing', False):
                st.markdown("""
                <div class="chat-message bot">
                    <div class="chat-bubble bot">
                        <div class="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Quick replies
        if st.session_state.chat_messages:
            suggestions = st.session_state.chatbot.get_follow_up_suggestions(
                user_id or 'guest'
            )
            
            if suggestions:
                st.markdown('<div class="quick-replies">', unsafe_allow_html=True)
                cols = st.columns(min(len(suggestions), 4))
                for idx, suggestion in enumerate(suggestions[:4]):
                    with cols[idx % 4]:
                        if st.button(
                            suggestion[:30] + ("..." if len(suggestion) > 30 else ""),
                            key=f"suggestion_{idx}",
                            use_container_width=True
                        ):
                            ChatWidget._send_message(
                                suggestion,
                                user_id,
                                user_data
                            )
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Message",
                placeholder=placeholder,
                key="chat_input",
                label_visibility="collapsed"
            )
        
        with col2:
            send_clicked = st.button(
                "📤",
                key="send_button",
                use_container_width=True
            )
        
        # Handle send
        if send_clicked and user_input:
            ChatWidget._send_message(user_input, user_id, user_data)
            st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.chat_messages = []
            if 'chatbot' in st.session_state:
                st.session_state.chatbot.clear_conversation(user_id or 'guest')
            st.rerun()
    
    @staticmethod
    def _send_message(
        message: str,
        user_id: Optional[str] = None,
        user_data: Optional[Dict[str, Any]] = None
    ):
        """
        Send a message to the chatbot and get response.
        
        Args:
            message: User message
            user_id: User ID
            user_data: User data
        """
        # Add user message
        st.session_state.chat_messages.append({
            'type': 'user',
            'content': message,
            'timestamp': datetime.now().strftime('%I:%M %p')
        })
        
        # Show typing indicator
        st.session_state.is_typing = True
        
        # Get response from chatbot
        chatbot = st.session_state.chatbot
        
        if user_data:
            chatbot.set_user_data(user_data)
        
        result = chatbot.process_message(
            message=message,
            user_id=user_id or 'guest',
            user_data=user_data
        )
        
        # Remove typing indicator
        st.session_state.is_typing = False
        
        # Add bot response
        st.session_state.chat_messages.append({
            'type': 'bot',
            'content': result['message'],
            'timestamp': datetime.now().strftime('%I:%M %p'),
            'intent': result.get('intent', ''),
            'confidence': result.get('confidence', 0)
        })
        
        # Clear input
        if 'chat_input' in st.session_state:
            st.session_state.chat_input = ""
    
    @staticmethod
    def render_common_questions():
        """
        Render common questions section.
        """
        st.markdown("### 💡 Common Questions")
        
        questions = [
            "🌍 What is my carbon footprint?",
            "💡 How can I reduce my footprint?",
            "⭐ What is my Eco Score?",
            "🏆 Give me eco-challenges",
            "💧 How to save water?",
            "♻️ How to reduce waste?",
            "⚡ How to save energy?",
            "🥗 Best sustainable diet tips?"
        ]
        
        cols = st.columns(4)
        for idx, question in enumerate(questions[:8]):
            with cols[idx % 4]:
                if st.button(question, key=f"common_q_{idx}", use_container_width=True):
                    # Send the question to chat
                    user_id = st.session_state.get('user_id', 'guest')
                    ChatWidget._send_message(question, user_id)
                    st.rerun()
    
    @staticmethod
    def render_chat_analytics(user_id: Optional[str] = None):
        """
        Render chat analytics.
        
        Args:
            user_id: User ID
        """
        if 'chatbot' not in st.session_state:
            return
        
        chatbot = st.session_state.chatbot
        stats = chatbot.get_conversation_stats(user_id or 'guest')
        
        if stats.get('total_messages', 0) == 0:
            st.info("No chat history yet. Start a conversation!")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💬 Messages",
                stats.get('total_messages', 0)
            )
        
        with col2:
            st.metric(
                "🎯 Topics",
                stats.get('unique_intents', 0)
            )
        
        with col3:
            st.metric(
                "📝 Avg Words",
                stats.get('avg_words_per_message', 0)
            )
        
        with col4:
            st.metric(
                "🔥 Top Intent",
                stats.get('top_intent', 'None').replace('_', ' ').title()
            )
        
        # Intent distribution
        if stats.get('intent_distribution'):
            st.markdown("#### 📊 Intent Distribution")
            intent_data = stats['intent_distribution']
            
            # Create a simple bar chart
            max_count = max(intent_data.values()) if intent_data else 1
            for intent, count in sorted(intent_data.items(), key=lambda x: x[1], reverse=True):
                pct = (count / max_count) * 100 if max_count > 0 else 0
                st.markdown(f"""
                <div style="margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;font-size:13px;">
                        <span>{intent.replace('_', ' ').title()}</span>
                        <span>{count}</span>
                    </div>
                    <div style="width:100%;height:6px;background:#e2e8f0;border-radius:4px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:#3b82f6;border-radius:4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)