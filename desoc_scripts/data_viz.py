import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and introduction
st.title("Farcaster")
st.write("This dashboard examines some Farcaster user behaviour in different timeframes.")

# Load the data
casts_by_hour = pd.read_csv("casts_by_hour.csv")
casts_by_day_of_week = pd.read_csv("casts_by_day_of_week.csv")
casts_by_month = pd.read_csv("casts_by_month.csv")

# Layout the columns
col1, col2 = st.columns((3,2))

# Column 1: Visualization by Month
with col1:
    # counter
    total_replies = casts_by_month["reply_c"].sum()
    total_casts = casts_by_month["casts_c"].sum()
    total = total_replies + total_casts
    st.markdown(f'<div style="font-size:24px;text-align:center;"><strong>total posts:</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:36px;text-align:center;color:purple;"><strong>{total}</strong></div>', unsafe_allow_html=True)
    # barchart
    st.markdown(f'<div style="font-size:24px;text-align:center;"><strong>posts over time</strong></div>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    # Bar chart for Casts and Replies
    ax.bar(casts_by_month["month"], casts_by_month["casts_c"], label="Casts", alpha=0.7, color='purple')
    ax.bar(casts_by_month["month"], casts_by_month["reply_c"], label="Replies", alpha=0.7, bottom=casts_by_month["casts_c"], color='pink')
    # Create a second Y axis
    ax2 = ax.twinx()
    ax2.plot(casts_by_month["month"], casts_by_month["rolling_sum"], label="Rolling Sum", color='black', linestyle='-')
    ax2.set_ylabel("Rolling Sum")
    # Set labels, legend, and display the plot
    ax.set_xlabel("Month")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")
    st.pyplot(fig)


# Column 2: Visualization by Hour
with col2:
    
    st.markdown(f'<div style="font-size:24px;text-align:center;"><strong>posts by hour </strong></div>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(casts_by_hour["hour"], casts_by_hour["casts_c"], label="Casts", alpha=0.7, color='purple')
    ax.bar(casts_by_hour["hour"], casts_by_hour["reply_c"], label="Replies", alpha=0.7, color='pink', bottom=casts_by_hour["casts_c"])
    ax.set_xlabel("Hour")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Visualization by Day of Week
    st.markdown(f'<div style="font-size:24px;text-align:center;"><strong>posts by day</strong></div>', unsafe_allow_html=True)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    fig, ax = plt.subplots()
    ax.bar(casts_by_day_of_week["day_of_week"], casts_by_day_of_week["casts_c"], label="Casts", alpha=0.7, color='purple')
    ax.bar(casts_by_day_of_week["day_of_week"], casts_by_day_of_week["reply_c"], label="Replies", alpha=0.7, color='pink', bottom=casts_by_day_of_week["casts_c"])
    ax.set_xticks(list(range(7)))
    ax.set_xticklabels(days)
    ax.set_ylabel("Count")
    st.pyplot(fig)
