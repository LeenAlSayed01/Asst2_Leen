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
selected_location = st.sidebar.selectbox("Select a location:", df["Location"].unique())

# Filter by No of student
min_students, max_students = df["No of student"].min(), df["No of student"].max()
students_range = st.sidebar.slider("Number of Students", min_students, max_students, (min_students, max_students))

# Filter by Overall Score
min_score, max_score = df["OverAll Score"].min(), df["OverAll Score"].max()
score_range = st.sidebar.slider("Overall Score", min_score, max_score, (min_score, max_score))

# Define a placeholder for user input
# Initialize session state to store user input
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Create a text input field
user_input = st.text_input("Enter your name:")

# Create a button to fetch user input and update the page title
if st.button("Submit"):
    st.session_state.user_input = user_input  # Store user input in session state
    st.title("Hello " + st.session_state.user_input + ", welcome to World University Rankings 2023")

# Filter the DataFrame based on user selections
filtered_df = df[(df["Location"] == selected_location) &
                 (df["No of student"] >= students_range[0]) &
                 (df["No of student"] <= students_range[1]) &
                 (df["OverAll Score"] >= score_range[0]) &
                 (df["OverAll Score"] <= score_range[1])]

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
    select_university = st.selectbox("Select a university:", filtered_df["Name of University"].unique())
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
