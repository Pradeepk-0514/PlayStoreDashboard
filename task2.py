import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz


def show():
    st.title("Global Installs Choropleth Map")


    ist = pytz.timezone('Asia/Kolkata')

    current_time = datetime.now(ist)

    if 18 <= current_time.hour < 20:
        

        df = pd.read_csv("Play Store Data.csv")


        df = df.dropna(subset=['Category', 'Installs'])


        df['Installs'] = df['Installs'].str.replace(
            '+',
            '',
            regex=False
        )

        df['Installs'] = df['Installs'].str.replace(
            ',',
            '',
            regex=False
        )

        df['Installs'] = pd.to_numeric(
            df['Installs'],
            errors='coerce'
        )


        df = df[
            ~df['Category'].str.startswith(
                ('A', 'C', 'G', 'S')
            )
        ]

    

        df = df[df['Installs'] > 1000000]



        top_categories = (
            df.groupby('Category')['Installs']
            .sum()
            .nlargest(5)
            .reset_index()
        )

    

        countries = [
            'India',
            'United States',
            'Brazil',
            'Canada',
            'Germany'
        ]

        top_categories['Country'] = countries

        

        fig = px.choropleth(

            top_categories,

            locations='Country',

            locationmode='country names',

            color='Installs',

            hover_name='Category',

            color_continuous_scale='Blues',

            title='Global Installs by App Category'
        )

        

        st.plotly_chart(fig)

    else:

        st.warning(
            "Choropleth map visible only between 6 PM and 8 PM IST"
        )