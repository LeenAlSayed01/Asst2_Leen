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
st.sidebar.text("Use the sliders to filter the universities based on your criteria.")

# Filter by No of student
min_students, max_students = df["No of student"].min(), df["No of student"].max()
students_range = st.sidebar.slider("Number of Students", min_students, max_students, (min_students, max_students))

# Filter by Overall Score
score_columns = ["OverAll Score", "Teaching Score", "Research Score", "Citations Score", "Industry Income Score", "International Outlook Score"]
score_ranges = {}
for column in score_columns:
    min_val, max_val = df[column].min(), df[column].max()
    score_ranges[column] = st.sidebar.slider(column, min_val, max_val, (min_val, max_val))

# Filter the DataFrame based on user selections
filtered_df = df[
    (df["No of student"] >= students_range[0]) &
    (df["No of student"] <= students_range[1])
]
for column, (min_val, max_val) in score_ranges.items():
    filtered_df = filtered_df[(df[column] >= min_val) & (df[column] <= max_val)]

# Introductory page content
st.title("World University Rankings 2023")
st.header("Welcome to the interactive dashboard!")
st.write("""
Explore the rankings, scores, and more based on your preferences. 
This dashboard provides insights into the 2023 world university rankings. You can filter the results by number of students, overall scores, and other specific scores. 
Feel free to play around with the filters on the left to customize your view.
""")

# Display the DataFrame and plots if user input is not empty
if st.checkbox("Click to see the webpage content"):
    st.subheader("The data")
    st.write("Below is the filtered data based on your selection criteria.")
    st.write(filtered_df)

    # Create a scatter plot using Plotly Express
    st.subheader("Scatter Plot: Overall Score vs. International Student Percentage")
    st.write("""
    This scatter plot provides a visual comparison between universities based on their overall score and the percentage of international students they have.
    Hover over the points to see more details.
    """)
    fig_scatter = px.scatter(filtered_df, x="OverAll Score", y="International Student", 
                             hover_name="Name of University", title="Scatter Plot: Overall Score vs. International Student Percentage")
    st.plotly_chart(fig_scatter)  
    
    # Figure 3
    st.subheader("University Location on World Map")
    st.write("""
    Select a specific university to see its location on the world map.
    """)
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

    # New Figure 4: Histogram of Overall Score
    st.subheader("Distribution of Universities based on Overall Score")
    st.write("""
    This histogram displays the distribution of universities based on their overall score. 
    Use the slider above to adjust the granularity of the bins.
    """)
    bin_selection = st.select_slider('Select number of bins:', options=[10, 20, 30, 40, 50, 60, 70], value=50)
    fig4 = px.histogram(filtered_df, x="OverAll Score", title="Distribution of Universities based on Overall Score", nbins=bin_selection)
    st.plotly_chart(fig4)

    # New Figure 5: Bar chart of average Score per Location
    st.subheader(f"Average {score_selection} per Location")
    st.write(f"""
    This bar chart displays the average {score_selection.lower()} of universities for each location. 
    Use the dropdown menu above to select a different score type.
    """)
    score_per_location = filtered_df.groupby('Location')[score_selection].mean().reset_index()
    fig5 = px.bar(score_per_location, x='Location', y=score_selection, title=f"Average {score_selection} per Location")
    st.plotly_chart(fig5)
