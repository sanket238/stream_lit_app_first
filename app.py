import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



st.set_page_config(layout='wide',page_title="StartUp Analysis")

df= pd.read_csv("startup_cleaned.csv")


def to_inr(dollar):
  inr= dollar*87.5
  return round(inr/10000000,2)



df['amount']=df["amount"].apply(to_inr)
df['date']=pd.to_datetime(df['date'],errors="coerce")
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year



#data cleaning
#df['Investors Name']=df['Investors Name'].fillna("Undisclosed")

def load_investor_details(investor):
    st.title(investor)

    
    #load the recent 5 investments of the investor
    last5_df= df[df['investors'].str.contains(investor)].head(5)[['date','startup','vertical','round','amount']]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)

    col1,col2= st.columns(2)
    with col1:
        #biggest Investments
        big_series= df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
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
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        
        st.subheader("Sectors Invested In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)

   
    year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader("Year by Year Investments")
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    st.pyplot(fig2)

def load_overall_analysis():
    st.title("Overall Analysis")

    col1,col2,col3,col4= st.columns(4)
    with col1:
        #total invested amount

        total= round(df['amount']).sum()

        st.metric('Total',str(total)+" Cr")
    with col2:
        #max amount infused in a startup
        max_funding=df.groupby('startup')['amount'].max().head(1).values[0]

        st.metric('Max Amount in Funding',str(max_funding)+" Cr")
    with col3:
        #average funding
        average_funding=df.groupby('startup')['amount'].sum().mean()
        st.metric("Average Funding",str(round(average_funding))+" Cr")

    with col4:
        #total company funded
        total_company=df['startup'].nunique()
        st.metric("Funded Startups",str(total_company))

    #mom chart
    st.header("MOM chart")
    selected_option=st.selectbox("Select Type",['Total',' Count'])

    if selected_option=="Total":
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()

    else:
        temp_df=df.groupby(['year','month'])['amount'].count().reset_index()
    
    temp_df['date'] = pd.to_datetime(temp_df[['year', 'month']].assign(day=1))
    #temp_df['x-axis']=temp_df['month'].astype(str)+ '-'+temp_df['year'].astype(str)

    st.subheader("MOM chart")
    fig3, ax3 = plt.subplots(figsize=(14,4))
    ax3.plot(temp_df['date'],temp_df['amount'])

    #x-axis changes
   
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=4))  # every 4 months
    plt.setp(ax3.get_xticklabels(), rotation=90, ha='right')
    plt.tight_layout()
    st.pyplot(fig3,use_container_width=True)    

    
    

    
    


    


        



st.sidebar.title("Startup Funding Analysis")

option=st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])

if option == "Overall Analysis":
    #mom chart - total +count
    #btn0=st.sidebar.button("Show Overall Analysis")
    #if btn0:
        load_overall_analysis()


elif option== "Startup":
    st.sidebar.selectbox("Select Startup",sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button("Find Startup Details")
    st.title("Startup Analysis")


else:
    selected_investor=st.sidebar.selectbox("Select Startup",sorted(set(df['investors'].str.split(',').sum())))
    btn2= st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)

        #recent Investments


    