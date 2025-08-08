import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

class Investor:

    def __init__(self,data_loader):
        self.df= data_loader.df
    
    def load_investor_details(self,investor):
        
        st.title(investor)

        
        #load the recent 5 investments of the investor
        last5_df= self.df[self.df['investors'].str.contains(investor)].head(5)[['date','startup','vertical','round','amount']]
        st.subheader("Most Recent Investments")
        st.dataframe(last5_df)

        col1,col2= st.columns(2)
        with col1:
            #biggest Investments
            big_series= self.df[self.df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
            st.subheader("Bigest Investments")
            fig, ax = plt.subplots()
            ax.tick_params(axis='x', labelsize=10,labelrotation=15)
            ax.tick_params(axis='y', labelsize=10)
            ax.bar(big_series.index,list(big_series.values))

            
            ax.set_xlabel("Investors", fontsize=10)
            ax.set_ylabel("Amount", fontsize=10)
            st.pyplot(fig)

        with col2:
            #sector invested in 
            vertical_series=self.df[self.df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
            
            st.subheader("Sectors Invested In")
            fig1, ax1 = plt.subplots()
            ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
            st.pyplot(fig1)

    
        year_series=self.df[self.df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader("Year by Year Investments")
        fig2, ax2 = plt.subplots(figsize=(12,4))
        ax2.plot(year_series.index,year_series.values, marker='o')

        #x-axis 
        ax2.set_xticks(year_series.index)
        ax2.set_xticklabels(year_series.index.astype(int))

        st.pyplot(fig2)