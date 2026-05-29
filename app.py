import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Chennai Budget Insights", layout="wide")
st.title("📊 Chennai Metropolitan Multi-Level Budget Dashboard (2024-25)")
st.write("Comparing localized Corporation spending against State and Union allocations.")


@st.cache_data
def load_corp_data():
    return pd.read_csv("A_corporation_line_items_reclassified.csv")

@st.cache_data
def load_cross_level_data():
    return pd.read_csv("C_all_levels_2024_25.csv")

df_corp = load_corp_data()
df_all = load_cross_level_data()


tab1, tab2 = st.tabs(["🏙️ Chennai Corporation Analysis", "🏛️ Cross-Level Comparisons (Corp vs. State vs. Union)"])


with tab1:
    
    total_budget = df_corp['amount_crore'].sum()
    infra_budget = df_corp[df_corp['simplified_sector'] == 'infrastructure']['amount_crore'].sum()
    infra_percentage = (infra_budget / total_budget) * 100

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Corporation Budget", f"₹{total_budget:,.2f} Cr")
    with col2:
        st.metric("Reclassified Infrastructure (Goods)", f"₹{infra_budget:,.2f} Cr")
    with col3:
        st.metric("Infrastructure Share", f"{infra_percentage:.1f}%")

    st.markdown("---")

    st.subheader("Spending Breakdown by Simplified Sector")
    summary = df_corp.groupby('simplified_sector')['amount_crore'].sum().reset_index()
    summary = summary.sort_values(by='amount_crore', ascending=True)

    fig1 = px.bar(
        summary, 
        x='amount_crore', 
        y='simplified_sector', 
        orientation='h',
        labels={'amount_crore': 'Amount (in ₹ Crores)', 'simplified_sector': 'Sector'},
        text_auto='.2s',
        color='amount_crore',
        color_continuous_scale='Viridis'
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, width='stretch')

    st.subheader("Explore Reclassified Line Items")
    st.dataframe(df_corp, width='stretch')


with tab2:
    st.subheader("Budget Allocations Across Different Levels of Government")
    st.write("Select a level of government to view its respective sector budget breakdown.")

    
    level_choice = st.selectbox("Select Government Level:", ["corporation", "state", "union"])
    
    
    filtered_df = df_all[df_all['level'] == level_choice]
    sector_summary = filtered_df.groupby('sector')['amount_crore'].sum().reset_index()
    sector_summary = sector_summary.sort_values(by='amount_crore', ascending=False)
    
    
    level_total = sector_summary['amount_crore'].sum()
    sector_summary['percentage'] = (sector_summary['amount_crore'] / level_total) * 100

    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        fig2 = px.pie(
            sector_summary, 
            values='amount_crore', 
            names='sector', 
            title=f"Sector Share for {level_choice.upper()} Budget (Total: ₹{level_total:,.2f} Cr)",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Plotly3
        )
        st.plotly_chart(fig2, width='stretch')
        
    with col_right:
        st.write(f"**Top Spending Sectors ({level_choice.capitalize()}):**")
        st.dataframe(
            sector_summary[['sector', 'amount_crore', 'percentage']].style.format({
                'amount_crore': '₹{:,.2f} Cr',
                'percentage': '{:.2f}%'
            }),
            width='stretch'
        )