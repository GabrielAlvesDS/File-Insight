import os
import streamlit as st
from dotenv import load_dotenv
from utils import query_agent_csv, query_agent_doc

# Customizando o layout da página (Centralizando e ajustando largura) 
st.set_page_config(page_title="Análise de Arquivos CSV ou DOCX", layout="centered", page_icon="💡")

if 'count_csv_free_trials' not in st.session_state:
    st.session_state['count_csv_free_trials'] = 0
if 'count_docx_free_trials' not in st.session_state:
    st.session_state['count_docx_free_trials'] = 0

# Verifica se a chave da API deve ser definida
if 'API_Key' not in st.session_state:
    if st.session_state['count_csv_free_trials'] < 1 and st.session_state['count_docx_free_trials'] < 1:
        st.session_state['API_Key'] = os.getenv("OPENAI_API_KEY", "")
    else: 
        st.session_state['API_Key'] = ''

# Customizando a sidebar
st.sidebar.title("API Key")
if st.session_state['count_csv_free_trials'] >= 1 and st.session_state['count_docx_free_trials'] >= 1:
    st.sidebar.markdown("<h2 '>Testes gratuitos esgotados! insira o seu API KEY da OpenAI</h2>", unsafe_allow_html=True)
st.session_state['API_Key'] = st.sidebar.text_input("What's your API key?", type="password")

# Título estilizado da aplicação
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Análise de Arquivos CSV ou DOCX</h1>", unsafe_allow_html=True)

# Sidebar - Escolher o tipo de arquivo
st.sidebar.markdown("<h2 '>Opções</h2>", unsafe_allow_html=True)
file_type = st.sidebar.selectbox("Escolha o tipo de arquivo", ["CSV", "DOCX"])

# Ajustar o layout com colunas para upload e consulta
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<h3 '>Upload de {file_type}:</h3>", unsafe_allow_html=True)
    data = st.file_uploader(f"Carregue seu arquivo {file_type}", type=["csv", "docx"])

with col2:
    st.markdown("<h3 '>Consulta:</h3>", unsafe_allow_html=True)
    query = st.text_area("Digite sua consulta", placeholder="Ex: Qual foi o faturamento em julho?")

# Botão para gerar a resposta (apenas 1)
button = st.button("Gerar Resposta")

# Função para exibir a resposta
if button:
    if data is not None:
        # Verifica se o número máximo de tentativas foi alcançado
        if (file_type == "CSV" and st.session_state['count_csv_free_trials'] >= 1) or \
           (file_type == "DOCX" and st.session_state['count_docx_free_trials'] >= 1):
            st.error(f"Limite de tentativas atingido! Você fez {st.session_state['count_csv_free_trials']} perguntas para CSV e {st.session_state['count_docx_free_trials']} perguntas para DOCX.")
        else:
            st.info("Processando sua consulta, por favor aguarde...")
            with st.spinner("Analisando o arquivo..."):
                try:
                    if file_type == "CSV" and data.name.endswith(".csv"):
                        answer = query_agent_csv(data, query)
                        st.session_state['count_csv_free_trials'] += 1

                    elif file_type == "DOCX" and data.name.endswith(".docx"):
                        answer = query_agent_doc(data, query)
                        st.session_state['count_docx_free_trials'] += 1

                    else:
                        st.error(f"Por favor, carregue um arquivo {file_type} válido.")
                        st.stop()

                    st.markdown(f"<h4 style='color: #4CAF50;'>Resposta:</h4>", unsafe_allow_html=True)
                    st.write(answer)
                
                except ValueError as e:
                    st.error(f"Erro ao processar o arquivo {file_type}: {e}")
                except Exception as e:
                    st.error(f"Erro inesperado: {e}")
    else:
        st.error("Por favor, faça upload de um arquivo.")
