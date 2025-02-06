import streamlit as st

with st.form("Cadastro Adoles"):
    
    foto = st.camera_input("Fotinha")
    nome = st.text_input("Nome")
    email = st.text_input("E-mail",)
    data_nasc = st.date_input("Data de nascimento",format="DD/MM/YYYY")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        st.write("nome", nome, "email", email,"data_nasc", data_nasc)
