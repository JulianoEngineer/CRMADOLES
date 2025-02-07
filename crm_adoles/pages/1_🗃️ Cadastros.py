import streamlit as st
import boto3

st.set_page_config(page_title="Cadastros", page_icon="🗃️")

s3 = boto3.resource('s3',    
                    aws_access_key_id = st.secrets["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws_secret_access_key"]
                    )
baldinho = s3.Bucket('crmadole')

st.header("Lista de pessoas cadastradas")

cadastrados = []
for balde in baldinho.objects.all():
    cadastrados.append(balde.key.split(".")[0].replace("_"," "))

#size_rows = len(cadastrados)/2
st.table(cadastrados)
