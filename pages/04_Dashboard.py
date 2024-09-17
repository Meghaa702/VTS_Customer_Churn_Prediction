import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(
    page_title="Churn Prediction App",
    page_icon="vts_logo1.png",
    layout='wide'
)

logo_path = "vts_logo.png"  
img_base64 = get_base64_image(logo_path)

st.markdown(f"""
    <div style='text-align: center; margin-top: 20px;'>
        <img src='data:image/png;base64,{img_base64}' style='width: 400px; height: auto;' />
    </div>
""", unsafe_allow_html=True)

df = pd.read_csv('Data/Dataset.csv')

def numeric(df):
    numeric = df.select_dtypes(include=[np.number])
    return numeric

def categorical(df):
    categorical = df.select_dtypes(exclude=np.number)
    return categorical

st.session_state['Button'] = None
st.write('Select a Dashboard to Display')

@st.spinner('Loading...')
def Univariate_plots():
    st.title("Univariate Analysis")
    col1, col2, col3 = st.columns(3)
    cols = categorical(df).columns.drop(['customerID'])
    for i, col in enumerate(cols):
        with [col1, col2, col3][i % 3]:
            data = df[col].value_counts()
            fig = px.pie(
                values=data,
                names=data.index,
                title=f"{col} Distribution",
                color_discrete_map={'German Shephard': 'rgb(255,255,0)'}
            )
            st.plotly_chart(fig)
                
    col4, col5, col6 = st.columns(3)
    with col4:
        fig = px.box(
            df['tenure'], 
            orientation='h',
            title='Distribution of Tenure',
            hover_data=None
        )
        fig.update_yaxes(visible=False, showticklabels=False)
        st.plotly_chart(fig)

    with col5:
        fig = px.box(
            df['MonthlyCharges'], 
            orientation='h',
            title='Distribution of MonthlyCharges',
            hover_data=None
        )
        fig.update_yaxes(visible=False, showticklabels=False)
        st.plotly_chart(fig)
        
    with col6:
        fig = px.box(
            df['TotalCharges'], 
            orientation='h',
            title='Distribution of TotalCharges',
            hover_data=None
        )
        fig.update_yaxes(visible=False, showticklabels=False)
        st.plotly_chart(fig)

@st.spinner('Loading...')
def Bivariate_plots():
    st.title('Bivariate Analysis')
    col1, col2, col3 = st.columns(3)
    cols = categorical(df).columns.drop(['customerID', 'Churn'])
    for i, col in enumerate(cols):
        with [col1, col2, col3][i % 3]:
            data = df.groupby('Churn')[col].value_counts().reset_index()
            fig = px.bar(
                data,
                x=data[col],
                y=data['count'],
                color=data['Churn'],
                title=f"Churn vs {col}",
                color_discrete_map={'German Shephard': 'rgb(255,255,0)'}
            )
            st.plotly_chart(fig)
            
    numbers = numeric(df)
    for i, col in enumerate(numbers.columns):
        data = df.groupby('Churn')[col].value_counts().reset_index()
        fig = px.bar(
            data,
            x=data[col],
            y=data['count'],
            color=data['Churn'],
            title=f"Churn vs {col}",
            color_discrete_map={'German Shephard': 'rgb(255,255,0)'}
        )
        st.plotly_chart(fig)
    return

def KPI_plots():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(value=df['Churn'].sum(), label='Churned Customers')

colA, colB = st.columns(2)
with colA:
    EDA = st.button('EDA Dashboard', use_container_width=True)
    if EDA:
        st.session_state['Button'] = 'EDA'
with colB:
    KPI = st.button('KPI Dashboard', use_container_width=True)
    if KPI:
        st.session_state['Button'] = 'KPI'

if st.session_state['Button'] == 'EDA':
    Univariate_plots()
    Bivariate_plots()

elif st.session_state['Button'] == 'KPI':
    KPI_plots()
