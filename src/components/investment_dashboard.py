"""
Investment Dashboard Component for EcoBuddy AI
Displays investment portfolio, savings, and environmental impact visualizations.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from src.lib.investment_tracker import InvestmentTracker, Investment
from src.lib.savings_calculator import SavingsCalculator
from src.lib.impact_calculator import ImpactCalculator


class InvestmentDashboard:
    """
    Interactive dashboard for green investments.
    """

    @staticmethod
    def render(user_id: str = None):
        """
        Render the investment dashboard.
        
        Args:
            user_id: User ID for personalized data
        """
        # Initialize components
        if 'investment_tracker' not in st.session_state:
            st.session_state.investment_tracker = InvestmentTracker(user_id)
        
        tracker = st.session_state.investment_tracker
        
        st.markdown("""
        <style>
            .investment-card {
                background: white;
                padding: 16px 20px;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
                text-align: center;
                margin-bottom: 12px;
            }
            .investment-value {
                font-size: 28px;
                font-weight: 700;
                color: #1e293b;
            }
            .investment-label {
                font-size: 13px;
                color: #64748b;
            }
            .investment-change {
                font-size: 14px;
                font-weight: 600;
            }
            .investment-change.positive {
                color: #22c55e;
            }
            .investment-change.negative {
                color: #dc2626;
            }
            .category-badge {
                display: inline-block;
                padding: 2px 10px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
            }
            .category-badge.solar { background: #fef3c7; color: #d97706; }
            .category-badge.ev { background: #dbeafe; color: #2563eb; }
            .category-badge.energy_efficiency { background: #dcfce7; color: #16a34a; }
            .category-badge.water { background: #e0f2fe; color: #0284c7; }
            .category-badge.waste { background: #f3e8ff; color: #7c3aed; }
            .category-badge.green_building { background: #ecfdf5; color: #059669; }
        </style>
        """, unsafe_allow_html=True)

        # Get portfolio summary
        summary = tracker.get_portfolio_summary()
        portfolio = tracker.get_portfolio()

        # Summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="investment-card">
                <div class="investment-value">${portfolio.total_invested:,.0f}</div>
                <div class="investment-label">💰 Total Invested</div>
                <div class="investment-change positive">+{len(tracker.get_all_investments())} investments</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="investment-card">
                <div class="investment-value">${portfolio.total_savings:,.0f}</div>
                <div class="investment-label">💵 Annual Savings</div>
                <div class="investment-change positive">ROI: {portfolio.overall_roi:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="investment-card">
                <div class="investment-value">{portfolio.total_co2_saved:,.0f}</div>
                <div class="investment-label">🌍 CO₂ Saved (kg)</div>
                <div class="investment-change positive">🌳 {portfolio.total_trees:.0f} trees</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="investment-card">
                <div class="investment-value">{portfolio.total_energy_saved:,.0f}</div>
                <div class="investment-label">⚡ Energy Saved (kWh)</div>
                <div class="investment-change positive">💧 {portfolio.total_water_saved:,.0f} L water</div>
            </div>
            """, unsafe_allow_html=True)

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "📈 Investments",
            "🌍 Impact",
            "🎯 Goals"
        ])

        with tab1:
            InvestmentDashboard._render_overview(tracker)
        
        with tab2:
            InvestmentDashboard._render_investments(tracker)
        
        with tab3:
            InvestmentDashboard._render_impact(tracker)
        
        with tab4:
            InvestmentDashboard._render_goals(tracker)

    @staticmethod
    def _render_overview(tracker: InvestmentTracker):
        """Render overview tab."""
        st.markdown("#### 📊 Portfolio Overview")
        
        # Category breakdown chart
        summary = tracker.get_portfolio_summary()
        categories = summary.get('by_category', {})
        
        if categories:
            # Prepare data
            cat_data = []
            for cat, data in categories.items():
                cat_data.append({
                    'Category': data['name'],
                    'Icon': data['icon'],
                    'Invested': data['total_invested'],
                    'Savings': data['total_savings'],
                    'CO2': data['total_co2'],
                    'Count': data['count']
                })
            
            df = pd.DataFrame(cat_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Investment by category pie chart
                fig = px.pie(
                    df,
                    values='Invested',
                    names='Category',
                    title='Investment Distribution by Category',
                    hover_data=['Count']
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Savings by category bar chart
                fig = px.bar(
                    df,
                    x='Category',
                    y='Savings',
                    title='Annual Savings by Category',
                    color='Category',
                    text='Savings'
                )
                fig.update_layout(height=350, showlegend=False)
                fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            # ROI comparison
            st.markdown("#### 📈 ROI by Category")
            
            df['ROI'] = (df['Savings'] / df['Invested'] * 100).fillna(0)
            
            fig = px.bar(
                df,
                x='Category',
                y='ROI',
                title='Return on Investment by Category',
                color='ROI',
                color_continuous_scale='Greens',
                text='ROI'
            )
            fig.update_layout(height=300)
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No investments yet. Start by adding your first green investment! 🌱")

    @staticmethod
    def _render_investments(tracker: InvestmentTracker):
        """Render investments tab."""
        st.markdown("#### 📈 Your Investments")
        
        investments = tracker.get_all_investments()
        
        if not investments:
            st.info("No investments recorded yet. Add your first green investment below! 🌱")
            InvestmentDashboard._render_add_investment_form(tracker)
            return
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = ['All'] + list(tracker.INVESTMENT_CATEGORIES.keys())
            filter_category = st.selectbox("Filter by Category", categories)
        
        with col2:
            statuses = ['All', 'active', 'completed', 'pending']
            filter_status = st.selectbox("Filter by Status", statuses)
        
        with col3:
            sort_by = st.selectbox("Sort by", ['Date', 'Amount', 'ROI', 'Savings'])
        
        # Filter investments
        filtered = investments
        if filter_category != 'All':
            filtered = [inv for inv in filtered if inv.category == filter_category]
        if filter_status != 'All':
            filtered = [inv for inv in filtered if inv.status == filter_status]
        
        # Sort
        if sort_by == 'Date':
            filtered.sort(key=lambda x: x.invested_date, reverse=True)
        elif sort_by == 'Amount':
            filtered.sort(key=lambda x: x.amount, reverse=True)
        elif sort_by == 'ROI':
            filtered.sort(key=lambda x: x.actual_roi, reverse=True)
        elif sort_by == 'Savings':
            filtered.sort(key=lambda x: x.annual_savings, reverse=True)
        
        # Display investments
        for inv in filtered:
            InvestmentDashboard._render_investment_card(inv, tracker)
        
        # Add investment button
        st.markdown("---")
        if st.button("➕ Add New Investment", use_container_width=True):
            st.session_state.show_add_investment = not st.session_state.get('show_add_investment', False)
        
        if st.session_state.get('show_add_investment', False):
            InvestmentDashboard._render_add_investment_form(tracker)

    @staticmethod
    def _render_investment_card(investment: Investment, tracker: InvestmentTracker):
        """Render a single investment card."""
        category_info = tracker.INVESTMENT_CATEGORIES.get(investment.category, {})
        roi = investment.actual_roi or investment.expected_roi
        
        status_colors = {
            'active': '🟢',
            'completed': '✅',
            'pending': '🟡'
        }
        
        st.markdown(f"""
        <div style="background:white;padding:16px;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                <div>
                    <span style="font-size:20px;">{category_info.get('icon', '📊')}</span>
                    <span style="font-weight:600;font-size:16px;margin-left:8px;">{investment.name}</span>
                    <span class="category-badge {investment.category}">{category_info.get('name', investment.category)}</span>
                    <span style="font-size:13px;color:#94a3b8;margin-left:8px;">{status_colors.get(investment.status, '')} {investment.status.title()}</span>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:700;font-size:18px;color:#1e293b;">${investment.amount:,.0f}</div>
                    <div style="font-size:13px;color:#64748b;">ROI: {roi:.1f}%</div>
                </div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px;font-size:13px;color:#64748b;">
                <div>💰 Savings: <strong>${investment.annual_savings:,.0f}/yr</strong></div>
                <div>🌍 CO₂: <strong>{investment.co2_saved:,.0f} kg/yr</strong></div>
                <div>⚡ Energy: <strong>{investment.energy_saved:,.0f} kWh/yr</strong></div>
                <div>🌳 Trees: <strong>{investment.trees_equivalent:.0f}</strong></div>
            </div>
            <div style="margin-top:6px;font-size:12px;color:#94a3b8;">
                📅 Invested: {investment.invested_date} 
                {f'• 📝 {investment.notes[:50]}...' if investment.notes else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("✏️ Edit", key=f"edit_{investment.id}"):
                st.session_state[f"editing_{investment.id}"] = True
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{investment.id}"):
                result = tracker.delete_investment(investment.id)
                if result['success']:
                    st.success(result['message'])
                    st.rerun()

    @staticmethod
    def _render_add_investment_form(tracker: InvestmentTracker):
        """Render add investment form."""
        st.markdown("#### ➕ Add New Investment")
        
        with st.form("add_investment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Investment Name*", placeholder="e.g., Solar Panels")
                category = st.selectbox(
                    "Category*",
                    options=list(tracker.INVESTMENT_CATEGORIES.keys()),
                    format_func=lambda x: f"{tracker.INVESTMENT_CATEGORIES[x]['icon']} {tracker.INVESTMENT_CATEGORIES[x]['name']}"
                )
                amount = st.number_input("Amount Invested ($)*", min_value=0.0, step=100.0)
            
            with col2:
                invested_date = st.date_input("Investment Date", value=datetime.now())
                expected_roi = st.number_input("Expected ROI (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
                status = st.selectbox("Status", options=['active', 'completed', 'pending'])
            
            annual_savings = st.number_input("Annual Savings ($)", min_value=0.0, value=0.0, step=10.0)
            notes = st.text_area("Notes (optional)", placeholder="Additional details about this investment...")
            
            if st.form_submit_button("💚 Add Investment", use_container_width=True):
                if name and category and amount > 0:
                    # Calculate impact
                    calc = ImpactCalculator()
                    impact = calc.calculate_lifetime_impact(amount, annual_savings * 0.5, 10)
                    
                    investment = Investment(
                        name=name,
                        category=category,
                        amount=amount,
                        invested_date=invested_date.isoformat(),
                        expected_roi=expected_roi,
                        annual_savings=annual_savings,
                        co2_saved=impact.get('annual_co2_kg', 0) or amount * 0.5,
                        energy_saved=annual_savings * 10,
                        water_saved=amount * 0.5,
                        trees_equivalent=impact.get('annual_co2_kg', 0) / 22,
                        status=status,
                        notes=notes
                    )
                    
                    result = tracker.add_investment(investment)
                    if result['success']:
                        st.success(result['message'])
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(result.get('error', 'Failed to add investment'))
                else:
                    st.warning("Please fill in all required fields (*)")

    @staticmethod
    def _render_impact(tracker: InvestmentTracker):
        """Render impact tab."""
        st.markdown("#### 🌍 Environmental Impact")
        
        portfolio = tracker.get_portfolio()
        
        # Impact metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="investment-card">
                <div class="investment-value">{portfolio.total_co2_saved:,.0f} kg</div>
                <div class="investment-label">🌍 CO₂ Saved</div>
                <div class="investment-change positive">Equivalent to {portfolio.total_co2_saved/1000:.1f} tons</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="investment-card">
                <div class="investment-value">{portfolio.total_trees:.0f}</div>
                <div class="investment-label">🌳 Trees Planted Equivalent</div>
                <div class="investment-change positive">~{portfolio.total_trees*22:,.0f} kg CO₂ absorbed/year</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="investment-card">
                <div class="investment-value">{portfolio.total_energy_saved:,.0f} kWh</div>
                <div class="investment-label">⚡ Energy Saved</div>
                <div class="investment-change positive">Powers {portfolio.total_energy_saved/365/10:.0f} homes/year</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Impact breakdown
        st.markdown("#### 📊 Impact Breakdown by Category")
        
        summary = tracker.get_portfolio_summary()
        categories = summary.get('by_category', {})
        
        if categories:
            cat_data = []
            for cat, data in categories.items():
                cat_data.append({
                    'Category': data['name'],
                    'Icon': data['icon'],
                    'CO2': data['total_co2'],
                    'Savings': data['total_savings']
                })
            
            df = pd.DataFrame(cat_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    df,
                    x='Category',
                    y='CO2',
                    title='CO₂ Saved by Category',
                    color='Category',
                    text='CO2'
                )
                fig.update_layout(height=350, showlegend=False)
                fig.update_traces(texttemplate='%{text:,.0f} kg', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    df,
                    x='Category',
                    y='Savings',
                    title='Savings by Category',
                    color='Category',
                    text='Savings'
                )
                fig.update_layout(height=350, showlegend=False)
                fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def _render_goals(tracker: InvestmentTracker):
        """Render goals tab."""
        st.markdown("#### 🎯 Investment Goals")
        
        goals = tracker.get_goals()
        progress = tracker.get_goal_progress()
        
        # Progress summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Total Goals", progress.get('total_goals', 0))
        with col2:
            st.metric("✅ Completed", progress.get('completed', 0))
        with col3:
            st.metric("⏳ In Progress", progress.get('in_progress', 0))
        with col4:
            st.metric("📊 Avg Progress", f"{progress.get('avg_progress', 0):.0f}%")
        
        st.markdown("---")
        
        # Add goal form
        with st.expander("➕ Add New Goal", expanded=False):
            with st.form("add_goal_form"):
                col1, col2 = st.columns(2)
                with col1:
                    goal_name = st.text_input("Goal Name*", placeholder="e.g., Solar Investment Fund")
                    target_amount = st.number_input("Target Amount ($)*", min_value=0.0, step=100.0)
                with col2:
                    deadline = st.date_input("Deadline", value=datetime.now() + timedelta(days=365))
                    priority = st.selectbox("Priority", options=['low', 'medium', 'high'])
                
                if st.form_submit_button("🎯 Add Goal", use_container_width=True):
                    if goal_name and target_amount > 0:
                        goal = InvestmentGoal(
                            name=goal_name,
                            target_amount=target_amount,
                            deadline=deadline.isoformat(),
                            priority=priority
                        )
                        result = tracker.add_goal(goal)
                        if result['success']:
                            st.success(result['message'])
                            st.rerun()
        
        # Display goals
        if goals:
            for goal in goals:
                progress_pct = goal.progress
                status_icon = "✅" if goal.status == 'completed' else "🔄" if goal.status == 'active' else "❌"
                
                st.markdown(f"""
                <div style="background:white;padding:14px 18px;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                        <div>
                            <span style="font-weight:600;font-size:16px;">{status_icon} {goal.name}</span>
                            <span style="font-size:13px;color:#94a3b8;margin-left:8px;">Priority: {goal.priority.title()}</span>
                        </div>
                        <div style="font-weight:600;color:#1e293b;">
                            ${goal.current_amount:,.0f} / ${goal.target_amount:,.0f}
                        </div>
                    </div>
                    <div style="margin-top:6px;">
                        <div style="width:100%;height:8px;background:#e2e8f0;border-radius:4px;overflow:hidden;">
                            <div style="width:{progress_pct}%;height:100%;background:linear-gradient(90deg,#3b82f6,#22c55e);border-radius:4px;"></div>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:12px;color:#94a3b8;margin-top:2px;">
                            <span>{progress_pct:.1f}% complete</span>
                            <span>📅 {goal.deadline[:10] if goal.deadline else 'No deadline'}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No goals set yet. Create your first investment goal! 🎯")