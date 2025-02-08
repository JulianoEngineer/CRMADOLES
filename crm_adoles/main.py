import streamlit as st
import base64
import json
import boto3    

st.set_page_config(page_title="Adoles CRM", page_icon="📝")

s3 = boto3.resource('s3',    
                    aws_access_key_id = st.secrets["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws_secret_access_key"]
                    )

with st.form("Cadastro Adoles",clear_on_submit=True):
    
    foto = st.camera_input("Fotinha")
    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone contato")
    rede_social = st.text_input("Rede Social")
    genero = st.selectbox("Genero",["M","F"])
    batizado = st.selectbox("Batizado(a)?",["S","N"])
    data_nasc = st.date_input("Data de nascimento",format="DD/MM/YYYY")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Cadastrar")

    if submitted:

        if foto is not None:
            # To read image file buffer with OpenCV:
            bytes_data = foto.getvalue()
            encoded_string = base64.b64encode(bytes_data)

        
        # Data to be written
        dictionary = {
            "Foto": encoded_string.decode(),
            "Nome": nome,
            "Telefone":telefone,
            "Rede Social": rede_social,
            "Genero": genero,
            "Batizado":batizado,
            "Data Nascimento": str(data_nasc)
        }
        
        #decoded = base64.b64decode(encoded_string.decode())
        #st.image(decoded)
        
        s3object = s3.Object('crmadole', f'{nome.replace(" ","_")}.json')


        # Serializing json
        #json_object = json.dumps(dictionary, indent=4)
        
        s3object.put(
            Body=(bytes(json.dumps(dictionary, indent=4).encode('UTF-8')))
        )

        st.toast("Adoles cadastrado!", icon=":material/check_circle:")