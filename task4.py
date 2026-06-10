import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz



def show():
    st.title("Installs Trend Analysis")



    ist = pytz.timezone('Asia/Kolkata')

    current_time = datetime.now(ist)

    if 18 <= current_time.hour < 21:
    

        df = pd.read_csv("Play Store Data.csv")

        

        df = df.dropna(subset=[
            'Category',
            'App',
            'Reviews',
            'Installs',
            'Last Updated'
        ])

        

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

        

        df['Reviews'] = pd.to_numeric(
            df['Reviews'],
            errors='coerce'
        )

        

        df['Last Updated'] = pd.to_datetime(
            df['Last Updated'],
            errors='coerce'
        )

        

        df = df[
            df['Category'].str.startswith(
                ('E', 'C', 'B')
            )
        ]

    

        df = df[
            ~df['App'].str.startswith(
                ('X', 'Y', 'Z')
            )
        ]

        df = df[
            ~df['App'].str.contains(
                'S',
                case=False,
                na=False
            )
        ]

        

        df = df[
            df['Reviews'] > 500
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

    

        df['Month'] = (
            df['Last Updated']
            .dt.to_period('M')
            .astype(str)
        )

        

        trend_data = df.groupby([
            'Month',
            'Category'
        ])['Installs'].sum().reset_index()

        

        trend_data['Growth'] = (
            trend_data.groupby('Category')['Installs']
            .pct_change()
        )

        

        fig, ax = plt.subplots(figsize=(14,7))

        categories = trend_data['Category'].unique()

        for category in categories:

            cat_data = trend_data[
                trend_data['Category'] == category
            ]

            ax.plot(
                cat_data['Month'],
                cat_data['Installs'],
                marker='o',
                label=category
            )

            growth_data = cat_data[
                cat_data['Growth'] > 0.20
            ]

            ax.fill_between(
                growth_data['Month'],
                growth_data['Installs'],
                alpha=0.3
            )

        plt.xticks(rotation=45)

        plt.title(
            "Total Installs Trend Over Time"
        )

        plt.xlabel("Month")

        plt.ylabel("Total Installs")

        plt.legend()

        st.pyplot(fig)

    else:

        st.warning(
            "Graph visible only between 6 PM and 9 PM IST"
        )