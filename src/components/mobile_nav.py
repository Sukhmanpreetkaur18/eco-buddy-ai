"""
Mobile Navigation Component for EcoBuddy AI
Provides touch-friendly navigation for mobile devices.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from src.lib.mobile_utils import MobileUtils


class MobileNav:
    """
    Mobile navigation component with bottom bar.
    """
    
    NAV_ITEMS = [
        {'id': 'home', 'label': 'Home', 'icon': '🏠', 'page': 'Dashboard'},
        {'id': 'footprint', 'label': 'Footprint', 'icon': '🌍', 'page': 'Carbon Footprint'},
        {'id': 'challenges', 'label': 'Challenges', 'icon': '🏆', 'page': 'Eco Calendar'},
        {'id': 'chatbot', 'label': 'Chat', 'icon': '🤖', 'page': 'Eco Chatbot'},
        {'id': 'profile', 'label': 'Profile', 'icon': '👤', 'page': 'Profile'}
    ]
    
    @staticmethod
    def render(active_tab: str = 'home'):
        """
        Render mobile navigation bar.
        
        Args:
            active_tab: Currently active tab ID
        """
        if not MobileUtils.is_small_screen():
            return
        
        st.markdown("""
        <style>
            .mobile-nav {
                display: flex !important;
                justify-content: space-around !important;
                position: fixed !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                background: #0f172a !important;
                padding: 6px 0 !important;
                border-top: 1px solid #334155 !important;
                z-index: 999 !important;
                box-shadow: 0 -4px 20px rgba(0,0,0,0.3) !important;
            }
            .mobile-nav-item {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                font-size: 10px !important;
                color: #94a3b8 !important;
                text-decoration: none !important;
                padding: 4px 8px !important;
                background: transparent !important;
                border: none !important;
                cursor: pointer !important;
                min-height: 50px !important;
                min-width: 50px !important;
                transition: all 0.2s !important;
                border-radius: 8px !important;
            }
            .mobile-nav-item:hover {
                background: rgba(74, 222, 128, 0.05) !important;
            }
            .mobile-nav-item.active {
                color: #4ade80 !important;
            }
            .mobile-nav-item .icon {
                font-size: 22px !important;
                line-height: 1.2 !important;
            }
            .mobile-nav-item .label {
                font-size: 9px !important;
                margin-top: 2px !important;
            }
            .mobile-nav-item .badge {
                position: absolute !important;
                top: -2px !important;
                right: -2px !important;
                background: #ef4444 !important;
                color: white !important;
                font-size: 10px !important;
                padding: 1px 6px !important;
                border-radius: 10px !important;
                min-width: 18px !important;
                text-align: center !important;
            }
            .mobile-nav-item .icon-wrapper {
                position: relative !important;
                display: inline-block !important;
            }
            
            /* Hide Streamlit sidebar on mobile */
            .css-1d391kg {
                display: none !important;
            }
            
            /* Add bottom padding for content */
            .main .block-container {
                padding-bottom: 80px !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Mobile nav HTML
        html = '<div class="mobile-nav">'
        
        for item in MobileNav.NAV_ITEMS:
            active_class = 'active' if item['id'] == active_tab else ''
            badge_html = ''
            
            # Add badge for notifications
            if item['id'] == 'chatbot' and st.session_state.get('unread_messages', 0) > 0:
                badge_html = f'<span class="badge">{st.session_state.unread_messages}</span>'
            
            html += f"""
            <button class="mobile-nav-item {active_class}" onclick="handleNavClick('{item['id']}')">
                <span class="icon-wrapper">
                    <span class="icon">{item['icon']}</span>
                    {badge_html}
                </span>
                <span class="label">{item['label']}</span>
            </button>
            """
        
        html += '</div>'
        
        st.markdown(html, unsafe_allow_html=True)
        
        # JavaScript for navigation
        st.markdown("""
        <script>
            function handleNavClick(id) {
                // Send navigation event to Streamlit
                const event = new CustomEvent('streamlit-nav', {
                    detail: { page: id }
                });
                document.dispatchEvent(event);
            }
            
            // Handle Streamlit events
            document.addEventListener('streamlit-nav', function(e) {
                // Streamlit will handle the navigation
                console.log('Navigating to:', e.detail.page);
            });
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_swipe_indicator():
        """
        Render swipe indicator for mobile.
        """
        if not MobileUtils.is_small_screen():
            return
        
        st.markdown("""
        <style>
            .swipe-indicator {
                text-align: center;
                padding: 8px;
                color: #94a3b8;
                font-size: 12px;
                margin-bottom: 16px;
            }
            .swipe-indicator .arrow {
                display: inline-block;
                animation: swipeAnim 1.5s ease-in-out infinite;
            }
            @keyframes swipeAnim {
                0%, 100% { transform: translateX(-10px); opacity: 0.5; }
                50% { transform: translateX(10px); opacity: 1; }
            }
        </style>
        <div class="swipe-indicator">
            <span class="arrow">👈</span>
            Swipe to navigate <span class="arrow">👉</span>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_bottom_sheet(title: str, content: str, is_open: bool = False):
        """
        Render a bottom sheet for mobile.
        
        Args:
            title: Sheet title
            content: Sheet content
            is_open: Whether sheet is open
        """
        if not MobileUtils.is_small_screen():
            return
        
        st.markdown(f"""
        <style>
            .bottom-sheet-overlay {{
                display: {'block' if is_open else 'none'};
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                z-index: 1000;
            }}
            .bottom-sheet {{
                position: fixed;
                bottom: {'0' if is_open else '-100%'};
                left: 0;
                right: 0;
                background: #0f172a;
                border-radius: 20px 20px 0 0;
                padding: 20px;
                z-index: 1001;
                transition: bottom 0.3s ease;
                max-height: 80vh;
                overflow-y: auto;
                border-top: 1px solid #334155;
            }}
            .bottom-sheet-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 12px;
                border-bottom: 1px solid #334155;
                margin-bottom: 12px;
            }}
            .bottom-sheet-title {{
                font-size: 18px;
                font-weight: 700;
                color: #f8fafc;
            }}
            .bottom-sheet-close {{
                background: none;
                border: none;
                color: #94a3b8;
                font-size: 24px;
                cursor: pointer;
                padding: 4px 8px;
            }}
            .bottom-sheet-content {{
                color: #e2e8f0;
                font-size: 14px;
                line-height: 1.6;
            }}
            .bottom-sheet-handle {{
                width: 40px;
                height: 4px;
                background: #334155;
                border-radius: 2px;
                margin: 0 auto 12px;
            }}
        </style>
        <div class="bottom-sheet-overlay" onclick="closeBottomSheet()"></div>
        <div class="bottom-sheet" id="bottomSheet">
            <div class="bottom-sheet-handle"></div>
            <div class="bottom-sheet-header">
                <div class="bottom-sheet-title">{title}</div>
                <button class="bottom-sheet-close" onclick="closeBottomSheet()">✕</button>
            </div>
            <div class="bottom-sheet-content">{content}</div>
        </div>
        <script>
            function closeBottomSheet() {{
                document.getElementById('bottomSheet').style.bottom = '-100%';
                document.querySelector('.bottom-sheet-overlay').style.display = 'none';
            }}
        </script>
        """, unsafe_allow_html=True)