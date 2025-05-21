import streamlit as st
import os
import google.generativeai as genai
import re
import json

# CSS para aumentar o tamanho do texto e emojis nos inputs e placeholders e reduzir margens
text_size = "1.2em"
emoji_size = "1.5em"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #C2C0A6;
    }}
    div.stButton > button:hover {{
        background-color: #ff6f61;
        color: white;
        border-color: #ff6f61;
    }}
    input[type="text"] {{
        font-size: {text_size} !important;
        margin-bottom: 0.1em;
        padding: 0.5em; 
    }}
    input[type="text"]::placeholder {{
        font-size: {text_size} !important;
        opacity: 0.7;
    }}
    .emoji-large {{
        font-size: {emoji_size} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

MODEL = "gemini-2.0-flash"
system_instruction = "Você é um assistente de culinária criativo."

def limpar_texto(texto):
    """Remove caracteres especiais e espaços extras do texto."""
    texto = re.sub(r"[^a-zA-Z0-9\s,]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto.lower()

class Receita:
    def __init__(self, nome, ingredientes, modo_preparo, preferencias=None, restricoes=None):
        self.nome = nome
        self.ingredientes = [limpar_texto(ingrediente) for ingrediente in ingredientes]
        self.modo_preparo = modo_preparo
        self.preferencias = [limpar_texto(p) for p in (preferencias if preferencias else [])]
        self.restricoes = [limpar_texto(r) for r in (restricoes if restricoes else [])]

    def adequada_para(self, especificacoes):
        if not especificacoes:
            return True
        especificacoes_limpas = [limpar_texto(e) for e in especificacoes]
        return all(esp in self.preferencias + self.restricoes for esp in especificacoes_limpas)

def sugerir_receitas(ingredientes, receitas, preferencias=None, restricoes=None):
    """Sugere receitas com base nos ingredientes, preferências e restrições do usuário."""
    ingredientes_limpos = [limpar_texto(ingrediente) for ingrediente in ingredientes]
    receitas_sugeridas = []
    for receita in receitas:
        ingredientes_na_receita = receita.ingredientes
        if all(ingrediente in ingredientes_limpos for ingrediente in ingredientes_na_receita):
            if preferencias and not receita.adequada_para(preferencias):
                continue
            if restricoes and not receita.adequada_para(restricoes):
                continue
            receitas_sugeridas.append(receita)
    return receitas_sugeridas

def obter_resposta_do_gemini(prompt, modelo=MODEL):
    """Obtém uma resposta do modelo Gemini."""
    try:
        response = modelo.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Erro ao obter resposta do Gemini: {e}")
        return None


def formatar_receita(texto_receita):
    """Tenta formatar o texto da receita em nome, ingredientes e modo de preparo."""
    nome = None
    ingredientes = []
    modo_preparo = None

    linhas = texto_receita.split('\n')
    estado = "nome"  # Estados: "nome", "ingredientes", "modo_preparo"

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        if estado == "nome":
            nome = linha
            estado = "ingredientes"
        elif estado == "ingredientes":
            if linha.lower().startswith("ingredientes") or linha.lower().startswith("lista de ingredientes"):
                continue
            elif re.match(r"[-*]\s+.+", linha):
                ingredientes.append(linha.split(maxsplit=1)[1].strip())
            elif modo_preparo is None and (linha.lower().startswith("modo de preparo") or linha.lower().startswith("preparo") or linha.lower().startswith("instruções")):
                estado = "modo_preparo"
                modo_preparo_linhas = []
            elif modo_preparo is None:
                modo_preparo_linhas = [linha]
                estado = "modo_preparo"
            elif estado == "modo_preparo":
                modo_preparo_linhas.append(linha)

    if modo_preparo_linhas:
        modo_preparo = "\n".join(modo_preparo_linhas)

    return nome, ingredientes, modo_preparo

def main():
    st.title("🧑‍🍳 ChefBot - Assistente Inteligente")
    st.write("\n")
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

    API_KEY = os.getenv('GOOGLE_API_KEY')

    # Configure a API e o modelo
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

    st.markdown(f'<span style="font-size: {emoji_size};">✍️</span> Quais ingredientes você tem em casa? (separados por vírgula)', unsafe_allow_html=True)
    ingredientes_str = st.text_input("", key=ingredientes_key, value=st.session_state[ingredientes_key]).lower()

    st.markdown(f'<span style="font-size: {emoji_size};">🤔</span> Você tem alguma preferência alimentar? (vegetariano, vegano, sem glúten, etc., separado por vírgula)', unsafe_allow_html=True)
    preferencias = st.text_input("", key=preferencias_key, value=st.session_state[preferencias_key]).lower()

    st.markdown(f'<span style="font-size: {emoji_size};">🚫</span> Você tem alguma restrição alimentar? (alergias, intolerâncias, etc., separado por vírgula)', unsafe_allow_html=True)
    restricoes = st.text_input("", key=restricoes_key, value=st.session_state[restricoes_key]).lower()

    st.write("\n")

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

            emoji_carregando = "🧑‍🍳"
            tamanho_emoji = "2em"
            mensagem = f'<span style="font-size: {tamanho_emoji};">{emoji_carregando}</span> Deixe-me pedir sugestões ao Chef Gemini...'
            st.markdown(mensagem, unsafe_allow_html=True)

            with st.spinner("Pensando com o Chef Gemini..."):
                prompt = f"""
                    Com os ingredientes: {', '.join(ingredientes)}, e considerando as preferências: {', '.join(preferencias_lista) or 'nenhuma'}, e restrições: {', '.join(restricoes_lista) or 'nenhuma'}, você pode sugerir uma receita criativa?
                    Liste 1 receita com um nome claro, uma lista de ingredientes e um modo de preparo conciso.
                    """
                resposta_gemini = obter_resposta_do_gemini(prompt)

                st.write(f"Resposta do Gemini: {resposta_gemini}")

                if resposta_gemini:
                    receitas_texto = resposta_gemini.split("\n\n")

                    if receitas_texto:
                        nome, ingredientes, modo_preparo = formatar_receita(receitas_texto[0])

                        if nome:
                            st.markdown(f"**Nome:** {nome.title()}")
                        if ingredientes:
                            st.markdown("**Ingredientes:**")
                            for ingrediente in ingredientes:
                                st.markdown(f"- {ingrediente}")
                        if modo_preparo:
                            st.markdown("**Modo de Preparo:**")
                            st.write(modo_preparo)
                        st.markdown("---")

                        st.session_state[ingredientes_key] = ""
                        st.session_state[preferencias_key] = ""
                        st.session_state[restricoes_key] = ""
                        st.rerun()
                    else:
                        st.warning("😞 Desculpe, a resposta do Gemini não pôde ser processada.")
                else:
                    st.warning("😞 Desculpe, o Gemini não conseguiu gerar sugestões no momento.")
        else:
            st.warning("Por favor, insira alguns ingredientes.")

if __name__ == "__main__":
    main()
