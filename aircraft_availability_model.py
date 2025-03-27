
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aircraft Availability Impact Model", layout="centered")

st.title("Aircraft Availability Impact Due to Tariff-Driven Sustainment Cost Increases")

st.markdown("""
This model estimates how aircraft availability rates (A-rates) change when sustainment budgets are not increased to match tariff-driven cost increases. 
You can toggle between linear and nonlinear elasticity to observe the different effects on readiness.
""")

# Inputs
st.sidebar.header("Input Assumptions")
base_avail = st.sidebar.slider("Baseline Aircraft Availability Rate (%)", 50, 90, 70)
sustainment_increase = st.sidebar.slider("Tariff-Driven Sustainment Cost Increase (%)", 0, 50, 15)
elasticity = st.sidebar.slider("Linear Elasticity (Availability per % Part Reduction)", 0.1, 1.0, 0.5)
nonlinear_factor = st.sidebar.slider("Nonlinear Exponent", 1.0, 3.0, 1.8)

# Toggle
model_type = st.radio("Choose elasticity model:", ["Linear", "Nonlinear"])

# Calculate part reduction (inverse of purchasing power)
part_reduction_pct = 1 - (1 / (1 + sustainment_increase / 100))

if model_type == "Linear":
    availability_drop = part_reduction_pct * elasticity * 100
else:
    availability_drop = (part_reduction_pct ** nonlinear_factor) * 100

new_avail = max(0, base_avail - availability_drop)

# Display Results
st.metric(label="Estimated New Aircraft Availability Rate (%)", value=f"{new_avail:.1f}")

# Plotting
x = np.linspace(0, 50, 100)
x_part_reduction = 1 - (1 / (1 + x / 100))

linear_impact = base_avail - (x_part_reduction * elasticity * 100)
nonlinear_impact = base_avail - ((x_part_reduction ** nonlinear_factor) * 100)

fig, ax = plt.subplots()
ax.plot(x, linear_impact, label="Linear Elasticity", linestyle="--")
ax.plot(x, nonlinear_impact, label=f"Nonlinear Elasticity (exp={nonlinear_factor})", linewidth=2)
ax.set_xlabel("Sustainment Cost Increase (%)")
ax.set_ylabel("Resulting Aircraft Availability Rate (%)")
ax.set_title("Aircraft Availability Degradation")
ax.set_ylim(0, 100)
ax.legend()
st.pyplot(fig)
