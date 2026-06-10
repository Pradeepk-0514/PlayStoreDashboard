import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import re


def show():
    st.title("Stacked Area Chart Analysis")



    ist = pytz.timezone('Asia/Kolkata')

    current_time = datetime.now(ist)

    if 16 <= current_time.hour < 18:

        

        df = pd.read_csv(
            "Play Store Data.csv"
        )

        

        df = df.dropna(subset=[

            'App',
            'Category',
            'Rating',
            'Reviews',
            'Size',
            'Installs',
            'Last Updated'
        ])

        

        df['Rating'] = pd.to_numeric(
            df['Rating'],
            errors='coerce'
        )

        df['Reviews'] = pd.to_numeric(
            df['Reviews'],
            errors='coerce'
        )

        

        df['Installs'] = (
            df['Installs']
            .str.replace('+', '', regex=False)
            .str.replace(',', '', regex=False)
        )

        df['Installs'] = pd.to_numeric(
            df['Installs'],
            errors='coerce'
        )

    

        def clean_size(size):

            if 'M' in str(size):
                return float(size.replace('M', ''))

            elif 'k' in str(size):
                return float(size.replace('k', '')) / 1024

            else:
                return None

        df['Size'] = (
            df['Size']
            .apply(clean_size)
        )

    

        df['Last Updated'] = pd.to_datetime(
            df['Last Updated'],
            errors='coerce'
        )

        

        df = df[
            df['Category'].str.startswith(
                ('T', 'P')
            )
        ]

        

        df = df[
            ~df['App'].str.contains(
                r'\d',
                regex=True,
                na=False
            )
        ]

        

        df = df[

            (df['Rating'] >= 4.2) &

            (df['Reviews'] > 1000) &

            (df['Size'] >= 20) &

            (df['Size'] <= 80)
        ]

        

        translations = {

            'TRAVEL_AND_LOCAL': 'Voyage et Local',

            'PRODUCTIVITY': 'Productividad',

            'PHOTOGRAPHY': '写真'
        }

        df['Category'] = (
            df['Category']
            .replace(translations)
        )

        

        df['Month'] = (

            df['Last Updated']
            .dt.to_period('M')
            .astype(str)
        )

        

        trend_data = df.groupby([

            'Month',
            'Category'

        ])['Installs'].sum().reset_index()

        

        pivot_data = trend_data.pivot(

            index='Month',

            columns='Category',

            values='Installs'

        ).fillna(0)

        

        growth = pivot_data.pct_change()

    

        fig, ax = plt.subplots(
            figsize=(14,7)
        )

        ax.stackplot(

            pivot_data.index,

            pivot_data.T,

            labels=pivot_data.columns,

            alpha=0.7
        )

        

        for i in range(len(growth.index)):

            if (growth.iloc[i] > 0.25).any():

                ax.axvspan(

                    i - 0.5,

                    i + 0.5,

                    alpha=0.2
                )

    

        plt.xticks(rotation=45)

        plt.title(
            "Cumulative Installs Over Time"
        )

        plt.xlabel("Month")

        plt.ylabel("Total Installs")

        plt.legend(
            loc='upper left'
        )

        

        st.pyplot(fig)

    else:

        st.warning(
            "Graph visible only between 4 PM and 6 PM IST"
        )