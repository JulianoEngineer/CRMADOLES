import streamlit as st
import boto3
import json
import math
import base64

st.set_page_config(page_title="Carômetro", page_icon="👦👧")

s3 = boto3.resource('s3',    
                    aws_access_key_id = st.secrets["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws_secret_access_key"]
                    )
baldinho = s3.Bucket('crmadole')

st.header("Lista de pessoas cadastradas")

cadastrados = {}
for balde in baldinho.objects.all():
    file_content = balde.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    nome = json_content['Nome']
    cadastrados[nome] = json_content['Foto']

rows = math.ceil(len(cadastrados.keys())/2)

for idx in range(rows):

    col1, col2 = st.columns(2)

    with col1:
        key = list(cadastrados.keys())[idx*2]
        st.markdown(f"### {key}")
        decoded = base64.b64decode(cadastrados[key])
        st.image(decoded)
    
    with col2:
        key = list(cadastrados.keys())[idx*2+1]
        st.markdown(f"### {key}")
        decoded = base64.b64decode(cadastrados[key])
        st.image(decoded)