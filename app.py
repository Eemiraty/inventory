import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Supply Chain EOQ Optimizer", layout="wide")

st.title("Supply Chain & Inventory Optimizer")
st.markdown("Interactive decision-support tool for calculating optimal order quantities (EOQ) and safety stock levels.")

# Sidebar input parameters
st.sidebar.header("Input Parameters")
demand = st.sidebar.number_input("Annual Demand (units, D)", min_value=100, max_value=500000, value=10000, step=500)
order_cost = st.sidebar.number_input("Fixed Order Cost ($/order, S)", min_value=1.0, max_value=1000.0, value=50.0, step=5.0)
holding_cost = st.sidebar.number_input("Holding Cost ($/unit/year, H)", min_value=0.1, max_value=100.0, value=4.0, step=0.5)
lead_time_days = st.sidebar.slider("Lead Time (days, L)", min_value=1, max_value=60, value=10)
service_level = st.sidebar.selectbox(
    "Service Level (Z-score)", 
    options=[("90% (Z=1.28)", 1.28), ("95% (Z=1.65)", 1.65), ("99% (Z=2.33)", 2.33)], 
    format_func=lambda x: x[0]
)[1]
daily_std_dev = st.sidebar.number_input("Daily Demand Standard Deviation (units, σ)", min_value=0.0, max_value=100.0, value=5.0)

# Calculations: Economic Order Quantity (EOQ) & Annual Costs
eoq = np.sqrt((2 * demand * order_cost) / holding_cost)
annual_orders = demand / eoq
total_order_cost = annual_orders * order_cost
total_holding_cost = (eoq / 2) * holding_cost
total_inventory_cost = total_order_cost + total_holding_cost

# Calculations: Safety Stock & Reorder Point (ROP)
workdays_per_year = 250
daily_demand = demand / workdays_per_year
safety_stock = service_level * daily_std_dev * np.sqrt(lead_time_days)
reorder_point = (daily_demand * lead_time_days) + safety_stock

# Metric cards display
col1, col2, col3, col4 = st.columns(4)
col1.metric("Optimal Lot Size (EOQ)", f"{int(eoq):,} units")
col2.metric("Orders per Year", f"{annual_orders:.1f}")
col3.metric("Safety Stock", f"{int(safety_stock):,} units")
col4.metric("Reorder Point (ROP)", f"{int(reorder_point):,} units")

st.divider()

# Cost curves visualization
q_range = np.linspace(max(10, int(eoq * 0.2)), int(eoq * 2.5), 200)
order_costs = (demand / q_range) * order_cost
holding_costs = (q_range / 2) * holding_cost
total_costs = order_costs + holding_costs

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(q_range, order_costs, label="Annual Ordering Cost", linestyle="--", color="gray")
ax.plot(q_range, holding_costs, label="Annual Holding Cost", linestyle="--", color="darkorange")
ax.plot(q_range, total_costs, label="Total Cost", color="navy", linewidth=2)
ax.axvline(eoq, color="crimson", linestyle=":", label=f"Optimal Quantity (EOQ = {int(eoq)})")

ax.set_xlabel("Order Quantity (Q)")
ax.set_ylabel("Annual Logistics Cost ($)")
ax.set_title("Inventory Cost Trade-off as a Function of Order Quantity")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)