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

# --- LISTA DE PSICÓLOGOS(AS) ---
profissionais = sorted([
    "Ana Laura", "Leoni", "Isadora", "Mayele", "Bruna", 
    "Muriel", "Raphaela", "Nathalia", "Jessica", "Naiara"
])

# --- LISTA OFICIAL DE PACIENTES ---
pacientes = sorted([
    "Antônio Gollub Corrêa Petersen", "Afonso Costa de Oliveira", "Agatha Bibiana Cardoso Padoin", 
    "Alice Godoy Pereira", "Ana Luiza Prado Martins", "Antônia Bianchini de Miranda", 
    "Aquiles Gabriel do Prado", "Arthur Boeira Lima", "Arthur Darlan de Oliveira", 
    "Arthur de Paulus Zabel", "Arthur Espíndola Graef", "Arthur Miguel Barros Ferreira", 
    "Artur da Silva de Freitas", "Athos Edgar França", "Augusto Leal Fagundes", 
    "Augusto Macuglia Brasileiro", "Ayran Henrique Ferreira de Jesus", "Breno Martins", 
    "Bethina Nonatto Avelino", "Barbara de Almeida Fajfer", "Benício Fernandes de Souza", 
    "Benjamim da Silva Schwatz", "Benjamim da Silva Vieira", "Benjamin Valentin dos Santos Arpon", 
    "Bernardo da Silva", "Bernardo Dominic Moreira", "Bernardo Fogaca Guedes", 
    "Bernardo Gonçalves da Silva", "Bernardo Henrique de Souza Roco Spacov", "Brayan Isaias Ferreira", 
    "Brayan Livina", "Bruno Henrique Custódio Ribeiro", "Bryan Cesar de Medeiros Avelino", 
    "Bryan Samuel Martinez da Silva", "Cristian Miguel Carvalho", "Catarina dos Santos", 
    "Christopher Felips Antonio", "Caetano Marques Gonçalves Neves", "Carlos Eduardo Marques Pinheiro", 
    "Carlos Guilherme Marinho Araújo", "Conrado Godoy Gritan", "Derick Jean Fernandes Nowasky", 
    "Daniel Henrique Dias Garcia", "Daniel Pereira Couto", "Daniel Vicente Klock de Oliveira", 
    "Daria Rebecca Revollo Moron", "Davi Augusto Ronchi Hermann", "Davi Chibiaque Weege", 
    "Davi Sanada Farkas", "Davi Vincensi Vitor", "David dos Santos Rodrigues", 
    "Dereck Allan dos Santos Pereira", "Derek de Souza Naymaier", "Diogo Rafael de Aguiar Alves", 
    "Don Bily Judson Oxean", "Eloah Michels", "Erick Carvalho Ortiz", "Edson Miguel Dias de Lima", 
    "Elena Lima Santos", "Eliabe Sena Messagi de Oliveira", "Eloise Gabriela Ferreira dos Santos", 
    "Emanuel Ricardo França", "Emilly Menegazzo Ferreira", "Enzo Andreta Cordeiro Heber", 
    "Ester dos Santos de Aquino", "Felipe Gabriel dos Santos Araújo", "Felipe Alessandro Martins Vieira", 
    "Fernando Gomes Ern", "Frederic Reichardt", "Gael Vieira Gualberto Nunes", "Gabriel Andretta Corrêa", 
    "Gabriel Comenale Almeida", "Gabriel Henrique de Oliveira Meller", "Gabriel Pereira de Aquino", 
    "Gilberto Langer Schons", "Guilherme Pandini Maioki Ribeiro", "Gustavo Furtado da Silva", 
    "Gustavo Mick Scheer", "Heitor Albani Passos", "Heitor Fernandes Menetrier", 
    "Heitor Pedroso Oliveira Silva", "Helena dos Santos Conte", "Heloisa Liz do Prado", 
    "Henrique Basto Cardoso", "Henrique Artur Lisboa Sales", "Henrique dos Santos Ponciano", 
    "Hugo Wilbert de Andrade", "Isabel Heloisa Mateus", "Isadora Barreto", "Isabelly Vitória Braz", 
    "Irhuan Amarante Oliveira", "Ítalo Gabriel Candotti", "Joana Abigail Rocha Ribeiro da Cruz", 
    "João Vitor Sousa da Silva", "João Guilherme Freitas Leme da Rosa", "João Miguel Castro dos Santos", 
    "João Miguel Maciel Teles", "João Pedro Teixeira Machado", "João Vicente Arion Oliveira", 
    "João Vicente Petry", "João Victor Cavalheiro Zimmermann", "Joaquim Gael Silva Pit", 
    "Julia Catherine Neves Queiroz", "Joatan Valdir Farias Ramos", "John Saymon Santos Schelemberg", 
    "José Lucas Oliveira Fonseca", "Kalleb Lunckers Pezzi", "Kauan Ruan de Souza Leodoro", 
    "Kevilin Lemos Sena", "Kevin Lopes de Souza", "Kim Antonella Ferraz Hindersmann", 
    "Luisa Umbelino Schneider", "Luan Feijó Machado Abromoviz", "Laura Jardim Tachholke", 
    "Lazaro Henrique Schulle Coelho", "Layla Bordon dos Santos", "Leandro Fontoura da Silva Paim", 
    "Leonardo Lamonica Campiotti", "Lian Marques Jablonski", "Livia Franco Souza", 
    "Livia Gonzaga de Alencar", "Lohan Gabriel França", "Lorenzo Costa Vieira", 
    "Lorenzo Hernandez Carneiro Prestes", "Luana Marnati de Jesus", "Lucas Ribeiro Moreira", 
    "Lucas Santana Y Monte de Vargas", "Luis Felipe Pessoa Januario", "Luisa de Matos Beims", 
    "Miguel da Costa Zeferino", "Mikael Silva Ferreira", "Maite Gomes Ern", "Maitê Leal Machado", 
    "Manoel Espindola Neto", "Manoella Pamplona Paim", "Manuella do Anjos Martins", 
    "Maria Heloísa Muniz Paulino", "Maria Heloisa Nonatto Viega", "Matteo Misael Ortiz Falco", 
    "Mickael Lourenço Teixeira", "Miguel Arthur Lourenço dos Santos", "Miguel Cortes Zeni", 
    "Miguel de Jesus Campos", "Miguel Haweroth Dias", "Miguel Henrique Tontini", 
    "Miguel Luiz Bonetti Pires", "Nicolas Escobar de Oliveira", "Nathaly dos Reis Ortiz", 
    "Nathan Yamada Perao", "Nicolas Gabriel de Oliveira Gomes", "Nicolas Gonçalves de Freitas", 
    "Nicolas Heitmann Rafaeli", "Nicolas Runschka", "Noah da Silva Penteado", "Noah Zoscke da Silva", 
    "Oliver Farias Backes", "Otavio do Prado", "Otávio Henrique Skoula Mera", "Pedro Antônio Amorim Vieira", 
    "Pedro Garcia Leite", "Pedro Guilherme da Silva Mohr", "Pedro Gustavo dos Santos da Silva", 
    "Pedro Henrique Ferreira Santana", "Pedro Ryan Rodrigues e Sousa", "Ruan Felipe Teixeira Mota", 
    "Rafael Pires de Oliveira", "Raimundo Alves Balieiro Neto", "Ramiro Costa Alves", "Ramses Buxman", 
    "Rhavi Isaac Tapparo", "Richard Cunha da Silva", "Samuel Kalebe Macedo Xavier", 
    "Samuel Rodrigues Galli", "Saymon Davi Silva dos Santos", "Sara dos Santos", "Sofia Amaral", 
    "Sophia Victória Santana", "Theo de Souza Antunes", "Thalles do Rosario Pereira", 
    "Theo Cerqueira Campos", "Theo Gomes Pereira", "Theo Leffer Ayres", "Uriel Priscila Virreira Revollo", 
    "Victor Gabriel Ferreira Wasem Schneider", "Valentina Cristan Melo", "Valentynna Wassem", 
    "Vicente Boniati de Matos", "Vicente Chibiaque Weege", "Vicente Romanel Correia", 
    "Victor Leonel de Souza", "Victoria Camara Lopes", "Vitor Ferreira da Silva", 
    "Yandres Davi Kilian", "Yasmin dos Anjos Martins"
])

