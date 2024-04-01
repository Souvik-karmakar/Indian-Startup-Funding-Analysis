import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout='wide',page_title="Startup funding analysis")
df=pd.read_csv("startup_cleaned.csv")
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def load_startup_details(startup):
    st.title("Startup Analysis: " + startup)
    startup_df = df[df['startup'] == startup]

    # Display basic information about the startup
    st.header("Basic Information")
    st.write("Industry Vertical:", startup_df['vertical'].iloc[0])
    st.write("Subvertical:", startup_df['subvertical'].iloc[0])
    st.write("City Location:", startup_df['city'].iloc[0])

    # Display funding rounds information
    st.header("Funding Rounds")
    st.dataframe(startup_df[['date', 'investors', 'inv_type', 'amount(CR)']])

def load_investor_details(investor):
    st.title("Investor Analysis: " + investor)
    investor_df = df[df['investors'].str.contains(investor)]

    # Load the recent 5 investments of the investor
    last_5_df = investor_df.head()[['date', 'startup', 'vertical', 'city', 'amount(CR)']]
    st.subheader("Most Recent Investments by " + investor)
    st.dataframe(last_5_df)

    # Display top investments by the investor
    col1, col2 = st.columns(2)
    with col1:
        # Biggest Investments
        big_series = investor_df.groupby('startup')['amount(CR)'].sum().sort_values(ascending=False).head(5)
        st.subheader("Biggest Investments by " + investor)
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(big_series.index, big_series.values)
        plt.xticks(rotation=90)
        st.pyplot(fig)

    with col2:
        # Sectors invested in
        vertical_series = investor_df.groupby('vertical')['amount(CR)'].sum().sort_values(ascending=False)
        st.subheader("Sectors invested in by " + investor)
        fig1, ax1 = plt.subplots(figsize=(14, 6))
        ax1.bar(vertical_series.index, vertical_series.values)
        plt.xticks(rotation=90)
        st.pyplot(fig1)

    # Display investment type distribution
    col3, col4 = st.columns(2)
    with col3:
        inv_type_series = investor_df.groupby('inv_type')['amount(CR)'].sum().sort_values(ascending=False)
        st.subheader("Investment type by " + investor)
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.pie(inv_type_series, labels=inv_type_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        # Investment based on cities
        city_series = investor_df.groupby('city')['amount(CR)'].sum().sort_values(ascending=False)
        st.subheader("Investment based on cities by " + investor)
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    # Year-over-Year Investment
    investor_df['year'] = investor_df['date'].dt.year
    year_series = investor_df.groupby('year')['amount(CR)'].sum().sort_values(ascending=False)
    st.subheader("Year-over-Year Investment by " + investor)
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)
    st.pyplot(fig4)

    # Similar Investors Analysis
    st.header("Similar Investors")
    similar_investors_df = df[df['startup'].isin(investor_df['startup'])]
    similar_investors = similar_investors_df['investors'].str.split(', ').explode().unique()
    similar_investors = [inv.strip() for inv in similar_investors if inv.strip() != investor]

    if len(similar_investors) > 0:
        st.write("Investors who have invested in similar startups:")
        st.write(", ".join(similar_investors))
    else:
        st.write("No similar investors found for " + investor)

