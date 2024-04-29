import streamlit as st
from main import run
import threading
import time
import os

def main():
    st.set_page_config(page_title="Task Results Interface", layout="wide")

    # Custom CSS
    st.markdown("""
        <style>
            body {
                font-family: 'Hack', monospace;
                background-color: #121212;
                color: #fff;
            }

            .sidebar {
                background-color: #1e1e1e;
                padding: 3rem;
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
            }

            .main-content {
                padding: 2rem;
            }

            h2 {
                font-size: 1.75rem;
                font-weight: 700;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #4CAF50;
            }

            .form-label {
                font-size: 0.80rem;
                font-weight: 300;
                margin-bottom: 0.5rem;
            }

            .form-input,
            .form-button {
                padding: 0.75rem;
                border-radius: 0.5rem;
                border: none;
                width: 100%;
                box-sizing: border-box;
                margin-bottom: 1rem;
            }

            .form-input {
                background-color: #2c2c2c;
                color: #fff;
                font-size: 0.75rem;
            }

            .form-button {
                background-color: #4CAF50;
                color: #fff;
                cursor: pointer;
                transition: background-color 0.3s ease;
                margin-top: 0.5rem;
            }

            .form-button:hover {
                background-color: #81C784;
            }

            .form-button.cancel-button {
                background-color: #f44336;
            }

            .form-button.cancel-button:hover {
                background-color: #e57373;
            }

            .form-button:disabled {
                background-color: #81C784;
                cursor: not-allowed;
            }

            .form-button.cancel-button:disabled {
                background-color: #e57373;
            }

            .result-container {
                background-color: #2c2c2c;
                border-radius: 0 0 0.5rem 0.5rem;
                padding: 1rem;
                height: calc(97vh - 4rem);
                width: auto;
            }

            .editable-textarea {
                font-size: 0.90rem;
                background-color: transparent;
                color: #fff;
                width: 100%;
                height: 100%;
                border: none;
                padding: 0.5rem;
                border-radius: 0.25rem;
                resize: none;
                overflow: auto;
            }

            .application-log {
                font-size: 0.70rem;
                background-color: #2c2c2c;
                color: #fff;
                padding: 1rem;
                border-radius: 0.5rem;
                height: 100%;
                overflow-y: scroll;
                margin-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("<h2>🔐 Chave de API - Claude AI</h2>", unsafe_allow_html=True)
        api_key = st.text_input("API Key", key="api_key_input", type="password")
        if api_key:
            os.environ['CLAUDE_API_KEY'] = api_key
            st.markdown("<h2>🚣 Crew Inputs - Criador de Aulas</h2>", unsafe_allow_html=True)
            topico_aula = st.text_input("Tópico da aula", placeholder="Digite qual o tópico da aula")
            publico_alvo = st.text_input("Público-alvo", placeholder="Digite qual é o público alvo")
            kickoff_button = st.button("Kickoff Crew", type="primary")
            cancel_button = st.empty()  # Cria um espaço reservado para o botão Cancel
        else:
            st.warning("Por favor, defina a API Key")

    # Main content
    st.markdown("<h2>📝 Output Tasks</h2>", unsafe_allow_html=True)
    task_results = st.empty()
    if not task_results:
        with st.spinner("Loading..."):
            pass


    cancel_event = threading.Event()
    crew_ementa = None

    def run_thread():
        nonlocal crew_ementa
        result = run(topico_aula, publico_alvo, cancel_event)
        if result is not None:
            crew_ementa = result

    if 'kickoff_button' in locals() and kickoff_button:
        thread = threading.Thread(target=run_thread)
        thread.start()
        # kickoff_button.button("Kickoff Crew", key="kickoff_button", disabled=True)
        cancel_button.button("Cancel", key="cancel_button", on_click=cancel_event.set)
        while thread.is_alive():
            thread.join(1)
            if cancel_event.is_set():
                cancel_event.set()
                cancel_event.clear()
                st.warning('Tarefas canceladas')
                break
        
        if crew_ementa:
            output_ementa = crew_ementa.get('tasks_outputs', [])
            if output_ementa:
                tasks_ementa = ""
                for i in range(len(output_ementa)):
                    tasks_ementa += f"# TAREFA {i+1}:\n\n"
                    tasks_ementa += output_ementa[i].exported_output + "\n\n"
                task_results.text_area("", value=tasks_ementa, placeholder="🤖 Jovem Padawan, preencher o formulário ao lado você deve. Com cada campo preenchido, mais próximo da sabedoria Jedi você estará. Grogu também começou seu treinamento com pequenos passos!", height=500, key="task_results")
            else:
                st.error('Erro ao extrair tarefas')

if __name__ == "__main__":
    main()