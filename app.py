import streamlit as st
import os
import google.generativeai as genai
import re
import json

# Defina o nome do modelo e a instrução do sistema
MODEL = "gemini-2.0-flash"
system_instruction = "Você é um assistente de culinária criativo."

# Inicialize model como None para evitar o UnboundLocalError inicialmente
model = None

def limpar_texto(texto):
    # ... (sua função limpar_texto) ...

class Receita:
    # ... (sua classe Receita) ...

def sugerir_receitas(ingredientes, receitas, preferencias=None, restricoes=None):
    # ... (sua função sugerir_receitas) ...

def obter_resposta_do_gemini(prompt, modelo=model): # Use o modelo global aqui
    """Obtém uma resposta do modelo Gemini."""
    if modelo is None:
        st.error("Erro: O modelo Gemini não foi inicializado. Verifique a configuração da chave da API.")
        return None
    try:
        response = modelo.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Erro ao obter resposta do Gemini: {e}")
        return None

def formatar_receita(texto_receita):
    # ... (sua função formatar_receita) ...

def main():
    st.title("🧑‍🍳 ChefBot - Assistente Inteligente")
    st.write("Olá! Bem-vindo ao ChefBot. Posso sugerir algumas receitas criativas com base nos ingredientes que você tem em casa!")
    st.write("\n")

    ingredientes_key = "ingredientes_input"
    preferencias_key = "preferencias_input"
    restricoes_key = "restricoes_input"

    if ingredientes_key not in st.session_state:
        st.session_state[ingredientes_key] = ""
    if preferencias_key not in st.session_state:
        st.session_state[preferencias_key] = ""
    if restricoes_key not in st.session_state:
        st.session_state[restricoes_key] = ""

    # Carregue a chave da API das variáveis de ambiente (Streamlit Secrets)
    API_KEY = os.getenv('GEMINI_API_KEY')

    # Configure a API e o modelo
    global model
    if API_KEY:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            model_name=MODEL,
            system_instruction=system_instruction
        )
        st.write("API do Gemini configurada usando variável de ambiente.") # Mensagem de confirmação
    else:
        st.error("Erro: A variável de ambiente 'GEMINI_API_KEY' não está definida. Certifique-se de configurar o Secret no Streamlit Cloud.")
        return # Impede a execução do restante do main() se a chave não estiver configurada

    ingredientes_str = st.text_input("✍️ Quais ingredientes você tem em casa? (separados por vírgula)", key=ingredientes_key, value=st.session_state[ingredientes_key]).lower()
    preferencias = st.text_input("🤔 Você tem alguma preferência alimentar? (vegetariano, vegano, sem glúten, etc., separado por vírgula)", key=preferencias_key, value=st.session_state[preferencias_key]).lower()
    restricoes = st.text_input("🚫 Você tem alguma restrição alimentar? (alergias, intolerâncias, etc., separado por vírgula)", key=restricoes_key, value=st.session_state[restricoes_key]).lower()

    if st.button("Buscar Receitas"):
        if ingredientes_str:
            # ... (restante da sua lógica de busca de receitas) ...
            with st.spinner("Pensando com o Chef Gemini..."):
                prompt = f"""
                    Com os ingredientes: {', '.join(ingredientes)}, e considerando as preferências: {', '.join(preferencias_lista) or 'nenhuma'}, e restrições: {', '.join(restricoes_lista) or 'nenhuma'}, você pode sugerir uma receita criativa?
                    Liste 1 receita com um nome claro, uma lista de ingredientes e um modo de preparo conciso.
                    """
                resposta_gemini = obter_resposta_do_gemini(prompt)

                if resposta_gemini:
                    # ... (restante da sua lógica de exibição da receita) ...
                else:
                    st.warning("😞 Desculpe, o Gemini não conseguiu gerar sugestões no momento.")
        else:
            st.warning("Por favor, insira alguns ingredientes.")

if __name__ == "__main__":
    main()
