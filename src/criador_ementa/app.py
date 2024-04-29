from flask import Flask, jsonify, request, render_template, Response
from flask_cors import CORS
from tools.log_utils import log_route
from tools.log_utils import app_logger
import threading

app = Flask(__name__)
CORS(app)

cancel_requested = False

@app.route('/criador_ementa')
def index():
    return render_template('index.html')


@app.route('/tarefas', methods=['POST'])
def tarefas():
    from main import run
    global cancel_requested

    topico_aula = request.form['topico_aula']
    app_logger.info(f'Tópico da aula: {topico_aula}')
    publico_alvo = request.form['publico_alvo']
    app_logger.info(f'Público alvo: {publico_alvo}')

    if topico_aula and publico_alvo:
        app_logger.info('🚀 Iniciando a criação da ementa...')
        cancel_event = threading.Event()
        crew_ementa = None

        def run_thread():
            nonlocal crew_ementa
            app_logger.info('🔍 Iniciando a pesquisa...')
            result = run(topico_aula, publico_alvo, cancel_event)
            app_logger.info('✅ Ementa criada com sucesso!')
            if result is not None:
                app_logger.info('📝 Salvando a ementa...')
                crew_ementa = result
                app_logger.info('🖖 Finalizando a criação da ementa...')

        app_logger.info('🚀 Iniciando a thread...')
        thread = threading.Thread(target=run_thread)
        thread.start()

        while thread.is_alive():
            thread.join(1)
            if cancel_requested:
                app_logger.info('🚨 Cancelando tarefas...')
                cancel_event.set()
                cancel_requested = False
                app_logger.info('🚨 Tarefas canceladas!')
                return jsonify({'message': 'Tarefas canceladas'}), 200

        tasks_ementa = {}
        if crew_ementa:
            app_logger.info('📝 Extraindo tarefas...')
            output_ementa = crew_ementa.get('tasks_outputs', [])
            if output_ementa:
                app_logger.info('✅ Tarefas extraídas com sucesso!')
                for i in range(len(output_ementa)):
                    tasks_ementa[i] = output_ementa[i].exported_output
                    app_logger.info(f'✅ Tarefa {i} extraída com sucesso!')
            else:
                app_logger.error('❌ Erro ao extrair tarefas!')
                return jsonify({'error': 'Erro ao extrair tarefas'}), 400

        app_logger.info(f'➡️ Tarefas extraídas: {tasks_ementa}')
        app_logger.info('🖖 Finalizando a criação da ementa...')
        return jsonify({
            'tasks_ementa': tasks_ementa,
        })
    else:
        return jsonify({'error': 'Parâmetros inválidos'}), 400


@app.route('/cancelar', methods=['POST'])
def cancelar():
    global cancel_requested
    cancel_requested = True
    app_logger.info('🚨 Cancelamento solicitado!')
    return jsonify({'message': 'Cancelamento solicitado'}), 200

@app.route('/log')
def get_log():
    return log_route()

if __name__ == '__main__':
    app.run(port=8888, debug=True)