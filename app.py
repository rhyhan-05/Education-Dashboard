import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Education Dashboard", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("Metro Cities Education Dashboard")

df_original = pd.read_csv("data.csv")
df_original.columns = df_original.columns.str.strip()

df = df_original.copy()

metro_states = [
    "Maharashtra",
    "Karnataka",
    "Tamil Nadu",
    "Telangana",
    "West Bengal",
    "Delhi"
]

state_col = df.columns[0]
df = df[df[state_col].isin(metro_states)]

for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

st.sidebar.title("Filters")

selected_states = st.sidebar.multiselect(
    "Select Metro States",
    df[state_col].unique(),
    default=df[state_col].unique()
)

selected_column = st.sidebar.selectbox(
    "Select Data Column",
    numeric_cols
)

df_filtered = df[df[state_col].isin(selected_states)]

if "view" not in st.session_state:
    st.session_state.view = None

st.markdown("### Dashboard Controls")

col1, col2, col3, col4 = st.columns(4)

if col1.button("Bar Graph"):
    st.session_state.view = "bar"

if col2.button("Pie Chart"):
    st.session_state.view = "pie"

if col3.button("Boxplot"):
    st.session_state.view = "box"

if col4.button("Data"):
    st.session_state.view = "data"

col5, col6 = st.columns(2)

if col5.button("Boys vs Girls"):
    st.session_state.view = "gender"

if col6.button("Reset"):
    st.session_state.view = None

st.markdown("### Key Metrics")

total_value = df_filtered[selected_column].sum()

c1, c2 = st.columns(2)
c1.metric("Selected Category Total", int(total_value))
c2.metric("States Selected", len(selected_states))

if st.session_state.view == "bar":
    st.subheader("State-wise Analysis")
    fig, ax = plt.subplots()
    df_state = df_filtered.groupby(state_col)[selected_column].sum().sort_values()
    ax.bar(df_state.index, df_state.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif st.session_state.view == "pie":
    st.subheader("Distribution")
    df_pie = df_filtered.groupby(state_col)[selected_column].sum()
    if len(df_pie) > 1:
        fig, ax = plt.subplots()
        ax.pie(df_pie.values, labels=df_pie.index, autopct="%1.1f%%")
        st.pyplot(fig)
    else:
        st.warning("Select at least 2 states")

elif st.session_state.view == "box":
    st.subheader("State-wise Distribution (All Categories)")
    fig, ax = plt.subplots()
    data = []
    labels = []
    numeric_cols = df_filtered.select_dtypes(include='number').columns
    for state in df_filtered[state_col].unique():
        row = df_filtered[df_filtered[state_col] == state][numeric_cols]
        values = row.values.flatten()
        values = values[~pd.isna(values)]
        if len(values) > 0:
            data.append(values)
            labels.append(state)
    ax.boxplot(data, labels=labels)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif st.session_state.view == "gender":
    st.subheader("Gender-wise Comparison")
    boys_col = None
    girls_col = None
    other_col = None
    for col in df.columns:
        if "boy" in col.lower():
            boys_col = col
        elif "girl" in col.lower():
            girls_col = col
        elif "other" in col.lower():
            other_col = col
    if boys_col and girls_col:
        fig, ax = plt.subplots()
        data = df_filtered.groupby(state_col)[[boys_col, girls_col]].sum()
        if other_col:
            data[other_col] = df_filtered.groupby(state_col)[other_col].sum()
        data.plot(kind="bar", ax=ax, width=0.7)
        ax.set_ylabel("Enrollment")
        ax.set_xlabel("States")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Gender data not found in dataset")

elif st.session_state.view == "data":
    st.subheader("Full Dataset")
    st.dataframe(df_original)
    st.subheader("Filtered Dataset")
    st.dataframe(df_filtered)