"""
Mobile Utilities for EcoBuddy AI
Provides device detection, responsive helpers, and mobile-specific functions.
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple
import re
import json
from datetime import datetime


class MobileUtils:
    """
    Utility class for mobile detection and responsive design.
    """
    
    @staticmethod
    def is_mobile() -> bool:
        """
        Detect if the user is on a mobile device.
        
        Returns:
            True if mobile device, False otherwise
        """
        user_agent = st.session_state.get('user_agent', '')
        
        if not user_agent:
            return False
        
        # Common mobile user agent patterns
        mobile_patterns = [
            r'android',
            r'iphone',
            r'ipad',
            r'ipod',
            r'blackberry',
            r'windows phone',
            r'opera mini',
            r'mobile',
            r'tablet'
        ]
        
        user_agent_lower = user_agent.lower()
        for pattern in mobile_patterns:
            if re.search(pattern, user_agent_lower):
                return True
        
        return False
    
    @staticmethod
    def get_device_type() -> str:
        """
        Get the device type.
        
        Returns:
            Device type: 'mobile', 'tablet', 'desktop'
        """
        user_agent = st.session_state.get('user_agent', '').lower()
        
        if not user_agent:
            return 'desktop'
        
        if 'tablet' in user_agent or 'ipad' in user_agent:
            return 'tablet'
        
        if MobileUtils.is_mobile():
            return 'mobile'
        
        return 'desktop'
    
    @staticmethod
    def get_screen_size() -> Dict[str, int]:
        """
        Get screen size from session or default.
        
        Returns:
            Dictionary with width and height
        """
        return {
            'width': st.session_state.get('screen_width', 1200),
            'height': st.session_state.get('screen_height', 800)
        }
    
    @staticmethod
    def is_small_screen() -> bool:
        """
        Check if screen is small (mobile).
        
        Returns:
            True if small screen
        """
        screen = MobileUtils.get_screen_size()
        return screen['width'] < 768
    
    @staticmethod
    def is_medium_screen() -> bool:
        """
        Check if screen is medium (tablet).
        
        Returns:
            True if medium screen
        """
        screen = MobileUtils.get_screen_size()
        return 768 <= screen['width'] < 1024
    
    @staticmethod
    def is_large_screen() -> bool:
        """
        Check if screen is large (desktop).
        
        Returns:
            True if large screen
        """
        screen = MobileUtils.get_screen_size()
        return screen['width'] >= 1024
    
    @staticmethod
    def get_responsive_columns(count: int) -> int:
        """
        Get number of columns based on screen size.
        
        Args:
            count: Number of columns on desktop
        
        Returns:
            Adjusted column count for current screen
        """
        if MobileUtils.is_small_screen():
            return 1
        elif MobileUtils.is_medium_screen():
            return max(1, count // 2)
        else:
            return count
    
    @staticmethod
    def get_responsive_font_size(base_size: int = 16) -> int:
        """
        Get responsive font size.
        
        Args:
            base_size: Base font size in pixels
        
        Returns:
            Adjusted font size
        """
        if MobileUtils.is_small_screen():
            return base_size - 2
        elif MobileUtils.is_medium_screen():
            return base_size
        else:
            return base_size + 2
    
    @staticmethod
    def get_responsive_padding(base_padding: int = 20) -> int:
        """
        Get responsive padding.
        
        Args:
            base_padding: Base padding in pixels
        
        Returns:
            Adjusted padding
        """
        if MobileUtils.is_small_screen():
            return base_padding // 2
        else:
            return base_padding
    
    @staticmethod
    def is_ios() -> bool:
        """
        Check if device is iOS.
        
        Returns:
            True if iOS device
        """
        user_agent = st.session_state.get('user_agent', '').lower()
        return 'iphone' in user_agent or 'ipad' in user_agent or 'ipod' in user_agent
    
    @staticmethod
    def is_android() -> bool:
        """
        Check if device is Android.
        
        Returns:
            True if Android device
        """
        user_agent = st.session_state.get('user_agent', '').lower()
        return 'android' in user_agent
    
    @staticmethod
    def get_os() -> str:
        """
        Get operating system.
        
        Returns:
            OS name: 'ios', 'android', 'windows', 'macos', 'linux', 'unknown'
        """
        user_agent = st.session_state.get('user_agent', '').lower()
        
        if 'iphone' in user_agent or 'ipad' in user_agent:
            return 'ios'
        elif 'android' in user_agent:
            return 'android'
        elif 'windows' in user_agent:
            return 'windows'
        elif 'mac' in user_agent:
            return 'macos'
        elif 'linux' in user_agent:
            return 'linux'
        else:
            return 'unknown'
    
    @staticmethod
    def get_browser() -> str:
        """
        Get browser name.
        
        Returns:
            Browser name: 'chrome', 'firefox', 'safari', 'edge', 'opera', 'unknown'
        """
        user_agent = st.session_state.get('user_agent', '').lower()
        
        if 'chrome' in user_agent and 'edge' not in user_agent:
            return 'chrome'
        elif 'firefox' in user_agent:
            return 'firefox'
        elif 'safari' in user_agent and 'chrome' not in user_agent:
            return 'safari'
        elif 'edge' in user_agent:
            return 'edge'
        elif 'opera' in user_agent:
            return 'opera'
        else:
            return 'unknown'
    
    @staticmethod
    def get_responsive_chart_height(base_height: int = 400) -> int:
        """
        Get responsive chart height.
        
        Args:
            base_height: Base height in pixels
        
        Returns:
            Adjusted chart height
        """
        if MobileUtils.is_small_screen():
            return base_height - 100
        elif MobileUtils.is_medium_screen():
            return base_height - 50
        else:
            return base_height
    
    @staticmethod
    def get_mobile_css() -> str:
        """
        Get mobile-specific CSS.
        
        Returns:
            CSS string for mobile optimization
        """
        return """
        /* Mobile Responsive Styles */
        @media (max-width: 768px) {
            /* Adjust main container */
            .main .block-container {
                padding: 0.5rem 0.5rem !important;
            }
            
            /* Make text smaller on mobile */
            h1 { font-size: 1.5rem !important; }
            h2 { font-size: 1.2rem !important; }
            h3 { font-size: 1rem !important; }
            
            /* Full width buttons on mobile */
            .stButton button {
                width: 100% !important;
                font-size: 14px !important;
                padding: 10px !important;
            }
            
            /* Adjust metric cards */
            .metric-card {
                padding: 10px !important;
                margin-bottom: 8px !important;
            }
            
            /* Smaller metrics */
            .metric-value {
                font-size: 20px !important;
            }
            
            /* Adjust columns */
            .row-widget {
                flex-direction: column !important;
            }
            
            /* Hide sidebars on mobile */
            .css-1d391kg {
                width: 0 !important;
            }
            
            /* Touch-friendly inputs */
            input, select, textarea {
                font-size: 16px !important;
                padding: 12px !important;
            }
            
            /* Better spacing */
            .element-container {
                margin-bottom: 8px !important;
            }
            
            /* Mobile navigation */
            .mobile-nav {
                display: flex !important;
                justify-content: space-around !important;
                position: fixed !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                background: #0f172a !important;
                padding: 8px 0 !important;
                border-top: 1px solid #334155 !important;
                z-index: 999 !important;
            }
            
            .mobile-nav-item {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                font-size: 10px !important;
                color: #94a3b8 !important;
                text-decoration: none !important;
                padding: 4px 8px !important;
            }
            
            .mobile-nav-item.active {
                color: #4ade80 !important;
            }
            
            .mobile-nav-item .icon {
                font-size: 20px !important;
            }
            
            /* Fix for Streamlit elements */
            .stMarkdown {
                font-size: 14px !important;
            }
            
            .stDataFrame {
                font-size: 12px !important;
            }
            
            /* Tab navigation */
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: wrap !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                font-size: 12px !important;
                padding: 4px 8px !important;
            }
            
            /* Touch target sizes */
            button, .stButton button, .stDownloadButton button {
                min-height: 44px !important;
                min-width: 44px !important;
            }
            
            a, .stLink {
                min-height: 44px !important;
                padding: 8px !important;
            }
        }
        
        /* Tablet adjustments */
        @media (min-width: 769px) and (max-width: 1024px) {
            .main .block-container {
                padding: 1rem 1rem !important;
            }
            
            .stButton button {
                font-size: 15px !important;
                padding: 8px 16px !important;
            }
        }
        """
    
    @staticmethod
    def inject_mobile_meta_tags() -> str:
        """
        Generate mobile meta tags.
        
        Returns:
            HTML meta tags for mobile optimization
        """
        return """
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="theme-color" content="#0f172a">
        """
    
    @staticmethod
    def get_app_icon() -> str:
        """
        Get app icon for PWA.
        
        Returns:
            Icon HTML
        """
        return """
        <link rel="apple-touch-icon" sizes="180x180" href="/static/icons/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/icons/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/icons/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="apple-mobile-web-app-title" content="EcoBuddy AI">
        """
    
    @staticmethod
    def is_pwa_installed() -> bool:
        """
        Check if PWA is installed.
        
        Returns:
            True if installed
        """
        return st.session_state.get('pwa_installed', False)
    
    @staticmethod
    def get_push_notification_permission() -> bool:
        """
        Check if push notifications are allowed.
        
        Returns:
            True if allowed
        """
        return st.session_state.get('push_permission', False)
    
    @staticmethod
    def get_cache_status() -> Dict[str, Any]:
        """
        Get cache status.
        
        Returns:
            Cache status dictionary
        """
        return {
            'cached_files': st.session_state.get('cached_files', 0),
            'cache_size_mb': st.session_state.get('cache_size_mb', 0),
            'last_updated': st.session_state.get('cache_last_updated', '')
        }