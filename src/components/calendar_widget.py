"""
Calendar Widget for EcoBuddy AI
Displays an interactive calendar with challenge markers.
"""

import streamlit as st
from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional
import calendar
import pandas as pd

from src.lib.challenge_calendar import ChallengeCalendar


class CalendarWidget:
    """
    Interactive calendar widget for displaying eco-challenges.
    """

    @staticmethod
    def render(
        year: int = None,
        month: int = None,
        user_id: str = None,
        show_legend: bool = True,
        height: int = 500
    ):
        """
        Render the calendar widget.
        
        Args:
            year: Year to display
            month: Month to display (1-12)
            user_id: User ID for personalized data
            show_legend: Show legend
            height: Height of the calendar
        """
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month

        # Initialize calendar
        calendar_obj = ChallengeCalendar(user_id)
        month_data = calendar_obj.get_month(year, month)
        today = date.today()

        # Navigation
        col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
        
        with col1:
            if st.button("◀️", key="prev_month"):
                if month == 1:
                    year -= 1
                    month = 12
                else:
                    month -= 1
                st.session_state['calendar_month'] = month
                st.session_state['calendar_year'] = year
                st.rerun()
        
        with col2:
            st.write(f"**{calendar.month_name[month]} {year}**")
        
        with col3:
            if st.button("▶️", key="next_month"):
                if month == 12:
                    year += 1
                    month = 1
                else:
                    month += 1
                st.session_state['calendar_month'] = month
                st.session_state['calendar_year'] = year
                st.rerun()
        
        with col4:
            if st.button("📅 Today", key="today_btn", use_container_width=True):
                st.session_state['calendar_month'] = datetime.now().month
                st.session_state['calendar_year'] = datetime.now().year
                st.rerun()

        # Calendar grid
        days = calendar_obj.get_month(year, month)
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        # Create HTML for calendar
        html = f"""
        <style>
            .calendar-grid {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 2px;
                background: #f1f5f9;
                padding: 4px;
                border-radius: 8px;
            }}
            .calendar-header {{
                background: #e2e8f0;
                padding: 8px;
                text-align: center;
                font-weight: 600;
                font-size: 12px;
                color: #475569;
                border-radius: 4px;
            }}
            .calendar-day {{
                background: white;
                padding: 6px;
                text-align: center;
                min-height: 60px;
                border-radius: 4px;
                transition: all 0.2s;
                cursor: pointer;
                position: relative;
            }}
            .calendar-day:hover {{
                transform: scale(1.02);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .calendar-day.today {{
                border: 2px solid #3b82f6;
                background: #eff6ff;
            }}
            .calendar-day.completed {{
                background: #dcfce7;
                border: 1px solid #22c55e;
            }}
            .calendar-day.partial {{
                background: #fef3c7;
                border: 1px solid #f59e0b;
            }}
            .calendar-day.empty {{
                background: transparent;
                min-height: 0;
                padding: 0;
            }}
            .day-number {{
                font-size: 14px;
                font-weight: 600;
                color: #1e293b;
                text-align: left;
                margin-bottom: 2px;
            }}
            .day-dot {{
                display: inline-block;
                width: 6px;
                height: 6px;
                border-radius: 50%;
                margin: 1px;
            }}
            .day-dot.completed {{
                background: #22c55e;
            }}
            .day-dot.incomplete {{
                background: #94a3b8;
            }}
            .day-dot.active {{
                background: #3b82f6;
                animation: pulse 1.5s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.2); }}
            }}
            .day-streak {{
                font-size: 10px;
                color: #f59e0b;
                font-weight: 600;
                position: absolute;
                bottom: 2px;
                right: 4px;
            }}
            .day-badge {{
                font-size: 10px;
                position: absolute;
                top: 2px;
                right: 4px;
            }}
        </style>
        <div class="calendar-grid">
        """

        # Headers
        for weekday in weekdays:
            html += f'<div class="calendar-header">{weekday}</div>'

        # Days
        first_day = date(year, month, 1)
        first_weekday = first_day.weekday()
        days_in_month = calendar.monthrange(year, month)[1]

        # Empty cells before first day
        for _ in range(first_weekday):
            html += '<div class="calendar-day empty"></div>'

        for day_num in range(1, days_in_month + 1):
            current_date = date(year, month, day_num)
            is_today = current_date == today
            is_past = current_date < today

            # Find day data
            day_data = next((d for d in days if d.date == current_date), None)
            
            if day_data:
                completion_pct = day_data.get_completion_percentage()
                is_completed = day_data.is_completed()
                has_challenges = day_data.total_challenges > 0
                streak = day_data.streak

                # Determine class
                if is_today:
                    day_class = "calendar-day today"
                elif is_completed:
                    day_class = "calendar-day completed"
                elif completion_pct > 0:
                    day_class = "calendar-day partial"
                else:
                    day_class = "calendar-day"

                # Build day HTML
                html += f'<div class="{day_class}" onclick="handleDayClick({year},{month},{day_num})">'
                html += f'<div class="day-number">{day_num}</div>'

                # Show challenge dots
                if has_challenges:
                    for i in range(min(day_data.total_challenges, 3)):
                        if i < day_data.completion_count:
                            html += f'<span class="day-dot completed"></span>'
                        else:
                            html += f'<span class="day-dot incomplete"></span>'

                # Show streak
                if streak > 0:
                    html += f'<span class="day-streak">🔥{streak}</span>'

                # Show badges
                if day_data.badges:
                    html += f'<span class="day-badge">🏅</span>'

                html += '</div>'
            else:
                html += f'<div class="calendar-day"><div class="day-number">{day_num}</div></div>'

        html += '</div>'

        # Legend
        if show_legend:
            html += """
            <div style="display:flex; gap: 16px; margin-top: 12px; flex-wrap: wrap; padding: 8px;">
                <div style="display:flex; align-items:center; gap:4px;">
                    <span style="display:inline-block; width:12px; height:12px; background:#22c55e; border-radius:4px;"></span>
                    <span style="font-size:12px; color:#475569;">Completed</span>
                </div>
                <div style="display:flex; align-items:center; gap:4px;">
                    <span style="display:inline-block; width:12px; height:12px; background:#fef3c7; border-radius:4px; border:1px solid #f59e0b;"></span>
                    <span style="font-size:12px; color:#475569;">Partial</span>
                </div>
                <div style="display:flex; align-items:center; gap:4px;">
                    <span style="display:inline-block; width:12px; height:12px; background:#eff6ff; border-radius:4px; border:2px solid #3b82f6;"></span>
                    <span style="font-size:12px; color:#475569;">Today</span>
                </div>
                <div style="display:flex; align-items:center; gap:4px;">
                    <span style="display:inline-block; width:6px; height:6px; background:#22c55e; border-radius:50%;"></span>
                    <span style="font-size:12px; color:#475569;">Challenge completed</span>
                </div>
                <div style="display:flex; align-items:center; gap:4px;">
                    <span style="display:inline-block; width:6px; height:6px; background:#94a3b8; border-radius:50%;"></span>
                    <span style="font-size:12px; color:#475569;">Challenge pending</span>
                </div>
                <div style="display:flex; align-items:center; gap:4px;">
                    <span style="font-size:14px;">🔥</span>
                    <span style="font-size:12px; color:#475569;">Streak day</span>
                </div>
            </div>
            """

        st.markdown(html, unsafe_allow_html=True)

        # Monthly stats
        stats = calendar_obj.get_monthly_stats(year, month)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("✅ Completed", f"{stats['completed']}/{stats['total_challenges']}")
        
        with col2:
            st.metric("📊 Rate", f"{stats['completion_rate']:.1f}%")
        
        with col3:
            st.metric("⭐ Points", stats['points_earned'])
        
        with col4:
            st.metric("🔥 Streak", stats['streak'])
        
        with col5:
            st.metric("🏅 Best", stats['best_streak'])

    @staticmethod
    def render_day_details(day_data: Dict[str, Any]):
        """Render details for a specific day."""
        if not day_data:
            st.info("No challenges for this day")
            return

        challenges = day_data.get('challenges', [])
        if not challenges:
            st.info("No challenges for this day")
            return

        st.markdown(f"#### 📅 Challenges for {day_data['date']}")
        
        for challenge in challenges:
            is_completed = challenge.get('completed', False)
            status = "✅" if is_completed else "⏳"
            
            with st.container():
                col1, col2, col3 = st.columns([4, 2, 1])
                with col1:
                    st.write(f"{status} {challenge.get('title', '')}")
                with col2:
                    difficulty = challenge.get('difficulty', 'easy')
                    colors = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴', 'very_hard': '🔴'}
                    st.write(f"Difficulty: {colors.get(difficulty, '🟢')}")
                with col3:
                    st.write(f"⭐ {challenge.get('points', 0)} pts")