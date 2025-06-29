from preswald import connect, get_df, table, text, plotly, slider
import pandas as pd
import plotly.express as px
from datetime import datetime

connect()
df = get_df("startup_funding")

if df is not None:
    # Data cleaning
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df['DateStr'] = df['Date'].dt.strftime('%Y-%m-%d')
    df['Amount'] = pd.to_numeric(df['Amount in INR(cr)'].str.replace(r'[^\d.]', ''), errors='coerce')
    df = df.dropna(subset=['Amount'])
    df = df[df['Amount'] > 0]

    # --- Visually centered and beautiful top section ---
    text("""
    
    
# 🚀

# **Indian Startup Funding Dashboard**

*Real-time insights into India's startup ecosystem*


""")
    # -------------------------------------------------

    # --- Rest of your dashboard code (unchanged) ---
    total_funding = df['Amount'].sum()
    avg_funding = df['Amount'].mean()
    total_startups = df['Startup'].nunique()
    total_cities = df['City'].nunique()

    text("## 📊 Key Metrics")
    text(f"""
- **💰 Total Funding:** ₹{total_funding:,.2f} Cr  
- **📈 Average Deal:** ₹{avg_funding:,.2f} Cr  
- **🏢 Funded Startups:** {total_startups:,}  
- **🌆 Active Cities:** {total_cities:,}
    """)

    text("## 💸 Filter by Minimum Funding Amount")
    amount_filter = slider(
        "Minimum Funding (Cr)",
        min_val=float(df['Amount'].min()),
        max_val=float(df['Amount'].max()),
        default=float(df['Amount'].min())
    )
    filtered_df = df[df['Amount'] >= amount_filter]

    text("## 🏙️ Top 10 Cities by Funding")
    city_data = filtered_df.groupby('City')['Amount'].sum().nlargest(10).reset_index()
    fig_city = px.bar(
        city_data, x='City', y='Amount',
        title="Top 10 Cities by Funding",
        template='plotly_white',
        color_discrete_sequence=['#2563eb']
    )
    plotly(fig_city)
    text("_These are the most funded cities for startups._")

    text("## 🧾 Investment Round Distribution")
    round_data = filtered_df.groupby('Investment Round')['Amount'].sum().reset_index()
    fig_round = px.pie(
        round_data, values='Amount', names='Investment Round',
        title="Share by Funding Round",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    plotly(fig_round)
    text("_Which funding stages dominate India's scene?_")

    text("## 🏭 Top 10 Industry Sectors")
    sector_data = filtered_df.groupby('Vertical')['Amount'].sum().nlargest(10).reset_index()
    fig_sector = px.bar(
        sector_data, x='Vertical', y='Amount',
        title="Top Industry Verticals",
        template='plotly_white',
        color_discrete_sequence=['#10b981']
    )
    plotly(fig_sector)
    text("_These verticals have received the most funding._")

    text("## 📋 Recent Funding Deals")
    display_cols = ['DateStr', 'Startup', 'Vertical', 'City', 'Investment Round', 'Amount in INR(cr)']
    table(filtered_df[display_cols].sort_values('DateStr', ascending=False))

    top_city = city_data.iloc[0]['City'] if not city_data.empty else "N/A"
    top_round = round_data.iloc[0]['Investment Round'] if not round_data.empty else "N/A"
    top_sector = sector_data.iloc[0]['Vertical'] if not sector_data.empty else "N/A"
    text("## 🔍 Key Insights")
    text(f"""
- 🏆 **Top City:** {top_city}  
- 💫 **Top Investment Round:** {top_round}  
- 🚀 **Top Sector:** {top_sector}  
- 📊 **Deals Displayed:** {len(filtered_df):,}
- 💸 **Filter:** Minimum ₹{amount_filter:,.2f} Cr
    """)

    text("---")
    text(f"*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*")
    text("*Powered by Preswald | User: DRAKEN-1974*")

else:
    text("# ❌ Error Loading Data")
    text("Please check your data source and configuration.")