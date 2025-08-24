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
for obj in baldinho.objects.filter(Prefix="perfis/"):
    if obj.key.endswith("/"):
        continue
    nome = obj.key.split("/")[-1]  # pega só o nome do arquivo
    nome = nome.split(".")[0].replace("_", " ")  # remove extensão e ajusta underscores
    cadastrados.append(nome)
    
#size_rows = len(cadastrados)/2
st.table(cadastrados)
