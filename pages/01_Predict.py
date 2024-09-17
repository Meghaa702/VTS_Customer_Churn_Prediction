import os
import streamlit as st
import joblib
import pandas as pd
import sys
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


st.set_page_config(
    page_title="Churn Prediction App",
    page_icon="vts_logo1.png",
    layout='wide'
)

# Add logo at the top center of the page

import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_path = "vts_logo.png"  
img_base64 = get_base64_image(logo_path)

st.markdown(f"""
    <div style='text-align: center; margin-top: 20px;'>
        <img src='data:image/png;base64,{img_base64}' style='width: 400px; height: auto;' />
    </div>
""", unsafe_allow_html=True)


st.title('Select a Model and Predict the Future')


@st.cache_resource(show_spinner='Loading prediction Models')
def load_adaboost():
    pipeline = joblib.load('./models/adaboost.joblib')
    return pipeline


@st.cache_resource(show_spinner='Loading prediction Models')
def load_logisticreg():
    pipeline = joblib.load('./models/logisticregression.joblib')
    return pipeline


@st.cache_resource(show_spinner='Loading prediction Models')
def load_randomforest():
    pipeline = joblib.load('./models/randomforest.joblib')
    return pipeline


encoder = joblib.load('./models/encoder.joblib')

if 'pipeline' not in st.session_state:
    st.session_state['pipeline'] = None

if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = None

if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

def selected_model():
    col1, col2, col3 = st.columns(3)
    with col1:
        AB = st.button('Adaboost')
        if AB:
            st.session_state['selected_model'] = 'adaboost'
            st.session_state['pipeline'] = load_adaboost()

    with col2:
        LR = st.button('Logistic Regression')
        if LR:
            st.session_state['selected_model'] = 'logistic_regression'
            st.session_state['pipeline'] = load_logisticreg()

    with col3:
        RF = st.button('Random Forest')
        if RF:
            st.session_state['selected_model'] = 'random_forest'
            st.session_state['pipeline'] = load_randomforest()


def make_prediction(features: pd.DataFrame, model):
    prediction = model.predict(features)
    probability = model.predict_proba(features)

    return prediction, probability


def predict():
    selected_model()

    if st.session_state['selected_model'] is None:
        st.warning('No Model Selected, Please Select a Model to continue')
    else:
        st.success(f'Selected model is: {st.session_state["selected_model"]}')

    with st.form('input features'):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write('### Demographics')
            gender = st.radio('gender', options=['Male', 'Female'], key='gender', horizontal=True)
            SeniorCitizen = st.radio('SeniorCitizen', options=[0, 1], key='SeniorCitizen', horizontal=True)
            Partner = st.radio('Partner', options=['Yes', 'No'], key='Partner', horizontal=True)
            Dependents = st.radio('Dependents', options=['Yes', 'No'], key='Dependents', horizontal=True)

        with col2:
            st.write('### Basic Services')
            PhoneService = st.radio('PhoneService', options=['Yes', 'No'], key='PhoneService', horizontal=True)
            MultipleLines = st.radio('MultipleLines', options=['Yes', 'No'], key='MultipleLines', horizontal=True)
            InternetService = st.radio('InternetService', options=['Fiber optic', 'DSL', 'No'], key='InternetService')
            OnlineSecurity = st.radio('OnlineSecurity', options=['Yes', 'No'], key='OnlineSecurity', horizontal=True)

        with col3:
            st.write('### Other Services')
            OnlineBackup = st.radio('OnlineBackup', options=['Yes', 'No'], key='OnlineBackup', horizontal=True)
            DeviceProtection = st.radio('DeviceProtection', options=['Yes', 'No'], key='DeviceProtection', horizontal=True)
            TechSupport = st.radio('TechSupport', options=['Yes', 'No'], key='TechSupport', horizontal=True)
            StreamingTV = st.radio('StreamingTV', options=['Yes', 'No'], key='StreamingTV', horizontal=True)
            StreamingMovies = st.radio('StreamingMovies', options=['Yes', 'No'], key='StreamingMovies', horizontal=True)

        with col4:
            st.write('### Billing')
            Contract = st.radio('Contract', options=['Month-to-month', 'Two year', 'One year'], key='Contract')
            PaperlessBilling = st.radio('PaperlessBilling', options=['Yes', 'No'], key='PaperlessBilling', horizontal=True)
            PaymentMethod = st.radio('PaymentMethod', options=['Electronic check', 'Credit card (automatic)', 'Mailed check', 'Bank transfer (automatic)'], key='PaymentMethod')

        col5, col6, col7 = st.columns(3)
        with col5:
            tenure = st.slider('tenure', min_value=1, max_value=71, step=1, key='tenure')

        with col6:
            MonthlyCharges = st.slider('MonthlyCharges', min_value=1, key='MonthlyCharges')

        with col7:
            TotalCharges = MonthlyCharges * tenure
            st.metric(label='Total Charges', value=TotalCharges)

        if st.form_submit_button('Submit'):
            st.session_state['button_clicked'] = True

            input_features = pd.DataFrame({
                'tenure': [tenure],
                'monthlycharges': [MonthlyCharges],
                'totalcharges': [TotalCharges],
                'partner': [Partner],
                'dependents': [Dependents],
                'phoneservice': [PhoneService],
                'multiplelines': [MultipleLines],
                'internetservice': [InternetService],
                'onlinesecurity': [OnlineSecurity],
                'onlinebackup': [OnlineBackup],
                'deviceprotection': [DeviceProtection],
                'techsupport': [TechSupport],
                'streamingtv': [StreamingTV],
                'streamingmovies': [StreamingMovies],
                'contract': [Contract],
                'paperlessbilling': [PaperlessBilling],
                'paymentmethod': [PaymentMethod],
                'seniorcitizen': [SeniorCitizen],
                'gender': [gender]
            })
            pred_features = input_features.astype('object')

            if st.session_state['pipeline'] is not None:
                prediction, probabilities = make_prediction(pred_features, st.session_state['pipeline'])
            else:
                st.error('No Model Selected, Please Select a Model above to continue')
                sys.exit()

            if prediction == 0:
                prediction = 'Stay'
            else:
                prediction = 'Churn'

            probability = pd.DataFrame(probabilities).T
            stay_proba = round(probability[0][0] * 100, ndigits=2)
            churn_proba = round(probability[0][1] * 100, ndigits=2)

            st.markdown("### **Prediction Results**")
            if prediction == 'Stay':
                st.success(f"The customer has a {stay_proba}% probability of staying")
            else:
                st.error(f"The customer is likely to leave with a {churn_proba}% probability")

            input_features['prediction'] = [prediction]
            input_features['churn probability %'] = [churn_proba]
            input_features['remain probability %'] = [stay_proba]
            input_features['model_used'] = [st.session_state['selected_model']]

            if os.path.exists('Data/history.csv'):
                history_data = pd.read_csv('Data/history.csv')
                history_data = pd.concat([history_data, input_features], ignore_index=True)
            else:
                history_data = input_features

            history_data.to_csv('Data/history.csv', index=False)


if __name__ == '__main__':
    predict()
    if st.session_state['button_clicked']:
        response = st.radio('Do you want to try another model?', options=['No', 'Yes'])
        if response == 'Yes':
            st.session_state['button_clicked'] = False
            st.session_state['selected_model'] = None
            st.session_state['pipeline'] = None
            st.experimental_rerun()
