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

# Filter by No of student
min_students, max_students = df["No of student"].min(), df["No of student"].max()
students_range = st.sidebar.slider("Number of Students", min_students, max_students, (min_students, max_students))

# Filter by Overall Score
min_score, max_score = df["OverAll Score"].min(), df["OverAll Score"].max()
score_range = st.sidebar.slider("Overall Score", min_score, max_score, (min_score, max_score))

# Filter by Teaching Score
min_teaching, max_teaching = df["Teaching Score"].min(), df["Teaching Score"].max()
teaching_range = st.sidebar.slider("Teaching Score", min_teaching, max_teaching, (min_teaching, max_teaching))

# Filter by Research Score
min_research, max_research = df["Research Score"].min(), df["Research Score"].max()
research_range = st.sidebar.slider("Research Score", min_research, max_research, (min_research, max_research))

# Filter by Citations Score
min_citations, max_citations = df["Citations Score"].min(), df["Citations Score"].max()
citations_range = st.sidebar.slider("Citations Score", min_citations, max_citations, (min_citations, max_citations))

# Filter by Industry Income Score
min_industry, max_industry = df["Industry Income Score"].min(), df["Industry Income Score"].max()
industry_range = st.sidebar.slider("Industry Income Score", min_industry, max_industry, (min_industry, max_industry))

# Filter by International Outlook Score
min_international, max_international = df["International Outlook Score"].min(), df["International Outlook Score"].max()
international_range = st.sidebar.slider("International Outlook Score", min_international, max_international, (min_international, max_international))

# Select a University
universities = ['All'] + list(df["Name of University"].dropna().unique())
select_university = st.sidebar.selectbox("Select a university:", universities)

# Filter the DataFrame based on user selections
filtered_df = df[
    (df["No of student"] >= students_range[0]) &
    (df["No of student"] <= students_range[1]) &
    (df["OverAll Score"] >= score_range[0]) &
    (df["OverAll Score"] <= score_range[1]) &
    (df["Teaching Score"] >= teaching_range[0]) &
    (df["Teaching Score"] <= teaching_range[1]) &
    (df["Research Score"] >= research_range[0]) &
    (df["Research Score"] <= research_range[1]) &
    (df["Citations Score"] >= citations_range[0]) &
    (df["Citations Score"] <= citations_range[1]) &
    (df["Industry Income Score"] >= industry_range[0]) &
    (df["Industry Income Score"] <= industry_range[1]) &
    (df["International Outlook Score"] >= international_range[0]) &
    (df["International Outlook Score"] <= international_range[1])
]
if select_university != 'All':
    filtered_df = filtered_df[filtered_df["Name of University"] == select_university]

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
    if select_university != 'All':
        fig3 = px.choropleth(
            filtered_df,
            locations="Location",
            locationmode="country names",
            color="Name of University",
            hover_name="Location",
            color_continuous_scale=px.colors.sequential.Plasma,
            projection="natural earth",
        )
        st.plotly_chart(fig3)
