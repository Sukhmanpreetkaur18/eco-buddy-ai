"""
Green Investment Tracker Page - Full page interface for tracking eco-investments
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from src.lib.investment_tracker import InvestmentTracker
from src.lib.savings_calculator import SavingsCalculator
from src.lib.impact_calculator import ImpactCalculator
from src.lib.investment_reports import InvestmentReports
from src.components.investment_dashboard import InvestmentDashboard


def render_green_investments(user_id: str = None):
    """
    Render the Green Investment Tracker page.
    
    Args:
        user_id: User ID for personalized data
    """
    
    st.markdown("""
    <style>
        .page-header {
            background: linear-gradient(135deg, #0f172a, #1a2e1a);
            padding: 24px 32px;
            border-radius: 12px;
            margin-bottom: 24px;
            border: 1px solid rgba(74, 222, 128, 0.2);
        }
        .page-header h1 {
            color: #4ade80;
            font-size: 28px;
            font-weight: 700;
            margin: 0;
        }
        .page-header p {
            color: #94a3b8;
            margin: 8px 0 0 0;
            font-size: 15px;
        }
        .page-header .badge {
            display: inline-block;
            background: #22c55e;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 8px;
        }
        .metric-card {
            background: rgba(15, 23, 42, 0.6);
            padding: 16px 20px;
            border-radius: 10px;
            border: 1px solid rgba(74, 222, 128, 0.15);
            text-align: center;
        }
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: #4ade80;
        }
        .metric-label {
            font-size: 13px;
            color: #94a3b8;
        }
        .calculator-section {
            background: rgba(15, 23, 42, 0.4);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(74, 222, 128, 0.1);
            margin-bottom: 16px;
        }
        .result-box {
            background: rgba(74, 222, 128, 0.05);
            padding: 16px 20px;
            border-radius: 8px;
            border-left: 4px solid #4ade80;
            margin-top: 12px;
        }
        .result-box .label {
            font-size: 13px;
            color: #94a3b8;
        }
        .result-box .value {
            font-size: 20px;
            font-weight: 700;
            color: #4ade80;
        }
        .recommendation-card {
            background: rgba(15, 23, 42, 0.6);
            padding: 16px 20px;
            border-radius: 8px;
            border: 1px solid rgba(74, 222, 128, 0.1);
            margin-bottom: 8px;
            transition: all 0.2s;
        }
        .recommendation-card:hover {
            border-color: rgba(74, 222, 128, 0.3);
            transform: translateX(4px);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="page-header">
        <h1>💰 Green Investment Tracker</h1>
        <p>Track your eco-friendly investments, calculate savings, and see your environmental impact!</p>
        <span class="badge">🌱 Sustainable Investing</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize tracker
    if 'investment_tracker' not in st.session_state:
        st.session_state.investment_tracker = InvestmentTracker(user_id)
    
    tracker = st.session_state.investment_tracker
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "➕ Add Investment",
        "🧮 Calculators",
        "📈 Reports",
        "💡 Recommendations"
    ])
    
    with tab1:
        InvestmentDashboard.render(user_id)
    
    with tab2:
        render_add_investment_form(tracker)
    
    with tab3:
        render_calculators()
    
    with tab4:
        render_reports(tracker)
    
    with tab5:
        render_recommendations(tracker)


