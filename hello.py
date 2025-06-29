from preswald import connect, get_df, table, text, plotly, slider
import pandas as pd
import plotly.express as px
from datetime import datetime

connect()
df = get_df("startup_funding")

if df is not None:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df['DateStr'] = df['Date'].dt.strftime('%Y-%m-%d')
    df['Amount'] = pd.to_numeric(
        df['Amount in INR(cr)'].str.replace(r'[^\d.]', '', regex=True), errors='coerce'
    )
    df = df.dropna(subset=['Amount'])
    df = df[df['Amount'] > 0]

    text(
        "# Indian Startup Funding Dashboard\n"
        "*Real-time insights into India's startup ecosystem*"
    )

    total_funding = df['Amount'].sum()
    avg_funding = df['Amount'].mean()
    total_startups = df['Startup'].nunique()
    total_cities = df['City'].nunique()

    text("## Key Metrics\n")
    text(
        "| Metric               | Value                |\n"
        "|----------------------|---------------------|\n"
        f"| **Total Funding**    | ₹{total_funding:,.0f} Cr |\n"
        f"| **Average Deal Size**| ₹{avg_funding:,.2f} Cr |\n"
        f"| **Funded Startups**  | {total_startups:,}         |\n"
        f"| **Active Cities**    | {total_cities:,}           |"
    )

    text("## Recent Funding Deals")
    display_cols = ['DateStr', 'Startup', 'Vertical', 'City', 'Investment Round', 'Amount in INR(cr)']
    table(df[display_cols].sort_values('DateStr', ascending=False))

    text("## Filter by Minimum Funding Amount")
    amount_filter = slider(
        "Minimum Funding (Cr)",
        min_val=float(df['Amount'].min()),
        max_val=float(df['Amount'].max()),
        default=float(df['Amount'].min())
    )
    filtered_df = df[df['Amount'] >= amount_filter]

    text("## Top 10 Cities by Funding")
    city_data = filtered_df.groupby('City')['Amount'].sum().nlargest(10).reset_index()
    fig_city = px.bar(
        city_data, x='City', y='Amount',
        title="Top 10 Cities by Funding",
        template='plotly_white',
        color_discrete_sequence=['#2563eb']
    )
    plotly(fig_city)
    text("_These cities have attracted the most startup funding._")

    text("## Investment Round Distribution")
    round_data = filtered_df.groupby('Investment Round')['Amount'].sum().reset_index()
    round_data = round_data.sort_values('Amount', ascending=False)
    top_n = 5
    if len(round_data) > top_n:
        top_rounds = round_data.head(top_n)
        other = pd.DataFrame({
            'Investment Round': ['Other'],
            'Amount': [round_data['Amount'][top_n:].sum()]
        })
        round_data_display = pd.concat([top_rounds, other], ignore_index=True)
    else:
        round_data_display = round_data

    fig_round = px.pie(
        round_data_display,
        values='Amount',
        names='Investment Round',
        title="Share by Top Investment Rounds",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_round.update_traces(textinfo='percent+label')
    fig_round.update_layout(title_x=0.5)
    plotly(fig_round)
    text("_Distribution of funding across different investment rounds._")

    text("## Top 10 Industry Sectors")
    sector_data = filtered_df.groupby('Vertical')['Amount'].sum().nlargest(10).reset_index()
    fig_sector = px.bar(
        sector_data, x='Vertical', y='Amount',
        title="Top Industry Verticals",
        template='plotly_white',
        color_discrete_sequence=['#10b981']
    )
    plotly(fig_sector)
    text("_Sectors with the highest total funding._")

    top_city = city_data.iloc[0]['City'] if not city_data.empty else "N/A"
    top_round = round_data.iloc[0]['Investment Round'] if not round_data.empty else "N/A"
    top_sector = sector_data.iloc[0]['Vertical'] if not sector_data.empty else "N/A"
    text("## Insights Summary")
    text(
        f"**Top City:** {top_city}  \n"
        f"**Top Investment Round:** {top_round}  \n"
        f"**Top Sector:** {top_sector}  \n"
        f"**Deals Displayed:** {len(filtered_df):,}  \n"
        f"**Applied Filter:** Minimum ₹{amount_filter:,.2f} Cr"
    )

    text("---")
    text(f"*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*")
    text("*Powered by Preswald*")

else:
    text("# Error Loading Data")
    text("Please check your data source and configuration.")