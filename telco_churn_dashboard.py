

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="Telco Communication Service - Customer Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📱"
)

# Dark-themed color palette with high contrast
COLORS = {
    'primary': '#e5e7eb',        # Light gray for text
    'secondary': '#9ca3af',      # Mid gray for secondary text
    'accent': '#4f46e5',         # Indigo for highlights
    'success': '#10b981',        # Vibrant emerald for positive metrics
    'warning': '#f59e0b',        # Amber for warnings
    'danger': '#ef4444',         # Red for negative metrics
    'info': '#3b82f6',           # Blue for informational elements
    'light': '#f8fafc',          # Near-white for accents
    'dark': '#111827',           # Deep dark gray for background
    'muted': '#6b7280',          # Muted gray for subtle text
    'background': '#000000',     # Solid black background
    'surface': '#1f2937',        # Slightly lighter dark gray for cards
    'border': '#4b5563',         # Darker gray for borders
    'gradient_start': '#4f46e5', # Indigo gradient start
    'gradient_end': '#06b6d4'    # Cyan gradient end
}

# Enhanced Custom CSS for dark theme with high contrast
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .main {{
        background: {COLORS['background']};
        min-height: 100vh;
        padding: 20px;
    }}

    .header-container {{
        background: {COLORS['surface']};
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 32px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }}

    .header-container:hover {{
        transform: translateY(-4px);
    }}

    .logo-container {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 12px;
    }}

    .logo-placeholder {{
        width: 64px;
        height: 64px;
        background: linear-gradient(45deg, {COLORS['accent']}, {COLORS['info']});
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: {COLORS['light']};
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }}

    .logo-placeholder:hover {{
        transform: scale(1.05);
    }}

    .company-name {{
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: {COLORS['primary']};
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }}

    .company-tagline {{
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: {COLORS['secondary']};
        margin: 0;
        font-weight: 400;
    }}

    .stTabs [data-baseweb="tab"] {{
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: {COLORS['primary']};
        background: {COLORS['surface']};
        border-radius: 12px;
        padding: 12px 24px;
        margin-right: 8px;
        border: 1px solid {COLORS['border']};
        transition: all 0.3s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background: {COLORS['border']};
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: linear-gradient(45deg, {COLORS['accent']}, {COLORS['info']});
        color: {COLORS['light']};
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }}

    .metric-card {{
        background: {COLORS['surface']};
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin-bottom: 24px;
        border: 1px solid {COLORS['border']};
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        backdrop-filter: blur(12px);
    }}

    .metric-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
    }}

    .metric-title {{
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: {COLORS['secondary']};
        margin-bottom: 8px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}

    .metric-value {{
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: {COLORS['primary']};
        margin-bottom: 6px;
    }}

    .metric-delta {{
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: {COLORS['danger']};
        font-weight: 600;
    }}

    .metric-delta.positive {{
        color: {COLORS['success']};
    }}

    .insight-card {{
        background: {COLORS['surface']};
        border-radius: 16px;
        padding: 24px;
        margin: 24px 0;
        border-left: 6px solid {COLORS['accent']};
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
        transition: transform 0.3s ease;
    }}

    .insight-card:hover {{
        transform: translateY(-4px);
    }}

    .insight-title {{
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin-bottom: 12px;
    }}

    .insight-text {{
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: {COLORS['secondary']};
        line-height: 1.7;
    }}

    h1, h2, h3 {{
        font-family: 'Inter', sans-serif;
        color: {COLORS['primary']};
        font-weight: 600;
    }}

    .stMarkdown {{
        font-family: 'Inter', sans-serif;
        color: {COLORS['secondary']};
    }}

    .stSidebar {{
        background: {COLORS['surface']};
        color: {COLORS['secondary']};
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }}

    .stSidebar .stMultiSelect div, .stSidebar .stSlider div {{
        color: {COLORS['primary']};
    }}

    .stButton>button {{
        background: linear-gradient(45deg, {COLORS['accent']}, {COLORS['info']});
        color: {COLORS['light']};
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }}

    .filter-section {{
        background: {COLORS['surface']};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
    }}

    .section-header {{
        font-family: 'Inter', sans-serif;
        font-size: 24px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin-bottom: 16px;
        text-align: center;
    }}

    .dashboard-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        color: {COLORS['secondary']};
        text-align: center;
        margin-bottom: 32px;
        font-weight: 400;
    }}
