import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para Tablet
st.set_page_config(page_title="Gestão Clínica ABA", layout="centered")

st.title("📊 Registro de Hierarquia de Dicas")
st.subheader("Casa do Autista - Coordenação")

# 1. Entrada de Dados
with st.form("registro_sessao"):
    nome = st.text_input("Nome da Criança")
    data = st.date_input("Data da Sessão")
    
    col1, col2 = st.columns(2)
    with col1:
        ft = st.number_input("Dica Física Total (FT)", min_value=0, step=1)
        fp = st.number_input("Dica Física Parcial (FP)", min_value=0, step=1)
        gt = st.number_input("Dica Gestual (GT)", min_value=0, step=1)
    with col2:
        vt = st.number_input("Dica Verbal (VT)", min_value=0, step=1)
        id_ind = st.number_input("Independente (ID)", min_value=0, step=1)
    
    submit = st.form_submit_button("Salvar Registro")

# 2. Lógica de Cálculo (Exemplo de Peso para Independência)
# Atribuímos valores: ID=4, VT=3, GT=2, FP=1, FT=0
if submit:
    total_respostas = ft + fp + gt + vt + id_ind
    if total_respostas > 0:
        score_independencia = ((id_ind * 4) + (vt * 3) + (gt * 2) + (fp * 1)) / (total_respostas * 4) * 100
        st.success(f"Sessão de {nome} registrada! Nível de Independência: {score_independencia:.2f}%")
        
        # Aqui o código salvaria em um banco de dados ou CSV
    else:
        st.warning("Por favor, insira ao menos uma resposta.")

# 3. Visualização (Simulação de histórico)
st.divider()
st.write("### Tendência de Aprendizagem")
# Exemplo de gráfico para o tablet
dados_exemplo = pd.DataFrame({
    'Data': pd.date_range(start='2026-03-01', periods=5),
    'Independência (%)': [20, 35, 30, 55, 70]
})
fig = px.line(dados_exemplo, x='Data', y='Independência (%)', markers=True)
st.plotly_chart(fig, use_container_width=True)
