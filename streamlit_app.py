
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="USAF Tariff Impact Model", layout="wide")

st.title("USAF Aircraft Tariff Impact Estimator (2025–2050)")

# Sidebar Inputs
st.sidebar.header("Tariff & Cost Assumptions")
steel_tariff = st.sidebar.slider("Steel/Aluminum Tariff (%)", 0, 50, 25)
component_tariff = st.sidebar.slider("Component Tariff (%)", 0, 50, 25)
china_tariff = st.sidebar.slider("China Blanket Tariff (%)", 0, 30, 20)
pass_through = st.sidebar.slider("Pass-Through to DoD (%)", 0, 100, 75)

st.sidebar.header("Base Cost & Growth Assumptions")
aircraft_cost = st.sidebar.number_input("Base Aircraft Cost (USD Millions)", 10, 300, 90)
procure_growth = st.sidebar.slider("Annual Procurement Growth Rate (%)", 0.0, 10.0, 4.0)
sustainment_base = st.sidebar.number_input("Sustainment Base Cost (USD Millions)", 100, 5000, 1200)
forecast_years = st.sidebar.slider("Forecast Horizon (Years)", 4, 25, 25)

# Constants
years = list(range(2025, 2025 + forecast_years))
material_share = 0.15
component_share = 0.25
china_share = 0.10

# Calculations
results = []
for i, year in enumerate(years):
    growth_factor = (1 + procure_growth / 100) ** i
    mat_cost = aircraft_cost * material_share * (steel_tariff / 100)
    comp_cost = aircraft_cost * component_share * (component_tariff / 100)
    chn_cost = aircraft_cost * china_share * (china_tariff / 100)
    total_procure_delta = (mat_cost + comp_cost + chn_cost) * (pass_through / 100)
    total_procure_delta *= growth_factor

    sustainment_delta = sustainment_base * 0.25 * (pass_through / 100) * (1 + 0.025) ** i

    results.append({
        "Year": year,
        "Procurement Impact ($M)": round(total_procure_delta, 2),
        "Sustainment Impact ($M)": round(sustainment_delta, 2),
        "Total Annual Impact ($M)": round(total_procure_delta + sustainment_delta, 2)
    })

df = pd.DataFrame(results)

# Output: Table
st.subheader("Annual Tariff-Related Cost Impact")
st.dataframe(df.set_index("Year"))

# Output: Graph
st.subheader("Cost Impact Over Time")
fig, ax = plt.subplots()
ax.plot(df["Year"], df["Procurement Impact ($M)"], label="Procurement", marker='o')
ax.plot(df["Year"], df["Sustainment Impact ($M)"], label="Sustainment", marker='o')
ax.plot(df["Year"], df["Total Annual Impact ($M)"], label="Total", linestyle='--', marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Cost Impact ($M)")
ax.set_title("Projected Tariff-Related Cost Impact (2025–{})".format(years[-1]))
ax.legend()
st.pyplot(fig)

# Cumulative Impact
cumulative_cost = df["Total Annual Impact ($M)"].sum()
st.subheader(f"Total Cumulative Impact (2025–{years[-1]}): **${cumulative_cost:,.2f}M**")
