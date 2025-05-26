import streamlit as st
import os
import google.generativeai as genai
import re

# ==============================
# 🎨 Estilo da Aplicação
# ==============================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #C2C0A6;
        color: #333333;
    }
    div.stButton > button {
        border: 2px solid #808080;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        background-color: #e1e5d3;
        color: black;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #bccab3;
        border-color: #333333;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==============================
# 🔑 Configuração da API Gemini
# ==============================
API_KEY = os.getenv('GOOGLE_API_KEY')

if API_KEY:
    genai.configure(api_key=API_KEY)
    MODEL = genai.GenerativeModel(
        model_name="gemini-2.0-pro",
        system_instruction="Você é um assistente de culinária criativo e organizado. Ofereça receitas bem estruturadas, claras, usando linguagem simpática e acessível."
    )
else:
    st.error("🚨 A variável de ambiente 'GOOGLE_API_KEY' não está configurada.")
    st.stop()


# ==============================
# 🔧 Funções Auxiliares
# ==============================

def limpar_texto(texto):
    texto = re.sub(r"[^a-zA-Z0-9áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ\s,]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto.lower()

def obter_resposta_gemini(prompt):
    try:
        resposta = MODEL.generate_content(prompt)
        return resposta.text
    except Exception as e:
        st.error(f"Erro ao consultar o Gemini: {e}")
        return None

def formatar_receitas(resposta):
    blocos = resposta.strip().split("\n\n")
    receitas = []

    for bloco in blocos:
        nome = ""
        ingredientes = []
        modo_preparo = ""
        estado = None

        linhas = bloco.strip().split("\n")
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue

            if not nome:
                nome = linha
                continue

            if linha.lower().startswith(("ingredientes", "lista de ingredientes")):
                estado = "ingredientes"
                continue
            elif linha.lower().startswith(("modo de preparo", "preparo", "instruções")):
                estado = "modo_preparo"
                continue

            if estado == "ingredientes":
                if linha.startswith(("-", "*")):
                    ingredientes.append(linha[1:].strip())
                else:
                    ingredientes.append(linha.strip())
            elif estado == "modo_preparo":
                modo_preparo += linha + " "

        receitas.append({
            "nome": nome.title(),
            "ingredientes": ingredientes,
            "modo_preparo": modo_preparo.strip()
        })

    return receitas


# ==============================
# 🚀 Interface Streamlit
# ==============================

st.title("🧑‍🍳 ChefBot - Seu Assistente Culinário Inteligente")
st.subheader("Crie receitas deliciosas com o que você tem em casa!")

st.markdown("---")

# 🔸 Inputs do usuário
ingredientes = st.text_input(
    "🛒 Ingredientes disponíveis (separados por vírgula):"
)

preferencias = st.text_input(
    "🌱 Preferências alimentares (vegetariano, vegano, low carb, etc.):"
)

restricoes = st.text_input(
    "⚠️ Restrições (alergias, sem glúten, sem lactose, etc.):"
)

st.markdown("---")


# 🔸 Botão de geração
if st.button("🍽️ Buscar Receitas"):
    if not ingredientes:
        st.warning("Por favor, insira ao menos um ingrediente!")
        st.stop()

    with st.spinner("👨‍🍳 O Chef está preparando sugestões..."):
        prompt = f"""
        Crie 2 receitas culinárias que usem os seguintes ingredientes: {ingredientes}.
        Considere as preferências: {preferencias if preferencias else 'nenhuma'} e restrições: {restricoes if restricoes else 'nenhuma'}.
        
        Para cada receita, forneça:
        - Nome da receita
        - Lista de ingredientes (em formato de lista com marcadores)
        - Modo de preparo claro e objetivo

        Responda no formato organizado e separado por parágrafos para cada receita.
        """

        resposta = obter_resposta_gemini(prompt)

        if resposta:
            receitas = formatar_receitas(resposta)

            for idx, receita in enumerate(receitas, start=1):
                st.subheader(f"🍳 Receita {idx}: {receita['nome']}")
                st.markdown("**🥗 Ingredientes:**")
                for ingrediente in receita['ingredientes']:
                    st.markdown(f"- {ingrediente}")

                st.markdown("**🔥 Modo de Preparo:**")
                st.markdown(receita['modo_preparo'])
                st.markdown("---")
        else:
            st.error("❌ Não foi possível obter receitas no momento. Tente novamente.")

if __name__ == "__main__":
    main()