# --- FORMULÁRIO DE REGISTRO ---
with st.form("registro_aba", clear_on_submit=True):
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        paciente_selecionado = st.selectbox("Selecione a Criança", [""] + pacientes)
        data_sessao = st.date_input("Data da Avaliação", datetime.now())
    with col_t2:
        nome_treino = st.text_input("Programa / Treino", placeholder="Ex: Mando, Tato, Imitação...")
        psicologo_responsavel = st.selectbox("Psicólogo(a) Responsável", [""] + profissionais)

    st.write("---")
    st.write("### Registro de Dicas (Frequência)")
    c1, c2, c3, c4, c5 = st.columns(5)
    
    ft = c1.number_input("FT", min_value=0, step=1, help="Física Total")
    fp = c2.number_input("FP", min_value=0, step=1, help="Física Parcial")
    gt = c3.number_input("GT", min_value=0, step=1, help="Gestual")
    vt = c4.number_input("VT", min_value=0, step=1, help="Verbal")
    id_ind = c5.number_input("ID", min_value=0, step=1, help="Independente")

    botao_salvar = st.form_submit_button("💾 SALVAR REGISTRO", use_container_width=True)

# --- LÓGICA DE SALVAMENTO ACUMULATIVO ---
if botao_salvar:
    if paciente_selecionado != "" and nome_treino != "" and psicologo_responsavel != "":
        total_tentativas = ft + fp + gt + vt + id_ind
        
        if total_tentativas > 0:
            # Lógica de subtração: ID=1.0, VT=0.75, GT=0.50, FP=0.25, FT=0.0
            pontos = (id_ind * 1.0) + (vt * 0.75) + (gt * 0.5) + (fp * 0.25) + (ft * 0.0)
            score = (pontos / total_tentativas) * 100
            
            try:
                df_hist = conn.read(spreadsheet=url, ttl=0)

                nova_linha = pd.DataFrame([{
                    "Data": data_sessao.strftime("%d/%m/%Y"),
                    "Paciente": paciente_selecionado,
                    "Treino": nome_treino.strip().upper(),
                    "FT": ft, "FP": fp, "GT": gt, "VT": vt, "ID": id_ind,
                    "Total Tentativas": total_tentativas,
                    "Independência (%)": f"{score:.2f}%",
                    "Psicólogo(a)": psicologo_responsavel
                }])

                df_final = pd.concat([df_hist, nova_linha], ignore_index=True)
                conn.update(spreadsheet=url, data=df_final)
                
                st.success(f"✅ Registro salvo com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("⚠️ Insira ao menos uma tentativa.")
    else:
        st.warning("⚠️ Verifique se selecionou o Paciente, o Treino e o(a) Psicólogo(a).")

# --- CONSULTA RÁPIDA ---
st.divider()
if st.checkbox("Visualizar Banco de Dados Atual"):
    try:
        dados_conferencia = conn.read(spreadsheet=url, ttl=0)
        st.dataframe(dados_conferencia, use_container_width=True)
    except:
        st.info("Planilha vazia ou em carregamento.")
