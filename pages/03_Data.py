import streamlit as st
import numpy as np
import pandas as pd
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

st.title('Check the data used in building this Web app')
st.write('Click the buttons to show the dataset')

df = pd.read_csv('Data/Dataset.csv')

def show_numerics():
    numeric = df.select_dtypes(include=[np.number]).columns
    for col in numeric:
        df[col] = df[col].apply(lambda x: f"{x:.2f}")
    return df[numeric]

def show_categoricals():
    categorical = df.select_dtypes(exclude=[np.number]).columns
    return df[categorical].drop(columns=['customerID'])

def SysRerun():
    st.experimental_rerun()

col1, col2, col3 = st.columns(3)
with col1:
    All = st.button('Full Dataset', help='Display the full dataset')
with col2:
    Numerics = st.button('Numeric Columns', help='Display only the numeric columns')
with col3:
    Categorical = st.button('Categorical Columns', help='Display only Categorical columns')

if Numerics:
    st.dataframe(show_numerics())
    Hide = st.button('Hide', help='Hide the Data')
    if Hide:
        SysRerun()
    
elif Categorical:
    st.dataframe(show_categoricals())
    Hide = st.button('Hide', help='Hide the Data')
    if Hide:
        SysRerun()

elif All:
    st.dataframe(df)
    Hide = st.button('Hide', help='Hide the Data')
    if Hide:
        SysRerun()
else:
    pass
