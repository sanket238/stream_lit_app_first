import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from dataloader import Dataloader
from classes.overall import Overall
from classes.investor import Investor


st.title("🚀 Startup Funding Analysis (India)")


st.set_page_config(layout='wide',page_title="StartUp Analysis")



df= pd.read_csv("startup_cleaned.csv")

dataloader= Dataloader("startup_cleaned.csv")
df=dataloader.df

st.sidebar.title("Startup Funding Analysis")

option=st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])

if option == "Overall Analysis":
    #mom chart - total +count
        overall=Overall(dataloader)
        overall.load_overall_analysis()

elif option== "Startup":
    st.sidebar.selectbox("Select Startup",sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button("Find Startup Details")
    st.title("Startup Analysis")

else:
    selected_investor=st.sidebar.selectbox("Select Startup",sorted(set(df['investors'].str.split(',').sum())))
    btn2= st.sidebar.button("Find Investor Details")
    if btn2:
        investor=Investor(dataloader)
        investor.load_investor_details(selected_investor)

        #recent Investments







    
    

    
    


    


        






    