</style>
""", unsafe_allow_html=True)

# Load the dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("./dataset/ml_ready_telco.csv")
        df = df.rename(columns={
            "Tenure in Months": "Tenure",
            "Churn Label": "Churn",
            "Monthly Charge": "MonthlyCharges",
            "Total Charges": "TotalCharges"
        })
        bool_cols = ["Senior Citizen", "Married", "Dependents", "Phone Service", "Multiple Lines",
                     "Internet Service", "Online Security", "Online Backup", "Device Protection Plan",
                     "Premium Tech Support", "Streaming TV", "Streaming Movies", "Streaming Music",
                     "Unlimited Data", "Paperless Billing"]
        for col in bool_cols:
            if col in df.columns:
                df[col] = df[col].replace({"True": True, "False": False, "Yes": True, "No": False})
        df["CitizenshipStatus"] = df["Senior Citizen"].apply(lambda x: "Senior Citizen" if x else "Young Citizen")
        df["ChurnStatus"] = df["Churn"].apply(lambda x: "Churned" if x == "Yes" else "Retained")
        numeric_cols = ["MonthlyCharges", "TotalCharges", "Tenure", "Age"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("Dataset 'ml_ready_telco.csv' not found. Please check the file path.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Load data
df = load_data()
if df.empty:
    st.stop()

# Header with company branding
st.markdown(f"""
<div class="header-container">
    <div class="logo-container">
        <div class="logo-placeholder">TC</div>
        <div>
            <h1 class="company-name">Telco Communication Service</h1>
            <p class="company-tagline">Empowering Customer Insights with Advanced Analytics</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<p class="dashboard-subtitle">Unleashing actionable insights for strategic customer retention and growth</p>', unsafe_allow_html=True)

# Calculate key metrics
total_customers = len(df)
churned_customers = len(df[df["Churn"] == "Yes"])
retained_customers = total_customers - churned_customers
churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0
retention_rate = 100 - churn_rate
monthly_revenue_loss = df["MonthlyCharges"].sum() if "MonthlyCharges" in df.columns else 0
avg_monthly_charges = df["MonthlyCharges"].mean() if "MonthlyCharges" in df.columns else 0
total_revenue = df["TotalCharges"].sum() if "TotalCharges" in df.columns else 0
avg_tenure = df["Tenure"].mean() if "Tenure" in df.columns else 0
avg_age = df["Age"].mean() if "Age" in df.columns else 0
satisfaction_score = df["Satisfaction Score"].mean() if "Satisfaction Score" in df.columns else 0

# Sidebar for filters
with st.sidebar:
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🔍 Data Filters</h3>', unsafe_allow_html=True)
    
    available_cols = df.columns.tolist()
    
    if "Gender" in available_cols:
        gender_filter = st.multiselect(
            "👥 Gender",
            options=df["Gender"].unique(),
            default=df["Gender"].unique(),
            help="Filter customers by gender"
        )
    else:
        gender_filter = []
    
    if "Contract" in available_cols:
        contract_filter = st.multiselect(
            "📝 Contract Type",
            options=df["Contract"].unique(),
            default=df["Contract"].unique(),
            help="Filter by contract duration"
        )
    else:
        contract_filter = []
    
    if "Internet Service" in available_cols:
        internet_filter = st.multiselect(
            "🌐 Internet Service",
            options=df["Internet Service"].unique(),
            default=df["Internet Service"].unique(),
            help="Filter by internet service type"
        )
    else:
        internet_filter = []
    
    if "Age" in available_cols:
        age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
        age_range = st.slider(
            "👶 Age Range",
            min_value=age_min,
            max_value=age_max,
            value=(age_min, age_max),
            help="Select customer age range"
        )
    else:
        age_range = (0, 100)
    
    if "Tenure" in available_cols:
        tenure_min, tenure_max = int(df["Tenure"].min()), int(df["Tenure"].max())
        tenure_range = st.slider(
            "⏰ Tenure Range (Months)",
            min_value=tenure_min,
            max_value=tenure_max,
            value=(tenure_min, tenure_max),
            help="Filter by customer tenure"
        )
    else:
        tenure_range = (0, 100)
    
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered_df = df.copy()
if "Gender" in available_cols and gender_filter:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender_filter)]
if "Contract" in available_cols and contract_filter:
    filtered_df = filtered_df[filtered_df["Contract"].isin(contract_filter)]
if "Internet Service" in available_cols and internet_filter:
    filtered_df = filtered_df[filtered_df["Internet Service"].isin(internet_filter)]
if "Age" in available_cols:
    filtered_df = filtered_df[filtered_df["Age"].between(age_range[0], age_range[1])]
