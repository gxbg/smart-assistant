import json
import sys
from src.guardrails import GuardrailSystem
from src.chain import AssistantChain

def exibir_resultado(resultado: dict):
    print('\n' + '='*50)
    print('RESULTADO DO PIPELINE')
    print('='*50)
    c = resultado['classificacao']
    print(f"Tipo: {c['tipo']} | Urgencia: {c['urgencia']}")
    print(f"Tema: {c['tema']}")
    p = resultado['processamento']
    print(f"Sentimento: {p['sentimento']} | Prioridade: {p['prioridade']}")
    r = resultado['resposta_final']
    print(f"\nRESPOSTA DA MAYA:")
    print(f"{r['resposta']}")
    print(f"\nAcao sugerida: {r['acao_sugerida']}")
    if r.get('tempo_resolucao'):
        print(f"Tempo estimado: {r['tempo_resolucao']}")
    print(f"Confianca: {r['confianca']}")
    print('='*50)

def modo_interativo():
    print('\n' + '='*50)
    print('GAMERZONE SMART ASSISTANT')
    print('Assistente: Maya | Modelo: llama3.2')
    print('Digite sair para encerrar')
    print('='*50)
    guard = GuardrailSystem()
    chain = AssistantChain()
    while True:
        print()
        mensagem = input('Voce: ').strip()
        if mensagem.lower() in ['sair', 'exit', 'quit']:
            print('Encerrando... Obrigado!')
            break
        seguro, motivo = guard.validar_input(mensagem)
        if not seguro:
            print(f'[BLOQUEADO] {motivo}')
            continue
        mensagem = guard.sanitizar_input(mensagem)
        resultado = chain.processar_mensagem(mensagem)
        resposta_texto = resultado['resposta_final']['resposta']
        seguro_out, motivo_out = guard.validar_output(resposta_texto)
        if not seguro_out:
            print(f'[OUTPUT BLOQUEADO] {motivo_out}')
            print('Maya: Desculpe, nao consigo processar essa solicitacao.')
            continue
        exibir_resultado(resultado)

def modo_avaliacao():
    print('\n[MODO AVALIACAO]')
    print('Execute: py src/evaluator.py')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'avaliar':
        modo_avaliacao()
    else:
        modo_interativo()
