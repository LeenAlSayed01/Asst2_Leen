import pandas as pd
import streamlit as st
import plotly.express as px


# Load your CSV data
url = "https://raw.githubusercontent.com/LeenAlSayed01/Asst2_Leen/main/World%20University%20Rankings%202023%201.csv"
df = pd.read_csv(url)



# Define a placeholder for user input
import streamlit as st

# Initialize session state to store user input
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Create a text input field
user_input = st.text_input("Enter your name:")

# Create a button to fetch user input and update the page title
if st.button("Submit"):
    st.session_state.user_input = user_input  # Store user input in session state
    st.title("Hello " + st.session_state.user_input + ", welcome to World University Rankings 2023")

# Display the DataFrame and plots if user input is not empty
if st.checkbox("Click to see the webpage content"):
    st.subheader("The data")
    st.write(df)

    # Create a scatter plot using Plotly Express
    st.subheader("Scatter Plot: Overall Score vs. International Student Percentage")
    fig_scatter = px.scatter(df, x="OverAll Score", y="International Student", 
                            hover_name="Name of University", title="Scatter Plot: Overall Score vs. International Student Percentage")
   
    st.plotly_chart(fig_scatter)  
     

    #fig 2
    fig2 = px.line(df, x="No of student", y="No of student per staff", color="Name of University",
                    title="Changes in University Rankings Over Time")
    st.plotly_chart(fig2)

    #fig3
    
    
    
    
    
    select_university = st.selectbox("Select a university:", df["Name of University"].unique())
    filtered_df = df[df["Name of University"] == select_university]
   
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

import pandas as pd
import streamlit as st
import plotly.express as px

# Load your CSV data
url = "https://raw.githubusercontent.com/LeenAlSayed01/Asst2_Leen/main/World%20University%20Rankings%202023%201.csv"
df = pd.read_csv(url)