if "Tenure" in available_cols:
    filtered_df = filtered_df[filtered_df["Tenure"].between(tenure_range[0], tenure_range[1])]

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Try adjusting your filter criteria.")
    st.stop()

# Update filtered metrics
filtered_total_customers = len(filtered_df)
filtered_churned_customers = len(filtered_df[filtered_df["Churn"] == "Yes"])
filtered_retained_customers = filtered_total_customers - filtered_churned_customers
filtered_churn_rate = (filtered_churned_customers / filtered_total_customers * 100) if filtered_total_customers > 0 else 0
filtered_retention_rate = 100 - filtered_churn_rate
filtered_monthly_revenue_loss = filtered_df[filtered_df["Churn"] == "Yes"]["MonthlyCharges"].sum() if "MonthlyCharges" in filtered_df.columns else 0

# Key Performance Indicators
st.markdown('<h2 class="section-header">📊 Key Performance Indicators</h2>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">Total Customers</div>
        <div class="metric-value">{filtered_total_customers:,}</div>
        <div class="metric-delta">Active subscriber base</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">Churn Rate</div>
        <div class="metric-value">{filtered_churn_rate:.1f}%</div>
        <div class="metric-delta">{filtered_churned_customers:,} customers lost</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">Retention Rate</div>
        <div class="metric-value">{filtered_retention_rate:.1f}%</div>
        <div class="metric-delta positive">{filtered_retained_customers:,} customers retained</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">Revenue at Risk</div>
        <div class="metric-value">${filtered_monthly_revenue_loss:,.0f}</div>
        <div class="metric-delta">Monthly revenue loss</div>
    </div>
    ''', unsafe_allow_html=True)

with col5:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">Avg Monthly Charges</div>
        <div class="metric-value">${avg_monthly_charges:.0f}</div>
        <div class="metric-delta">Per customer ARPU</div>
    </div>
    ''', unsafe_allow_html=True)

# Download filtered data
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_telco_data.csv",
    mime="text/csv",
    use_container_width=True
)

# Tabs for detailed analysis
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Customer Overview", "💰 Financial Analysis", "📱 Service Analytics", "🎯 Churn Insights"])

# Tab 1: Customer Overview
# [Previous code remains unchanged until Tab 1]

# Tab 1: Customer Overview
# [Previous code remains unchanged until Tab 1]

