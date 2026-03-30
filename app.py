import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Configurações do Tablet
st.set_page_config(page_title="Gestão Clínica ABA", layout="centered")

st.title("📊 Registro de Hierarquia de Dicas")
st.subheader("Casa do Autista - Registro Direto")

# Link da sua planilha (ajustado para conexão)
url = "https://docs.google.com/spreadsheets/d/1qYarfuNSvsNA3IZ60jtff9VC3eFUqJ_ksENQa4OoGys/edit?usp=sharing"

# Criando a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Formulário de Entrada
with st.form("registro_sessao", clear_on_submit=True):
    nome = st.text_input("Nome da Criança")
    data_sessao = st.date_input("Data da Sessão", datetime.now())
    
    col1, col2 = st.columns(2)
    with col1:
        ft = st.number_input("Dica Física Total (FT)", min_value=0, step=1)
        fp = st.number_input("Dica Física Parcial (FP)", min_value=0, step=1)
        gt = st.number_input("Dica Gestual (GT)", min_value=0, step=1)
    with col2:
        vt = st.number_input("Dica Verbal (VT)", min_value=0, step=1)
        id_ind = st.number_input("Independente (ID)", min_value=0, step=1)
    
    botao_salvar = st.form_submit_button("✅ Salvar na Planilha")

if botao_salvar:
    if nome:
        # Cálculo de Independência
        total = ft + fp + gt + vt + id_ind
        score = ((id_ind * 4) + (vt * 3) + (gt * 2) + (fp * 1)) / (total * 4) * 100 if total > 0 else 0
        
        # Preparando a nova linha para a planilha
        nova_linha = pd.DataFrame([{
            "Data": data_sessao.strftime("%d/%m/%Y"),
            "Paciente": nome,
            "FT": ft, "FP": fp, "GT": gt, "VT": vt, "ID": id_ind,
            "Independencia": f"{score:.2f}%"
        }])

        # Lendo dados atuais e adicionando o novo
        dados_atuais = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7])
        dados_atualizados = pd.concat([dados_atuais, nova_linha], ignore_index=True)
        
        # Salvando de volta na planilha
        conn.update(spreadsheet=url, data=dados_atualizados)
        st.success(f"Dados de {nome} enviados para a planilha!")
    else:
        st.error("Por favor, preencha o nome da criança.")
