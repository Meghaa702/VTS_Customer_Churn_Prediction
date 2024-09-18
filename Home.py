import streamlit as st
from pathlib import Path
import base64

st.set_page_config(
    page_title="VTS Customer Churn Prediction App",
    page_icon="vts_logo1.png",
    layout='wide'
)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_path = 'vts_logo.png'
img_base64 = get_base64_image(image_path)

st.markdown('''
    <style>
    body {
        background-color: white;
        color: black;
        font-family: Arial, sans-serif;
    }
    .logo {
        text-align: center;
        margin-top: 20px;
    }
    .container {
        padding: 20px;
    }
    h1, h2, p, ul, li {
        color: black;
    }
    .welcome-container {
        text-align: center;
    }
    </style>
''', unsafe_allow_html=True)

st.markdown(f'''
    <div class="logo">
        <img src="data:image/png;base64,{img_base64}" alt="Logo" style="width: 400px;"/>
    </div>
''', unsafe_allow_html=True)

st.markdown('''
    <div class="welcome-container">
        <h1>Welcome to the VTS Customer Churn Prediction App</h1>
        <p>This application has been developed with dedication by Team Zigma.</p>
    </div>
''', unsafe_allow_html=True)

st.markdown('''
    <style>
    .container p {
        text-indent: 30px;
        text-align: justify;
    }
    .container ul {
        padding-left: 40px;
    }
    .container li {
        margin-bottom: 10px;
    }
    </style>
    <div class="container">
    <p>Our app leverages advanced machine learning algorithms to analyze customer data and identify patterns that indicate a high risk. Review and analyze past predictions, and gain a deeper understanding of your customers' behavior. Our intuitive design ensures a seamless and efficient experience. Simply input your customer data, select from our robust machine learning models (AdaBoost, Logistic Regression, or Random Forest), and get instant predictions on the likelihood of customer churn.</p>

    <h2>Key Features</h2>
    <ul>
        <li><b>Machine Learning Models:</b> Choose from AdaBoost, Logistic Regression, or Random Forest models to find the best fit for your dataset.</li>
        <li><b>Streamlined Prediction Process:</b> Get quick and accurate results with our efficient prediction process.</li>
        <li><b>Data Retrieval:</b> Access your prediction history anytime, stored in a convenient "history.csv" file.</li>
        <li><b>Data Display:</b> Easily review and analyze past predictions in a clear and organized tabular format.</li>
    </ul>

    <h1>GET STARTED TODAY!</h1>
    <p>Explore our app and discover the value of accurate churn prediction.</p>
    </div>
''', unsafe_allow_html=True)

st.markdown('### ================================================ ')
