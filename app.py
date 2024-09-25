import os
import streamlit as st
from dotenv import load_dotenv
from utils import query_agent_csv, query_agent_doc

# Customizando o layout da página (Centralizando e ajustando largura) 
st.set_page_config(page_title="Análise de Arquivos CSV ou DOCX", layout="centered", page_icon="💡")

# Verifica se a chave da API deve ser definida
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = os.getenv("OPENAI_API_KEY", "")

# Inicializando contadores de tentativas
if 'count_csv_free_trials' not in st.session_state:
    st.session_state['count_csv_free_trials'] = 2  
if 'count_docx_free_trials' not in st.session_state:
    st.session_state['count_docx_free_trials'] = 2 

# Título estilizado da aplicação
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
    
    # Verificando a API Key
    if st.sidebar.button("Verificar API Key"):
        if st.session_state['API_Key']:  # Apenas verifica se a chave não está vazia
            # Aqui você pode adicionar a lógica para verificar se a chave é válida.
            # Por exemplo, você pode fazer uma chamada de teste para a API.
            is_valid_key = True  # Substitua isso pela lógica de validação real
            if is_valid_key:
                st.sidebar.success("API Key verificada com sucesso!")
            else:
                st.sidebar.error("API Key inválida. Tente novamente.")
else:
    # Apenas mantém a API Key no estado sem exibi-la
    st.sidebar.text_input("Sua API Key (mantida em sigilo)", type="password", value="", disabled=True)

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
        if (file_type == "CSV" and st.session_state['count_csv_free_trials'] < 1) or \
           (file_type == "DOCX" and st.session_state['count_docx_free_trials'] < 1):
            st.error(f"Limite de tentativas atingido! Você fez {1 - st.session_state['count_csv_free_trials']} perguntas para CSV e {1 - st.session_state['count_docx_free_trials']} perguntas para DOCX.")
        else:
            st.info("Processando sua consulta, por favor aguarde...")
            with st.spinner("Analisando o arquivo..."):
                try:
                    if file_type == "CSV" and data.name.endswith(".csv"):
                        answer = query_agent_csv(data, query)
                        st.session_state['count_csv_free_trials'] -= 1  # Reduz a contagem de tentativas

                    elif file_type == "DOCX" and data.name.endswith(".docx"):
                        answer = query_agent_doc(data, query)
                        st.session_state['count_docx_free_trials'] -= 1  # Reduz a contagem de tentativas

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