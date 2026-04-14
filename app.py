import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Education Dashboard")

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

if "show_bar" not in st.session_state:
    st.session_state.show_bar = False

if "show_pie" not in st.session_state:
    st.session_state.show_pie = False

if "show_data" not in st.session_state:
    st.session_state.show_data = False

st.sidebar.title("Controls")

selected_states = st.sidebar.multiselect(
    "Select States",
    metro_states
)

if st.sidebar.button("Show Bar Graph"):
    st.session_state.show_bar = True
    st.session_state.show_pie = False
    st.session_state.show_data = False

if st.sidebar.button("Show Pie Chart"):
    st.session_state.show_pie = True
    st.session_state.show_bar = False
    st.session_state.show_data = False

if st.sidebar.button("Show Data"):
    st.session_state.show_data = True
    st.session_state.show_bar = False
    st.session_state.show_pie = False

if st.button("Back / Reset"):
    st.session_state.show_bar = False
    st.session_state.show_pie = False
    st.session_state.show_data = False
    selected_states = []

if selected_states:
    df_filtered = df[df["State"].isin(selected_states)]
else:
    df_filtered = df

if st.session_state.show_bar:
    st.subheader("State-wise Enrollment")
    df_bar = df_filtered.sort_values(by="Enrollment", ascending=True)

    fig, ax = plt.subplots()
    ax.barh(df_bar["State"], df_bar["Enrollment"])
    ax.set_xlabel("Enrollment")
    ax.set_ylabel("State")

    st.pyplot(fig)

if st.session_state.show_pie:
    if len(selected_states) <= 1:
        st.warning("Select at least 2 states to view Pie Chart")
    else:
        st.subheader("Enrollment Distribution")

        fig2, ax2 = plt.subplots()
        ax2.pie(
            df_filtered["Enrollment"],
            labels=df_filtered["State"],
            autopct="%1.1f%%"
        )

        st.pyplot(fig2)

if st.session_state.show_data:
    st.subheader("Dataset")
    st.dataframe(df_filtered)