def load_overall_analysis():
    st.title("Overall Analysis")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        # Total Invested amount
        total = round(df['amount(CR)'].sum())
        st.metric("Total", str(total) + " Cr")
    with col6:
        # Max Infused amount
        Max_fund = df.groupby('startup')['amount(CR)'].max().sort_values(ascending=False).head(1).values[0]
        st.metric("Max Fund raised", str(Max_fund) + " Cr")
    with col7:
        # Avg Infused amount
        Avg_fund = round(df.groupby('startup')['amount(CR)'].sum().mean(), 2)
        st.metric("Average", str(Avg_fund) + " Cr")
    with col8:
        # Total Funded Startups
        Count = df['startup'].nunique()
        st.metric("Total Funded Startups", str(Count))

    st.header("MOM Graph")
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount(CR)'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount(CR)'].count().reset_index()
    # Combine 'year' and 'month' columns to create x-values
    temp_df['x_val'] = temp_df['year'].astype('str') + '-' + temp_df['month'].astype('str')
    # Plot the data
    st.subheader("MOM Investment")
    fig5, ax5 = plt.subplots(figsize=(16, 6))
    ax5.plot(temp_df['x_val'], temp_df['amount(CR)'])
    # Rotate the x-axis tick labels for better readability
    plt.xticks(rotation=90)
    st.pyplot(fig5)

    col9,col10=st.columns(2)
    with col9:
       # Sector analysis by count
       sector_counts = df['vertical'].value_counts()
       # Select top sectors based on count
       top_sectors_count = sector_counts.head(5)
       # Plot Sector Analysis Pie for top sectors by count
       fig6,ax6=plt.subplots(figsize=(10, 6))
       ax6.pie(top_sectors_count, labels=top_sectors_count.index, autopct='%1.1f%%', startangle=140)
       plt.title('Top Sectors by Count of Investments')
       st.pyplot(fig6)
    with col10:
       # Sector analysis by sum
       sector_sums = df.groupby('vertical')['amount(CR)'].sum()
       # Select top sectors based on sum
       top_sectors_sum = sector_sums.head(5)
       # Plot Sector Analysis Pie for top sectors by count
       fig7,ax7=plt.subplots(figsize=(10, 6))
       ax7.pie(top_sectors_sum, labels=top_sectors_sum.index, autopct='%1.1f%%', startangle=140)
       plt.title('Top Sectors by sum of Investments')
       st.pyplot(fig7)
    col11,col12=st.columns(2)
    with col11:
        st.subheader("Top 5 Investment type")
        funding_types = df['inv_type'].value_counts().head(5)
        fig8, ax8 = plt.subplots(figsize=(6, 4))
        ax8.bar(funding_types.index, funding_types.values)
        funding_types.plot(kind='bar')
        plt.xlabel('Funding Type')
        plt.ylabel('Count')
        plt.title('Type of Funding')
        st.pyplot(fig8)
    with col12:
        st.subheader("Top 5 Funded cities")
        funded_city = df['city'].value_counts().head(5)
        fig9, ax9 = plt.subplots(figsize=(6, 4))
        ax9.bar(funded_city.index, funded_city.values)
        funded_city.plot(kind='bar')
        plt.xlabel('City')
        plt.ylabel('Count')
        plt.title('Funded Cities')
        st.pyplot(fig9)

    # Add Top Startups year-wise analysis
    st.header("Top Startups - Year Wise")
    top_startups_year_wise = df.groupby(['year', 'startup'])['amount(CR)'].sum().reset_index()
    top_startups_year_wise = top_startups_year_wise.sort_values(by=['year', 'amount(CR)'], ascending=[True, False])

    # Select top 5 startups for each year
    top_5_startups_year_wise = top_startups_year_wise.groupby('year').head(5)

    fig10, ax10 = plt.subplots(figsize=(12, 8))  # Increase the figure size
    for year, data in top_5_startups_year_wise.groupby('year'):
        ax10.barh(data['startup'], data['amount(CR)'], label=str(year))  # Use barh for horizontal bar chart
    ax10.legend()
    plt.xlabel('Investment Amount (CR)')
    plt.ylabel('Startup')
    plt.title('Top Startup Year Wise')
    plt.tight_layout()  # Adjust layout to prevent overlap
    st.pyplot(fig10)

    # Add Top Investors analysis
    st.header("Top Investors - Year Wise")
    top_investors_year_wise = df.groupby(['year', 'investors'])['amount(CR)'].sum().reset_index()
    top_investors_year_wise = top_investors_year_wise.sort_values(by=['year', 'amount(CR)'], ascending=[True, False])

    # Select top 5 investors for each year
    top_5_investors_year_wise = top_investors_year_wise.groupby('year').head(5)

    fig11, ax11 = plt.subplots(figsize=(12, 8))  # Increase the figure size
    for year, data in top_5_investors_year_wise.groupby('year'):
        ax11.barh(data['investors'], data['amount(CR)'], label=str(year))  # Use barh for horizontal bar chart

    ax11.legend()
    plt.xlabel('Investment Amount (CR)')
    plt.ylabel('Investor')
    plt.title('Top Investor Year Wise')
    plt.tight_layout()  # Adjust layout to prevent overlap
    st.pyplot(fig11)

    # Add Funding Heatmap
    st.header("Funding Heatmap")

    # Pivot table to prepare data for heatmap
    heatmap_data = df.pivot_table(index='month', columns='year', values='amount(CR)', aggfunc='sum')

    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f", linewidths=.5)
    plt.title('Funding Heatmap')
    plt.xlabel('Year')
    plt.ylabel('Month')
    st.pyplot(plt)


df['Investors Name']=df['investors'].fillna("Undisclosed")
# st.dataframe(df)
st.sidebar.title("Startup Fund Analysis")
option=st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor'])

if option=='Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    # Populate startup dropdown with cleaned startup names
    selected_startup = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
    if btn1:
        load_startup_details(selected_startup)

else:
    selected_investor=st.sidebar.selectbox("Select Investor",sorted(set(df['investors'].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)
