# https://pypi.org/project/streamlit-authenticator/
# https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/
# pip install streamlit-authenticator

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np

import yaml
from yaml.loader import SafeLoader

#hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
#print(hashed_passwords)

import pydeck as pdk

chart_data = pd.DataFrame(
   #np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
   np.random.randn(60, 2) / [50, 50] + [51.23228000, -0.33380000], 
   columns=['lat', 'lon'])

def show3DMap():
    st.pydeck_chart(pdk.Deck(
        map_style= 'light',     #'dark',              #None,
        initial_view_state=pdk.ViewState(
            latitude=51.23228000,
            longitude=-0.33380000,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
            'HexagonLayer',
            data=chart_data,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def showMap():
    df = pd.DataFrame(
    #np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],               #San Francisco
    np.random.randn(40, 2) / [50, 50] + [51.23228000, -0.33380000],     # Dorking
    columns=['lat', 'lon'])
    st.map(df)

def showLogin():
    authenticator.login('Login', 'main')

    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'main', key='unique_key')
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Docking Map')
        show3DMap()
        
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

def writeConfig(config1):
    # Update config.yaml file wedget ================================================================
    with open('config.yaml', 'w') as file:
        st.write(config1)
        yaml.dump(config1, file, default_flow_style=False)
        
def showRegister():
    # Register new users wedget ====================================================================
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
            #st.write(config)
            writeConfig(config)
    except Exception as e:
        st.error(e)

def showResetPassword():
    # Reset password wedget ========================================================================
    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"], 'Reset password'):
                st.success('Password modified successfully')
                writeConfig(config)
        except Exception as e:
            st.error(e)

def showForgotPassword():
    # Forgot password wedget =======================================================================
    try:
        username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
        if username_of_forgotten_password:
            st.success('New password to be sent securely')
            # Random password should be transferred to user securely
        else:
            st.error('Username not found')
    except Exception as e:
        st.error(e)    

def showUpdate():
    # update user details wedget ====================================================================
    try:
        if authenticator.update_user_details(st.session_state["username"], 'Update user details'):
            st.success('Entries updated successfully')
            #st.write(config)
            writeConfig(config)
    except Exception as e:
        st.error(e)


    
option = st.sidebar.selectbox(
    'What would you like to do?',
    ('Login', 'Register','Reset Password', 'Forgot Password','Update'))
st.sidebar.write('You selected:', option)
if (option=='Login'):
    showLogin()
elif (option=='Register'):
    showRegister()
elif (option=='Forgot Password'):
    showForgotPassword()
elif (option=='Reset Password'):
    showResetPassword()
elif (option=='Update'):
    showUpdate()
else:
    showLogin()




    

    
