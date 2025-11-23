import streamlit as st
from gtts import gTTS
from io import BytesIO
import time 
import PyPDF2 
import re 
import uuid 
# Removidos imports não utilizados

# --- CONFIGURAÇÕES DO SISTEMA ---
MAX_CHARS_PER_CHUNK = 3500
SAFETY_DELAY = 1.5 
ACCESSIBLE_FONT = "Arial, sans-serif"

# --- CHAVES DE NAVEGAÇÃO ---
TAB_AUDIO = "🎙️ Gerador de Audiolivros e Áudio"
TAB_TASKS = "📝 Assistente de Tarefas e Foco"


# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if 'text_area_input' not in st.session_state:
    st.session_state["text_area_input"] = ""

# 🔑 ESTADO: Armazena qual aba está ativa (padrao: audio)
if 'active_tab_key' not in st.session_state:
    st.session_state['active_tab_key'] = TAB_AUDIO

# Estado para o Cronômetro de Foco (Pomodoro)
if 'timer_running' not in st.session_state:
    st.session_state['timer_running'] = False
if 'timer_total_seconds' not in st.session_state:
    st.session_state['timer_total_seconds'] = 0
if 'timer_start_time' not in st.session_state:
    st.session_state['timer_start_time'] = 0
if 'timer_phase' not in st.session_state:
    st.session_state['timer_phase'] = 'Foco'
if 'break_duration' not in st.session_state:
    st.session_state['break_duration'] = 5 * 60

# Estado para o Assistente de Planejamento de Tarefas
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = [] 

# Estado para a CHAVE de INPUT da Tarefa
if 'new_task_description_input' not in st.session_state:
    st.session_state['new_task_description_input'] = ""
    
