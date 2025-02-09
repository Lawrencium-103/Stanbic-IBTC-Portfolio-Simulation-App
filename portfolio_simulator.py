import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ---- Global Styling ----
st.markdown(
    """
    <style>
    body {
        font-family: "Century Gothic", sans-serif; /* Century Gothic or fallback */
        color: <Change this Text Colour to all aspects of the web pages>;
        background-color: <Colour code for what you need>; /* Light blue background */
    }
    h1, h2, h3 {
        color: <Colour Code that you want for the title>; /* Dark Blue */
    }
    /* Sidebar background and text color */
    [data-testid="stSidebar"] {
        background-color: #F0F8FF; /* Light blue sidebar */
        color: <Make the colour here 
        change from White or any text that you do not want here>;
    }

    /* Sidebar text set to Black */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: <This code is a reference - all code must match,
    so please change - and let me know how we can improve the style for your website >;
    }

    /* Adjust slider color */
    .stSlider>div>div>div>div {
        background-color: <Adjustments to create an even better UI/;
    }
    /* Style radio buttons*/
    .stRadio > label {
        color: <Change>; /* This will be the main colour*/
        font-weight: normal;
    }

    /* Bold text - a different colour - make sure it follows all themes*/
    b, strong {
        color:  /* A brighter blue - edit this to make it fit your new change */ !important;
    }
    [data-baseweb="select"] > div { /* Change the text for you to follow*/
        border-color: <Please find a great colour for your theme - that we are looking to solve> ;
        color: <Change the text colour to whatever you desire to change here>;
    }

    /* Dataframe styling (Black Text on standard background*/
    .dataframe th {
        background-color: #D0DAE0 !important;
        color: #000000 !important;
    }
    .dataframe td {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Helper Functions ----
def simulate_portfolio(principal, years, money_market_allocation, equity_fund_allocation, money_market_return, equity_fund_return):
    """Simulates portfolio performance over time."""
    data = []
    total_value = principal
    for year in range(years):
        mm_investment = total_value * money_market_allocation
        eq_investment = total_value * equity_fund_allocation

        mm_profit = mm_investment * money_market_return
        eq_profit = eq_investment * equity_fund_return

        total_profit = mm_profit + eq_profit
        total_value += total_profit

        data.append({
            "Year": year + 1,
            "Money Market Return": mm_profit,
            "Equity Fund Return": eq_profit,
            "Total Profit": total_profit,
            "Total Value": total_value,
        })

    df = pd.DataFrame(data)

    # Calculate monthly and quarterly returns
    df["Monthly Return"] = df["Total Profit"] / 12
    df["Quarterly Return"] = df["Total Profit"] / 4

    return df

# ---- Title and Introduction ----
st.title("Portfolio Simulation for Stanbic IBTC Funds")
st.write("""
This app simulates potential investment returns for a portfolio consisting of the 
Stanbic IBTC Money Market Fund and the Stanbic IBTC Nigerian Equity Fund. 
It's for illustrative purposes only and not financial advice."https://www.stanbicibtcfundsmanagement.com/invest-now-4ev6leqy/"
""")

# ---- Home Page ----
def home_page():
    st.title("Portfolio Simulation")
    st.write("""
    Explore potential investment returns. Higher Equity Allocation increases potential profits, but also significantly increases risk of losses.
    """)

    # ---- User Inputs ----
    with st.sidebar:
        st.header("Simulation Parameters")

        principal = st.number_input("Initial Investment (Naira)", min_value=5000, value=2000000, step=1000)
        years = st.slider("Investment Horizon (Years)", min_value=1, max_value=100, value=2, step=1)

        risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])

        # Define allocation based on risk level
        if risk_level == "Low":
            money_market_allocation = 1.0  # 100%
            equity_fund_allocation = 0.0  # 0%
        elif risk_level == "Medium":
            money_market_allocation = 0.7  # 70%
            equity_fund_allocation = 0.3  # 30%
        else:
            money_market_allocation = 0.3  # 30%
            equity_fund_allocation = 0.7  # 70%

        st.header("Performance Assumptions (Annual)")

        # Base Returns
        money_market_return = st.number_input("Money Market Return (%)", min_value=-20.0, max_value=50.0, value=22.01, step=0.1) / 100
        equity_fund_return = st.number_input("Equity Fund Return (%)", min_value=-20.0, max_value=50.0, value=35.49, step=0.1) / 100

        # Scenario selection (Radio Buttons)
        market_scenario = st.radio("Market Scenario", ["Base Case", "Bear Market", "Moderate Market", "Stagnant Market"])

        # Adjust returns based on scenario
        if market_scenario == "Bear Market":
            mm_return = st.number_input("Bear Market MM Return (%)", value=15.0, step=0.1) / 100
            eq_return = st.number_input("Bear Market EQ Return (%)", value=-15.0, step=0.1) / 100
        elif market_scenario == "Moderate Market":
            mm_return = st.number_input("Moderate MM Return (%)", value=20.0, step=0.1) / 100
            eq_return = st.number_input("Moderate EQ Return (%)", value=20.0, step=0.1) / 100
        elif market_scenario == "Stagnant Market":
            mm_return = st.number_input("Stagnant MM Return (%)", value=18.0, step=0.1) / 100
            eq_return = st.number_input("Stagnant EQ Return (%)", value=5.0, step=0.1) / 100
        else:  # Base Case
            mm_return = money_market_return
            eq_return = equity_fund_return

        # ---- Simulation ----
        df_results = simulate_portfolio(principal, years, money_market_allocation, equity_fund_allocation, mm_return, eq_return)

    # ---- Main Content ----
    st.header("Simulation Results")

    # Calculate Gross Principal
    gross_principal = df_results["Total Value"].iloc[-1]
    profit = gross_principal - principal
    profit_color = "green" if profit >= 0 else "red"  # Determine color based on profit

    st.markdown(f"<h3 style='text-align: center; color: {profit_color};'>Gross Principal: {gross_principal:,.2f} Naira ({market_scenario})</h3>", unsafe_allow_html=True)

    st.subheader("Key Parameters")
    st.write(f"**Initial Principal:** {principal:,.2f} Naira")
    st.write(f"**Investment Horizon:** {years} Years")
    st.write(f"**Risk Level:** {risk_level}")
    st.write(f"**Money Market Allocation:** {money_market_allocation*100:.0f}%")
    st.write(f"**Equity Fund Allocation:** {equity_fund_allocation*100:.0f}%")
    st.write(f"**Money Market Return:** {mm_return*100:.2f}%")
    st.write(f"**Equity Fund Return:** {eq_return*100:.2f}%")

    st.subheader("Returns Summary")
    st.dataframe(df_results[["Year", "Monthly Return", "Quarterly Return", "Total Profit", "Total Value"]].style.format("{:,.2f}"))

    # ---- Charts ----
    st.subheader("Portfolio Value Over Time ({})".format(market_scenario))

    # Find the global minimum and maximum values for all your markets
    global_min = min(df_results["Total Value"].min(), principal)
    global_max = df_results["Total Value"].max()

    # Create the Altair Chart
    chart = alt.Chart(df_results).mark_area(
        color='#ADD8E6',  # set area color to a slightly light navy/blue
        opacity=0.3  # Set opacity to 30%
    ).encode(
        x=alt.X('Year:O', title="Year"),
        y=alt.Y('Total Value:Q',
            title="Total Value",
            scale=alt.Scale(domain=[global_min, global_max])  # Set the scale
        )
    ).properties(
        width=700,
        height=400
    )

    # Add a horizontal line at y=0
    rule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='red').encode(y='y:Q')

    # Overlay the chart with the rule
    st.altair_chart(chart + rule, use_container_width=True)

    st.subheader("Profit Over Time ({})".format(market_scenario))
    # Display the chart, mapping the 'Profit Color' column to the area chart
    st.line_chart(df_results[["Year", "Total Profit"]].set_index("Year"))

    # Disclaimer Section at bottom
    st.markdown("---")
    st.markdown("**Disclaimer:** This app is for educational purposes only and does not provide financial advice. Consult with a qualified professional before making investment decisions.")

# ---- About Me Page ----
def about_me_page():
    st.title("About Me: Lawrence Oladeji")
    st.write("""
    This app was created by me, Lawrence Oladeji, to explore the simulation of financial instrument portfolio performance.
    """)

    st.header("Lawrence Oladeji")
    st.write("Contact: oladeji.lawrence@gmail.com, +234 9038819790")

    st.subheader("Experience")
    st.write("""
        Seeking to leverage proven analytical and technical skills within a forward-thinking fintech or financial asset management environment. Core competencies include:
        """)

    st.markdown("""
        *   **Data Analysis & Insight Generation:**
            *   Identifying key trends, anomalies, and actionable insights from complex datasets.
            *   Proficient in statistical analysis and data visualization techniques.
            *   Adaptable to various financial datasets (market data, portfolio performance, risk metrics).
        *   **Cloud Proficiency:**
            *   Supported data engineer with cloud storage task in Google Cloud Platform, Azure, and AWS.
            *   Supported data engineer in building and managing scalable cloud-based data infrastructure.
            *   Contributed to data movement, data storage, ETL processes, automation, and data pipeline tasks discussing, useful for management to make decison.
        *   **Analytical Toolset:**
            *   Proficient with tools like Excel, Google Sheets, Power BI, Tableau, R, and Python.
            *   Skilled in financial modeling, reporting, and predictive analytics (including Machine Learning).
        *   **Process Optimization with AI:**
            *   Designing and implementing Standard Operating Procedures using AI no-code tools (ChatGPT, TeamGPT, Activepieces).
            *   Streamlining data curation and improving efficiency for data-driven tasks.
        *   **Data Quality & Reliability:**
            *   Expertise in data triangulation project(designed data variability template including 5 metrics)
            *   Ensuring all data used are sound, reliable, and accurate before using it to make decisions.
        """)

    st.subheader("Key Strengths")
    st.write("""
        *   Data-Driven Decision Making
        *   Technical Proficiency and Adaptability
        *   Problem Solving and Innovation
        *   Communication and Collaboration
        """)

    # Disclaimer Section at bottom
    st.markdown("---")  # Visual separator
    st.markdown("**Disclaimer:** This app is for educational purposes only and does not provide financial advice. Consult with a qualified professional before making investment decisions.")


# ---- Main App Flow ----
def app():
    # Navigation
    page = st.sidebar.radio("Navigation", ["Simulator", "About Me"])

    if page == "Simulator":
        home_page()
    elif page == "About Me":
        about_me_page()

# ---- Run the App ----
if __name__ == "__main__":
    app()