import streamlit as st
import boto3
import json
import base64

st.set_page_config(page_title="Carômetro", page_icon="👦👧")

s3 = boto3.resource(
    's3',
    aws_access_key_id=st.secrets["aws_access_key_id"],
    aws_secret_access_key=st.secrets["aws_secret_access_key"],
)
baldinho = s3.Bucket('crmadole')

st.header("Lista de pessoas cadastradas")

pessoas = []
# Busca apenas dentro do "diretório" (prefixo) perfis/
for obj in baldinho.objects.filter(Prefix="perfis/"):
    # pula o marcador de diretório (quando existir)
    if obj.key.endswith("/"):
        continue
    try:
        body = obj.get()["Body"].read().decode("utf-8")
        data = json.loads(body)
        nome = data.get("Nome")
        foto_b64 = data.get("Foto")
        if nome and foto_b64:
            pessoas.append((nome, foto_b64))
    except Exception as e:
        st.warning(f"Não foi possível ler '{obj.key}': {e}")

# ordena alfabeticamente pelo nome (opcional)
pessoas.sort(key=lambda x: x[0].lower())

# renderiza em grid 2 colunas, lidando com quantidade ímpar
for i in range(0, len(pessoas), 2):
    col1, col2 = st.columns(2)

    nome1, foto1 = pessoas[i]
    with col1:
        st.markdown(f"### {nome1}")
        st.image(base64.b64decode(foto1))

    if i + 1 < len(pessoas):
        nome2, foto2 = pessoas[i + 1]
        with col2:
            st.markdown(f"### {nome2}")
            st.image(base64.b64decode(foto2))

st.caption(f"{len(pessoas)} pessoa(s) cadastrada(s)")
