import streamlit as st
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
import base64

st.set_page_config(
    page_title="VTS Customer Churn Prediction App",
    page_icon="vts_logo1.png",  
    layout='wide'
)

names = ['Visitor', 'Admin']
usernames = ['user', 'admin']

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {
    "usernames": {
        "user": {
            "name": "Visitor",
            "password": hashed_passwords[0]
        },
        "admin": {
            "name": "Admin",
            "password": hashed_passwords[1]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    'churn_app',  # app name
    'abcdefg',  # key
    10
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

col1, col2 = st.columns([2, 1])

with col1:
    if not st.session_state.get('authentication_status'):
        st.markdown('### **Login**')
        name, authentication_status, username = authenticator.login('Login', 'main')
        st.session_state['name'] = name
        st.session_state['authentication_status'] = authentication_status
        st.session_state['username'] = username

        if authentication_status == None:
            st.info('Please Log in to continue')
            # st.markdown('### **Demo credentials**')
            # st.write('Username: user')
            # st.write('Password: abc123')
            st.markdown('''
                <style>
                [data-testid="stSidebar"] {
                    visibility: hidden;
                }
                </style>
                ''', unsafe_allow_html=True)

if st.session_state.get('authentication_status') == False:
    with col1:
        st.title('Welcome to the VTS Customer Churn Prediction App')
        st.write('This application has been developed with dedication by Team Zigma.')
        # st.write('See something you like? Leave us a star on [GitHub](https://github.com/Team-Zigma).⭐️😍')
        # st.write('Connect with us on [LinkedIn](https://www.linkedin.com/in/team-zigma/) for further discussions.')

    with col2:
        st.error('Wrong username / password')
        st.info('Please try again with the credentials below')
        st.markdown('### **Demo credentials**')
        st.write('Username: user')
        st.write('Password: abc123')
        st.markdown('''
        <style>
        [data-testid="stSidebar"] {
            visibility: hidden;
        }
        </style>
        ''', unsafe_allow_html=True)

if st.session_state.get('authentication_status'):
    st.button(f'{st.session_state["name"]} logged in')
    st.title(f'Heya {st.session_state["username"]}!!')

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
    <h1>Welcome to the VTS Customer Churn Prediction App</h1>
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
    authenticator.logout('Logout', 'main')
