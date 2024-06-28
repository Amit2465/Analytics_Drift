import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import time

df = pd.read_csv('analyticsdrift.csv')


st.title('Scrapy Analyzer :chart_with_upwards_trend: ')
st.write('Scrapy Analyzer is an intuitive web application crafted for scraping, analyzing, and downloading data from the Analytics Drift website. Whether you\'re interested in exploring recent articles, tracking link behaviors, conducting exploratory data analysis (EDA), or exporting data for further analysis, Scrapy Analyzer provides robust tools to extract insights seamlessly.')



# -------------------------------- Sidebar --------------------------------------------------------
sidebar_df = df
st.sidebar.info('Please provide the date range for which you would like to scrape data')
start = st.sidebar.date_input('Start Date')
start = pd.to_datetime(start)  
end = st.sidebar.date_input('End Date')
end = pd.to_datetime(end)
all_data = st.sidebar.checkbox('Scrape all data')
st.sidebar.caption('Note: Only select this button if you want to scrape all data')

scrape_start = pd.to_datetime(sidebar_df['Article Date'].iloc[0])
scrape_end = pd.to_datetime(sidebar_df['Article Date'].iloc[-1])


if all_data:
    sidebar_df = sidebar_df
elif start < scrape_start and end < scrape_start:
    st.sidebar.warning(f'you can select data from {scrape_start} to {scrape_end}')
elif start > scrape_end and end > scrape_end:
    st.sidebar.warning(f'you can select data from {scrape_start} to {scrape_end}')
else:
    sidebar_df = sidebar_df[(pd.to_datetime(df['Article Date']) >= start) & (pd.to_datetime(sidebar_df['Article Date']) <= end)]  
       


st.sidebar.info('Select the columns you would like to scrape')
columns_name = ['All','Article Heading', 'Article Section', 'Article Date', 'Article Url', 'External Links', 'Internal Links', 'Broken Links', 'Links Open in new tab', 'Links open in same tab', 'Sponsored Links']
selected_columns = st.sidebar.multiselect('Columns', columns_name)
st.sidebar.markdown('### Output')
if 'All' in selected_columns and len(selected_columns) == 1:
    output_df = st.sidebar.write(df[columns_name[1:]])
elif 'All' in selected_columns and len(selected_columns) > 1:
    st.sidebar.warning('Please select only one column if you want to display all columns')
else:
    output_df = st.sidebar.write(df[selected_columns])
     

def download_csv(df):
    csv = sidebar_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'data:file/csv;base64,{b64}'    
    button_label = 'Click here to download'
    
    st.sidebar.info('Generating Download link...')
    time.sleep(3) 
    st.sidebar.success('Download link generated successfully')
    st.sidebar.markdown(f'<a href="{href}" download="scraped_data.csv"><button>{button_label}</button></a>', unsafe_allow_html=True)

if st.sidebar.button('Download CSV'):
    download_csv(sidebar_df)


# -------------------------------- Main Page --------------------------------------------------------

# Function to count broken links
def count_broken_links(df):
    total_broken_links = 0
    for index, row in df.iterrows():
        links = row['Broken Links']
        if isinstance(links, str):  # Check if it's a string
            links_list = links.split(',')
            num_broken_links = len(links_list)
            total_broken_links += num_broken_links
    return total_broken_links

# Function to count sponsored links
def count_sponsored_links(df):
    total_sponsored_links = 0
    for index, row in df.iterrows():
        links = row['Sponsored_Links']
        if isinstance(links, str):  
            links_list = links.split(',')
            num_sponsored_links = len(links_list)
            total_sponsored_links += num_sponsored_links
    return total_sponsored_links

# Function to count internal links
def count_internal_links(df):
    total_internal_links = 0
    for index, row in df.iterrows():
        links = row['Lnternal Llinks']
        if isinstance(links, str): 
            links_list = links.split(',')
            num_internal_links = len(links_list)
            total_internal_links += num_internal_links
    return total_internal_links

# Function to count external links
def count_external_links(df):
    total_external_links = 0
    for index, row in df.iterrows():
        links = row['External Links']
        if isinstance(links, str):  # Check if it's a string
            links_list = links.split(',')
            num_external_links = len(links_list)
            total_external_links += num_external_links
    return total_external_links

# Function to count new tab links
def count_new_tab_links(df):
    total_new_tab_links = 0
    for index, row in df.iterrows():
        links = row['Links Open in new tab']
        if isinstance(links, str):  
            links_list = links.split(',')
            num_new_tab_links = len(links_list)
            total_new_tab_links += num_new_tab_links
    return total_new_tab_links

# Function to count same tab links
def count_same_tab_links(df):
    total_same_tab_links = 0
    for index, row in df.iterrows():
        links = row['Links open in same tab']
        if isinstance(links, str): 
            links_list = links.split(',')
            num_same_tab_links = len(links_list)
            total_same_tab_links += num_same_tab_links
    return total_same_tab_links

