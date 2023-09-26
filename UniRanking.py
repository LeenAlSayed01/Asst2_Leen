import pandas as pd
import streamlit as st
import plotly.express as px
# Load your CSV data
df = pd.read_csv("C:/Users/Leen/OneDrive/Documents/World University Rankings 2023 1.csv")

# Create a Streamlit app
st.title("World University Rankings 2023")

# Display the DataFrame
st.write(df)

# Create a scatter plot using Plotly Express
st.subheader("Scatter Plot: Overall Score vs. International Student Percentage")
fig_scatter = px.scatter(df, x="OverAll Score", y="International Student", 
                         hover_name="Name of University", title="Scatter Plot: Overall Score vs. International Student Percentage")
st.plotly_chart(fig_scatter)



