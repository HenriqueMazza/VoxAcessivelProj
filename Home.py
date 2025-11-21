import streamlit as st

# --- INJEÇÃO DE CSS (Centralização, Estilo e Ocultar Elementos) ---
CSS_ESTILO = """
    <style>
    /* Esconde o footer "Made with Streamlit" e o menu principal (Hambúrguer) */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Ajusta o espaçamento, largura máxima e centraliza o conteúdo principal */
    .main .block-container {
        padding-top: 2rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 2rem;
        max-width: 900px;
        margin: auto;
    }
    
    /* Centraliza todos os elementos de texto e imagem por padrão no container principal */
    .stApp > header, .main > div > div > div {
        text-align: center;
    }
    
    /* Centraliza títulos */
    h1, h2, h3, h4, h5, h6 {
        text-align: center;
        width: 100%;
    }

    /* Estilo para o título principal */
    h1 {
        color: #007bff;
        border-bottom: 3px solid #4CAF50;
        padding-bottom: 15px;
        margin-bottom: 30px;
        font-size: 2.8em;
    }
    
    /* Destaque para sub-cabeçalhos importantes */
    h2 {
        color: #4CAF50;
        margin-top: 30px;
        margin-bottom: 15px;
        border-left: none;
        padding-left: 0;
    }

    /* Estilo para o bloco de Destaque (Objetivo) - Fundo mais claro */
    .st.success {
        background-color: #e6ffe6;
        color: #2e8b57;
        border-left: 8px solid #4CAF50;
        padding: 15px;
        border-radius: 8px;
        font-size: 1.1em;
        margin-bottom: 25px;
        text-align: left;
        line-height: 1.6;
    }

    /* Estilo para o bloco de Contexto Social (Colunas) */
    .st.info {
        background-color: #f0f8ff;
        color: #1e90ff;
        border-left: 8px solid #007bff;
        padding: 15px;
        border-radius: 8px;
        font-size: 1.1em;
        margin-bottom: 25px;
        text-align: left;
        line-height: 1.6;
    }

    /* ESTILO PARA O BOTÃO FINAL DE ACESSO (Mais quadrado e centralizado) */
    .link-button-style {
        background-color: #007bff;
        color: white !important;
        font-size: 1.2em;
        padding: 25px 40px; 
        border-radius: 10px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        display: inline-block; 
        width: auto; 
        text-align: center;
        margin: 40px auto;
        text-decoration: none; 
    }
    .link-button-style:hover {
        background-color: #0056b3; 
        transform: translateY(-2px);
    }
    
    /* Estilo para Imagens */
    .stImage > img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        width: 100%;
        height: auto; 
        object-fit: cover;
    }
    
    /* Estilo para centralizar o texto da chamada para ação */
    .center-text-block p {
        text-align: center !important;
    }

    /* Alinha o texto das colunas justificadamente */
    .stText p {
        text-align: justify;
    }

    /* Estilo específico para o texto do Objetivo Principal centralizado (Sem botão) */
    .objective-text {
        text-align: center;
        font-size: 1.2em;
        line-height: 1.7;
        margin-top: 15px;
        margin-bottom: 30px;
        color: #f0f0f0; /* Cor clara para o texto */
    }


    </style>
"""
st.markdown(CSS_ESTILO, unsafe_allow_html=True)


