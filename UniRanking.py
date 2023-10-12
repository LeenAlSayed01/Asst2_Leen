import pandas as pd
import streamlit as st
import plotly.express as px

# Load the CSV data
url = "https://raw.githubusercontent.com/LeenAlSayed01/Asst2_Leen/main/World%20University%20Rankings%202023%201.csv"
df = pd.read_csv(url)

# Handle nan values and convert "No of student" to integer type
df["No of student"] = df["No of student"].str.replace(',', '').fillna('0').astype(int)

# Handle "OverAll Score" column: Convert ranges to their average and handle nan values
def handle_score(score):
    if isinstance(score, str) and '–' in score:
        low, high = score.split('–')
        return (float(low) + float(high)) / 2
    return float(score)

df["OverAll Score"] = df["OverAll Score"].apply(handle_score).fillna(0)

# Sidebar filters
st.sidebar.title("Filters")

# Filter by Location
selected_location = st.sidebar.selectbox("Select a location:", ['All'] + sorted(df["Location"].unique().tolist()))

# Filter by No of student
min_students, max_students = df["No of student"].min(), df["No of student"].max()
students_range = st.sidebar.slider("Number of Students", min_students, max_students, (min_students, max_students))

# Filter by Overall Score
min_score, max_score = df["OverAll Score"].min(), df["OverAll Score"].max()
score_range = st.sidebar.slider("Overall Score", min_score, max_score, (min_score, max_score))

# Filter the DataFrame based on user selections
filtered_df = df.copy()
if selected_location != 'All':
    filtered_df = filtered_df[filtered_df["Location"] == selected_location]
filtered_df = filtered_df[
    (filtered_df["No of student"] >= students_range[0]) &
    (filtered_df["No of student"] <= students_range[1]) &
    (filtered_df["OverAll Score"] >= score_range[0]) &
    (filtered_df["OverAll Score"] <= score_range[1])
]

# Introductory page content
st.title("World University Rankings 2023")
st.header("Welcome to the interactive dashboard!")
st.subheader("Explore rankings, scores, and more based on your preferences.")

# Display the DataFrame and plots if user input is not empty
if st.checkbox("Click to see the webpage content"):
    st.subheader("The data")
    st.write(filtered_df)

    # Create a scatter plot using Plotly Express
    st.subheader("Scatter Plot: Overall Score vs. International Student Percentage")
    fig_scatter = px.scatter(filtered_df, x="OverAll Score", y="International Student", 
                             hover_name="Name of University", title="Scatter Plot: Overall Score vs. International Student Percentage")
    st.plotly_chart(fig_scatter)  
    
    # Figure 2
    fig2 = px.line(filtered_df, x="No of student", y="No of student per staff", color="Name of University",
                   title="Changes in University Rankings Over Time")
    st.plotly_chart(fig2)

    # Figure 3
    select_university = st.selectbox("Select a university:", ['All'] + filtered_df["Name of University"].unique().tolist())
    if select_university != 'All':
        university_df = filtered_df[filtered_df["Name of University"] == select_university]
        fig3 = px.choropleth(
            university_df,
            locations="Location",
            locationmode="country names",
            color="Name of University",
            hover_name="Location",
            color_continuous_scale=px.colors.sequential.Plasma,
            projection="natural earth",
        )
        st.plotly_chart(fig3)
