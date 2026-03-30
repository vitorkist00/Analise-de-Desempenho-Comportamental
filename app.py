import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configurações do App
st.set_page_config(page_title="Gestão Clínica - Casa do Autista", layout="wide")

st.title("📊 Registro de Desempenho Comportamental")
st.subheader("Coordenação Clínica - Casa do Autista")

# URL da sua planilha
url = "https://docs.google.com/spreadsheets/d/1qYarfuNSvsNA3IZ60jtff9VC3eFUqJ_ksENQa4OoGys/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LISTA OFICIAL DE PACIENTES ---
pacientes = sorted([
    "Afonso Costa", "Agatha Bibiana Cardoso Padoin", "Alice Godoy Pereira", "Ana Luiza Prado Martins",
    "Antonia Bianchini de Miranda", "Aquiles Gabriel", "Arthur Boeira Lima", "Arthur Darlan de Oliveira",
    "Arthur de Paulus", "Arthur Miguel Barros Ferreira", "Arthur Spindola Graef", "Artur da Silva de Freitas",
    "Athos Edgar Fra", "Augusto Leal Almeida Fagundes", "Augusto Mucuglia Brasileiro", "Ayran Henrique de Jesus",
    "Barbara de Almeida", "Benício Fernandes de Souza", "Benício Rontani", "Benjamin da Silva Schwatz",
    "Benjamin da Silva Vieira", "Benjamin Valentin dos Santos Arpon", "Bernardo da Silva", "Bernardo Dominic Moreira",
    "Bernardo Fogaça Guedes", "Bernardo Gonçalves da Silva", "Bernardo Henrique de Souza Roco Spacou",
    "Brayan Isaias Ferreira", "Brayan Livina", "Bruno Henrique Cistódio Melo", "Bryan Cesar de Medeiros Avelino",
    "Bryan Samuel Martinez da Silva", "Caetano Marques Gonçalves Neves", "Carlos Eduardo Marques Pereira",
    "Carlos Guilherme Marinho Araújo", "Conrado Godoy", "Daniel Henrique Dias Garcia", "Daniel Pereira Couto",
    "Daniel Vicente Klock de Oliveira", "Daria Rebecca Revollo Moron", "Davi Augusto Ronchi", "Davi Chibiaque",
    "Davi Leonardo P", "Davi Sanada Farkas", "Davi Vicenzi Vitor", "David dos Santos Rodrigues",
    "Dereck Allan dos Santos Pereira", "Dereck de Souza Naymaier", "Diogo Rafael de Aguiar Alves", "Don Billy Judson",
    "Edson Miguel Dias de Lima", "Elena Lima Santos", "Eliabe Sena Messagi de Oliveira", "Eloise Gabrieli da Costa Ferreira",
    "Emanuel Ricardo França", "Emilly Menegazzo Ferreira", "Enzo Andreta Cordeiro Heber", "Enzo Busato", "Ester dos Santos",
    "Felipe Alessandro Martins Vieira", "Fernando Gomes Ern", "Frederic Reichardt", "Gabriel Andretta Correa",
    "Gabriel Comenale", "Gabriel Henrique de Oliveira Meller", "Gabriel Pereira Aquino", "Gilberto Langer Schons",
    "Guilherme Pandini Maioki Ribeiro", "Gustavo Furtado da Silva", "Gustavo Mick", "Heitor Albani Passos",
    "Heitor Fernandes", "Heitor Fernandes Menetrier", "Heitor Pedroso", "Helena dos Santos Conte", "Heloisa Liz do Prado",
    "Henrique Artur Lisboa Sales", "Henrique Basto", "Henrique dos Santos Ponciano", "Hugo Wilbert",
    "Irhuan Amarante Oliveira", "Ítalo Gabriel Can", "Joana Abigail Rocha Ribeiro da Cruz",
    "João Guilherme Freitas Leme da Rosa", "João Levi Pinotti Yanagawa", "João Miguel Castro dos Santos",
    "João Miguel Maciel Teles", "João Pedro Teixeira Machado", "João Vicente Airon Oliveira", "João Vicente Petry",
    "João Vitor Cavalheiro / Zimermann?", "Joaquim Dias de Mendonça", "Joaquim Gael Silva Pit", "Joatan Valdir Farias",
    "John Saymon Sa", "José Lucas Oliveira Fonseca", "Julia Catherine Neves Queiroz", "Kalleb Lunckers",
    "Kauan Ruan de Souza Leodoro", "Kevelin Lemos Sena", "Kevin Lopes de Souza", "Kim Antonella Ferraz Hindersmann",
    "Laura Anna Machado da Silva", "Layla Bordon", "Leandro Fontoura da Silva Paim", "Leonardo Lamonica",
    "Lian Marques Jablonski", "Livia Franco Souza", "Livia Gonzaga de Alencar", "Lohan Gabriel França",
    "Lorenzo Costa Vieira", "Lorenzo Hernandez Carneiro Prestes", "Luana Marnati de Jesus", "Lucas Ribeiro Moreira",
    "Lucas Santa Y Monte de Vargas", "Luisa de Matos Beims", "Luiz Felipe Januario", "Maite Gomes Ern",
    "Maitê Leal Machado", "Manoel Espindola Neto", "Manoela Pamplona Paim", "Manuela Maria Camargo Deschamps",
    "Manuella dos Anjos", "Maria Heloísa M", "Maria Heloisa Nonato", "Matteo Misael Ortiz Falco", "Mickael Lourenço",
    "Miguel Arthur Lourenço dos Santos", "Miguel Cortes", "Miguel de Jesus", "Miguel Haweroth Dias",
    "Miguel Henrique Tontini", "Miguel Luiz Bonetti Pires", "Nathaly dos Reis Ortiz", "Nathan Yamada Perão",
    "Nicolas Gabriel Gomes", "Nicolas Gonçalves", "Nicolas Heitmann Rafaeli", "Nicolas Runscka", "Noah da Silva Penteado",
    "Noah Zoscke da Silva", "Oliver Farias Backes", "Oliver Gael Fidelis Berber", "Otavio do Prado",
    "Otávio Henrique Skoula Mera", "Pedro Antonio Amorim Vieira", "Pedro Garcia Leite", "Pedro Guilherme da Silva Mohr",
    "Pedro Gustavo dos Santos", "Pedro Henrique Ferreira", "Pedro Ryan Rodrigues e Sousa", "Rafael Pires de Oliveira",
    "Raimundo Alves Balieiro Neto", "Ramiro Costa Alves", "Ramses Buxman", "Rhavi Isaac Tapparo", "Richard Cunha da Silva",
    "Samuel Rodrigues Galli", "Sarah Cristina da Silva", "Saymon Davi Sil", "Sofia Amaral", "Sophia Victória Santana",
    "Thalles do Rosário", "Theo Cerqueira Campos", "Theo Dias de Jesus", "Theo Gomes Pereira", "Theo Leffer Ayres",
    "Theylor da Silva Pires", "Uriel Priscila Virreira Revollo", "Valentina C Melo", "Valentina Eduarda Santos da Silva Ferreira",
    "Valentynna Wassem", "Vicente Boniatti de Matos", "Vicente Chibiaque", "Vicente da Silva Betim", "Vicente Romanel",
    "Victor Leonel de Souza", "Victoria Camara Lopes", "Vitor Ferreira da Silva", "Yandres Davi Kilian",
    "Yasmin dos Anjos Martins", "Yuri Gabriel Fries"
])