st.set_page_config(
    page_title="Início | VoxAcessível",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- 1. CABEÇALHO E TÍTULO ---
st.title(" VoxAcessível: Democratizando o Acesso à Informação")
st.markdown("### Um Projeto Universitário de Impacto Social para uma Sociedade Mais Justa")
st.markdown("---")

# --- 2. BANNER PRINCIPAL ---
st.image("images/banner.png", caption="Tecnologia a serviço da inclusão", use_container_width=True)
st.markdown("---")

# --- 3. FOCO DO PROJETO: CARROSSEL ESTÁTICO (LADO A LADO) ---
st.subheader("Nosso Foco: Acessibilidade e Inclusão")

focos = [
    {"img": "images/foco1.jpg", "caption": "Acesso Universal", "text": "Quebrar as barreiras textuais, permitindo que o conteúdo digital seja acessado por todos."},
    {"img": "images/foco2.jpg", "caption": "Educação Sem Limites", "text": "Potencializar o aprendizado para estudantes com dislexia, deficiência visual ou analfabetismo funcional."},
    {"img": "images/foco3.jpg", "caption": "Tecnologia Cidadã", "text": "Utilizar Python e Streamlit para garantir que a tecnologia seja uma força para a igualdade e inclusão."}
]

# Cria 3 colunas para exibir os focos
col_foco1, col_foco2, col_foco3 = st.columns(3) 

with col_foco1:
    st.image(focos[0]["img"], use_container_width=True)
    st.markdown(f"**{focos[0]['caption']}**")
    st.caption(focos[0]["text"])

with col_foco2:
    st.image(focos[1]["img"], use_container_width=True)
    st.markdown(f"**{focos[1]['caption']}**")
    st.caption(focos[1]["text"])

with col_foco3:
    st.image(focos[2]["img"], use_container_width=True)
    st.markdown(f"**{focos[2]['caption']}**")
    st.caption(focos[2]["text"])

st.markdown("---")


# --- 4. SEÇÃO DE PROBLEMATIZAÇÃO ---
st.subheader("O Problema que Queremos Resolver: A Barreira do Texto")

col_problema1, col_problema2 = st.columns([1, 2])

with col_problema1:
    st.image("images/problema.jpg",
             caption="O acesso à informação ainda é um desafio para muitos.", use_container_width=True)

with col_problema2:
    st.markdown("""
A vasta maioria do conteúdo digital na internet é apresentada em formato de texto. Isso cria uma **barreira intransponível** para diversos grupos:
* **Pessoas com Deficiência Visual:** Embora existam leitores de tela, a experiência muitas vezes é complexa, cara ou não intuitiva.
* **Indivíduos com Dislexia:** O texto pode ser uma fonte de frustração e lentidão no aprendizado.
* **Analfabetismo Funcional:** Pessoas que, mesmo sabendo ler, têm dificuldade em compreender textos complexos.

O VoxAcessível oferece uma solução de baixo custo, imediata e user-friendly, utilizando a avançada tecnologia de **Text-to-Speech do Google (gTTS)** para garantir que a informação alcance a todos, fortalecendo a **democratização do conhecimento**.
""")

st.markdown("---")

# --- 5. CONTEXTO SOCIAL E DADOS ---
st.subheader("Impacto Social: Quem Será Beneficiado?")

col_dados1, col_dados2 = st.columns([3, 2]) 

with col_dados1:
    st.info("""
    O desafio de acesso à informação é uma realidade para uma parcela significativa da população. No Brasil, estimativas apontam que **mais de 45 milhões** de pessoas podem se beneficiar diretamente de tecnologias assistivas como o VoxAcessível.
    
    Dados Chave:
    * **Deficiência Visual:** Cerca de **7 milhões** de brasileiros.
    * **Dislexia e Dificuldades de Leitura:** Estima-se que até **10-15%** da população enfrente algum grau de dislexia.
    * **Analfabetismo Funcional:** Um desafio que atinge aproximadamente **29%** da população adulta.

    Ao oferecer uma solução gratuita e acessível, o VoxAcessível ataca um problema de **inclusão social**, transformando a forma como milhões de brasileiros interagem com o mundo digital.
    """)

with col_dados2:
    st.image("images/foco4.jpeg", caption="O áudio como ferramenta de inclusão.", use_container_width=True)

st.markdown("---")


# --- 6. SEÇÃO OBJETIVO PRINCIPAL (AGORA SIMPLES E CENTRALIZADO) ---
st.subheader("O Nosso Objetivo É Claro")

# Usa colunas para centralizar o texto do objetivo
col_obj_antes, col_obj_principal, col_obj_depois = st.columns([1, 4, 1])

with col_obj_principal:
    # Apenas o texto, centralizado com a classe CSS
    st.markdown("""
    <p class="objective-text">
    Desenvolver uma aplicação web simples, intuitiva e acessível para converter textos digitais em áudio de alta qualidade. Com o VoxAcessível, visamos reduzir drasticamente a exclusão informacional de milhões de pessoas, promovendo a cidadania digital plena.
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 7. CHAMADA PARA AÇÃO COM BOTÃO FUNCIONAL (Botão Único) ---
st.subheader("Experimente o VoxAcessível Agora!")
st.markdown("""
<div class="center-text-block">
    <p>Clique no botão abaixo para ir diretamente para a nossa ferramenta e veja como é fácil 
    transformar texto em áudio.</p>
</div>
""", unsafe_allow_html=True)

# Usa colunas para centralizar o botão final
col_btn_antes, col_btn_centro, col_btn_depois = st.columns([1, 1, 1])

with col_btn_centro:
    # O LINK FINAL E CORRETO (Botão Único, Mais Quadrado e Centralizado)
    st.markdown("""
    <a href="/Ferramenta" class="link-button-style">  Acessar a Ferramenta VoxAcessível
    </a>
    """, unsafe_allow_html=True)
