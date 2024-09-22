from __future__ import annotations
from jaclang import jac_import as __jac_import__
import typing as _jac_typ
if _jac_typ.TYPE_CHECKING:
    import streamlit as st
else:
    st, = __jac_import__(target='streamlit', base_path=__file__, lng='py', absorb=False, mdl_alias='st', items={})
if _jac_typ.TYPE_CHECKING:
    import requests
else:
    requests, = __jac_import__(target='requests', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={})

def bootstrap_frontend(token: str) -> None:
    st.write('Welcome to your Demo Agent!')
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    if (prompt := st.chat_input('What is up?')):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):
            response = requests.post('http://localhost:8000/walker/interact', json={'message': prompt, 'session_id': '123'}, headers={'Authorization': f'Bearer {token}'})
            if response.status_code == 200:
                response = response.json()
                print(response)
                st.write(response['reports'][0]['response'])
                st.session_state.messages.append({'role': 'assistant', 'content': response['reports'][0]['response']})
INSTANCE_URL = 'http://localhost:8000'
TEST_USER_EMAIL = 'test@mail.com'
TEST_USER_PASSWORD = 'password'
response = requests.post(f'{INSTANCE_URL}/user/login', json={'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
if response.status_code != 200:
    response = requests.post(f'{INSTANCE_URL}/user/register', json={'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
    assert response.status_code == 201
    response = requests.post(f'{INSTANCE_URL}/user/login', json={'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
    assert response.status_code == 200
token = response.json()['token']
print('Token:', token)
bootstrap_frontend(token)