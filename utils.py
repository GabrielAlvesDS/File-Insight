from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from docx import Document

def query_agent_csv(data, query):
    try:
        # Ler o CSV a partir do buffer do UploadedFile
        df = pd.read_csv(data, encoding='ISO-8859-1', decimal='.', delimiter=',')        
        llm = ChatOpenAI(model='gpt-4o-mini')
        
        # Criar o agente de pandas dataframe com código perigoso permitido
        agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
        result = agent.run(query)
        return result
    
    except ValueError as e:
        raise ValueError(f"Erro ao criar o agente: {e}")
    except Exception as e:
        raise Exception(f"Erro inesperado: {e}")

def query_agent_doc(data, query):
    # Aqui, você pode adicionar lógica para processar arquivos DOC
    return "Função para análise de DOC ainda não implementada."

def read_docx(file):
    """Função para ler o conteúdo de um arquivo DOCX."""
    try:
        doc = Document(file)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return "\n".join(full_text)  # Retorna todo o texto do documento
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo DOCX: {e}")

def query_agent_doc(data, query):
    try:
        # Ler o arquivo DOCX
        doc_text = read_docx(data)
        
        # Certificar-se de que o modelo e a configuração estão corretos
        llm = ChatOpenAI(model='gpt-4o-mini')
        
        # Aqui podemos fazer perguntas sobre o texto extraído
        prompt = f"O seguinte é o conteúdo de um documento: {doc_text}\n\nResponda à seguinte pergunta: {query}"
        response = llm(prompt).content  
        
        return response
    except ValueError as e:
        raise ValueError(f"Erro ao criar o agente: {e}")
    except Exception as e:
        raise Exception(f"Erro inesperado: {e}")