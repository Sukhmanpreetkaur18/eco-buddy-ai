"""
Mobile Dashboard Page - Optimized mobile view for EcoBuddy AI
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go

from src.lib.mobile_utils import MobileUtils
from src.components.mobile_nav import MobileNav
from src.components.responsive_layout import ResponsiveLayout


def render_mobile_dashboard(user_id: str = None):
    """
    Render the mobile-optimized dashboard.
    
    Args:
        user_id: User ID for personalized data
    """
    
    # Apply mobile CSS
    st.markdown(MobileUtils.get_mobile_css(), unsafe_allow_html=True)
    st.markdown(ResponsiveLayout.get_responsive_font_css(), unsafe_allow_html=True)
    
    # Check if mobile
    is_mobile = MobileUtils.is_small_screen()
    
    # Header
    st.markdown("""
    <style>
        .mobile-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(74, 222, 128, 0.15);
            margin-bottom: 16px;
        }
        .mobile-header .title {
            font-size: 20px;
            font-weight: 700;
            color: #4ade80;
        }
        .mobile-header .subtitle {
            font-size: 12px;
            color: #94a3b8;
        }
        .mobile-header .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(74, 222, 128, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            border: 1px solid rgba(74, 222, 128, 0.2);
        }
        .quick-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-bottom: 16px;
        }
        .quick-stat {
            background: rgba(15, 23, 42, 0.6);
            padding: 12px;
            border-radius: 10px;
            border: 1px solid rgba(74, 222, 128, 0.1);
            text-align: center;
        }
        .quick-stat .value {
            font-size: 20px;
            font-weight: 700;
            color: #4ade80;
        }
        .quick-stat .label {
            font-size: 11px;
            color: #94a3b8;
        }
        .section-title {
            font-size: 16px;
            font-weight: 600;
            color: #e2e8f0;
            margin: 12px 0 8px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Mobile Header
    st.markdown("""
    <div class="mobile-header">
        <div>
            <div class="title">🌱 EcoBuddy AI</div>
            <div class="subtitle">Your Sustainability Assistant</div>
        </div>
        <div class="avatar">👤</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown('<div class="quick-stats">', unsafe_allow_html=True)
    
    # Get stats (mock data for demo)
    stats = [
        {'label': '🌍 Footprint', 'value': '2.4t'},
        {'label': '⭐ Eco Score', 'value': '78'},
        {'label': '🔥 Streak', 'value': '12d'},
        {'label': '🏆 Challenges', 'value': '8'}
    ]
    
    for stat in stats:
        st.markdown(f"""
        <div class="quick-stat">
            <div class="value">{stat['value']}</div>
            <div class="label">{stat['label']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for mobile
    if is_mobile:
        # Use dropdown for mobile
        tab_options = ['📊 Overview', '🌍 Footprint', '🏆 Challenges', '🤖 Chat']
        selected_tab = st.selectbox('', tab_options, index=0, label_visibility='collapsed')
        
        if selected_tab == '📊 Overview':
            render_mobile_overview()
        elif selected_tab == '🌍 Footprint':
            render_mobile_footprint()
        elif selected_tab == '🏆 Challenges':
            render_mobile_challenges()
        elif selected_tab == '🤖 Chat':
            render_mobile_chat()
    else:
        # Use tabs for desktop
        tab1, tab2, tab3, tab4 = st.tabs(['📊 Overview', '🌍 Footprint', '🏆 Challenges', '🤖 Chat'])
        
        with tab1:
            render_mobile_overview()
        with tab2:
            render_mobile_footprint()
        with tab3:
            render_mobile_challenges()
        with tab4:
            render_mobile_chat()
    
    # Mobile navigation (only on mobile)
    if is_mobile:
        MobileNav.render(active_tab='home')
        st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)  # Bottom padding for nav


def render_mobile_overview():
    """Render mobile overview section."""
    st.markdown('<div class="section-title">📊 Weekly Progress</div>', unsafe_allow_html=True)
    
    # Sample weekly data
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    values = [65, 72, 68, 80, 75, 85, 90]
    
    fig = go.Figure(data=[
        go.Bar(
            x=days,
            y=values,
            marker_color='#4ade80',
            text=values,
            textposition='auto',
            textfont={'color': 'white'}
        )
    ])
    
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        showlegend=False
    )
    
    ResponsiveLayout.responsive_chart(fig, height=250)
    
    # Recent activity
    st.markdown('<div class="section-title">🕐 Recent Activity</div>', unsafe_allow_html=True)
    
    activities = [
        {'icon': '✅', 'text': 'Completed daily challenge', 'time': '2h ago'},
        {'icon': '🌍', 'text': 'Carbon footprint updated', 'time': '5h ago'},
        {'icon': '⭐', 'text': 'Eco Score improved to 78', 'time': '1d ago'}
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);">
            <div>
                <span style="margin-right:8px;">{activity['icon']}</span>
                <span style="color:#e2e8f0;font-size:14px;">{activity['text']}</span>
            </div>
            <span style="color:#64748b;font-size:12px;">{activity['time']}</span>
        </div>
        """, unsafe_allow_html=True)


def render_mobile_footprint():
    """Render mobile footprint section."""
    st.markdown('<div class="section-title">🌍 Carbon Footprint</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6);padding:16px;border-radius:10px;text-align:center;border:1px solid rgba(74,222,128,0.1);">
            <div style="font-size:28px;font-weight:700;color:#4ade80;">2.4</div>
            <div style="font-size:12px;color:#94a3b8;">tons CO₂/year</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6);padding:16px;border-radius:10px;text-align:center;border:1px solid rgba(74,222,128,0.1);">
            <div style="font-size:28px;font-weight:700;color:#fbbf24;">-15%</div>
            <div style="font-size:12px;color:#94a3b8;">vs last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📊 Breakdown</div>', unsafe_allow_html=True)
    
    # Breakdown chart
    categories = ['Transport', 'Energy', 'Diet', 'Waste']
    values = [35, 30, 20, 15]
    colors = ['#4ade80', '#fbbf24', '#60a5fa', '#f87171']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=categories,
            values=values,
            marker=dict(colors=colors),
            hole=0.6,
            textinfo='label+percent',
            textfont=dict(size=12, color='white')
        )
    ])
    
    fig.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    ResponsiveLayout.responsive_chart(fig, height=280)


def render_mobile_challenges():
    """Render mobile challenges section."""
    st.markdown('<div class="section-title">🏆 Today\'s Challenges</div>', unsafe_allow_html=True)
    
    challenges = [
        {'title': '🚶 Walk 15 minutes', 'points': 10, 'status': 'pending'},
        {'title': '♻️ Recycle waste', 'points': 15, 'status': 'completed'},
        {'title': '💡 Turn off lights', 'points': 10, 'status': 'pending'}
    ]
    
    for challenge in challenges:
        status_icon = '✅' if challenge['status'] == 'completed' else '⏳'
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:rgba(15,23,42,0.6);border-radius:8px;border:1px solid {'rgba(74,222,128,0.2)' if challenge['status'] == 'completed' else 'rgba(74,222,128,0.05)'};margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span>{challenge['title']}</span>
            </div>
            <div style="display:flex;align-items:center;gap:6px;">
                <span style="color:#fbbf24;font-size:13px;">⭐{challenge['points']}</span>
                <span style="font-size:16px;">{status_icon}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🎯 Get More Challenges", use_container_width=True):
        st.success("New challenges generated! 🌱")


def render_mobile_chat():
    """Render mobile chat section."""
    st.markdown('<div class="section-title">🤖 Quick Chat</div>', unsafe_allow_html=True)
    
    # Quick chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        message = st.text_input("", placeholder="Ask EcoBuddy...", label_visibility="collapsed")
    with col2:
        if st.button("Send", use_container_width=True):
            st.success("🌱 🌍 What would you like to know about sustainability?")
    
    # Quick actions
    st.markdown('<div class="section-title">💡 Quick Actions</div>', unsafe_allow_html=True)
    
    actions = [
        {'icon': '🌍', 'label': 'My Footprint'},
        {'icon': '⭐', 'label': 'Eco Score'},
        {'icon': '💡', 'label': 'Get Tips'},
        {'icon': '🔥', 'label': 'Daily Challenge'}
    ]
    
    cols = st.columns(4)
    for i, action in enumerate(actions):
        with cols[i]:
            if st.button(f"{action['icon']}\n{action['label']}", use_container_width=True):
                st.info(f"Loading {action['label']}...")