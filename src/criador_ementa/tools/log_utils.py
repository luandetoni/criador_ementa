import logging
from io import StringIO
from flask import jsonify

# Configuração do logger da aplicação
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.INFO)

# Configuração do logger do Flask
flask_logger = logging.getLogger('werkzeug')

# Criação do StringIO para capturar os logs
log_capture_string = StringIO()

# Criação dos handlers para os loggers
app_handler = logging.StreamHandler(log_capture_string)
flask_handler = logging.StreamHandler(log_capture_string)

# Definição do formato dos logs
log_formatter = logging.Formatter('%(message)s')
app_handler.setFormatter(log_formatter)
flask_handler.setFormatter(log_formatter)

# Adição dos handlers aos loggers
app_logger.addHandler(app_handler)
flask_logger.addHandler(flask_handler)

def get_log_contents():
    log_contents = log_capture_string.getvalue()
    log_capture_string.seek(0)
    log_capture_string.truncate(0)
    return log_contents.strip()

def log_route():
    log_contents = get_log_contents()
    filtered_logs = []
    for log in log_contents.split('\n'):
        if '/log' not in log:
            filtered_logs.append(log)
    filtered_log_contents = '\n\n'.join(filtered_logs)
    last_log = log_contents.split('\n')[-1]
    if last_log and '/log' not in last_log:
        filtered_log_contents += '\n' + last_log
    return jsonify({'log': filtered_log_contents})



# def log_route():
#     log_contents = get_log_contents()
#     filtered_logs = []
#     for log in log_contents.split('\n'):
#         if ('main.py' in log or 'app.py' in log) and '/log' not in log:
#             filtered_logs.append(log)
#     filtered_log_contents = '\n'.join(filtered_logs)
#     last_log = log_contents.split('\n')[-1]
#     if last_log and '/log' not in last_log:
#         filtered_log_contents += '\n' + last_log
#     return jsonify({'log': filtered_log_contents})