# --- FUNÇÃO PARA EXTRAIR TEXTO DE PDF ---
def extract_text_from_pdf(pdf_file):
    """Lê um arquivo PDF e retorna todo o texto extraído."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = []
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text.append(content)
        return "\n".join(text)
    except Exception as e:
        st.error(f"Erro ao ler PDF: {e}")
        return ""


# --- FUNÇÃO PARA DIVIDIR O TEXTO EM BLOCOS (CHUNK) ---
def chunk_text(text, max_chars):
    """Divide o texto longo em blocos menores que o limite da API (gTTS)."""
    chunks = []
    text = ' '.join(text.split())

    if len(text) <= max_chars:
        return [text]

    i = 0
    while i < len(text):
        max_possible_cut = min(i + max_chars, len(text))
        cut_point = -1
        # Procura um ponto de corte em pontuações para não quebrar a frase no meio
        for sep in ['.', '!', '?']: 
            found_sep = text.rfind(sep, i, max_possible_cut)
            if found_sep > cut_point:
                cut_point = found_sep
        
        if cut_point == -1:
             cut_point = max_possible_cut
        
        chunk = text[i:cut_point].strip()
        chunks.append(chunk)

        i = cut_point
        # Avança para o próximo caractere após a pontuação/espaço
        while i < len(text) and text[i] in ['.', '!', '?', ' ']:
            i += 1
            
    return [c for c in chunks if c]


# --- FUNÇÃO PARA INJETAR CSS DINÂMICO ---
def inject_dynamic_css(font_size, line_height, font_family):
    """Injeta CSS para controlar a acessibilidade visual e botões."""
    css = f"""
        <style>
        /* Ocultar elementos padrão do Streamlit */
        footer {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}

        /* Estilo para o st.text_area */
        .stTextArea textarea {{
            font-family: {font_family} !important;
            font-size: {font_size}px !important;
            line-height: {line_height} !important;
        }}
        .stButton>button {{
            background-color: #ff4b4b; 
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 5px; 
        }}
        .stButton>button:hover {{
            background-color: #e03c3c;
        }}
        /* Estilo especial para o botão de CANCELAR do Timer */
        .stButton button[key*="cancel_focus_timer"] {{
            background-color: #dc3545; 
        }}
        .stButton button[key*="cancel_focus_timer"]:hover {{
            background-color: #c82333;
        }}

        /* --- ESTILOS PARA O ASSISTENTE DE TAREFAS --- */
        .task-item {{
            display: flex;
            align-items: center;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 8px;
            border: 1px solid #333;
            background-color: #262730; 
        }}
        .task-item.completed {{
            text-decoration: line-through;
            opacity: 0.6;
            background-color: #1e2025;
            border-color: #1e2025;
        }}
        .task-description {{
            flex-grow: 1;
            font-size: 16px;
            color: white;
        }}
        .task-details {{
            font-size: 13px;
            color: #aaa;
            margin-left: 15px;
            white-space: nowrap; 
        }}

        /* Cores de Prioridade */
        .priority-high {{ border-left: 5px solid #e74c3c; }} 
        .priority-medium {{ border-left: 5px solid #f39c12; }} 
        .priority-low {{ border-left: 5px solid #2ecc71; }} 

        /* Estilo para os botões de ação na lista de tarefas */
        .task-actions .stButton>button {{
            width: auto;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            margin-left: 5px;
            margin-top: 0;
        }}
        .task-actions .stButton button[data-testid="baseButton-secondary"] {{ 
            background-color: #6c757d;
        }}
        .task-actions .stButton button[data-testid="baseButton-secondary"]:hover {{
            background-color: #5a6268;
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# --- FUNÇÃO PARA GERAR ANÚNCIO DE ÁUDIO ---
@st.cache_data
def generate_audio_announcement(text, lang_code):
    """Gera o áudio para um texto de anúncio e o retorna."""
    try:
        tts = gTTS(text=text, lang=lang_code)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp.read()
    except Exception as e:
        return None

# --- FUNÇÃO POMODORO TIMER (NÃO-BLOQUEANTE) ---
def start_pomodoro_timer(focus_minutes, break_minutes, lang_code, audio_placeholder):
    """Inicia o ciclo Pomodoro configurando o estado inicial."""
    
    st.session_state['timer_total_seconds'] = focus_minutes * 60
    st.session_state['timer_start_time'] = time.time()
    st.session_state['timer_running'] = True
    st.session_state['timer_phase'] = 'Foco'
    st.session_state['break_duration'] = break_minutes * 60

    start_focus_msg = "Atenção! O ciclo de foco começou. Concentre-se."
    start_focus_audio = generate_audio_announcement(start_focus_msg, lang_code)
    if start_focus_audio:
        audio_placeholder.audio(start_focus_audio, format="audio/mp3", autoplay=True)

    # st.rerun() é necessário aqui para forçar o início imediato do loop do timer
    st.rerun() 


# --- FUNÇÕES DO ASSISTENTE DE TAREFAS ---
def add_task_callback():
    """
    Adiciona a tarefa. st.rerun() removido.
    Usa a chave 'new_task_description_input' para o widget.
    """
    description = st.session_state.get('new_task_description_input') 
    priority = st.session_state.get('new_task_priority_select')
    estimated_time = st.session_state.get('new_task_time_input')

    if description and description.strip():
        task = {
            "id": str(uuid.uuid4()),
            "description": description.strip(),
            "priority": priority,
            "estimated_time": estimated_time,
            "completed": False,
            "timestamp": time.time()
        }
        st.session_state['tasks'].append(task)
        st.success("Tarefa adicionada!")
        
        # Limpa o input no próximo rerun automático do Streamlit
        st.session_state['new_task_description_input'] = ""
        
        # Garante que a ABA TAREFAS permaneça ativa após o rerun automático
        st.session_state['active_tab_key'] = TAB_TASKS
        
    else:
        st.warning("A descrição da tarefa não pode estar vazia.")


def complete_task(task_id):
    """
    Conclui a tarefa. st.rerun() removido.
    """
    for task in st.session_state['tasks']:
        if task['id'] == task_id:
            task['completed'] = True
            st.success(f"Tarefa '{task['description']}' concluída!")
            return

def delete_task(task_id):
    """
    Exclui a tarefa. st.rerun() removido.
    """
    st.session_state['tasks'] = [task for task in st.session_state['tasks'] if task['id'] != task_id]
    st.warning("Tarefa excluída.")


# --- FUNÇÃO PRINCIPAL ---
def main():
    
    st.set_page_config(layout="wide") 
    
    st.title(" ✨ Ferramentas de Acessibilidade e Produtividade")
    st.markdown("---")

    # Garante que os valores iniciais de font/line height existam
    if 'font_size' not in st.session_state: st.session_state['font_size'] = 18
    if 'line_height' not in st.session_state: st.session_state['line_height'] = 1.5
        
    inject_dynamic_css(st.session_state['font_size'], st.session_state['line_height'], ACCESSIBLE_FONT)


    # --- SELETOR DE ABA (Simulação de st.tabs para compatibilidade) ---
    tab_titles = [TAB_AUDIO, TAB_TASKS]
    
    # Usa um radio button para simular a navegação da aba
    selected_tab = st.radio(
        "Selecione a Ferramenta:",
        tab_titles,
        index=tab_titles.index(st.session_state.get('active_tab_key', TAB_AUDIO)),
        horizontal=True,
        key='tab_selector'
    )
    
    # Atualiza o estado da aba ativa
    st.session_state['active_tab_key'] = selected_tab

    st.markdown("---")

    # --- ABA: GERADOR DE ÁUDIO E AUDIOLIVROS ---
    if st.session_state['active_tab_key'] == TAB_AUDIO:
        st.header("Gerador de Audiolivros e Áudio")
        col_input, col_options = st.columns([3, 1])

        # --- COLUNA DE OPÇÕES ---
        with col_options:
            st.markdown("### Opções de Voz")
            language = st.selectbox("Escolha o Idioma:", 
                                    ["Português (BR)", "Inglês (EUA)"], 
                                    key="lang_select_audio")
            lang_code = "pt" if language == "Português (BR)" else "en"
            
            is_slow = st.checkbox("Leitura Lenta (Melhor para Dislexia)", value=False, key="is_slow_audio")
            st.markdown("---")

            # MODO ACESSIBILIDADE VISUAL
            st.markdown("### Acessibilidade Visual (Global)")
            st.caption("Ajuste para Dislexia e Baixa Visão. Afeta ambas as abas.")
            st.session_state['font_size'] = st.slider("Tamanho da Fonte (px):", 14, 30, st.session_state['font_size'], key="global_font_size")
            st.session_state['line_height'] = st.slider("Espaçamento de Linha:", 1.0, 3.0, st.session_state['line_height'], 0.1, key="global_line_height")
            
            inject_dynamic_css(st.session_state['font_size'], st.session_state['line_height'], ACCESSIBLE_FONT)
            
            st.markdown("---")
            
            # --- CRONÔMETRO DE FOCO (POMODORO) ---
            st.markdown("### ⏱️ Cronômetro de Foco")
            st.caption("Apoio para concentração (TDAH).")

            focus_min = st.number_input("Duração do Foco (min):", min_value=1, value=25, key='focus_input', disabled=st.session_state['timer_running'])
            break_min = st.number_input("Duração da Pausa (min):", min_value=1, value=5, key='break_input', disabled=st.session_state['timer_running'])
            
            timer_status = st.empty()
            timer_audio = st.empty()
            
            # --- LÓGICA DE GERENCIAMENTO DO TIMER ---
            if st.session_state['timer_running']:
                
                elapsed_time = time.time() - st.session_state['timer_start_time']
                total_duration = st.session_state['timer_total_seconds']
                remaining_time = max(0, total_duration - elapsed_time)
                
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                
                if st.button("🛑 Cancelar Foco", key="cancel_focus_timer_audio_tab"): 
                    st.session_state['timer_running'] = False
                    st.session_state['timer_phase'] = 'Foco' 
                    st.session_state['timer_total_seconds'] = 0 
                    timer_status.error("Ciclo de Foco Cancelado Manualmente.")
                    st.rerun() 
                
                if remaining_time > 0:
                    if st.session_state['timer_phase'] == 'Foco':
                        timer_status.info(f"Foco Ativo: {minutes:02d}:{seconds:02d} restantes.")
                    else:
                        timer_status.warning(f"Pausa Ativa: {minutes:02d}:{seconds:02d} restantes.")
                    
                    time.sleep(1) 
                    st.rerun() 
                
                else:
                    if st.session_state['timer_phase'] == 'Foco':
                        st.session_state['timer_phase'] = 'Pausa'
                        st.session_state['timer_total_seconds'] = st.session_state['break_duration']
                        st.session_state['timer_start_time'] = time.time()
                        
                        break_time_msg = "Parabéns! Fim do ciclo de foco. Faça uma pausa."
                        break_time_audio = generate_audio_announcement(break_time_msg, lang_code)
                        if break_time_audio:
                            timer_audio.audio(break_time_audio, format="audio/mp3", autoplay=True)
                            
                        st.rerun()

                    else: 
                        st.session_state['timer_running'] = False
                        timer_status.success("Ciclo Pomodoro Concluído. 🚀")
                        
                        end_break_msg = "A pausa terminou. Um ciclo completo foi finalizado."
                        end_break_audio = generate_audio_announcement(end_break_msg, lang_code)
                        if end_break_audio:
                            timer_audio.audio(end_break_audio, format="audio/mp3", autoplay=True)
                        
                        st.rerun() 
            
            else:
                if st.button("🔴 Iniciar Foco", key="start_focus_timer_audio_tab"): 
                    start_pomodoro_timer(focus_min, break_min, lang_code, timer_audio)

        # --- COLUNA DE INPUT ---
        with col_input:
            
            st.markdown("### Adicione o Conteúdo para Audiolivro")
            
            uploaded_file = st.file_uploader("Carregar arquivo PDF (Opcional)", type=["pdf"], key="pdf_uploader_audio_tab")
            
            if uploaded_file is not None:
                if "last_uploaded" not in st.session_state or st.session_state["last_uploaded"] != uploaded_file.name:
                    with st.spinner("Extraindo texto do PDF..."):
                        extracted_text = extract_text_from_pdf(uploaded_file)
                        if extracted_text:
                            st.session_state["text_area_input"] = extracted_text
                            st.session_state["last_uploaded"] = uploaded_file.name
                            st.success("Texto do PDF carregado! Você pode editá-lo abaixo.")
            
            final_text = st.text_area(
                "Texto para Áudio:",
                height=300,
                placeholder="Digite seu texto ou carregue um PDF...",
                key="text_area_input" 
            )

            # --- GERAÇÃO DE ÁUDIO ---
            if st.button("🎙️ Gerar Áudio e Download", key="generate_audio_button"):
                if final_text and final_text.strip():
                    with st.spinner("Gerando áudio... Isso pode levar um tempo para textos longos."):
                        
                        text_chunks = chunk_text(final_text, MAX_CHARS_PER_CHUNK)
                        full_audio_bytes = BytesIO()

                        for chunk in text_chunks:
                            try:
                                tts = gTTS(text=chunk, lang=lang_code, slow=is_slow)
                                chunk_mp3 = BytesIO()
                                tts.write_to_fp(chunk_mp3)
                                chunk_mp3.seek(0)
                                full_audio_bytes.write(chunk_mp3.read())
                                time.sleep(SAFETY_DELAY) # Atraso para evitar bloqueio da API
                            except Exception as e:
                                st.error(f"Erro ao gerar áudio: {e}")
                                return
                        
                        full_audio_bytes.seek(0)
                        
                        st.success("Áudio gerado com sucesso!")
                        st.audio(full_audio_bytes.read(), format="audio/mp3")

                        st.download_button(
                            label="Baixar Arquivo MP3",
                            data=full_audio_bytes.read(),
                            file_name="audiolivro_acessivel.mp3",
                            mime="audio/mp3",
                            key="download_button"
                        )
                else:
                    st.warning("Por favor, insira algum texto ou carregue um PDF.")

            # --- MENSAGEM MOTIVACIONAL ADICIONADA AQUI ---
            st.markdown("---")
            st.markdown(
                """
                 **Lembrete:** Cada palavra lida ou ouvida é um passo à frente. 
                Sua dedicação é a chave para o sucesso! Continue firme. 🚀
                """
            )
            st.markdown("---")
            # ------------------------------------------------


    # --- ABA: ASSISTENTE DE TAREFAS E FOCO ---
    elif st.session_state['active_tab_key'] == TAB_TASKS:
        
        st.header("Assistente de Tarefas e Foco")
        st.markdown("Gerencie suas tarefas com prioridade e estimativa de tempo para melhorar o foco e a organização.")

        st.markdown("### Adicionar Nova Tarefa")
        
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        
        with col1:
            # CHAVE: 'new_task_description_input'
            st.text_input("Descrição da Tarefa:", key='new_task_description_input', placeholder="Iniciar pesquisa de projeto")
            
        with col2:
            st.selectbox("Prioridade:", ["Baixa", "Média", "Alta"], key='new_task_priority_select')
            
        with col3:
            st.number_input("Tempo Est. (min):", min_value=1, value=30, key='new_task_time_input')

        with col4:
            # Botão de adição de tarefa
            st.button("Adicionar Tarefa", on_click=add_task_callback, key='add_task_button')
            
        
        st.markdown("---")
        st.markdown("### 📋 Minhas Tarefas")

        if st.session_state['tasks']:
            
            # Ordenação das tarefas: prioridade > não concluída > tempo
            priority_order = {"Alta": 3, "Média": 2, "Baixa": 1}
            sorted_tasks = sorted(
                st.session_state['tasks'],
                key=lambda x: (x['completed'], -priority_order.get(x['priority'], 0), x['timestamp'])
            )
            
            for task in sorted_tasks:
                
                priority_class = f"priority-{task['priority'].lower()}"
                completed_class = " completed" if task['completed'] else ""
                
                # Exibe o conteúdo da tarefa
                st.markdown(f"""
                    <div class="task-item {priority_class}{completed_class}">
                        <span class="task-description">{task['description']}</span>
                        <span class="task-details">
                            Prioridade: {task['priority']} | 
                            Tempo Estimado: {task['estimated_time']} min
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Ações de tarefa
                with st.container():
                    col_b1, col_b2, col_b3 = st.columns([8, 1, 1]) 
                    
                    if not task['completed']:
                        with col_b2:
                            st.button("✔️ Concluir", key=f"complete_{task['id']}", on_click=complete_task, args=(task['id'],))
                        with col_b3:
                            st.button("🗑️ Excluir", key=f"delete_uncompleted_{task['id']}", on_click=delete_task, args=(task['id'],))
                    else:
                        with col_b3: # Colocado apenas no final para melhor alinhamento
                            st.button("🗑️ Excluir", key=f"delete_completed_{task['id']}", on_click=delete_task, args=(task['id'],))
                        
                
        else:
            st.info("Nenhuma tarefa adicionada ainda. Comece a planejar!")

if __name__ == '__main__':
    main()