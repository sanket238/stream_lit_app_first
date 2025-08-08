import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

class Overall:
    
    def __init__(self,data_loader):
        self.df= data_loader.df

   
    def load_overall_analysis(self):
        st.markdown("""
        This dashboard presents an **interactive analysis of startup funding in India**  
        covering the period **January 2015 to August 2017**.

        You can explore:
        - 💰 **Total and Average Funding Trends**
        - 📈 **Month-over-Month (MoM) Growth**
        - 🏢 **Startup-specific Funding Details**
        - 🤝 **Investor-specific Portfolios**

        Use the sidebar to switch between **Overall Analysis**, **Startup View**, and **Investor View**.
        """)
        st.header("Overall Analysis")

        col1,col2,col3,col4= st.columns(4)
        with col1:
            #total invested amount

            total= round(self.df['amount']).sum()

            st.metric('Total',str(total)+" Cr")
        with col2:
            #max amount infused in a startup
            max_funding=self.df.groupby('startup')['amount'].max().head(1).values[0]

            st.metric('Max Amount in Funding',str(max_funding)+" Cr")
        with col3:
            #average funding
            average_funding=self.df.groupby('startup')['amount'].sum().mean()
            st.metric("Average Funding",str(round(average_funding))+" Cr")

        with col4:
            #total company funded
            total_company=self.df['startup'].nunique()
            st.metric("Funded Startups",str(total_company))

        #mom chart
        st.subheader("MOM chart")
        selected_option=st.selectbox("Select Type",['Total',' Count'])

        if selected_option=="Total":
            temp_df=self.df.groupby(['year','month'])['amount'].sum().reset_index()

        else:
            temp_df=self.df.groupby(['year','month'])['amount'].count().reset_index()
        
        temp_df['date'] = pd.to_datetime(temp_df[['year', 'month']].assign(day=1))
        #temp_df['x-axis']=temp_df['month'].astype(str)+ '-'+temp_df['year'].astype(str)

        fig3, ax3 = plt.subplots(figsize=(14,4))
        ax3.plot(temp_df['date'],temp_df['amount'])

        #x-axis changes
    
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
        ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=4))  # every 4 months
        plt.setp(ax3.get_xticklabels(), rotation=90, ha='right')
        plt.tight_layout()
        st.pyplot(fig3,use_container_width=True)    