# Counting links
brkoen_link_card = count_broken_links(df)
sponsored_link_card = count_sponsored_links(df)
internal_link_card = count_internal_links(df)
external_link_card = count_external_links(df)
new_tab_link_card = count_new_tab_links(df)
same_tab_link_card = count_same_tab_links(df)


st.markdown('<hr>', unsafe_allow_html=True)
st.title('Analysis Dashboard')
st.markdown('</br>', unsafe_allow_html=True)



with st.expander('Total Number of Links Analysis'):
    st.markdown(f"Total broken links: {brkoen_link_card}")
    st.markdown(f"Total sponsored links: {sponsored_link_card}")
    st.markdown(f"Total internal links: {internal_link_card}")
    st.markdown(f"Total external links: {external_link_card}")
    st.markdown(f"Total new tab links: {new_tab_link_card}")
    st.markdown(f"Total same tab links: {same_tab_link_card}")
    st.markdown('<hr>', unsafe_allow_html=True)
    st.bar_chart({
        "Broken Links": brkoen_link_card,
        "Sponsored Links": sponsored_link_card,
        "Internal Links": internal_link_card,
        "External Links": external_link_card,
        "New Tab Links": new_tab_link_card,
        "Same Tab Links": same_tab_link_card
    })

st.markdown('<hr>', unsafe_allow_html=True)


# Post divided in each section
st.info('Posts divided in each section')
section_counts = df['Article Section'].value_counts()   

fig = px.pie(
    names=section_counts.index,
    values=section_counts.values,
    hole = 0.4
)
st.plotly_chart(fig)
st.markdown('<hr>', unsafe_allow_html=True)




# Total number of posts in each section
st.info('Total number of posts in each section')
st.bar_chart(section_counts, height=300) 
st.markdown('</br>', unsafe_allow_html=True)


# Number of articles by author
st.info('Number of Articles by Author')
author_counts = df['Author Name'].value_counts().reset_index()
author_counts.columns = ['Author Name', 'Count'] 
fig = px.bar(author_counts, x='Author Name', y='Count')
fig.update_layout(xaxis_title='Author Name', yaxis_title='Number of Articles')
st.plotly_chart(fig)
st.markdown('<br>', unsafe_allow_html=True)



# Select The author name to see the author performace
st.info('Author Performance Analysis')

# Expander for the author search and selection section
with st.expander('Select an author to see their performance in each section.'):
    
    search_term = st.text_input('Enter name:', '')
    st.caption('Note : Write the first few letters of the author name and hit the enter button you get the suggestions')
    if search_term:
        filtered_names = df[df['Author Name'].str.contains(search_term, case=False)]['Author Name'].unique()

        if len(filtered_names) > 0:
            st.success(f'{len(filtered_names)} authors found with the given search term.')
            selected_author = st.selectbox('Select an author:', filtered_names, index=0)
            st.write(f'Selected author: {selected_author}')
            
            author_counts = df['Author Name'].value_counts().reset_index()
            author_counts.columns = ['Author Name', 'Count']
            total_articles = author_counts[author_counts['Author Name'] == selected_author]['Count'].values[0]
            st.write(f'Total articles by {selected_author}: {total_articles}')
            
            st.write(f'Number of Articles written by {selected_author} in each section:')
            st.bar_chart(df[df['Author Name'] == selected_author]['Article Section'].value_counts())
        else:
            st.warning('No author found with the given search term.')
    else:
        st.write('Enter a search term to begin.')
st.markdown('</br>', unsafe_allow_html=True)        







st.info('Total number of posts by date')
selection = st.selectbox('Select time period', ['Week', 'Month', 'Year'])

# Convert 'Article Date' to datetime if not already done
df['Article Date'] = pd.to_datetime(df['Article Date'])

if selection == 'Week':
    df['Week'] = df['Article Date'].dt.isocalendar().week
    total_posts = df.groupby('Week')['Article Heading'].count()
    st.bar_chart(total_posts, height=300)

elif selection == 'Month':
    df['Month'] = df['Article Date'].dt.month
    total_posts = df.groupby('Month')['Article Heading'].count()
    st.bar_chart(total_posts, height=300)

else:
    df['Year'] = df['Article Date'].dt.year
    total_posts = df.groupby('Year')['Article Heading'].count()
    st.bar_chart(total_posts, height=300)

st.markdown('<hr>', unsafe_allow_html=True)
st.info('New tab links vs Same tab links')
st.bar_chart({
    'New Tab Links': count_new_tab_links(df),
    'Same Tab Links': count_same_tab_links(df)
})

st.markdown('<hr>', unsafe_allow_html=True)
st.info('External links vs Internal links')
st.bar_chart({
    'External Links': count_external_links(df),
    'Internal Links': count_internal_links(df)
})
