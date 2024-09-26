from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from docx import Document

def query_agent_csv(data, query, decimal_type='.', delimiter_type=','):
    try:
        df = pd.read_csv(data, encoding='ISO-8859-1', decimal = decimal_type, delimiter = delimiter_type)        
        llm = ChatOpenAI(model='gpt-4o-mini')
        
        agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
        result = agent.run(query)
        return result
    
    except ValueError as e:
        raise ValueError(f"Erro ao criar o agente: {e}")
    except Exception as e:
        raise Exception(f"Erro inesperado: {e}")

def read_docx(file):
    try:
        doc = Document(file)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return "\n".join(full_text)
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo DOCX: {e}")

def query_agent_doc(data, query):
    try:
        doc_text = read_docx(data)
        
        llm = ChatOpenAI(model='gpt-4o-mini')
        
        prompt = f"O seguinte é o conteúdo de um documento: {doc_text}\n\nResponda à seguinte pergunta: {query}"
        response = llm(prompt).content  
        
        return response
    except ValueError as e:
        raise ValueError(f"Erro ao criar o agente: {e}")
    except Exception as e:
        raise Exception(f"Erro inesperado: {e}")