# Tab 1: Customer Overview
with tab1:
    st.markdown('<h2 class="section-header">Customer Demographics & Behavior Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        churn_counts = filtered_df["ChurnStatus"].value_counts()
        fig_churn_dist = go.Figure(data=[go.Pie(
            labels=churn_counts.index,
            values=churn_counts.values,
            hole=0.5,
            marker=dict(colors=[COLORS['success'],COLORS['danger']], line=dict(color=COLORS['light'], width=2)),
            textfont=dict(size=16, color=COLORS['primary']),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        fig_churn_dist.update_layout(
            title=dict(text="Customer Churn Distribution", font=dict(size=22, color=COLORS['primary']), x=0.5),
            template='plotly_dark',
            font=dict(family="Inter", size=14, color=COLORS['primary']),
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['background'],
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, bgcolor=COLORS['surface']),
            annotations=[dict(text=f'{filtered_churn_rate:.1f}%<br>Churn Rate', 
                            x=0.5, y=0.5, font_size=20, showarrow=False, font_color=COLORS['primary'])]
        )
        st.plotly_chart(fig_churn_dist, use_container_width=True)
        
        if "Gender" in filtered_df.columns and not filtered_df.empty:
            gender_churn = filtered_df.groupby("Gender").agg({
                "Churn": lambda x: (x == "Yes").sum(),
                "Gender": "count"
            }).rename(columns={"Gender": "Total"})
            gender_churn["Churn_Rate"] = (gender_churn["Churn"] / gender_churn["Total"] * 100).round(1)
            if gender_churn.empty:
                st.warning("⚠️ No data available for Gender analysis after filtering.")
            else:
                # Reset index to make "Gender" a column
                gender_churn = gender_churn.reset_index()
                # Debug: Verify the structure (remove after testing)
                # st.write(gender_churn)
                if "Gender" not in gender_churn.columns:
                    st.warning("⚠️ 'Gender' column not found in grouped data. Check dataset structure.")
                else:
                    fig_gender = px.bar(
                        gender_churn,
                        x="Gender",
                        y="Churn_Rate",
                        title="Churn Rate by Gender",
                        color="Churn_Rate",
                        color_continuous_scale=[[0, COLORS['success']], [1, COLORS['danger']]],
                        text="Churn_Rate"
                    )
                    fig_gender.update_traces(
                        texttemplate='%{text}%',
                        textposition='auto',
                        marker=dict(line=dict(color=COLORS['light'], width=1))
                    )
                    max_churn_rate = gender_churn["Churn_Rate"].max()
                    for index, row in gender_churn.iterrows():
                        offset = 2 if row["Churn_Rate"] < max_churn_rate * 0.7 else 5
                        fig_gender.add_annotation(
                            x=row["Gender"],  # Now should work as "Gender" is a column
                            y=row["Churn_Rate"] + offset,
                            text=f"{row['Churn_Rate']}%",
                            showarrow=False,
                            font=dict(size=12, color=COLORS['primary']),
                            bgcolor=COLORS['surface'],
                            bordercolor=COLORS['border'],
                            borderwidth=1,
                            opacity=0.9
                        )
                    fig_gender.update_layout(
                        template='plotly_dark',
                        font=dict(family="Inter", size=14, color=COLORS['primary']),
                        paper_bgcolor=COLORS['background'],
                        plot_bgcolor=COLORS['background'],
                        title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                        yaxis_title="Churn Rate (%)",
                        yaxis_range=[0, max_churn_rate + 10],
                        showlegend=False,
                        bargap=0.3
                    )
                    st.plotly_chart(fig_gender, use_container_width=True)
        else:
            st.warning("⚠️ 'Gender' column not found in the dataset or data is empty after filtering.")
    

    with col2:
            if "Age" in filtered_df.columns:
                fig_age_dist = px.histogram(
                    filtered_df.sort_values("ChurnStatus", ascending=False),
                    x="Age",
                    color="ChurnStatus",
                    nbins=20,
                    color_discrete_map={'Churned': COLORS['danger'], 'Retained': COLORS['success']},
                    barmode='overlay',
                    opacity=0.7
                )
                fig_age_dist.update_traces(
                    opacity=0.5, selector=dict(name='Retained'),
                    marker=dict(line=dict(color=COLORS['light'], width=1))
                )
                fig_age_dist.update_traces(
                    opacity=1.0, selector=dict(name='Churned'),
                    marker=dict(line=dict(color=COLORS['light'], width=1))
                )
                fig_age_dist.update_layout(
                    template='plotly_dark',
                    font=dict(family="Inter", size=14, color=COLORS['primary']),
                    paper_bgcolor=COLORS['background'],
                    plot_bgcolor=COLORS['background'],
                    title=dict(text="Age Distribution by Churn Status", font=dict(size=20, color=COLORS['primary']), x=0.5),
                    xaxis_title="Age",
                    yaxis_title="Count",
                    legend=dict(
                        bgcolor=COLORS['surface'],
                        font=dict(color=COLORS['primary']),
                        orientation="h",
                        yanchor="bottom",
                        y=-0.3,
                        xanchor="center",
                        x=0.5
                    )
                )
                st.plotly_chart(fig_age_dist, use_container_width=True)
            
            if "Senior Citizen" in filtered_df.columns:
                senior_analysis = filtered_df.groupby("CitizenshipStatus").agg({
                    "Churn": lambda x: (x == "Yes").sum(),
                    "CitizenshipStatus": "count"
                }).rename(columns={"CitizenshipStatus": "Total"})
                senior_analysis["Churn_Rate"] = (senior_analysis["Churn"] / senior_analysis["Total"] * 100).round(1)
                if senior_analysis.empty:
                    st.warning("⚠️ No data available for Senior Citizen analysis after filtering.")
                else:
                    # Reset index to make "CitizenshipStatus" a column
                    senior_analysis = senior_analysis.reset_index()
                    # Debug: Verify the structure (remove after testing)
                    # st.write(senior_analysis)
                    if "CitizenshipStatus" not in senior_analysis.columns:
                        st.warning("⚠️ 'CitizenshipStatus' column not found in grouped data. Check dataset structure.")
                    else:
                        fig_senior = px.bar(
                            senior_analysis,
                            x="CitizenshipStatus",
                            y="Churn_Rate",
                            title="Churn Rate by Age Group",
                            color="Churn_Rate",
                            color_continuous_scale=[[0, COLORS['success']], [1, COLORS['danger']]],
                            text="Churn_Rate"
                        )
                        fig_senior.update_traces(
                            texttemplate='%{text}%',
                            textposition='auto',
                            marker=dict(line=dict(color=COLORS['light'], width=1))
                        )
                        max_churn_rate = senior_analysis["Churn_Rate"].max()
                        for index, row in senior_analysis.iterrows():
                            offset = 2 if row["Churn_Rate"] < max_churn_rate * 0.7 else 5
                            fig_senior.add_annotation(
                                x=row["CitizenshipStatus"],  # Now should work as a column
                                y=row["Churn_Rate"] + offset,
                                text=f"{row['Churn_Rate']}%",
                                showarrow=False,
                                font=dict(size=12, color=COLORS['primary']),
                                bgcolor=COLORS['surface'],
                                bordercolor=COLORS['border'],
                                borderwidth=1,
                                opacity=0.9
                            )
                        fig_senior.update_layout(
                            template='plotly_dark',
                            font=dict(family="Inter", size=14, color=COLORS['primary']),
                            paper_bgcolor=COLORS['background'],
                            plot_bgcolor=COLORS['background'],
                            title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                            yaxis_title="Churn Rate (%)",
                            yaxis_range=[0, max_churn_rate + 10],
                            showlegend=False,
                            bargap=0.3
                        )
                        st.plotly_chart(fig_senior, use_container_width=True)
            else:
                st.warning("⚠️ 'Senior Citizen' column not found in the dataset.")





# Tab 2: Financial Analysis
with tab2:
    st.markdown('<h2 class="section-header">Financial Performance & Revenue Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "MonthlyCharges" in filtered_df.columns:
            fig_charges = px.box(
                filtered_df,
                y="MonthlyCharges",
                x="ChurnStatus",
                title="Monthly Charges Distribution by Churn Status",
                color="ChurnStatus",
                color_discrete_map={'Churned': COLORS['danger'], 'Retained': COLORS['success']}
            )
            fig_charges.update_traces(
                marker=dict(line=dict(color=COLORS['light'], width=1)),
                boxmean=True
            )
            fig_charges.update_layout(
                template='plotly_dark',
                font=dict(family="Inter", size=14, color=COLORS['primary']),
                paper_bgcolor=COLORS['background'],
                plot_bgcolor=COLORS['background'],
                title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                yaxis_title="Monthly Charges ($)",
                showlegend=True,
                legend=dict(bgcolor=COLORS['surface'], font=dict(color=COLORS['primary']))
            )
            st.plotly_chart(fig_charges, use_container_width=True)
        
        if "TotalCharges" in filtered_df.columns:
            revenue_impact = filtered_df.groupby("ChurnStatus")["TotalCharges"].sum().reset_index()
            if revenue_impact.empty:
                st.warning("⚠️ No data available for Revenue Impact analysis after filtering.")
            else:
                fig_revenue = px.bar(
                    revenue_impact,
                    x="ChurnStatus",
                    y="TotalCharges",
                    title="Total Revenue by Customer Status",
                    color="ChurnStatus",
                    color_discrete_map={'Churned': COLORS['danger'], 'Retained': COLORS['success']},
                    text="TotalCharges"
                )
                fig_revenue.update_traces(
                    texttemplate='$%{text:,.0f}', 
                    textposition='outside',
                    marker=dict(line=dict(color=COLORS['light'], width=1))
                )
                # Add custom annotations for TotalCharges with dynamic positioning
                max_total_charges = revenue_impact["TotalCharges"].max()
                for index, row in revenue_impact.iterrows():
                    offset = 2 if row["TotalCharges"] < max_total_charges * 0.7 else 5
                    fig_revenue.add_annotation(
                        x=row["ChurnStatus"],  # Use "ChurnStatus" as the x-value
                        y=row["TotalCharges"] + offset,
                        text=f"${row['TotalCharges']:,.0f}",
                        showarrow=False,
                        font=dict(size=12, color=COLORS['primary']),
                        bgcolor=COLORS['surface'],
                        bordercolor=COLORS['border'],
                        borderwidth=1,
                        opacity=0.9
                    )
                fig_revenue.update_layout(
                    template='plotly_dark',
                    font=dict(family="Inter", size=14, color=COLORS['primary']),
                    paper_bgcolor=COLORS['background'],
                    plot_bgcolor=COLORS['background'],
                    title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                    yaxis_title="Total Revenue ($)",
                    showlegend=True,
                    legend=dict(bgcolor=COLORS['surface'], font=dict(color=COLORS['primary'])),
                    yaxis_range=[0, max_total_charges * 1.1]  # Add padding for annotations
                )
                st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        if "Tenure" in filtered_df.columns and "MonthlyCharges" in filtered_df.columns:
            fig_scatter = px.scatter(
                filtered_df,
                x="Tenure",
                y="MonthlyCharges",
                color="ChurnStatus",
                title="Customer Tenure vs Monthly Charges",
                color_discrete_map={'Churned': COLORS['danger'], 'Retained': COLORS['success']},
                opacity=0.7,
                size_max=15
            )
            fig_scatter.update_traces(
                marker=dict(line=dict(color=COLORS['light'], width=1))
            )
            fig_scatter.update_layout(
                template='plotly_dark',
                font=dict(family="Inter", size=14, color=COLORS['primary']),
                paper_bgcolor=COLORS['background'],
                plot_bgcolor=COLORS['background'],
                title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                xaxis_title="Tenure (Months)",
                yaxis_title="Monthly Charges ($)",
                legend=dict(bgcolor=COLORS['surface'], font=dict(color=COLORS['primary']))
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        if "Contract" in filtered_df.columns:
            contract_analysis = filtered_df.groupby("Contract").agg({
                "Churn": lambda x: (x == "Yes").sum(),
                "Contract": "count"
            }).rename(columns={"Contract": "Total"})
            contract_analysis["Churn_Rate"] = (contract_analysis["Churn"] / contract_analysis["Total"] * 100).round(1)
            
            fig_contract = px.bar(
                contract_analysis.reset_index(),
                x="Contract",
                y="Churn_Rate",
                title="Churn Rate by Contract Type",
                color="Churn_Rate",
                color_continuous_scale=[[0, COLORS['success']], [1, COLORS['danger']]],
                text="Churn_Rate"
            )
            fig_contract.update_traces(
                texttemplate='%{text}%', 
                textposition='outside',
                marker=dict(line=dict(color=COLORS['light'], width=1))
            )
            fig_contract.update_layout(
                template='plotly_dark',
                font=dict(family="Inter", size=14, color=COLORS['primary']),
                paper_bgcolor=COLORS['background'],
                plot_bgcolor=COLORS['background'],
                title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                yaxis_title="Churn Rate (%)",
                showlegend=False,
                bargap=0.2
            )
            max_churn = contract_analysis["Churn_Rate"].max()
            max_contract = contract_analysis["Churn_Rate"].idxmax()
            fig_contract.add_annotation(
                x=max_contract, y=max_churn, text=f"Highest churn: {max_churn:.1f}%",
                showarrow=True, arrowhead=1, yshift=10, font=dict(color=COLORS['primary'], size=12), bgcolor=COLORS['surface']
            )
            st.plotly_chart(fig_contract, use_container_width=True)


# [Previous code remains unchanged until Tab 3]

# Tab 3: Service Analytics
with tab3:
    st.markdown('<h2 class="section-header">Service Utilization & Subscription Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if "Internet Service" in filtered_df.columns:
            internet_analysis = filtered_df.groupby("Internet Service").agg({
                "Churn": lambda x: (x == "Yes").sum(),
                "Internet Service": "count"
            }).rename(columns={"Internet Service": "Total"})
            internet_analysis["Churn_Rate"] = (internet_analysis["Churn"] / internet_analysis["Total"] * 100).round(1)
            if internet_analysis.empty:
                st.warning("⚠️ No data available for Internet Service analysis after filtering.")
            else:
                internet_analysis = internet_analysis.reset_index()
                if "Internet Service" not in internet_analysis.columns:
                    st.warning("⚠️ 'Internet Service' column not found in grouped data. Check dataset structure.")
                else:
                    fig_internet = px.bar(
                        internet_analysis,
                        x="Internet Service",
                        y="Churn_Rate",
                        title="Churn Rate by Internet Service",
                        color="Churn_Rate",
                        color_continuous_scale=[[0, COLORS['success']], [1, COLORS['danger']]],
                        text="Churn_Rate"
                    )
                    fig_internet.update_traces(
                        texttemplate='%{text}%', 
                        textposition='outside',
                        marker=dict(line=dict(color=COLORS['light'], width=1))
                    )
                    max_churn_rate = internet_analysis["Churn_Rate"].max()
                    for index, row in internet_analysis.iterrows():
                        offset = 2 if row["Churn_Rate"] < max_churn_rate * 0.7 else 5
                        fig_internet.add_annotation(
                            x=row["Internet Service"],
                            y=row["Churn_Rate"] + offset,
                            text=f"{row['Churn_Rate']}%",
                            showarrow=False,
                            font=dict(size=12, color=COLORS['primary']),
                            bgcolor=COLORS['surface'],
                            bordercolor=COLORS['border'],
                            borderwidth=1,
                            opacity=0.9
                        )
                    fig_internet.update_layout(
                        template='plotly_dark',
                        font=dict(family="Inter", size=14, color=COLORS['primary']),
                        paper_bgcolor=COLORS['background'],
                        plot_bgcolor=COLORS['background'],
                        title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                        yaxis_title="Churn Rate (%)",
                        showlegend=False,
                        bargap=0.2,
                        yaxis_range=[0, max_churn_rate * 1.1]
                    )
                    st.plotly_chart(fig_internet, use_container_width=True)
    
    with col2:
        if "Phone Service" in filtered_df.columns:
            phone_analysis = filtered_df.groupby("Phone Service").agg({
                "Churn": lambda x: (x == "Yes").sum(),
                "Phone Service": "count"
            }).rename(columns={"Phone Service": "Total"})
            phone_analysis["Churn_Rate"] = (phone_analysis["Churn"] / phone_analysis["Total"] * 100).round(1)
            if phone_analysis.empty:
                st.warning("⚠️ No data available for Phone Service analysis after filtering.")
            else:
                phone_analysis = phone_analysis.reset_index()
                if "Phone Service" not in phone_analysis.columns:
                    st.warning("⚠️ 'Phone Service' column not found in grouped data. Check dataset structure.")
                else:
                    fig_phone = px.bar(
                        phone_analysis,
                        x="Phone Service",
                        y="Churn_Rate",
                        title="Churn Rate by Phone Service",
                        color="Churn_Rate",
                        color_continuous_scale=[[0, COLORS['success']], [1, COLORS['danger']]],
                        text="Churn_Rate"
                    )
                    fig_phone.update_traces(
                        texttemplate='%{text}%', 
                        textposition='outside',
                        marker=dict(line=dict(color=COLORS['light'], width=1))
                    )
                    max_churn_rate = phone_analysis["Churn_Rate"].max()
                    for index, row in phone_analysis.iterrows():
                        offset = 2 if row["Churn_Rate"] < max_churn_rate * 0.7 else 5
                        fig_phone.add_annotation(
                            x=row["Phone Service"],
                            y=row["Churn_Rate"] + offset,
                            text=f"{row['Churn_Rate']}%",
                            showarrow=False,
                            font=dict(size=12, color=COLORS['primary']),
                            bgcolor=COLORS['surface'],
                            bordercolor=COLORS['border'],
                            borderwidth=1,
                            opacity=0.9
                        )
                    fig_phone.update_layout(
                        template='plotly_dark',
                        font=dict(family="Inter", size=14, color=COLORS['primary']),
                        paper_bgcolor=COLORS['background'],
                        plot_bgcolor=COLORS['background'],
                        title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                        yaxis_title="Churn Rate (%)",
                        showlegend=False,
                        bargap=0.2,
                        yaxis_range=[0, max_churn_rate * 1.1]
                    )
                    st.plotly_chart(fig_phone, use_container_width=True)
    
    with col3:
        if "Number of Referrals" in filtered_df.columns:
            referral_analysis = filtered_df.groupby("Number of Referrals").agg({
                "Churn": lambda x: (x == "Yes").sum(),
                "Number of Referrals": "count"
            }).rename(columns={"Number of Referrals": "Total"})
            referral_analysis["Churn_Rate"] = (referral_analysis["Churn"] / referral_analysis["Total"] * 100).round(1)
            if referral_analysis.empty:
                st.warning("⚠️ No data available for Number of Referrals analysis after filtering.")
            else:
                referral_analysis = referral_analysis.reset_index()
                if "Number of Referrals" not in referral_analysis.columns:
                    st.warning("⚠️ 'Number of Referrals' column not found in grouped data. Check dataset structure.")
                else:
                    fig_referral = px.bar(
                        referral_analysis,
                        x="Number of Referrals",
                        y="Churn_Rate",
                        title="Churn Rate by Number of Referrals",
                        color="Churn_Rate",
                        color_continuous_scale=[[0, COLORS['success']], [1, COLORS['danger']]],
                        text="Churn_Rate"
                    )
                    fig_referral.update_traces(
                        texttemplate='%{text}%', 
                        textposition='outside',
                        marker=dict(line=dict(color=COLORS['light'], width=1))
                    )
                    max_churn_rate = referral_analysis["Churn_Rate"].max()
                    for index, row in referral_analysis.iterrows():
                        offset = 2 if row["Churn_Rate"] < max_churn_rate * 0.7 else 5
                        fig_referral.add_annotation(
                            x=row["Number of Referrals"],
                            y=row["Churn_Rate"] + offset,
                            text=f"{row['Churn_Rate']}%",
                            showarrow=False,
                            font=dict(size=12, color=COLORS['primary']),
                            bgcolor=COLORS['surface'],
                            bordercolor=COLORS['border'],
                            borderwidth=1,
                            opacity=0.9
                        )
                    fig_referral.update_layout(
                        template='plotly_dark',
                        font=dict(family="Inter", size=14, color=COLORS['primary']),
                        paper_bgcolor=COLORS['background'],
                        plot_bgcolor=COLORS['background'],
                        title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
                        yaxis_title="Churn Rate (%)",
                        showlegend=False,
                        bargap=0.2,
                        yaxis_range=[0, max_churn_rate * 1.1]
                    )
                    st.plotly_chart(fig_referral, use_container_width=True)

# [Remaining tabs (Tab 4) remain unchanged]
# Tab 4: Churn Insights
with tab4:
    st.markdown('<h2 class="section-header">Churn Insights & Recommendations</h2>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Key Observations</div>
        <div class="insight-text">
            <ul>
                <li><b>High Churn in Month-to-Month Contracts</b>: Customers on month-to-month contracts exhibit significantly higher churn rates compared to one-year or two-year contracts.</li>
                <li><b>Internet Service Impact</b>: Customers with Fiber Optic internet service show higher churn rates, possibly due to service quality or pricing concerns.</li>
                <li><b>Low Referral Customers</b>: Customers with fewer referrals (0-2) have higher churn rates, indicating a lack of loyalty or engagement.</li>
                <li><b>Monthly Charges</b>: Customers with higher monthly charges (>$80) are more likely to churn, suggesting price sensitivity.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Actionable Recommendations</div>
        <div class="insight-text">
            <ul>
                <li><b>Promote Long-Term Contracts</b>: Offer incentives (e.g., discounts, free upgrades) for customers to switch to one-year or two-year contracts to reduce churn.</li>
                <li><b>Improve Fiber Optic Service</b>: Investigate service quality issues for Fiber Optic customers and enhance support or pricing plans.</li>
                <li><b>Boost Referral Programs</b>: Strengthen referral incentives to increase customer engagement and loyalty.</li>
                <li><b>Flexible Pricing</b>: Introduce tiered pricing or loyalty discounts for high-paying customers to mitigate churn due to high monthly charges.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if "Satisfaction Score" in filtered_df.columns:
        satisfaction_analysis = filtered_df.groupby("Satisfaction Score").agg({
            "Churn": lambda x: (x == "Yes").sum(),
            "Satisfaction Score": "count"
        }).rename(columns={"Satisfaction Score": "Total"})
        satisfaction_analysis["Churn_Rate"] = (satisfaction_analysis["Churn"] / satisfaction_analysis["Total"] * 100).round(1)
        
        fig_satisfaction = px.bar(
            satisfaction_analysis.reset_index(),
            x="Satisfaction Score",
            y="Churn_Rate",
            title="Churn Rate by Satisfaction Score",
            color="Churn_Rate",
            color_continuous_scale=[[0, COLORS['success']], [1, COLORS['danger']]],
            text="Churn_Rate"
        )
        fig_satisfaction.update_traces(
            texttemplate='%{text}%', 
            textposition='outside',
            marker=dict(line=dict(color=COLORS['light'], width=1))
        )
        fig_satisfaction.update_layout(
            template='plotly_dark',
            font=dict(family="Inter", size=14, color=COLORS['primary']),
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['background'],
            title=dict(font=dict(size=20, color=COLORS['primary']), x=0.5),
            yaxis_title="Churn Rate (%)",
            showlegend=False,
            bargap=0.2
        )
        max_churn = satisfaction_analysis["Churn_Rate"].max()
        max_satisfaction = satisfaction_analysis["Churn_Rate"].idxmax()
        fig_satisfaction.add_annotation(
            x=max_satisfaction, y=max_churn, text=f"Highest churn: {max_churn:.1f}%",
            showarrow=True, arrowhead=1, yshift=10, font=dict(color=COLORS['primary'], size=12), bgcolor=COLORS['surface']
        )
        st.plotly_chart(fig_satisfaction, use_container_width=True)