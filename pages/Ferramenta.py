import streamlit as st
from gtts import gTTS
from io import BytesIO
import time # ESSENCIAL: Usado para adicionar pausas e evitar o erro 429 (Too Many Requests)

# O limite máximo de caracteres por requisição para evitar o erro 429
# Usamos um limite seguro para o gTTS
MAX_CHARS_PER_CHUNK = 3500
# Tempo de espera entre cada requisição para o Google (Otimizado contra 429)
SAFETY_DELAY = 3.0


# --- FUNÇÃO PARA DIVIDIR O TEXTO EM BLOCOS (CHUNK) ---
def chunk_text(text, max_chars):
    """Divide o texto longo em blocos menores que o limite da API (gTTS)."""
    chunks = []
    
    # Se o texto for menor que o limite, retorna como um único bloco
    if len(text) <= max_chars:
        return [text]

    i = 0
    while i < len(text):
        # 1. Tenta cortar no limite máximo permitido (4500)
        max_possible_cut = min(i + max_chars, len(text))
        
        # 2. Busca o último ponto final/interrogação/exclamação ANTES do limite
        cut_point = -1
        for sep in ['.', '!', '?']:
            # rfind busca a última ocorrência no intervalo
            found_sep = text.rfind(sep, i, max_possible_cut)
            if found_sep > cut_point:
                cut_point = found_sep
        
        # 3. Se não encontrar uma pontuação satisfatória, corta no limite máximo (4500)
        if cut_point == -1:
             cut_point = max_possible_cut
        
        # Adiciona o bloco (chunk) à lista
        chunk = text[i:cut_point].strip()
        chunks.append(chunk)

        # Atualiza o índice inicial para o próximo ciclo
        i = cut_point
        # Avança o índice para pular o separador (ponto final, espaço, etc.), se houver
        while i < len(text) and text[i] in ['.', '!', '?', ' ']:
            i += 1
            
    return [c for c in chunks if c] # Retorna apenas blocos não vazios


# --- CONFIGURAÇÃO DA PÁGINA E CSS (Inalterada) ---
st.set_page_config(
    page_title="Ferramenta | VoxAcessível",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

CSS_ESTILO = """
    <style>
    /* Ocultar elementos padrão do Streamlit */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Centraliza o conteúdo */
    .stApp {
        text-align: center;
    }
    
    /* Estilo para o botão de geração de áudio */
    .stButton>button {
        background-color: #ff4b4b; /* Vermelho/Rosa do Streamlit */
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #e03c3c;
    }
    
    /* Garante que o input de texto e o uploader fiquem alinhados */
    .stTextInput, .stFileUploader {
        text-align: left;
    }
    
    /* Alinhamento do input de texto */
    .stTextArea {
        text-align: left;
    }
    
    /* Alinha o texto das colunas justificadamente, exceto nas legendas */
    .stText p {
        text-align: justify;
    }
    </style>
"""
st.markdown(CSS_ESTILO, unsafe_allow_html=True)


# --- FUNÇÃO PRINCIPAL ---
def main():
    st.title(" VoxAcessível: Gerador de Audiolivros e Áudio")
    st.markdown("---")

    col_input, col_options = st.columns([3, 1])

    # --- COLUNA DE OPÇÕES ---
    with col_options:
        st.markdown("### Opções de Voz")
        language = st.selectbox("Escolha o Idioma:", 
                                ["Português (BR)", "Inglês (EUA)"], 
                                key="lang_select")
        lang_code = "pt" if language == "Português (BR)" else "en"
        st.markdown("---")
        st.markdown("Opções Avançadas indisponíveis no momento.")


    # --- COLUNA DE INPUT ---
    with col_input:
        st.markdown("### Adicione o Conteúdo (Máx. 4500 caracteres por sessão)")
        
        # --- INPUT DE TEXTO MANUAL ---
        final_text = st.text_area(
            "Insira o texto aqui:",
            max_chars=MAX_CHARS_PER_CHUNK, 
            height=300,
            placeholder="Ex: A inclusão digital é um passo fundamental para a cidadania plena.",
            key="text_area_input"
        )
        
        st.markdown("### Gerar Áudio")
        
        # Botão para gerar o áudio
        if st.button("🎙️ Gerar Áudio", key="generate_button"):
            if not final_text:
                st.warning("Por favor, adicione texto para gerar o áudio.")
            else:
                # --- CHUNKING E GERAÇÃO DE ÁUDIO OTIMIZADA ---
                
                text_chunks = chunk_text(final_text, MAX_CHARS_PER_CHUNK)
                full_mp3_data = BytesIO()
                status_placeholder = st.empty()
                
                try:
                    for i, chunk in enumerate(text_chunks):
                        
                        # A PAUSA ESSENCIAL para evitar o erro 429
                        if i > 0:
                            time.sleep(SAFETY_DELAY) 
                        
                        status_placeholder.info(f"Processando bloco {i+1} de {len(text_chunks)} (caracteres: {len(chunk)})...")
                        
                        # Gera o áudio para o bloco
                        tts = gTTS(text=chunk, lang=lang_code, slow=False)
                        
                        # Salva o áudio do bloco no buffer temporário
                        chunk_mp3 = BytesIO()
                        tts.write_to_fp(chunk_mp3)
                        chunk_mp3.seek(0)
                        
                        # Adiciona o áudio do bloco ao buffer final
                        full_mp3_data.write(chunk_mp3.read())
                    
                    status_placeholder.empty()
                    st.success("Audiolivro Gerado com Sucesso! 🎧")
                    
                    # Prepara o buffer final para a reprodução e download
                    full_mp3_data.seek(0)

                    # Exibe o player de áudio
                    st.audio(full_mp3_data, format="audio/mp3")

                    # Botão para download
                    st.download_button(
                        label="⬇️ Download do Audiolivro (MP3)",
                        data=full_mp3_data,
                        file_name="voxacessivel_audiolivro.mp3",
                        mime="audio/mp3",
                        key="download_button"
                    )
                
                except Exception as e:
                    status_placeholder.empty()
                    st.error(f"Falha na Geração de Áudio. Verifique sua conexão. Erro: {e}")
                    st.warning("Tente simplificar o texto, pois a API pode falhar com caracteres muito incomuns.")

    st.markdown("---")
    st.caption("Tecnologias: Python, Streamlit e gTTS. O texto longo é processado em blocos para evitar limites da API.")

if __name__ == '__main__':
    main()