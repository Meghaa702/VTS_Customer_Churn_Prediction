import streamlit as st
import pandas as pd
import os
import time
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

st.title('Prediction History')

def load_history():
    if os.path.exists('Data/history.csv'):
        history_df = pd.read_csv('Data/history.csv')
    else:
        history_df = pd.DataFrame()  
    return history_df

def clear_history():
    if os.path.exists('Data/history.csv'):
        with st.spinner('Cleaning past history...'):
            os.remove('Data/history.csv')
            time.sleep(3)
        st.success('History Cleared Successfully')
        time.sleep(3)  
        st.experimental_rerun()
    else:
        st.warning("History is already empty.")
        time.sleep(2)  
        st.experimental_rerun()

def main(): 
    history_df = load_history()
    
    
    if not history_df.empty:
        st.write(history_df)
    else:
        st.error("History is empty.")
    
    
    if st.button('Clear History'):
        clear_history()
        time.sleep(2)  
        st.experimental_rerun()

if __name__ == '__main__':
    main()
