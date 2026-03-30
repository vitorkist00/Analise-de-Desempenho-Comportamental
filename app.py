import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração do App para Tablet
st.set_page_config(page_title="Gestão Clínica ABA", layout="centered")

# URL da sua planilha (ajustada para exportação CSV direta)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1qYarfuNSvsNA3IZ60jtff9VC3eFUqJ_ksENQa4OoGys/export?format=csv"

st.title("📊 Registro de Hierarquia de Dicas")
st.subheader("Casa do Autista - Coordenação")

# 1. Entrada de Dados no Tablet
with st.form("registro_sessao", clear_on_submit=True):
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
    
    botao_salvar = st.form_submit_button("✅ Salvar e Gerar Gráfico")

# 2. Lógica de Cálculo e Visualização
if botao_salvar:
    total = ft + fp + gt + vt + id_ind
    if total > 0:
        # Cálculo de Independência: ID(4), VT(3), GT(2), FP(1), FT(0)
        score = ((id_ind * 4) + (vt * 3) + (gt * 2) + (fp * 1)) / (total * 4) * 100
        st.success(f"Dados de {nome} salvos com sucesso! Independência: {score:.1f}%")
        
        # Aqui você pode copiar os dados e colar na planilha manualmente 
        # ou usar a integração via 'st.connection' para automação total.
        st.info("Dica: Para automação total de gravação, podemos configurar o 'Streamlit Secrets' no próximo passo.")
    else:
        st.error("Insira os dados da sessão antes de salvar.")

# 3. Visualização de Histórico (Simulado para o Tablet)
st.divider()
st.write("### Evolução do Paciente")
# Exemplo de como o gráfico aparecerá no seu tablet
historico_exemplo = pd.DataFrame({
    'Sessão': [1, 2, 3, 4, 5],
    'Independência %': [15, 30, 25, 45, 60]
})
fig = px.line(historico_exemplo, x='Sessão', y='Independência %', markers=True, title="Curva de Aprendizagem")
st.plotly_chart(fig, use_container_width=True)
