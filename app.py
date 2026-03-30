import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configurações do Tablet
st.set_page_config(page_title="Gestão Clínica ABA", layout="centered")

st.title("📊 Registro de Hierarquia de Dicas")
st.subheader("Casa do Autista - Coordenação")

# 1. Entrada de Dados
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
    
    botao_salvar = st.form_submit_button("✅ Gerar link de Gravação")

if botao_salvar:
    if nome:
        total = ft + fp + gt + vt + id_ind
        score = ((id_ind * 4) + (vt * 3) + (gt * 2) + (fp * 1)) / (total * 4) * 100 if total > 0 else 0
        
        st.success(f"Cálculo Concluído para {nome}!")
        st.metric("Independência", f"{score:.1f}%")
        
        # Como o Google bloqueia gravações diretas sem chaves de segurança pesadas,
        # vamos usar um botão que abre a planilha já com os dados prontos ou 
        # simplesmente exibe os dados para você dar um 'Check' final.
        
        st.info("Para gravar agora, copie os dados abaixo para sua planilha:")
        dados_txt = f"{data_sessao.strftime('%d/%m/%Y')};{nome};{ft};{fp};{gt};{vt};{id_ind};{score:.1f}%"
        st.code(dados_txt)
    else:
        st.error("Por favor, preencha o nome.")

# Gráfico de exemplo para visualização no tablet
st.divider()
st.write("### Visualização de Progresso")
df_vis = pd.DataFrame({'Sessão': [1,2,3,4], 'Independência': [10, 25, 40, 60]})
fig = px.line(df_vis, x='Sessão', y='Independência', markers=True)
st.plotly_chart(fig, use_container_width=True)
