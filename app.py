import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Smart Dashboard", layout="wide")

st.title("Smart Education Dashboard")

# Load data
df = pd.read_csv("data.csv")

df = df.rename(columns={
    'India/State/ UT': 'State',
    'Enrolment - Private Unaided Recognized - Total (Pre-Primary to Higher Secondary) - Total': 'Enrollment'
})

df = df[df['State'] != 'India']

# Metro states
metro_states = [
    "Maharashtra", "Delhi", "Karnataka",
    "Tamil Nadu", "Telangana", "West Bengal"
]

df = df[df['State'].isin(metro_states)]

#  STATE SELECTION
selected_states = st.multiselect(
    "Select Metro States",
    df['State'].unique(),
    default=[]
)

filtered_df = df[df['State'].isin(selected_states)]

# BUTTON CONTROL (FIXED LOGIC)
if "mode" not in st.session_state:
    st.session_state.mode = None

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(" Data"):
        st.session_state.mode = "data"

with col2:
    if st.button("Graph"):
        st.session_state.mode = "graph"

with col3:
    if st.button(" Pie"):
        st.session_state.mode = "pie"

# KPI
if len(filtered_df) > 0:
    st.metric("Total Enrollment", int(filtered_df['Enrollment'].sum()))

# OUTPUT CONTROL (ONLY ONE SHOWS)
if st.session_state.mode == "data":
    st.subheader(" Data")
    st.dataframe(filtered_df)

elif st.session_state.mode == "graph":
    st.subheader(" Graph")

    fig, ax = plt.subplots()
    filtered_df.sort_values('Enrollment').plot(
        kind='barh', x='State', y='Enrollment', ax=ax
    )
    st.pyplot(fig)

elif st.session_state.mode == "pie":
    st.subheader(" Pie Chart")

    fig, ax = plt.subplots()
    ax.pie(
        filtered_df['Enrollment'],
        labels=filtered_df['State'],
        autopct='%1.1f%%'
    )
    st.pyplot(fig)

# Insights (separate button)
if st.button(" Insights"):
    if len(filtered_df) > 0:
        top = filtered_df.sort_values('Enrollment', ascending=False).iloc[0]['State']
        st.success(f"{top} has highest enrollment.")
        