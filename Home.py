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
    page_title="Início | VoxAcelera", # NOVO TÍTULO
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- 1. CABEÇALHO E TÍTULO ---
st.title("VoxAcelera: Otimizando Leitura e Produtividade em Áudio") # NOVO TÍTULO
st.markdown("### Aumente sua eficiência na gestão de documentos e tempo") # NOVO SLOGAN
st.markdown("---")

# --- 2. BANNER PRINCIPAL ---
# NOVO CAPTION: Foco em Multitarefa e Produtividade
st.image("images/banner.png", caption="Ferramentas de gestão de tempo e conteúdo para máxima performance profissional.", use_container_width=True) 
st.markdown("---")

# --- 3. FOCO DO PROJETO: CARROSSEL ESTÁTICO (LADO A LADO) ---
st.subheader("Nosso Foco: Eficiência e Gestão de Tempo") # NOVO SUBTÍTULO

focos = [
    {"img": "images/foco1.jpg", "caption": "Multitarefa Inteligente", "text": "Consuma relatórios e artigos complexos por áudio enquanto executa outras tarefas críticas."},
    {"img": "images/foco2.jpg", "caption": "Otimização de Leitura", "text": "Converta PDFs e documentos longos em minutos, acelerando o aprendizado e a revisão de informações."},
    {"img": "images/foco3.jpg", "caption": "Foco Estruturado", "text": "Utilize o cronômetro Pomodoro e o assistente de tarefas para eliminar a procrastinação e manter a alta concentração."}
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
st.subheader("O Problema que Queremos Resolver: A Sobrecarga de Informação") # NOVO SUBTÍTULO

col_problema1, col_problema2 = st.columns([1, 2])

with col_problema1:
    st.image("images/problema.jpg",
              caption="O tempo gasto em leitura densa é um dreno na produtividade.", use_container_width=True) # NOVO CAPTION

with col_problema2:
    st.markdown("""
A vasta maioria dos dados e instruções cruciais para o seu trabalho está contida em **documentos de texto (PDFs, relatórios, manuais)**. Isso cria uma **barreira de eficiência**:
* **Perda de Tempo:** Profissionais e estudantes gastam horas lendo, revisando e relendo informações que poderiam ser consumidas auditivamente.
* **Fadiga Cognitiva:** A leitura prolongada de textos densos leva à exaustão e reduz a capacidade de tomada de decisão.
* **Multitarefa Ineficiente:** Você precisa processar informações e, ao mesmo tempo, executar tarefas práticas, o que é impossível apenas lendo.

O VoxAcelera oferece uma solução imediata, transformando qualquer texto, especialmente PDFs, em **áudio de alta qualidade** (via gTTS), permitindo que você consuma o conteúdo onde e quando quiser, **maximizando o Retorno sobre o Tempo (ROT)**.
""") # NOVO TEXTO

st.markdown("---")

# --- 5. NOVA SEÇÃO: FOCO NO DÉFICIT DE ATENÇÃO (TDAH) ---
st.subheader("O Desafio da Concentração e da Procrastinação") # NOVO SUBTÍTULO (Foco na Procrastinação)

col_tdah1, col_tdah2 = st.columns([2, 1])

with col_tdah1:
    st.info("""
    Manter o foco em tarefas longas e repetitivas é um desafio universal na era digital. A **procrastinação** e o **déficit de atenção** afetam a execução de projetos críticos.
    
    Nossa abordagem de Foco Estruturado oferece benefícios duplos:
    
    * **Estrutura de Execução (Pomodoro):** Impõe blocos de **foco profundo e ininterrupto** (25 min), seguidos por pausas obrigatórias, combatendo a dispersão.
    * **Gestão de Tarefas Ágil:** Permite que você defina a **Prioridade** e o **Tempo Estimado** para cada tarefa, garantindo que você esteja sempre trabalhando no que gera mais valor.
    * **Consumo Dinâmico (Áudio):** Permite que você **ouça** informações complexas em vez de apenas ler, reduzindo a monotonia e ativando o **aprendizado multimodal** para uma melhor retenção.
    
    O VoxAcelera é o seu aliado para transformar a intenção de ser produtivo em **execução consistente**.
    """) # NOVO TEXTO

with col_tdah2:
    # IMAGEM RELEVANTE PARA FOCO/ATENÇÃO (Substitua pela imagem real)
    st.image("images/foco_atencao.png", caption="Estrutura e áudio para execução de tarefas.", use_container_width=True) 
    
st.markdown("---")


# --- 6. CONTEXTO SOCIAL E DADOS (Atualizado com Menção) ---
st.subheader("Valor Agregado: Quem Ganha com a Eficiência?") # NOVO SUBTÍTULO

col_dados1, col_dados2 = st.columns([3, 2]) 

with col_dados1:
    st.info("""
    A busca por ferramentas de produtividade e otimização de tempo é uma necessidade crescente no mercado de trabalho. O VoxAcelera agrega valor para:
    
    * **Profissionais Ocupados:** Que precisam consumir documentos rapidamente (relatórios, contratos) sem estarem presos a uma tela.
    * **Estudantes de Alto Nível:** Que precisam absorver vastos volumes de material para exames e pesquisas.
    * **Usuários com Desafios de Leitura:** Embora o foco seja Produtividade, a função de **Acessibilidade Visual** (espaçamento, tamanho da fonte) é um bônus vital para quem tem dislexia ou dificuldades de leitura, garantindo que a **eficiência seja acessível a todos**.
    
    Ao integrar conversão de áudio, gestão de tarefas e foco estruturado, o VoxAcelera não apenas economiza tempo, mas melhora a **qualidade da sua performance cognitiva**.
    """) # NOVO TEXTO

with col_dados2:
    st.image("images/foco4.jpeg", caption="Aumento da velocidade de consumo de conteúdo.", use_container_width=True) # NOVO CAPTION

st.markdown("---")


# --- 7. SEÇÃO OBJETIVO PRINCIPAL (AGORA SIMPLES E CENTRALIZADO) ---
st.subheader("O Nosso Objetivo É Claro: Máxima Performance") # NOVO SUBTÍTULO

# Usa colunas para centralizar o texto do objetivo
col_obj_antes, col_obj_principal, col_obj_depois = st.columns([1, 4, 1])

with col_obj_principal:
    # Apenas o texto, centralizado com a classe CSS
    st.markdown("""
    <p class="objective-text">
    Entregar uma aplicação web poderosa e intuitiva que transforma documentos densos em áudio de alta qualidade e oferece ferramentas de gestão de tempo (Pomodoro e Tarefas). Com o VoxAcelera, visamos otimizar a rotina de trabalho e estudo, promovendo a máxima performance individual.
    </p>
    """, unsafe_allow_html=True) # NOVO TEXTO

st.markdown("---")

# --- 8. CHAMADA PARA AÇÃO COM BOTÃO FUNCIONAL (Botão Único) ---
st.subheader("Acelere sua Produtividade Agora!") # NOVO SUBTÍTULO
st.markdown("""
<div class="center-text-block">
    <p>Clique no botão abaixo para acessar as ferramentas e comece a otimizar sua leitura e seu foco hoje mesmo.</p>
</div>
""", unsafe_allow_html=True)

# Usa colunas para centralizar o botão final
col_btn_antes, col_btn_centro, col_btn_depois = st.columns([1, 1, 1])

with col_btn_centro:
    # O LINK FINAL E CORRETO
    st.markdown("""
    <a href="/Ferramenta" class="link-button-style">  Acessar o VoxAcelera
    </a>
    """, unsafe_allow_html=True)