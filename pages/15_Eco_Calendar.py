"""
Eco Calendar Page - Full page interface for the Gamified Eco Challenges Calendar
Provides calendar view, challenge management, streak tracking, and rewards.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import plotly.graph_objects as go
import plotly.express as px

from src.lib.challenge_calendar import ChallengeCalendar
from src.lib.challenge_generator import ChallengeGenerator
from src.lib.streak_tracker import StreakTracker
from src.lib.challenge_rewards import ChallengeRewards
from src.components.calendar_widget import CalendarWidget


def render_eco_calendar(user_id: str = None):
    """
    Render the Eco Calendar page.
    
    Args:
        user_id: User ID for personalized data
    """
    
    st.markdown("""
    <style>
        .calendar-header {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            padding: 24px 32px;
            border-radius: 12px;
            margin-bottom: 24px;
            border: 1px solid #334155;
        }
        .calendar-header h1 {
            color: #f8fafc;
            font-size: 28px;
            font-weight: 700;
            margin: 0;
        }
        .calendar-header p {
            color: #94a3b8;
            margin: 8px 0 0 0;
            font-size: 15px;
        }
        .calendar-header .badge {
            display: inline-block;
            background: #22c55e;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 8px;
        }
        .streak-card {
            background: white;
            padding: 16px 20px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            text-align: center;
            margin-bottom: 12px;
        }
        .streak-number {
            font-size: 36px;
            font-weight: 800;
            color: #f59e0b;
        }
        .streak-label {
            font-size: 13px;
            color: #64748b;
        }
        .reward-card {
            background: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .reward-card .icon {
            font-size: 24px;
        }
        .reward-card .name {
            font-weight: 600;
            color: #1e293b;
        }
        .reward-card .status {
            font-size: 12px;
            padding: 2px 10px;
            border-radius: 12px;
        }
        .reward-card .status.unlocked {
            background: #dcfce7;
            color: #16a34a;
        }
        .reward-card .status.locked {
            background: #f1f5f9;
            color: #94a3b8;
        }
        .challenge-card {
            background: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 8px;
            transition: all 0.2s;
        }
        .challenge-card:hover {
            border-color: #3b82f6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        .challenge-card .title {
            font-weight: 600;
            color: #1e293b;
        }
        .challenge-card .description {
            font-size: 13px;
            color: #64748b;
        }
        .challenge-card .points {
            font-size: 14px;
            font-weight: 600;
            color: #f59e0b;
        }
        .difficulty-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }
        .difficulty-badge.easy {
            background: #dcfce7;
            color: #16a34a;
        }
        .difficulty-badge.medium {
            background: #fef3c7;
            color: #d97706;
        }
        .difficulty-badge.hard {
            background: #fee2e2;
            color: #dc2626;
        }
        .difficulty-badge.very_hard {
            background: #fef2f2;
            color: #991b1b;
        }
        .tier-card {
            background: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            text-align: center;
        }
        .tier-icon {
            font-size: 32px;
        }
        .tier-name {
            font-weight: 700;
            font-size: 16px;
        }
        .tier-progress {
            margin-top: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="calendar-header">
        <h1>📅 Eco Challenges Calendar</h1>
        <p>Complete daily, weekly, and monthly challenges to earn points, build streaks, and unlock rewards!</p>
        <span class="badge">🔥 Challenges Active</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    if 'calendar_data' not in st.session_state:
        st.session_state.calendar_data = ChallengeCalendar(user_id)
    
    if 'challenge_gen' not in st.session_state:
        st.session_state.challenge_gen = ChallengeGenerator()
    
    if 'streak_tracker' not in st.session_state:
        st.session_state.streak_tracker = StreakTracker(user_id)
    
    if 'reward_manager' not in st.session_state:
        st.session_state.reward_manager = ChallengeRewards()
    
    if 'today_challenges' not in st.session_state:
        st.session_state.today_challenges = st.session_state.challenge_gen.generate_all_challenges()
    
    # Layout: Main content + Sidebar
    main_col, sidebar_col = st.columns([2, 1])
    
    with main_col:
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📅 Calendar",
            "🎯 Today's Challenges",
            "🏆 Rewards",
            "📊 Progress"
        ])
        
        with tab1:
            # Calendar widget
            year = st.session_state.get('calendar_year', datetime.now().year)
            month = st.session_state.get('calendar_month', datetime.now().month)
            
            CalendarWidget.render(
                year=year,
                month=month,
                user_id=user_id,
                show_legend=True
            )
            
            # Quick stats
            st.markdown("---")
            st.markdown("#### 📊 Monthly Overview")
            
            calendar = st.session_state.calendar_data
            stats = calendar.get_monthly_stats(year, month)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📋 Total", stats['total_challenges'])
            with col2:
                st.metric("✅ Done", stats['completed'])
            with col3:
                st.metric("📈 Rate", f"{stats['completion_rate']:.1f}%")
            with col4:
                st.metric("⭐ Points", stats['points_earned'])
        
        with tab2:
            render_today_challenges(user_id)
        
        with tab3:
            render_rewards(user_id)
        
        with tab4:
            render_progress(user_id)
    
    with sidebar_col:
        render_sidebar(user_id)


