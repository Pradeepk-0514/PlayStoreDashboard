import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz


def show():
    st.title("Google Play Store Dashboard")



    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)

    if 15 <= current_time.hour < 17:
    

        df = pd.read_csv("Play Store Data.csv")

        

        
        df = df.dropna(subset=['Rating', 'Reviews', 'Size', 'Installs', 'Last Updated'])

    
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

        

        def clean_size(size):
            if 'M' in size:
                return float(size.replace('M', ''))
            elif 'k' in size:
                return float(size.replace('k', '')) / 1024
            else:
                return None

        df['Size'] = df['Size'].apply(clean_size)

        

        df['Installs'] = df['Installs'].str.replace('+', '', regex=False)
        df['Installs'] = df['Installs'].str.replace(',', '', regex=False)

        df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    

        df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

    
        df = df[df['Last Updated'].dt.month == 1]

        

        df = df[
            (df['Rating'] >= 4.0) &
            (df['Size'] >= 10)
        ]

    

        top_categories = (
            df.groupby('Category')['Installs']
            .sum()
            .nlargest(10)
            .index
        )

        df_top = df[df['Category'].isin(top_categories)]

        

        result = df_top.groupby('Category').agg({
            'Rating': 'mean',
            'Reviews': 'sum'
        }).reset_index()

    

        fig, ax = plt.subplots(figsize=(12,6))

        x = range(len(result))

        ax.bar(x,
            result['Rating'],
            width=0.4,
            label='Average Rating')

        ax.bar([i + 0.4 for i in x],
            result['Reviews'],
            width=0.4,
            label='Total Reviews')

        ax.set_xticks([i + 0.2 for i in x])

        ax.set_xticklabels(
            result['Category'],
            rotation=45
        )

        ax.set_title("Top 10 Categories by Installs")

        ax.legend()

        
        st.pyplot(fig)

    else:

        st.warning("⏰ Graph visible only between 3 PM and 5 PM IST")