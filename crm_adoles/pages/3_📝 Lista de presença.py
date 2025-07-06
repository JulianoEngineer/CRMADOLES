import streamlit as st
import boto3
import json
import base64
from datetime import datetime

st.set_page_config(page_title="Lista de Chamada", page_icon="📝")

s3 = boto3.resource('s3',    
                    aws_access_key_id = st.secrets["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws_secret_access_key"]
                    )
baldinho = s3.Bucket('crmadole')

st.header("Registro de Presença")

# Fetch existing cadastros for the pre-determined list
cadastrados_nomes = []
cadastrados_data = {} 
for balde in baldinho.objects.all(): 
    if balde.key.endswith('.json') and not balde.key.startswith('attendance/'): 
        try: 
            file_content = balde.get()['Body'].read().decode('utf-8') 
            json_content = json.loads(file_content) 
            cadastrados_data[json_content['Nome']] = json_content 
        except json.JSONDecodeError: 
            st.warning(f"Skipping malformed JSON file: {balde.key}") 

with st.form("attendance_form", clear_on_submit=True):
    event_date = st.date_input("Data do Evento", value=datetime.now().date())
    event_time = st.time_input("Hora do Evento", value=datetime.now().time())
    event_name = st.text_input("Nome do Evento")

    st.subheader("Marcar Presença")
    
    attendance_list = {}
    
    # Determine the number of columns based on screen width
    # Streamlit doesn't directly expose screen width, so we'll use a fixed number or adjust based on content
    num_columns = 2 # You can adjust this number
    cols = st.columns(num_columns)
    
    sorted_names = sorted(cadastrados_data.keys())
    for i, nome in enumerate(sorted_names):
        with cols[i % num_columns]:
            decoded_photo = base64.b64decode(cadastrados_data[nome]['Foto'])
            st.image(decoded_photo, width=100)
            attendance_list[nome] = st.checkbox(nome, key=f"checkbox_{nome}")

    st.subheader("Adicionar Nomes Extras")
    extra_names_input = st.text_area("Nomes extras (um por linha)")
    
    submitted = st.form_submit_button("Registrar Presença")

    if submitted:
        present_members = [name for name, present in attendance_list.items() if present]
        
        if extra_names_input:
            extra_names = [name.strip() for name in extra_names_input.split('\n') if name.strip()]
            present_members.extend(extra_names)

        if not event_name:
            st.error("Por favor, insira o nome do evento.")
        elif not present_members:
            st.warning("Nenhum membro foi marcado como presente.")
        else:
            st.success("Registrando lista de presença...")
        
        attendance_record = {
            "Data do Evento": str(event_date),
            "Hora do Evento": str(event_time),
            "Nome do Evento": event_name,
            "Presentes": present_members
        }

        # Save the attendance record to S3
        s3object = s3.Object('crmadole', f'attendance/{event_name.replace(" ", "_")}_{event_date}_{event_time}.json')
        s3object.put(Body=(json.dumps(attendance_record, indent=4, ensure_ascii=False).encode('utf-8')))

        st.success(f"Lista de presença para '{event_name}' registrada com sucesso!")

        