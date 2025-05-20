import streamlit as st
import os
import google.generativeai as genai
import re
import json

# Defina o nome do modelo e a instrução do sistema
MODEL = "gemini-2.0-flash"
system_instruction = "Você é um assistente de culinária criativo."

def obter_resposta_do_gemini(prompt, modelo=MODEL):
    """Obtém uma resposta do modelo Gemini."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Erro ao obter resposta do Gemini: {e}")
        return None

def main():
    st.title("🧑‍🍳 ChefBot - Resposta Direta")
    st.write("Olá! Bem-vindo ao ChefBot. Posso te dar a resposta do Gemini diretamente!")
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

    API_KEY = os.getenv('GOOGLE_API_KEY')

    global model
    if API_KEY:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            model_name=MODEL,
            system_instruction=system_instruction
        )
    else:
        st.error("Erro: A variável de ambiente 'GEMINI_API_KEY' não está definida. Certifique-se de configurar o Secret no Streamlit Cloud.")
        return

    ingredientes_str = st.text_input("✍️ Quais ingredientes você tem em casa? (separados por vírgula)", key=ingredientes_key, value=st.session_state[ingredientes_key]).lower()
    preferencias = st.text_input("🤔 Você tem alguma preferência alimentar? (vegetariano, vegano, sem glúten, etc., separado por vírgula)", key=preferencias_key, value=st.session_state[preferencias_key]).lower()
    restricoes = st.text_input("🚫 Você tem alguma restrição alimentar? (alergias, intolerâncias, etc., separado por vírgula)", key=restricoes_key, value=st.session_state[restricoes_key]).lower()

    if st.button("Obter Resposta"):
        if ingredientes_str:
            ingredientes = [ingrediente.strip() for ingrediente in ingredientes_str.split(",")]
            preferencias_lista = [p.strip() for p in preferencias.split(",") if p.strip()]
            restricoes_lista = [r.strip() for r in restricoes.split(",") if r.strip()]

            st.info(f"📄 Você informou os seguintes ingredientes: {', '.join(ingredientes)}.")
            if preferencias_lista:
                st.info(f"📄 Suas preferências são: {', '.join(preferencias_lista)}.")
            if restricoes_lista:
                st.info(f"📄 Suas restrições são: {', '.join(restricoes_lista)}.")
            st.write("\n")

            with st.spinner("Consultando o Chef Gemini..."):
                prompt = f"""
                    Com os ingredientes: {', '.join(ingredientes)}, e considerando as preferências: {', '.join(preferencias_lista) or 'nenhuma'}, e restrições: {', '.join(restricoes_lista) or 'nenhuma'}, você pode sugerir uma receita criativa?
                    Responda diretamente com a sugestão da receita.
                    """
                resposta_gemini = obter_resposta_do_gemini(prompt)

                if resposta_gemini:
                    st.subheader("Resposta do Gemini:")
                    st.write(resposta_gemini)

                    st.session_state[ingredientes_key] = ""
                    st.session_state[preferencias_key] = ""
                    st.session_state[restricoes_key] = ""
                    st.rerun()
                else:
                    st.warning("😞 Desculpe, o Gemini não conseguiu gerar uma resposta no momento.")
        else:
            st.warning("Por favor, insira alguns ingredientes.")

if __name__ == "__main__":
    main()
