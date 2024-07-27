import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data():
    return pd.read_csv('Data/Netflix_User.csv')

data = load_data()

# Custom CSS for styling
st.markdown("""
    <style>
    /* Full Background Color */
    body, .main, .css-1lcbmhc, .css-1q8dd3e, .css-1d391kg {
        background-color: black;
        color: white;
    }
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: black;
    }
    .css-1d391kg .css-1l02z79 {
        color: #fff;
    }
    .css-1d391kg .css-18e3g3r {
        background-color: #000;
    }
    /* Select box and Checkbox Styling */
    .css-1l02z79, .css-1cpxqw2, .css-10trblm {
        color: red !important;  /* Text color of the filters */
    }
    .css-1l02z79 .st-bq, .css-1cpxqw2 .st-bq, .css-10trblm .st-bq {
        color: #ff0000 !important;  /* Text color of the options */
    }
    .css-1l02z79 .st-bs, .css-1cpxqw2 .st-bs, .css-10trblm .st-bs {
        background-color: #ff0000 !important; /* Background color of the selected option */
    }
    .css-1l02z79 .st-br, .css-1cpxqw2 .st-br, .css-10trblm .st-br {
        border-color: #ff0000 !important; /* Border color of the options */
    }
    /* Metric Box Styling */
    .metric-box {
        background-color: #000;
        color: #fff;
        padding: 20px;
        border-radius: 0px;
        text-align: center;
        width: 320px;
        height: 110px;
        margin-bottom: 15px;
    }

    .metric-box.total-revenue {
    }

    .metric-box.total-subscriptions {
    }

    .metric-box .title {
        font-size: 15px;
        font-weight: bold;
    }

    .metric-box .value {
        font-size: 36px;
        color: #ff0000;
        font-weight: bold;
    }
    /* Layout and Color Adjustments */
    .container {
        display: flex;
        gap: 20px;
        margin-bottom: 40px;
    }
    .filters-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-left: 20px;
    }
    .chart-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .stButton button {
        background-color: red;
        color: white;
        border-radius: 5px;
        border: 1px solid red;
    }
    .stButton button:hover {
        background-color: #5E1914;
    }
    .button-container {
        display: flex;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar with navigation

st.sidebar.image('Images/Logo.png', width=300)  # Replace with the path to your Netflix image

# Navigation

page = st.sidebar.radio('Select Page', options=['Subscription Analysis', 'Revenue Analysis'])

# Filters

st.sidebar.write('Please Apply Filters')
subscription_type = st.sidebar.radio('Select Subscription Type', options=['All'] + list(data['Subscription Type'].unique()))

selected_countries = st.sidebar.multiselect(
    'Select Countries',
    options=data['Country'].unique(),
    default=data['Country'].unique()
)

col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    title = "NETFLIX User Subscription Analysis" if page == 'Subscription Analysis' else "NETFLIX Revenue Analysis"
    html_title = f"""
        <h1 style="font-size: 2.5em; margin: 0;">
            <span style="color: red;">{title.split()[0]}</span>
            <span style="color: white;">{' '.join(title.split()[1:])}</span>
        </h1>
        """
    st.markdown(html_title, unsafe_allow_html=True)

with col2:
    # Gender filter
    gender = st.selectbox(
        'Select Gender',
        options=['All'] + list(data['Gender'].unique()),
        key='gender'
    )

with col3:
    # Device filter
    device = st.selectbox(
        'Select Device',
        options=['All'] + list(data['Device'].unique()),
        key='device'
    )

# Apply filters
filtered_data = data.copy()
if subscription_type != 'All':
    filtered_data = filtered_data[filtered_data['Subscription Type'] == subscription_type]

if selected_countries:
    filtered_data = filtered_data[filtered_data['Country'].isin(selected_countries)]

if gender != 'All':
    filtered_data = filtered_data[filtered_data['Gender'] == gender]

if device != 'All':
    filtered_data = filtered_data[filtered_data['Device'] == device]

# Group age into categories
filtered_data['Age Group'] = pd.cut(filtered_data['Age'], bins=[0, 20, 40, 100], labels=['0-20', '20-40', '40+'])

# Metrics
total_users = filtered_data['User ID'].nunique()
total_revenue = filtered_data['Monthly Revenue'].sum()

html_content = f"""
<div style="display: flex; justify-content: space-between;">
    <div class="metric-box total-revenue" style="background-color:black;color:white;padding:10px;width:48%;">
        <div class="title" style="color:white;">Total Revenue</div>
        <div class="value" style="color:red;">$ {total_revenue} K</div>
    </div>
    <div class="metric-box total-subscriptions" style="background-color:black;color:white;padding:10px;width:48%;">
        <div class="title" style="color:white;">Total Subscriptions</div>
        <div class="value" style="color:red;">{total_users}</div>
    </div>
</div>
"""

st.markdown(html_content, unsafe_allow_html=True)

# Subscription Analysis

if page == 'Subscription Analysis':
    col1, col2 = st.columns([4,4])

    with col1:
        # Subscription by Gender
        fig_sub_gender = px.pie(
            filtered_data.groupby('Gender')['User ID'].count().reset_index(),
            values='User ID', names='Gender',
            title='Total Subscription by Gender',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_sub_gender.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            showlegend=True
        )
        fig_sub_gender.update_traces(textinfo='label+value')
        st.plotly_chart(fig_sub_gender, use_container_width=True)

    with col2:
        # Subscription by Country
        fig_sub_country = px.bar(
            filtered_data.groupby('Country')['User ID'].count().reset_index(),
            x='Country', y='User ID',
            title='Total Subscription by Country',
            color='User ID',
            color_continuous_scale='reds',
            text='User ID',
        )
        fig_sub_country.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            yaxis={'visible': False},
            showlegend=False
        )
        fig_sub_country.update_traces(textposition='outside')
        st.plotly_chart(fig_sub_country, use_container_width=True)

    col1, col2, col3 = st.columns([4,4,4])

    with col1:
        fig_sub_age = px.bar(
            filtered_data.groupby('Age Group')['User ID'].count().reset_index(),
            x='Age Group', y='User ID',
            title='Total Subscription by Age',
            color='User ID',
            color_continuous_scale='reds',
            text='User ID',
        )
        fig_sub_age.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            yaxis={'visible': False},
            showlegend=True
        )
        fig_sub_age.update_traces(textposition='outside')
        st.plotly_chart(fig_sub_age, use_container_width=True)
    
    with col2:
        fig_sub_type = px.bar(
            filtered_data.groupby('Subscription Type')['User ID'].count().reset_index(),
            x='Subscription Type', y='User ID',
            title='Total Subscription by Type',
            color='User ID',
            color_continuous_scale='reds',
            text='User ID',
        )
        fig_sub_type.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            yaxis={'visible': False},
            showlegend=False
        )
        fig_sub_type.update_traces(textposition='outside')
        st.plotly_chart(fig_sub_type, use_container_width=True)

    with col3:
        # Subscription by Device
        fig_sub_device = px.pie(
            filtered_data.groupby('Device')['User ID'].count().reset_index(),
            values='User ID', names='Device',
            title='Total Subscription by Device',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_sub_device.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            showlegend=True
        )
        fig_sub_device.update_traces(textinfo='label+value')
        st.plotly_chart(fig_sub_device, use_container_width=True)

# Revenue Analysis

elif page == 'Revenue Analysis':
    col1, col2 = st.columns([4,4])

    with col1:
        # Revenue by Gender
        fig_rev_gender = px.pie(
            filtered_data.groupby('Gender')['Monthly Revenue'].sum().reset_index(),
            values='Monthly Revenue', names='Gender',
            title='Total Revenue by Gender',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_rev_gender.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            showlegend=True
        )
        fig_rev_gender.update_traces(textinfo='label+value')
        st.plotly_chart(fig_rev_gender, use_container_width=True)

    with col2:
        # Revenue by Country
        fig_rev_country = px.bar(
            filtered_data.groupby('Country')['Monthly Revenue'].sum().reset_index(),
            x='Country', y='Monthly Revenue',
            title='Total Revenue by Country',
            color='Monthly Revenue',
            color_continuous_scale='reds',
            text='Monthly Revenue',
        )
        fig_rev_country.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            yaxis={'visible': False},
            showlegend=False
        )
        fig_rev_country.update_traces(textposition='outside')
        st.plotly_chart(fig_rev_country, use_container_width=True)

    col1, col2, col3 = st.columns([4,4,4])

    with col1:
        # Revenue by Age Group
        fig_rev_age = px.bar(
            filtered_data.groupby('Age Group')['Monthly Revenue'].sum().reset_index(),
            x='Age Group', y='Monthly Revenue',
            title='Total Revenue by Age',
            color='Monthly Revenue',
            color_continuous_scale='reds',
            text='Monthly Revenue',
        )
        fig_rev_age.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            yaxis={'visible': False},
            showlegend=False
        )
        fig_rev_age.update_traces(textposition='outside')
        st.plotly_chart(fig_rev_age, use_container_width=True)

    with col2:
        # Revenue by Subscription Type
        fig_rev_type = px.bar(
            filtered_data.groupby('Subscription Type')['Monthly Revenue'].sum().reset_index(),
            x='Subscription Type', y='Monthly Revenue',
            title='Total Revenue by Subscription Type',
            color='Monthly Revenue',
            color_continuous_scale='reds',
            text='Monthly Revenue',
        )
        fig_rev_type.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            yaxis={'visible': False},
            showlegend=False
        )
        fig_rev_type.update_traces(textposition='outside')
        st.plotly_chart(fig_rev_type, use_container_width=True)

    with col3:
        # Revenue by Device
        fig_rev_device = px.pie(
            filtered_data.groupby('Device')['Monthly Revenue'].sum().reset_index(),
            values='Monthly Revenue', names='Device',
            title='Total Revenue by Device',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_rev_device.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            showlegend=True
        )
        fig_rev_device.update_traces(textinfo='label+value')
        st.plotly_chart(fig_rev_device, use_container_width=True)
