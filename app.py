import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Education Dashboard", layout="wide")

st.title("Indian Education Enrollment Dashboard")

df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip()

df.rename(columns={
    df.columns[0]: "State",
    df.columns[1]: "Enrollment"
}, inplace=True)

df["Enrollment"] = pd.to_numeric(df["Enrollment"], errors="coerce")
df = df.dropna()

metro_states = [
    "Maharashtra",
    "Karnataka",
    "Tamil Nadu",
    "Telangana",
    "West Bengal",
    "Delhi"
]

df = df[df["State"].isin(metro_states)]

selected_states = st.multiselect("Select States", df["State"].unique())

if len(selected_states) > 0:
    df_filtered = df[df["State"].isin(selected_states)]
else:
    df_filtered = df

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Enrollment", int(df_filtered["Enrollment"].sum()))

with col2:
    st.metric("States Selected", len(df_filtered["State"].unique()))

st.subheader("State-wise Enrollment")

fig, ax = plt.subplots(figsize=(8, 5))
df_filtered = df_filtered.sort_values(by="Enrollment", ascending=True)

ax.barh(df_filtered["State"], df_filtered["Enrollment"])
ax.set_xlabel("Enrollment")
ax.set_ylabel("State")

st.pyplot(fig)

st.subheader("Enrollment Distribution")

fig2, ax2 = plt.subplots(figsize=(6, 6))

ax2.pie(
    df_filtered["Enrollment"],
    labels=df_filtered["State"],
    autopct="%1.1f%%"
)

st.pyplot(fig2)

st.subheader("Dataset Preview")
st.dataframe(df_filtered)
        