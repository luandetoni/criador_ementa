#!/usr/bin/env python
from crew import CrewCriadorEmenta
from colorama import Fore
from tools.log_utils import app_logger


def run(topic, publico_alvo, cancel_event=None):

    inputs = {
        'topic': topic,
        'publico_alvo': publico_alvo,
    }
    crew_ementa = CrewCriadorEmenta().crew().kickoff(inputs=inputs)
    
    tasks_ementa = {}
    if crew_ementa:
        output_ementa = crew_ementa.get('tasks_outputs', [])
        for i in range(len(output_ementa)):
            if cancel_event.is_set():
                break
            tasks_ementa[i] = output_ementa[i].exported_output

    return crew_ementa
        

if __name__ == '__main__':
    topic = input(Fore.GREEN + '## Digite o tópico da aula: ' + Fore.RESET)
    publico_alvo = input(Fore.GREEN + '## Digite o público alvo: ' + Fore.RESET)
    run(topic, publico_alvo)