def render_add_investment_form(tracker: InvestmentTracker):
    """Render add investment form."""
    st.markdown("#### ➕ Add New Green Investment")
    
    st.info("💡 Track your eco-friendly investments and see their environmental impact!")
    
    with st.form("add_investment_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Investment Name*", placeholder="e.g., Solar Panels, EV Charger")
            category = st.selectbox(
                "Category*",
                options=list(tracker.INVESTMENT_CATEGORIES.keys()),
                format_func=lambda x: f"{tracker.INVESTMENT_CATEGORIES[x]['icon']} {tracker.INVESTMENT_CATEGORIES[x]['name']}"
            )
            amount = st.number_input("Amount Invested ($)*", min_value=0.0, step=100.0, value=1000.0)
        
        with col2:
            invested_date = st.date_input("Investment Date", value=datetime.now())
            expected_roi = st.number_input("Expected ROI (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
            status = st.selectbox("Status", options=['active', 'completed', 'pending'])
        
        annual_savings = st.number_input("Annual Savings ($)", min_value=0.0, value=0.0, step=10.0)
        notes = st.text_area("Notes (optional)", placeholder="Additional details about this investment...")
        
        # Show estimated impact
        if amount > 0 and category:
            calc = ImpactCalculator()
            impact = calc.calculate_lifetime_impact(amount, amount * 0.5, 10)
            
            st.markdown("#### 📊 Estimated Impact")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🌍 CO₂ Saved", f"{impact.get('annual_co2_kg', 0):.0f} kg/yr")
            with col2:
                st.metric("🌳 Trees Equivalent", f"{impact.get('annual_co2_kg', 0) / 22:.0f}")
            with col3:
                st.metric("💰 Annual Savings", f"${annual_savings:.0f}" if annual_savings > 0 else "$0")
        
        if st.form_submit_button("💚 Add Investment", use_container_width=True):
            if name and category and amount > 0:
                impact = ImpactCalculator().calculate_lifetime_impact(amount, amount * 0.5, 10)
                
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


def render_calculators():
    """Render investment calculators."""
    st.markdown("#### 🧮 Investment Calculators")
    
    calc = SavingsCalculator()
    
    # Solar Calculator
    with st.expander("☀️ Solar Savings Calculator", expanded=True):
        st.markdown("Calculate savings from solar panel installation.")
        
        col1, col2 = st.columns(2)
        with col1:
            system_size = st.number_input("System Size (kW)", min_value=0.5, value=5.0, step=0.5)
            cost_per_watt = st.number_input("Cost per Watt ($)", min_value=1.0, value=3.0, step=0.1)
        with col2:
            sun_hours = st.number_input("Peak Sun Hours/Day", min_value=1.0, value=4.5, step=0.5)
            electricity_rate = st.number_input("Electricity Rate ($/kWh)", min_value=0.01, value=0.15, step=0.01)
        
        if st.button("Calculate Solar Savings", use_container_width=True):
            result = calc.calculate_solar_savings(system_size, cost_per_watt, sun_hours, electricity_rate)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Total Cost", f"${result['total_cost']:,.0f}")
            with col2:
                st.metric("💵 Annual Savings", f"${result['annual_savings']:,.0f}")
            with col3:
                st.metric("📈 Payback Period", f"{result['payback_period_years']:.1f} years")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🌍 CO₂ Offset", f"{result['co2_offset_kg']:,.0f} kg/yr")
            with col2:
                st.metric("🌳 Trees Equivalent", f"{result['trees_equivalent']:.0f}")
            with col3:
                st.metric("📊 ROI", f"{result['roi']:.0f}%")
            
            st.info(f"💡 25-Year Savings: **${result['twenty_five_year_savings']:,.0f}**")
    
    # EV Calculator
    with st.expander("🚗 Electric Vehicle Savings Calculator", expanded=False):
        st.markdown("Calculate savings from switching to an electric vehicle.")
        
        col1, col2 = st.columns(2)
        with col1:
            ev_cost = st.number_input("EV Cost ($)", min_value=10000, value=35000, step=1000)
            annual_miles = st.number_input("Annual Miles", min_value=1000, value=12000, step=1000)
        with col2:
            mpg = st.number_input("Current MPG", min_value=10, value=25, step=1)
            gas_price = st.number_input("Gas Price ($/gallon)", min_value=1.0, value=3.50, step=0.1)
        
        if st.button("Calculate EV Savings", use_container_width=True):
            result = calc.calculate_ev_savings(ev_cost, annual_miles, mpg, gas_price)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💵 Annual Savings", f"${result['annual_savings']:,.0f}")
            with col2:
                st.metric("📈 Payback Period", f"{result['payback_period_years']:.1f} years")
            with col3:
                st.metric("🌍 CO₂ Reduction", f"{result['co2_reduction_kg']:,.0f} kg/yr")
            
            st.info(f"💡 Annual Fuel Cost Savings: **${result['annual_savings']:,.0f}**")
    
    # Energy Efficiency Calculator
    with st.expander("💡 Energy Efficiency Savings Calculator", expanded=False):
        st.markdown("Calculate savings from energy efficiency upgrades.")
        
        col1, col2 = st.columns(2)
        with col1:
            upgrade_cost = st.number_input("Upgrade Cost ($)", min_value=0, value=1000, step=100)
            annual_savings_kwh = st.number_input("Annual Energy Savings (kWh)", min_value=0, value=2000, step=100)
        with col2:
            electricity_rate = st.number_input("Electricity Rate ($/kWh)", min_value=0.01, value=0.15, step=0.01)
        
        if st.button("Calculate Energy Savings", use_container_width=True):
            result = calc.calculate_energy_efficiency_savings(upgrade_cost, annual_savings_kwh, electricity_rate)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💵 Annual Savings", f"${result['annual_savings']:,.0f}")
            with col2:
                st.metric("📈 Payback Period", f"{result['payback_period_years']:.1f} years")
            with col3:
                st.metric("🌍 CO₂ Reduction", f"{result['co2_reduction_kg']:,.0f} kg/yr")


def render_reports(tracker: InvestmentTracker):
    """Render reports section."""
    st.markdown("#### 📈 Investment Reports")
    
    reports = InvestmentReports()
    investments = tracker.get_all_investments()
    
    if not investments:
        st.info("No investments to report. Add some investments first! 💰")
        return
    
    # Report type selector
    report_type = st.selectbox(
        "Select Report Type",
        options=['Summary Report', 'Impact Report', 'ROI Report', 'Full Export']
    )
    
    if st.button("📄 Generate Report", use_container_width=True):
        with st.spinner("Generating report..."):
            if report_type == 'Summary Report':
                report = reports.generate_summary_report([inv.__dict__ for inv in investments])
                st.json(report)
            elif report_type == 'Impact Report':
                report = reports.generate_impact_report([inv.__dict__ for inv in investments])
                st.json(report)
            elif report_type == 'ROI Report':
                report = reports.generate_roi_report([inv.__dict__ for inv in investments])
                st.json(report)
            elif report_type == 'Full Export':
                csv = reports.generate_csv_report([inv.__dict__ for inv in investments])
                st.download_button(
                    label="⬇️ Download CSV Report",
                    data=csv,
                    file_name=f"investment_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                st.success("Report exported successfully! 📊")


def render_recommendations(tracker: InvestmentTracker):
    """Render recommendations section."""
    st.markdown("#### 💡 Investment Recommendations")
    
    recommendations = tracker.get_recommendations()
    
    if not recommendations:
        st.info("You're doing great! Keep building your green portfolio! 🌱")
        return
    
    for rec in recommendations:
        st.markdown(f"""
        <div class="recommendation-card">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                <div>
                    <span style="font-size:20px;">{tracker.INVESTMENT_CATEGORIES[rec['category']]['icon']}</span>
                    <span style="font-weight:600;font-size:16px;margin-left:8px;">{rec['name']}</span>
                    <span style="font-size:13px;color:#94a3b8;margin-left:8px;">💰 ${rec['estimated_cost']:,.0f}</span>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:14px;color:#4ade80;">💵 Savings: ${rec['estimated_savings']}/yr</div>
                    <div style="font-size:13px;color:#94a3b8;">🌍 CO₂: {rec['estimated_co2_saved']} kg/yr</div>
                </div>
            </div>
            <div style="font-size:13px;color:#64748b;margin-top:6px;">
                💡 {rec['reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)