import pandas as pd
import streamlit as st
import plotly.express as px
# Load your CSV data
url = "https://raw.githubusercontent.com/LeenAlSayed01/Asst2_Leen/main/World%20University%20Rankings%202023%201.csv"
df = pd.read_csv("url)

# Create a Streamlit app
st.title("World University Rankings 2023")

# Display the DataFrame
st.write(df)

# Create a scatter plot using Plotly Express
st.subheader("Scatter Plot: Overall Score vs. International Student Percentage")
fig_scatter = px.scatter(df, x="OverAll Score", y="International Student", 
                         hover_name="Name of University", title="Scatter Plot: Overall Score vs. International Student Percentage")
st.plotly_chart(fig_scatter)



