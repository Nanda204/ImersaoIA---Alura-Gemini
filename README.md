# ImersaoIA---Alura-Gemini

# 🧑‍🍳 ChefBot: Seu Assistente Culinário Inteligente

**Diga os ingredientes que você tem na geladeira e deixe o ChefBot te mostrar as delícias que você pode preparar!** 

O ChefBot é um chatbot inteligente que utiliza o poder do Google Gemini para sugerir pratos criativos e personalizados, levando em conta seus ingredientes disponíveis, preferências alimentares e restrições. 

**Receitas fáceis, rápidas e deliciosas para todos os gostos!**

**Evite o desperdício e simplifique suas refeições!**

**Liberte o chef que há em você!**


## 🔗 Acesso

**Acesse o aplicativo do Streamlit :**
https://chefbotassistenteinteligente.streamlit.app/


**Como rodar no Google Colab:**

💻 Preparação no Colab:

-> Baixe o arquivo do sistema ChefBot (O arquivo .ipynb).
-> Abra o arquivo no Google Colab.

▶️ Execução no Colab:

1.  Abra um novo notebook no https://colab.research.google.com/
   
2.  No notebook aberto, execute cada célula de código sequencialmente, clicando no botão de "play" (▶️) ao lado de cada célula. 


## ✨ Funcionalidades

✅ **Entrada de Ingredientes:** Permite que o usuário liste os ingredientes disponíveis.

✅ **Entrada de Preferências:** O usuário pode especificar preferências alimentares (vegetariano, vegano, etc.).

✅ **Entrada de Restrições:** O usuário pode informar restrições alimentares (alergias, intolerâncias).

✅ **Sugestão de Receita:** Utiliza a API do Google Gemini para gerar sugestões de receitas personalizadas com base nas entradas do usuário.

✅ **Exibição da Receita:** Apresenta o nome da receita, a lista de ingredientes e o modo de preparo de forma clara.


## ℹ️ Contexto do Projeto

Este projeto foi desenvolvido durante a **Imersão IA** da Alura + Google Gemini, com o objetivo principal de **explorar o potencial da Inteligência Artificial Generativa**. É uma iniciativa da **Alura** em parceria com o **Google Gemini**, utilizando a **API do Google Gemini** para criar uma aplicação prática e útil no campo da culinária.


## 🎯 Objetivo do Projeto

✅ O objetivo principal do ChefBot é fornecer aos usuários uma maneira rápida e fácil de obter sugestões de receitas criativas e personalizadas, com base nos ingredientes que já possuem em casa. Além disso, busca inspirar os usuários a experimentar novas receitas e reduzir o desperdício de alimentos.

✅ É um chatbot inteligente de culinária desenvolvido para auxiliar você a descobrir novas receitas criativas e personalizadas.

✅ Utilizando a inteligência artificial generativa do Google Gemini, o ChefBot considera os ingredientes que você tem à disposição, suas preferências alimentares e quaisquer restrições para fornecer sugestões culinárias relevantes e inspiradoras.


## 🛠️ Tecnologia

As seguintes tecnologias foram utilizadas no desenvolvimento deste projeto:

✅ **Python:** A linguagem de programação principal utilizada para construir a lógica do aplicativo.
  
✅ **Streamlit:** Um framework Python de código aberto para criar aplicativos web interativos e compartilháveis para aprendizado de máquina e ciência de dados de forma rápida e fácil. Ele simplifica a criação da interface de usuário.

✅ **Google Generative AI (API do Google Gemini):** A API fornecida pelo Google para acessar modelos de linguagem grandes como o Gemini, capaz de gerar texto criativo e informativo, como as sugestões de receitas.

✅ **dotenv:** Uma biblioteca Python para carregar variáveis de ambiente de um arquivo `.env`. Usada para armazenar a chave da API do Google Gemini de forma segura.



## 🎨 Layout e Telas

![Tela App](https://github.com/user-attachments/assets/afd73311-af5b-4e0c-a455-dada60d39da6)


O layout do ChefBot é projetado para ser simples e intuitivo:

1.  **Título:** A tela principal apresenta o título "ChefBot: Seu Assistente Culinário Inteligente" de forma proeminente.
2.  **Descrição:** Uma breve descrição do propósito do ChefBot e suas funcionalidades é exibida abaixo do título para orientar o usuário.
3.  **Entrada de Ingredientes:** Um campo de texto ("Quais ingredientes você tem em casa?") permite que o usuário insira os ingredientes disponíveis, separados por vírgula.
4.  **Entrada de Preferências (Opcional):** Um campo de texto ("Você tem alguma preferência alimentar?") para especificar preferências.
5.  **Entrada de Restrições (Opcional):** Um campo de texto ("Você tem alguma restrição alimentar?") para informar restrições.
6.  **Botão de Busca:** Um botão ("Buscar Receitas") aciona a consulta ao Google Gemini com as informações fornecidas.
7.  **Área de Resultados:** Abaixo do botão, as sugestões de receitas são exibidas. Cada receita geralmente inclui:
    * **Nome:** O título da receita.
    * **Ingredientes:** Uma lista dos ingredientes necessários.
    * **Modo de Preparo:** As instruções passo a passo para preparar a receita.
8.  **Mensagens Informativas:** O aplicativo exibe mensagens informativas (por exemplo, confirmando os ingredientes inseridos) ou avisos (por exemplo, se nenhum ingrediente for fornecido ou se o Gemini não retornar resultados).

*(Se você tiver um mockup visual, pode adicionar uma seção aqui descrevendo cada tela com mais detalhes, ou até mesmo incluir uma imagem do mockup.)*


## ⚖️ Licença

✅ Este projeto está licenciado sob a [MIT License](LICENSE).
