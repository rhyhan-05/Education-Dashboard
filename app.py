import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Education Dashboard", layout="wide")

st.title("Indian Education Enrollment Dashboard")

df = pd.read_csv("data.csv")
df.columns = ["State", "Enrollment"]
df["Enrollment"] = pd.to_numeric(df["Enrollment"], errors="coerce")
df = df.dropna()

states = df["State"].unique()

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"

def go_dashboard():
    st.session_state.page = "dashboard"

if st.session_state.page == "home":
    st.subheader("Select States")
    selected_states = st.multiselect("Choose States", states)

    if st.button("Show Dashboard"):
        st.session_state.selected_states = selected_states
        go_dashboard()

elif st.session_state.page == "dashboard":
    st.button("⬅ Back", on_click=go_home)

    selected_states = st.session_state.get("selected_states", states)

    if selected_states:
        df_filtered = df[df["State"].isin(selected_states)]
    else:
        df_filtered = df

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Enrollment", int(df_filtered["Enrollment"].sum()))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(df_filtered["State"], df_filtered["Enrollment"])
    ax.set_xlabel("Enrollment")
    ax.set_ylabel("State")
    st.pyplot(fig)

    if len(df_filtered) > 1:
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(
            df_filtered["Enrollment"],
            labels=df_filtered["State"],
            autopct="%1.1f%%"
        )
        st.pyplot(fig2)
    else:
        st.info("Pie chart requires more than one state")

    st.subheader("Dataset Preview")
    st.dataframe(df_filtered)