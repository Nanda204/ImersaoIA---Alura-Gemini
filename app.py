!pip install google-genai

import streamlit as st
import os
from google.generativeai import GenerativeModel
import re
import json

from google.colab import userdata
os.environ['GOOGLE_API_KEY'] = userdata.get('GOOGLE_API_KEY')

from google import genai
client = genai. Client()

modelo = "gemini-2.0-flash"

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

def obter_resposta_do_gemini(prompt, modelo="gemini-2.0-flash"):
    """Obtém uma resposta do modelo Gemini."""
    try:
        model = GenerativeModel(modelo)
        response = model.generate_content(prompt)
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
            # Tenta identificar o nome da receita (pode ser a primeira linha não vazia)
            nome = linha
            estado = "ingredientes"
        elif estado == "ingredientes":
            # Procura por indicadores de ingredientes (e.g., listas com "- ", "* ", ou apenas itens separados)
            if linha.lower().startswith("ingredientes") or linha.lower().startswith("lista de ingredientes"):
                continue
            elif re.match(r"[-*]\s+.+", linha):
                ingredientes.append(linha.split(maxsplit=1)[1].strip())
            elif modo_preparo is None and (linha.lower().startswith("modo de preparo") or linha.lower().startswith("preparo") or linha.lower().startswith("instruções")):
                estado = "modo_preparo"
                modo_preparo_linhas = []
            elif modo_preparo is None:
                # Se não encontrou explicitamente "modo de preparo" e não é um item de lista,
                # pode ser o início do modo de preparo (tentativa heurística)
                modo_preparo_linhas = [linha]
                estado = "modo_preparo"
            elif estado == "modo_preparo":
                modo_preparo_linhas.append(linha)

    if modo_preparo_linhas:
        modo_preparo = "\n".join(modo_preparo_linhas)

    return nome, ingredientes, modo_preparo

def main():
    st.title("🧑‍🍳 ChefBot")
    st.write("Olá! Bem-vindo ao ChefBot. Posso sugerir algumas receitas criativas com base nos ingredientes que você tem em casa!")
    st.write("\n")

    ingredientes_str = st.text_input("✍️ Quais ingredientes você tem em casa? (separados por vírgula)").lower()
    preferencias = st.text_input("🤔 Você tem alguma preferência alimentar? (vegetariano, vegano, sem glúten, etc., separado por vírgula)").lower()
    restricoes = st.text_input("🚫 Você tem alguma restrição alimentar? (alergias, intolerâncias, etc., separado por vírgula)").lower()

    if st.button("Buscar Receitas"):
        if ingredientes_str:
            ingredientes = [ingrediente.strip() for ingrediente in ingredientes_str.split(",")]
            preferencias_lista = [p.strip() for p in preferencias.split(",") if p.strip()]
            restricoes_lista = [r.strip() for r in restricoes.split(",") if r.strip()]

            st.write(f"📄 Você informou os seguintes ingredientes: {', '.join(ingredientes)}.")
            if preferencias_lista:
                st.write(f"📄 Suas preferências são: {', '.join(preferencias_lista)}.")
            if restricoes_lista:
                st.write(f"📄 Suas restrições são: {', '.join(restricoes_lista)}.")
            st.write("\n")
            st.write("🧑‍🍳 Deixe-me pedir sugestões ao Chef Gemini...")

            prompt = f"""
            Com os ingredientes: {', '.join(ingredientes)}, e considerando as preferências: {', '.join(preferencias_lista) or 'nenhuma'}, e restrições: {', '.join(restricoes_lista) or 'nenhuma'}, você pode sugerir algumas receitas criativas?
            Liste 2 ou 3 receitas diferentes, cada uma com um nome claro, uma lista de ingredientes e um modo de preparo conciso.
            """
            resposta_gemini = obter_resposta_do_gemini(prompt)

            if resposta_gemini:
                st.subheader("Sugestões do Gemini:")
                receitas_texto = resposta_gemini.split("\n\n") # Tenta separar as receitas por dois quebras de linha

                for i, receita_texto in enumerate(receitas_texto):
                    st.subheader(f"Receita {i+1}")
                    nome, ingredientes, modo_preparo = formatar_receita(receita_texto)

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
            else:
                st.warning("😞 Desculpe, o Gemini não conseguiu gerar sugestões no momento. Tente novamente mais tarde ou com outros ingredientes.")
        else:
            st.warning("Por favor, insira alguns ingredientes.")

if __name__ == "__main__":
    main()