def render_today_challenges(user_id: str):
    """Render today's challenges."""
    st.markdown("#### 🎯 Today's Challenges")
    
    challenges = st.session_state.today_challenges
    
    if not challenges:
        st.info("No challenges for today. Check back tomorrow! 🌱")
        return
    
    # Show challenge categories
    daily = [c for c in challenges if c.get('type') == 'daily']
    weekly = [c for c in challenges if c.get('type') == 'weekly']
    monthly = [c for c in challenges if c.get('type') == 'monthly']
    
    if daily:
        st.markdown("##### 📅 Daily Challenges")
        for challenge in daily:
            render_challenge_card(challenge, user_id)
    
    if weekly:
        st.markdown("##### 📅 Weekly Challenges")
        for challenge in weekly:
            render_challenge_card(challenge, user_id)
    
    if monthly:
        st.markdown("##### 📅 Monthly Challenges")
        for challenge in monthly:
            render_challenge_card(challenge, user_id)
    
    # Challenge stats
    st.markdown("---")
    st.markdown("#### 📊 Challenge Stats")
    
    total = len(challenges)
    completed = 0
    total_points = sum(c.get('points', 0) for c in challenges)
    earned_points = 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Total", total)
    with col2:
        st.metric("⭐ Points", total_points)
    with col3:
        st.metric("📈 Progress", f"0%")