# --- FORMULÁRIO DE REGISTRO ---
with st.form("registro_aba", clear_on_submit=True):
    col_topo_1, col_topo_2 = st.columns(2)
    
    with col_topo_1:
        paciente_selecionado = st.selectbox("Selecione a Criança", [""] + pacientes)
        data_sessao = st.date_input("Data da Avaliação", datetime.now())
        
    with col_topo_2:
        nome_treino = st.text_input("Programa / Treino", placeholder="Ex: Contato Visual, Mando...")
        aplicador = st.text_input("Aplicador Responsável")

    st.write("---")
    st.write("### Registro de Dicas")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    ft = c1.number_input("FT", min_value=0, step=1)
    fp = c2.number_input("FP", min_value=0, step=1)
    gt = c3.number_input("GT", min_value=0, step=1)
    vt = c4.number_input("VT", min_value=0, step=1)
    id_ind = c5.number_input("ID", min_value=0, step=1)

    botao_salvar = st.form_submit_button("💾 SALVAR REGISTRO", use_container_width=True)

# --- LÓGICA DE SALVAMENTO ACUMULATIVO ---
if botao_salvar:
    if paciente_selecionado != "" and nome_treino != "":
        total = ft + fp + gt + vt + id_ind
        score = ((id_ind * 4) + (vt * 3) + (gt * 2) + (fp * 1)) / (total * 4) * 100 if total > 0 else 0
        
        try:
            # 1. Lê a planilha ATUALIZADA no momento do clique
            # O parâmetro ttl=0 garante que ele não use dados "velhos" do cache
            df_hist = conn.read(spreadsheet=url, ttl=0)

            # 2. Cria a nova linha
            nova_linha = pd.DataFrame([{
                "Data": data_sessao.strftime("%d/%m/%Y"),
                "Paciente": paciente_selecionado,
                "Treino": nome_treino.strip().upper(),
                "FT": ft, "FP": fp, "GT": gt, "VT": vt, "ID": id_ind,
                "Independência (%)": f"{score:.2f}%",
                "Aplicador": aplicador
            }])

            # 3. Une o histórico com a nova linha (concatenação)
            df_final = pd.concat([df_hist, nova_linha], ignore_index=True)
            
            # 4. Atualiza a planilha inteira com a lista completa
            conn.update(spreadsheet=url, data=df_final)
            
            st.success(f"✅ Registro acumulado com sucesso na planilha!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
    else:
        st.warning("⚠️ Selecione a criança e o nome do treino antes de salvar.")

# --- CONSULTA RÁPIDA ---
st.divider()
if st.checkbox("Visualizar Banco de Dados Atual"):
    try:
        # Mostra os dados reais da planilha para conferência
        dados_conferencia = conn.read(spreadsheet=url, ttl=0)
        st.dataframe(dados_conferencia, use_container_width=True)
    except:
        st.info("Nenhum dado encontrado.")
