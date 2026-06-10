import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz


def show():
    st.title("Bubble Chart Analysis")



    ist = pytz.timezone('Asia/Kolkata')

    current_time = datetime.now(ist)

    if 17 <= current_time.hour < 19:

        

        apps_df = pd.read_csv(
            "Play Store Data.csv"
        )

        reviews_df = pd.read_csv(
            "User Reviews.csv"
        )

        

        apps_df = apps_df.dropna(subset=[
            'App',
            'Category',
            'Rating',
            'Reviews',
            'Installs',
            'Size'
        ])

        reviews_df = reviews_df.dropna(subset=[
            'App',
            'Sentiment_Subjectivity'
        ])

        

        apps_df['Rating'] = pd.to_numeric(
            apps_df['Rating'],
            errors='coerce'
        )

        apps_df['Reviews'] = pd.to_numeric(
            apps_df['Reviews'],
            errors='coerce'
        )

        

        apps_df['Installs'] = (
            apps_df['Installs']
            .str.replace('+', '', regex=False)
            .str.replace(',', '', regex=False)
        )

        apps_df['Installs'] = pd.to_numeric(
            apps_df['Installs'],
            errors='coerce'
        )

        

        def clean_size(size):

            if 'M' in str(size):
                return float(size.replace('M', ''))

            elif 'k' in str(size):
                return float(size.replace('k', '')) / 1024

            else:
                return None

        apps_df['Size'] = (
            apps_df['Size']
            .apply(clean_size)
        )

        

        reviews_df['Sentiment_Subjectivity'] = (
            pd.to_numeric(
                reviews_df['Sentiment_Subjectivity'],
                errors='coerce'
            )
        )

        

        df = pd.merge(

            apps_df,

            reviews_df,

            on='App',

            how='inner'
        )

        
        allowed_categories = [

            'GAME',
            'BEAUTY',
            'BUSINESS',
            'COMICS',
            'COMMUNICATION',
            'DATING',
            'ENTERTAINMENT',
            'SOCIAL',
            'EVENTS'
        ]

        df = df[
            df['Category'].isin(
                allowed_categories
            )
        ]

        

        df = df[

            (df['Rating'] > 3.5) &

            (df['Reviews'] > 500) &

            (df['Installs'] > 50000) &

            (df['Sentiment_Subjectivity'] > 0.5)

        ]

        

        df = df[
            ~df['App'].str.contains(
                'S',
                case=False,
                na=False
            )
        ]

        

        translations = {

            'BEAUTY': 'Saundarya',

            'BUSINESS': 'Vanigam',

            'DATING': 'Partnersuche'
        }

        df['Category'] = (
            df['Category']
            .replace(translations)
        )

        

        fig = px.scatter(

            df,

            x='Size',

            y='Rating',

            size='Installs',

            color='Category',

            hover_name='App',

            title='Bubble Chart Analysis',

            size_max=60
        )

        

        fig.for_each_trace(

            lambda trace:

            trace.update(
                marker_color='pink'
            )

            if trace.name == 'GAME'

            else ()
        )

        

        st.plotly_chart(fig)

    else:

        st.warning(
            "Graph visible only between 5 PM and 7 PM IST"
        )