def render_challenge_card(challenge: Dict[str, Any], user_id: str):
    """Render a single challenge card."""
    difficulty = challenge.get('difficulty', 'easy')
    difficulty_class = difficulty.lower()
    
    col1, col2, col3 = st.columns([4, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="challenge-card">
            <div class="title">{challenge.get('title', '')}</div>
            <div class="description">{challenge.get('description', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <span class="difficulty-badge {difficulty_class}">{difficulty.title()}</span>
        <br>
        <span style="font-size:12px;color:#94a3b8;">{challenge.get('category', 'general').title()}</span>
        """, unsafe_allow_html=True)
    
    with col3:
        st.write(f"⭐ {challenge.get('points', 0)} pts")
        if st.button("✅ Complete", key=f"complete_{challenge.get('id', '')}", use_container_width=True):
            calendar = st.session_state.calendar_data
            result = calendar.complete_challenge(challenge.get('id', ''))
            if result.get('success'):
                st.success(result.get('message', 'Challenge completed! 🌟'))
                st.balloons()
                st.rerun()


def render_rewards(user_id: str):
    """Render rewards section."""
    st.markdown("#### 🏆 Your Rewards")
    
    reward_manager = st.session_state.reward_manager
    rewards = reward_manager.get_user_rewards(user_id or 'guest')
    stats = reward_manager.get_user_reward_stats(user_id or 'guest')
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏅 Total Rewards", stats['total_rewards'])
    with col2:
        st.metric("⭐ Total Points", stats['total_points'])
    with col3:
        st.metric("📊 Categories", len(stats['by_category']))
    
    st.markdown("---")
    
    # Rewards by category
    if rewards:
        for category in ['challenge', 'streak', 'milestone', 'special']:
            category_rewards = [r for r in rewards if r.category == category]
            if category_rewards:
                st.markdown(f"##### {category.title()} Rewards")
                for reward in category_rewards:
                    st.markdown(f"""
                    <div class="reward-card">
                        <div>
                            <span class="icon">{reward.icon}</span>
                            <span class="name">{reward.name}</span>
                        </div>
                        <div>
                            <span class="status unlocked">✅ Unlocked</span>
                            <span style="font-size:12px;color:#94a3b8;margin-left:8px;">⭐ {reward.points} pts</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Complete challenges to unlock rewards! 🎯")


def render_progress(user_id: str):
    """Render progress section."""
    st.markdown("#### 📊 Your Progress")
    
    streak_tracker = st.session_state.streak_tracker
    streak_info = streak_tracker.get_streak_info()
    
    # Streak stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Current", streak_info['current_streak'])
    with col2:
        st.metric("🏆 Best", streak_info['best_streak'])
    with col3:
        st.metric("👑 Tier", streak_info['tier'].title())
    with col4:
        st.metric("📅 Active", streak_info['total_days_active'])
    
    st.markdown("---")
    
    # Tier progress
    tier_progress = streak_tracker.get_tier_progress()
    st.markdown("#### 👑 Tier Progress")
    
    progress_pct = tier_progress.get('progress', 0)
    current_tier = tier_progress.get('current_tier', 'bronze')
    next_tier = tier_progress.get('next_tier')
    
    st.markdown(f"""
    <div class="tier-card">
        <div class="tier-icon">{streak_tracker.TIERS[current_tier]['icon']}</div>
        <div class="tier-name" style="color:{streak_tracker.TIERS[current_tier]['color']}">
            {current_tier.title()}
        </div>
        <div class="tier-progress">
            <div style="display:flex;justify-content:space-between;font-size:13px;color:#64748b;">
                <span>Current</span>
                <span>{'Next: ' + next_tier.title() if next_tier else 'Max Level!'}</span>
            </div>
            <div style="width:100%;height:8px;background:#e2e8f0;border-radius:4px;overflow:hidden;margin-top:4px;">
                <div style="width:{progress_pct}%;height:100%;background:linear-gradient(90deg,#3b82f6,#22c55e);border-radius:4px;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12px;color:#94a3b8;margin-top:4px;">
                <span>{streak_tracker.TIERS[current_tier]['min_streak']} days</span>
                <span>{streak_tracker.TIERS[next_tier]['min_streak'] if next_tier else '∞'} days</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Milestones progress
    st.markdown("#### 🎯 Milestones")
    milestones = streak_tracker.get_milestones_progress()
    
    for milestone in milestones[:5]:
        achieved = milestone['achieved']
        progress = milestone['progress']
        
        st.markdown(f"""
        <div style="margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;font-size:13px;">
                <span>{'✅' if achieved else '🎯'} {milestone['name']}</span>
                <span style="color:#f59e0b;">⭐ {milestone['points']} pts</span>
            </div>
            <div style="width:100%;height:6px;background:#e2e8f0;border-radius:4px;overflow:hidden;">
                <div style="width:{progress}%;height:100%;background:{'#22c55e' if achieved else '#3b82f6'};border-radius:4px;"></div>
            </div>
            <div style="font-size:11px;color:#94a3b8;text-align:right;">
                {milestone['badge']} {progress:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar(user_id: str):
    """Render sidebar with streak and quick actions."""
    
    st.markdown("### 🔥 Your Streak")
    
    streak_tracker = st.session_state.streak_tracker
    streak_info = streak_tracker.get_streak_info()
    
    st.markdown(f"""
    <div class="streak-card">
        <div class="streak-number">{streak_info['current_streak']}</div>
        <div class="streak-label">🔥 Day Streak</div>
        <div style="margin-top:4px;">
            <span style="font-size:13px;color:#f59e0b;">{streak_info['tier'].title()}</span>
            <span style="font-size:12px;color:#94a3b8;margin-left:8px;">
                🏆 Best: {streak_info['best_streak']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🎯 Generate New Challenges", use_container_width=True):
        st.session_state.today_challenges = st.session_state.challenge_gen.generate_all_challenges()
        st.success("New challenges generated! 🎉")
        st.rerun()
    
    if st.button("📊 View Full History", use_container_width=True):
        st.session_state.show_history = not st.session_state.get('show_history', False)
    
    st.markdown("---")
    
    # Challenge stats
    st.markdown("### 📊 Challenge Stats")
    
    calendar = st.session_state.calendar_data
    today = date.today()
    month_data = calendar.get_month(today.year, today.month)
    
    st.markdown(f"""
    <div style="background:#f8fafc;padding:12px 16px;border-radius:8px;margin-bottom:8px;">
        <div style="display:flex;justify-content:space-between;font-size:13px;">
            <span>📋 Total Challenges</span>
            <span><strong>{month_data.total_challenges}</strong></span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;">
            <span>✅ Completed</span>
            <span><strong>{month_data.completed_challenges}</strong></span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;">
            <span>📈 Completion Rate</span>
            <span><strong>{month_data.get_completion_rate():.1f}%</strong></span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;">
            <span>⭐ Points Earned</span>
            <span><strong>{month_data.earned_points}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upcoming challenges
    st.markdown("### 📅 Upcoming")
    upcoming = calendar.get_upcoming_challenges(3)
    
    if upcoming:
        for challenge in upcoming[:3]:
            st.markdown(f"""
            <div style="background:#f8fafc;padding:8px 12px;border-radius:6px;margin-bottom:4px;font-size:13px;">
                <div>{challenge.get('title', '')}</div>
                <div style="font-size:11px;color:#94a3b8;">
                    📅 {challenge.get('date', '')} • ⭐ {challenge.get('points', 0)} pts
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No upcoming challenges")