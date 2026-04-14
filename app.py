import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Education Dashboard", layout="wide")

st.title("Indian Education Enrollment Dashboard")

df = pd.read_csv("data.csv")

if len(df.columns) < 2:
    st.error("CSV format incorrect. Please check data.csv")
    st.stop()

df.columns = ["State", "Enrollment"]

df["Enrollment"] = pd.to_numeric(df["Enrollment"], errors="coerce")
df = df.dropna()

states = df["State"].unique()

selected_states = st.multiselect("Select States", states)

if selected_states:
    df_filtered = df[df["State"].isin(selected_states)]
else:
    df_filtered = df

st.metric("Total Enrollment", int(df_filtered["Enrollment"].sum()))

fig, ax = plt.subplots()
ax.barh(df_filtered["State"], df_filtered["Enrollment"])
st.pyplot(fig)

if len(df_filtered) > 1:
    fig2, ax2 = plt.subplots()
    ax2.pie(df_filtered["Enrollment"], labels=df_filtered["State"], autopct="%1.1f%%")
    st.pyplot(fig2)
else:
    st.info("Select more than one state for pie chart")

st.dataframe(df_filtered)