import os
import streamlit as st
from dotenv import load_dotenv
from utils import query_agent_csv, query_agent_doc

file_size_mb = 5
FILE_SIZE_LIMIT = file_size_mb * 1024 * 1024

# Customizando o layout da página (Centralizando e ajustando largura) 
st.set_page_config(page_title="Análise de Arquivos CSV ou DOCX", layout="centered", page_icon="💡")

# Verificação da chave da API
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = os.getenv("OPENAI_API_KEY", "")

# Inicializando contadores de tentativas
if 'count_csv_free_trials' not in st.session_state:
    st.session_state['count_csv_free_trials'] = 2  
if 'count_docx_free_trials' not in st.session_state:
    st.session_state['count_docx_free_trials'] = 2 

# Título
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Análise de Arquivos CSV ou DOCX</h1>", unsafe_allow_html=True)

# Sidebar - Escolher o tipo de arquivo
st.sidebar.title("Opções")
file_type = st.sidebar.selectbox("Escolha o tipo de arquivo", ["CSV", "DOCX"])

# Exibir contagem de tentativas restantes
st.sidebar.markdown("<h2 '>Tentativas Restantes</h2>", unsafe_allow_html=True)
st.sidebar.write(f"CSV: {st.session_state['count_csv_free_trials']} tentativas restantes")
st.sidebar.write(f"DOCX: {st.session_state['count_docx_free_trials']} tentativas restantes")

# Customizando a sidebar
st.sidebar.markdown("<h2 '>API Key</h2>", unsafe_allow_html=True)
if st.session_state['count_csv_free_trials'] <= 0 and st.session_state['count_docx_free_trials'] <= 0:
    st.sidebar.markdown("<h3 '>Testes gratuitos esgotados! Insira o seu API KEY da OpenAI:</h3>", unsafe_allow_html=True)
    st.session_state['API_Key'] = st.sidebar.text_input("What's your API key?", type="password", value="")
    
else:
    # Apenas mantém a API Key no estado sem exibi-la
    st.sidebar.text_input("Sua API Key (mantida em sigilo)", type="password", value="", disabled=True)

st.markdown(f"<h3 '>Upload de {file_type}:</h3>", unsafe_allow_html=True)

# Ajustar o layout com colunas para upload e consulta
if file_type == "CSV":
    col1, col2 = st.columns(2)
    with col1:
        col11, col12 = st.columns(2)
        with col11:
            decimal_type = st.radio("Escolha o tipo de decimal", [".", ","], index=0)
        with col12:
            delimiter_type = st.radio("Escolha o delimitador", [",", ";"], index=0)

        if decimal_type == delimiter_type:
            st.error("O delimitador e o separador decimal não podem ser iguais. Por favor, escolha valores diferentes.")
            st.stop()
    with col2:
        data = st.file_uploader(f"Carregue seu arquivo {file_type}", type=[file_type.lower()])
else:
    data = st.file_uploader(f"Carregue seu arquivo {file_type}", type="docx")
    
if data is not None:
    file_size = data.size
    if file_size > FILE_SIZE_LIMIT:
        st.error(f"O tamanho do arquivo excede o limite de {file_size_mb} MB. Seu arquivo tem {file_size / (1024 * 1024):.2f} MB.")
        st.stop()

st.markdown("<h3 '>Consulta:</h3>", unsafe_allow_html=True)
query = st.text_area("Digite sua consulta", placeholder="Ex: Qual foi o faturamento em julho?")


button = st.button("Gerar Resposta")

# Função para exibir a resposta
if button:
    if data is not None:
        # Verifica se o número máximo de tentativas foi alcançado
        if (file_type == "CSV" and st.session_state['count_csv_free_trials'] < 1):
            st.error(f"Limite de tentativas atingido! Você fez {1 - st.session_state['count_csv_free_trials']} perguntas para CSV e {1 - st.session_state['count_docx_free_trials']} perguntas para DOCX.")
        elif (file_type == "DOCX" and st.session_state['count_docx_free_trials'] < 1):
            st.error(f"Limite de tentativas atingido! Você fez {1 - st.session_state['count_csv_free_trials']} perguntas para CSV e {1 - st.session_state['count_docx_free_trials']} perguntas para DOCX.")
        else:
            st.info("Processando sua consulta, por favor aguarde...")
            with st.spinner("Analisando o arquivo..."):
                try:
                    if file_type == "CSV" and data.name.endswith(".csv"):
                        answer = query_agent_csv(data, query)
                        st.session_state['count_csv_free_trials'] -= 1

                    elif file_type == "DOCX" and data.name.endswith(".docx"):
                        answer = query_agent_doc(data, query)
                        st.session_state['count_docx_free_trials'] -= 1

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
