import streamlit as st
import boto3
import json
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Histórico de Chamadas", page_icon="📊")

s3 = boto3.resource('s3',    
                    aws_access_key_id = st.secrets["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws_secret_access_key"]
                    )
baldinho = s3.Bucket('crmadole')

st.header("Histórico de Chamadas")

attendance_records = []
for balde in baldinho.objects.all():
    if balde.key.startswith('attendance/') and balde.key.endswith('.json'):
        try:
            file_content = balde.get()['Body'].read().decode('utf-8')
            json_content = json.loads(file_content)
            attendance_records.append(json_content)
        except json.JSONDecodeError:
            st.warning(f"Skipping malformed JSON file: {balde.key}")

if not attendance_records:
    st.info("Nenhum registro de chamada encontrado.")
else:
    # Sort records by date and time
    attendance_records.sort(key=lambda x: (x.get('Data do Evento', ''), x.get('Hora do Evento', '')), reverse=True)

    for record in attendance_records:
        event_name = record.get("Nome do Evento", "N/A")
        event_date = record.get("Data do Evento", "N/A")
        event_time = record.get("Hora do Evento", "N/A")
        present_members = record.get("Presentes", [])

        st.subheader(f"{event_name}")
        st.write(f"**Data:** {event_date}")
        st.write(f"**Hora:** {event_time}")
        
        # Create a DataFrame for the attendance list
        # Only create a DataFrame if there are present members to avoid IndexError with openpyxl
        if present_members:
            df = pd.DataFrame({"Nome": present_members})
        else:
            df = pd.DataFrame({"Nome": ["Nenhum presente"]}) # Or an empty DataFrame if that's preferred

        # Create an in-memory Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name='Presença', index=False)
        output.seek(0) # Rewind the buffer to the beginning
        
        st.download_button(
            label="Baixar Lista de Presença (Excel)",
            data=output.getvalue(),
            file_name=f"lista_presenca_{event_name.replace(' ', '_')}_{event_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_button_{event_name}"
        )
        st.write("---")