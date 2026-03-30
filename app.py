import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configurações de exibição para o Tablet
st.set_page_config(page_title="Registro Clínico ABA", layout="centered")

st.title("📊 Registro de Hierarquia de Dicas")
st.subheader("Coordenação - Casa do Autista")

# URL da sua planilha
url = "https://docs.google.com/spreadsheets/d/1qYarfuNSvsNA3IZ60jtff9VC3eFUqJ_ksENQa4OoGys/edit?usp=sharing"

# Estabelece a conexão com o Google Sheets usando os Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulário de entrada de dados
with st.form("registro_aba", clear_on_submit=True):
    nome = st.text_input("Nome da Criança")
    data_sessao = st.date_input("Data da Sessão", datetime.now())
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        ft = st.number_input("Dica Física Total (FT)", min_value=0, step=1)
        fp = st.number_input("Dica Física Parcial (FP)", min_value=0, step=1)
        gt = st.number_input("Dica Gestual (GT)", min_value=0, step=1)
    with col2:
        vt = st.number_input("Dica Verbal (VT)", min_value=0, step=1)
        id_ind = st.number_input("Independente (ID)", min_value=0, step=1)
    
    botao_salvar = st.form_submit_button("✅ Gravar Dados na Planilha")

# Lógica de processamento e envio
if botao_salvar:
    if nome:
        # Cálculo de Independência: ID(4), VT(3), GT(2), FP(1), FT(0)
        total = ft + fp + gt + vt + id_ind
        score = ((id_ind * 4) + (vt * 3) + (gt * 2) + (fp * 1)) / (total * 4) * 100 if total > 0 else 0
        
        # 1. Ler os dados atuais da planilha
        try:
            df_atual = conn.read(spreadsheet=url)
            
            # 2. Criar a nova linha
            nova_linha = pd.DataFrame([{
                "Data": data_sessao.strftime("%d/%m/%Y"),
                "Paciente": nome,
                "FT": ft, "FP": fp, "GT": gt, "VT": vt, "ID": id_ind,
                "Independencia": f"{score:.2f}%"
            }])
            
            # 3. Concatenar e atualizar a planilha
            df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
            conn.update(spreadsheet=url, data=df_final)
            
            st.success(f"Excelente! Os dados de {nome} foram gravados. Independência: {score:.1f}%")
            st.balloons() # Efeito visual de sucesso
            
        except Exception as e:
            st.error("Erro na conexão. Verifique se os 'Secrets' foram colados corretamente no painel do Streamlit.")
            st.info("O e-mail da Conta de Serviço precisa ter permissão de 'Editor' na sua planilha.")
    else:
        st.warning("Por favor, introduza o nome do paciente.")
