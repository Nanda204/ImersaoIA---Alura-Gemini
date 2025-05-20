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
    st.title("🧑‍🍳 ChefBot - Sugestões de Receitas")
    st.write("Olá! Bem-vindo ao ChefBot. Posso sugerir até duas receitas criativas com base nos ingredientes que você tem em casa!")
    st.write("\n")

    ingredientes_key = "ingredientes_input"
    preferencias_key = "preferencias_input"
    restricoes_key = "restricoes_input"

    st.write(f"Inicializando {ingredientes_key}")
    if ingredientes_key not in st.session_state:
        st.session_state[ingredientes_key] = ""
    st.write(f"Estado de {ingredientes_key}: {st.session_state.get(ingredientes_key)}")

    st.write(f"Inicializando {preferencias_key}")
    if preferencias_key not in st.session_state:
        st.session_state[preferencias_key] = ""
    st.write(f"Estado de {preferencias_key}: {st.session_state.get(preferencias_key)}")

    st.write(f"Inicializando {restricoes_key}")
    if restricoes_key not in st.session_state:
        st.session_state[restricoes_key] = ""
    st.write(f"Estado de {restricoes_key}: {st.session_state.get(restricoes_key)}")

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

    if st.button("Buscar Receitas"):
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
                    Com os ingredientes: {', '.join(ingredientes)}, e considerando as preferências: {', '.join(preferencias_lista) or 'nenhuma'}, e restrições: {', '.join(restricoes_lista) or 'nenhuma'}, você pode sugerir duas receitas criativas?
                    Liste 2 receitas, cada uma com um nome claro, uma lista de ingredientes e um modo de preparo conciso, separadas por uma linha em branco.
                    """
                resposta_gemini = obter_resposta_do_gemini(prompt)

                if resposta_gemini:
                    st.subheader("Sugestões de Receitas:")
                    receitas_texto = resposta_gemini.strip().split("\n\n")  # Dividir por duas linhas em branco

                    for i, receita_texto in enumerate(receitas_texto):
                        st.subheader(f"Receita {i+1}:")
                        partes_receita = receita_texto.strip().split("\n")
                        nome = next((linha.split(": ", 1)[1].strip() for linha in partes_receita if linha.lower().startswith("nome:")), f"Nome não encontrado para receita {i+1}")
                        ingredientes_linhas = [linha.strip() for linha in partes_receita if linha.lower().startswith("ingredientes:")]
                        ingredientes = ingredientes_linhas[0].split(", ") if ingredientes_linhas else ["Ingredientes não encontrados"]
                        modo_preparo_linhas = [linha.strip() for linha in partes_receita if linha.lower().startswith("modo de preparo:")]
                        modo_preparo = "\n".join(modo_preparo_linhas[0].split("\n")[1:]) if modo_preparo_linhas else "Modo de preparo não encontrado"

                        st.markdown(f"**Nome:** {nome.title()}")
                        st.markdown("**Ingredientes:**")
                        for ingrediente in ingredientes:
                            st.markdown(f"- {ingrediente}")
                        st.markdown("**Modo de Preparo:**")
                        st.write(modo_preparo)
                        st.markdown("---")

                    if not receitas_texto:
                        st.warning("😞 Desculpe, o Gemini não retornou nenhuma receita.")
                    elif len(receitas_texto) < 2:
                        st.info("ℹ️ O Gemini retornou apenas uma receita.")

                    st.session_state[ingredientes_key] = ""
                    st.session_state[preferencias_key] = ""
                    st.session_state[restricoes_key] = ""
                    st.rerun()
                else:
                    st.warning("😞 Desculpe, o Gemini não conseguiu gerar sugestões no momento.")
        else:
            st.warning("Por favor, insira alguns ingredientes.")

if __name__ == "__main__":
    main()
