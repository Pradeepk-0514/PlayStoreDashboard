import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz


def show():
    st.title("Free vs Paid Apps Analysis")


    ist = pytz.timezone('Asia/Kolkata')

    current_time = datetime.now(ist)

    if 13 <= current_time.hour < 14:

        df = pd.read_csv("Play Store Data.csv")

    

        df = df.dropna(subset=[
            'Category',
            'Installs',
            'Price',
            'Android Ver',
            'Size',
            'Content Rating',
            'Type',
            'App'
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

        

        df['Price'] = df['Price'].str.replace(
            '$',
            '',
            regex=False
        )

        df['Price'] = pd.to_numeric(
            df['Price'],
            errors='coerce'
        )

        

        def clean_size(size):

            if 'M' in str(size):
                return float(size.replace('M', ''))

            elif 'k' in str(size):
                return float(size.replace('k', '')) / 1024

            else:
                return None

        df['Size'] = df['Size'].apply(clean_size)

        

        df['Android Ver'] = (
            df['Android Ver']
            .str.extract(r'(\d+\.\d+)')
        )

        df['Android Ver'] = pd.to_numeric(
            df['Android Ver'],
            errors='coerce'
        )

        

        df['Revenue'] = (
            df['Price'] * df['Installs']
        )

        

        df = df[
            (df['Installs'] > 10000) &
            (df['Revenue'] > 10000) &
            (df['Android Ver'] > 4.0) &
            (df['Size'] > 15) &
            (df['Content Rating'] == 'Everyone') &
            (df['App'].str.len() <= 30)
        ]

        

        top_categories = (
            df.groupby('Category')['Installs']
            .sum()
            .nlargest(3)
            .index
        )

        df = df[
            df['Category'].isin(top_categories)
        ]

        

        result = df.groupby('Type').agg({

            'Installs': 'mean',
            'Revenue': 'mean'

        }).reset_index()

        

        fig, ax1 = plt.subplots(figsize=(10,6))

        ax1.bar(
            result['Type'],
            result['Installs']
        )

        ax1.set_ylabel('Average Installs')

        ax2 = ax1.twinx()

        ax2.plot(
            result['Type'],
            result['Revenue'],
            marker='o',
            linewidth=3
        )

        ax2.set_ylabel('Revenue')

        plt.title(
            "Free vs Paid Apps Analysis"
        )

        st.pyplot(fig)

    else:

        st.warning(
            "Graph visible only between 1 PM and 2 PM IST"
        )