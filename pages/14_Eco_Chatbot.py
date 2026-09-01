"""
Eco Chatbot Page - Full page interface for the AI Eco-Chatbot
Provides a complete chat experience with settings, analytics, and history.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import time
import json

from src.components.chat_widget import ChatWidget
from src.ai.eco_chatbot import EcoChatbot


def render_eco_chatbot(user_id: str = None):
    """
    Render the Eco Chatbot page.
    
    Args:
        user_id: User ID for the chat session
    """
    
    # Custom CSS
    st.markdown("""
    <style>
        .chat-header {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            padding: 24px 32px;
            border-radius: 12px;
            margin-bottom: 24px;
            border: 1px solid #334155;
        }
        .chat-header h1 {
            color: #f8fafc;
            font-size: 28px;
            font-weight: 700;
            margin: 0;
        }
        .chat-header p {
            color: #94a3b8;
            margin: 8px 0 0 0;
            font-size: 15px;
        }
        .chat-header .badge {
            display: inline-block;
            background: #22c55e;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 8px;
        }
        .stat-card {
            background: white;
            padding: 16px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
        }
        .stat-label {
            font-size: 13px;
            color: #64748b;
        }
        .settings-section {
            background: white;
            padding: 16px 20px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            margin-bottom: 16px;
        }
        .settings-section h4 {
            color: #1e293b;
            margin: 0 0 8px 0;
            font-size: 15px;
        }
        .settings-section p {
            color: #64748b;
            font-size: 13px;
            margin: 0;
        }
        .history-item {
            padding: 10px 14px;
            background: #f8fafc;
            border-radius: 8px;
            margin-bottom: 6px;
            border-left: 3px solid #3b82f6;
        }
        .history-item .msg {
            font-size: 14px;
            color: #1e293b;
        }
        .history-item .time {
            font-size: 11px;
            color: #94a3b8;
        }
        .history-item .intent {
            font-size: 11px;
            color: #3b82f6;
            background: #dbeafe;
            padding: 2px 8px;
            border-radius: 10px;
        }
        .chat-tabs .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
        }
        .chat-tabs .stTabs [data-baseweb="tab"] {
            padding: 6px 12px;
            font-size: 13px;
        }
        .message-count-badge {
            display: inline-block;
            background: #3b82f6;
            color: white;
            border-radius: 50%;
            padding: 2px 8px;
            font-size: 11px;
            margin-left: 6px;
        }
        .quick-action-btn {
            width: 100%;
            text-align: left;
            padding: 8px 12px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            margin-bottom: 4px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 13px;
        }
        .quick-action-btn:hover {
            background: #dbeafe;
            border-color: #3b82f6;
        }
        .feedback-section {
            background: #f1f5f9;
            padding: 12px 16px;
            border-radius: 8px;
            margin-top: 12px;
        }
        .feedback-section .stars {
            display: flex;
            gap: 4px;
            font-size: 24px;
        }
        .feedback-section .stars span {
            cursor: pointer;
            transition: transform 0.2s;
        }
        .feedback-section .stars span:hover {
            transform: scale(1.2);
        }
        .feedback-section .stars .active {
            color: #f59e0b;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="chat-header">
        <h1>🤖 EcoBuddy AI Assistant</h1>
        <p>Your personal AI-powered sustainability coach. Ask me anything about reducing your carbon footprint, living sustainably, and making eco-friendly choices!</p>
        <span class="badge">🟢 Online</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = EcoChatbot()
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    if 'chat_settings' not in st.session_state:
        st.session_state.chat_settings = {
            'show_timestamp': True,
            'show_intent': False,
            'auto_scroll': True,
            'dark_mode': False,
            'font_size': 'medium'
        }
    
    if 'chat_feedback' not in st.session_state:
        st.session_state.chat_feedback = None
    
    if 'chat_rating' not in st.session_state:
        st.session_state.chat_rating = 0
    
    # Layout: Main chat + Sidebar
    chat_col, sidebar_col = st.columns([2, 1])
    
    with chat_col:
        # Chat widget with tabs
        tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Analytics", "ℹ️ About"])
        
        with tab1:
            ChatWidget.render(
                user_id=user_id,
                user_data=st.session_state.get('user_data', {}),
                placeholder="Ask me about sustainability, carbon footprint, or eco-tips...",
                height=450
            )
            
            st.markdown("---")
            
            # Common questions
            ChatWidget.render_common_questions()
        
        with tab2:
            render_chat_analytics(user_id)
        
        with tab3:
            render_chat_about()
    
    with sidebar_col:
        render_chat_sidebar(user_id)


def render_chat_analytics(user_id: str = None):
    """Render chat analytics tab."""
    
    st.markdown("### 📊 Chat Analytics")
    
    chatbot = st.session_state.chatbot
    stats = chatbot.get_conversation_stats(user_id or 'guest')
    summary = chatbot.get_conversation_summary(user_id or 'guest')
    
    if stats.get('total_messages', 0) == 0:
        st.info("No data yet. Start a conversation to see analytics!")
        return
    
    # Stats grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💬 Messages", stats.get('total_messages', 0))
    
    with col2:
        st.metric("🎯 Topics", stats.get('unique_intents', 0))
    
    with col3:
        st.metric("📝 Avg Words", stats.get('avg_words_per_message', 0))
    
    with col4:
        st.metric("📄 Avg Response", stats.get('avg_response_length', 0))
    
    st.markdown("---")
    
    # Intent distribution chart
    intent_data = stats.get('intent_distribution', {})
    
    if intent_data:
        st.markdown("#### 🎯 Intent Distribution")
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(intent_data.keys()),
                y=list(intent_data.values()),
                marker_color='#3b82f6',
                text=list(intent_data.values()),
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Intent",
            yaxis_title="Count",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed intent breakdown
        with st.expander("📋 Detailed Intent Breakdown"):
            df = pd.DataFrame({
                'Intent': list(intent_data.keys()),
                'Count': list(intent_data.values())
            }).sort_values('Count', ascending=False)
            
            df['Intent'] = df['Intent'].str.replace('_', ' ').str.title()
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Conversation timeline
    messages = st.session_state.chat_messages
    if messages:
        st.markdown("#### 📈 Message Timeline")
        
        # Create timeline data
        timeline_data = []
        for i, msg in enumerate(messages):
            timeline_data.append({
                'Index': i + 1,
                'Type': 'User' if msg['type'] == 'user' else 'Bot',
                'Length': len(msg['content'])
            })
        
        df_timeline = pd.DataFrame(timeline_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_timeline['Index'],
            y=df_timeline['Length'],
            mode='lines+markers',
            name='Message Length',
            marker=dict(
                color=[ '#3b82f6' if t == 'User' else '#22c55e' for t in df_timeline['Type'] ],
                size=10
            ),
            line=dict(color='#94a3b8', width=1)
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Message #",
            yaxis_title="Length (characters)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_chat_about():
    """Render about tab."""
    
    st.markdown("""
    ### 🤖 About EcoBuddy AI Assistant
    
    **EcoBuddy AI Assistant** is your personal AI-powered sustainability coach designed to help you:
    
    🌍 **Track Your Carbon Footprint** - Get personalized insights about your environmental impact
    
    💡 **Get Eco Tips** - Receive practical tips to reduce your carbon footprint
    
    🏆 **Take Challenges** - Participate in daily eco-challenges to build sustainable habits
    
    📊 **Monitor Progress** - Track your sustainability journey over time
    
    ### 🔍 How It Works
    
    1. **Ask a Question** - Type your question about sustainability
    2. **AI Understanding** - The AI analyzes your question and intent
    3. **Personalized Response** - Get tailored advice based on your profile
    4. **Follow-up** - Continue the conversation with suggested topics
    
    ### 🎯 What You Can Ask
    
    - "What is my carbon footprint?"
    - "How can I reduce my footprint?"
    - "Give me eco-tips"
    - "What challenges are available?"
    - "How to save water?"
    - "How to reduce waste?"
    - "How to save energy?"
    
    ### 🔒 Privacy
    
    Your conversations are private and only used to provide better recommendations.
    
    ### 📞 Feedback
    
    Your feedback helps improve the assistant. Use the rating system in the sidebar!
    """, unsafe_allow_html=True)


def render_chat_sidebar(user_id: str = None):
    """Render chat sidebar with settings and stats."""
    
    st.markdown("### ⚙️ Settings")
    
    with st.expander("Chat Settings", expanded=True):
        show_timestamp = st.checkbox(
            "Show timestamps",
            value=st.session_state.chat_settings['show_timestamp'],
            key="chat_show_timestamp"
        )
        show_intent = st.checkbox(
            "Show intent detection",
            value=st.session_state.chat_settings['show_intent'],
            key="chat_show_intent"
        )
        auto_scroll = st.checkbox(
            "Auto-scroll to new messages",
            value=st.session_state.chat_settings['auto_scroll'],
            key="chat_auto_scroll"
        )
        
        font_size = st.selectbox(
            "Font Size",
            options=["small", "medium", "large"],
            index=["small", "medium", "large"].index(st.session_state.chat_settings['font_size']),
            key="chat_font_size"
        )
        
        st.session_state.chat_settings['show_timestamp'] = show_timestamp
        st.session_state.chat_settings['show_intent'] = show_intent
        st.session_state.chat_settings['auto_scroll'] = auto_scroll
        st.session_state.chat_settings['font_size'] = font_size
    
    st.markdown("---")
    
    # Chat Stats
    st.markdown("### 📊 Chat Stats")
    
    chatbot = st.session_state.chatbot
    stats = chatbot.get_conversation_stats(user_id or 'guest')
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('total_messages', 0)}</div>
            <div class="stat-label">💬 Messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('unique_intents', 0)}</div>
            <div class="stat-label">🎯 Topics</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('avg_words_per_message', 0)}</div>
            <div class="stat-label">📝 Avg Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('avg_response_length', 0)}</div>
            <div class="stat-label">📄 Avg Response</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Intent Distribution
    st.markdown("### 🎯 Topic Distribution")
    intent_data = stats.get('intent_distribution', {})
    
    if intent_data:
        max_count = max(intent_data.values()) if intent_data else 1
        for intent, count in sorted(intent_data.items(), key=lambda x: x[1], reverse=True)[:5]:
            pct = (count / max_count) * 100 if max_count > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:4px;">
                <div style="display:flex;justify-content:space-between;font-size:12px;">
                    <span>{intent.replace('_', ' ').title()}</span>
                    <span>{count}</span>
                </div>
                <div style="width:100%;height:4px;background:#e2e8f0;border-radius:4px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:#3b82f6;border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No data yet. Start a conversation!")
    
    st.markdown("---")
    
    # Engagement Score
    st.markdown("### 🔥 Engagement Score")
    engagement = chatbot.get_engagement_score(user_id or 'guest')
    
    st.markdown(f"""
    <div style="text-align:center;padding:10px 0;">
        <div style="position:relative;display:inline-block;">
            <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" fill="none" stroke="#e2e8f0" stroke-width="10"/>
                <circle cx="60" cy="60" r="50" fill="none" stroke="#3b82f6" stroke-width="10" 
                    stroke-dasharray="{engagement * 314} 314" stroke-dashoffset="0" 
                    transform="rotate(-90 60 60)" stroke-linecap="round"/>
                <text x="60" y="68" text-anchor="middle" font-size="24" font-weight="700" fill="#1e293b">
                    {int(engagement * 100)}%
                </text>
            </svg>
        </div>
        <p style="font-size:13px;color:#64748b;margin-top:4px;">User Engagement Score</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.chatbot.clear_conversation(user_id or 'guest')
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.chatbot.reset_chatbot()
            st.session_state.chat_messages = []
            st.success("Chatbot reset successfully!")
            st.rerun()
    
    if st.button("📥 Export Chat", use_container_width=True):
        export_data = []
        for msg in st.session_state.chat_messages:
            export_data.append({
                'type': msg['type'],
                'content': msg['content'],
                'timestamp': msg.get('timestamp', '')
            })
        
        if export_data:
            df = pd.DataFrame(export_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Feedback
    st.markdown("### 💬 Feedback")
    
    st.markdown("""
    <div class="feedback-section">
        <p style="font-size:13px;margin-bottom:8px;">How was your experience?</p>
        <div class="stars">
            <span onclick="setRating(1)">⭐</span>
            <span onclick="setRating(2)">⭐</span>
            <span onclick="setRating(3)">⭐</span>
            <span onclick="setRating(4)">⭐</span>
            <span onclick="setRating(5)">⭐</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    rating = st.select_slider(
        "Rate your experience",
        options=[1, 2, 3, 4, 5],
        value=3,
        key="chat_rating_slider"
    )
    
    feedback_text = st.text_area("Any feedback?", placeholder="Share your thoughts...", key="chat_feedback_text")
    
    if st.button("Submit Feedback", use_container_width=True):
        if st.session_state.chatbot:
            st.session_state.chatbot.handle_feedback(
                user_id or 'guest',
                feedback_text,
                rating
            )
        st.success("Thank you for your feedback! 🙏")
        st.rerun()
    
    # Chat history expandable section
    with st.expander("📜 Chat History", expanded=False):
        messages = st.session_state.chat_messages
        
        if messages:
            for msg in messages[-20:]:  # Show last 20 messages
                msg_type = "🤖 Bot" if msg['type'] == 'bot' else "👤 You"
                st.markdown(f"""
                <div class="history-item">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span class="msg">{msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}</span>
                        <span class="intent">{msg_type}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-top:4px;">
                        <span class="time">{msg.get('timestamp', '')}</span>
                        {f'<span class="intent">{msg.get("intent", "")}</span>' if msg.get('intent') else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No chat history yet. Start a conversation with EcoBuddy!")
    
    # Footer
    st.markdown("""
    <div style="margin-top: 16px; padding: 12px; text-align: center; color: #94a3b8; font-size: 12px; border-top: 1px solid #e2e8f0;">
        <p>🌱 EcoBuddy AI Assistant v2.0</p>
        <p style="font-size: 10px;">Powered by AI • Your personal sustainability coach</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main entry point for the Eco Chatbot page."""
    user_id = st.session_state.get('user_id')
    render_eco_chatbot(user_id)


if __name__ == "__main__":
    main()