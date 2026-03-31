import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Hiring Growth Model", layout="centered")

# ---------------- TITLE ----------------
st.title("📈 Corporate Hiring Growth Simulator")

st.markdown("""
This application simulates **employee hiring growth** using the **Logistic Growth Model**.
It shows how companies gradually reach maximum workforce capacity.
""")

# ---------------- THEORY ----------------
with st.expander("📘 Project Theory"):
    st.write("""
### Logistic Growth Model

The hiring process follows a logistic growth pattern:

- Slow hiring at the beginning
- Rapid growth in middle phase
- Saturation when workforce limit is reached

### Formula:

N(t) = K / (1 + ((K - N0)/N0) * e^(-rt))

Where:
- **K** = Maximum workforce capacity
- **N0** = Initial employees
- **r** = Growth rate
- **t** = Time (years)

### Output:
- Total employees over time
- New hires per year
""")

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("⚙️ Model Parameters")

max_workforce = st.sidebar.number_input("Max Workforce (K)", value=10000)
initial_hired = st.sidebar.number_input("Initial Employees (N0)", value=500)
growth_rate = st.sidebar.slider("Growth Rate (r)", 0.01, 1.0, 0.35)
years = st.sidebar.slider("Years", 5, 50, 20)

# ---------------- MODEL FUNCTION ----------------
def model_hiring_growth(K, N0, r, years):
    t = np.arange(0, years)

    hired = K / (1 + ((K - N0) / N0) * np.exp(-r * t))
    new_hires = np.diff(hired, prepend=N0)

    return t, hired, new_hires

# ---------------- RUN MODEL ----------------
time, total_employees, recruitment_plan = model_hiring_growth(
    max_workforce, initial_hired, growth_rate, years
)

# ---------------- GRAPH ----------------
st.subheader("📊 Hiring Growth Visualization")

plt.style.use('default')  # clean white background

fig, ax1 = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('white')

# Total Employees Line
ax1.plot(time, total_employees, linewidth=3)
ax1.set_xlabel("Years")
ax1.set_ylabel("Total Employees")

# Max limit line
ax1.axhline(y=max_workforce, linestyle='--')

# Secondary Axis (Bar)
ax2 = ax1.twinx()
ax2.bar(time, recruitment_plan, alpha=0.3)
ax2.set_ylabel("New Hires")

plt.title("Hiring Growth: Logistic Model")
st.pyplot(fig)

# ---------------- RESULTS ----------------
st.subheader("📌 Key Insights")

st.write(f"🔹 Final Workforce: **{int(total_employees[-1])}**")
st.write(f"🔹 Peak Hiring Year: **{int(time[np.argmax(recruitment_plan)])}**")
st.write(f"🔹 Max Hiring in a Year: **{int(max(recruitment_plan))}**")

# ---------------- DATA TABLE ----------------
st.subheader("📋 Data Table")

df = pd.DataFrame({
    "Year": time,
    "Total Employees": total_employees,
    "New Hires": recruitment_plan
})

st.dataframe(df)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("👨‍💻 Developed for Academic Project | Logistic Growth Simulation")
