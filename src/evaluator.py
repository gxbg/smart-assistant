import json
import csv
import os
import matplotlib.pyplot as plt
from src.guardrails import GuardrailSystem
from src.chain import AssistantChain

class Evaluator:

    def __init__(self):
        self.guard = GuardrailSystem()
        self.chain = AssistantChain()
        self.resultados = []

    def carregar_json(self, caminho: str) -> list:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)

    def testar_legitimos(self) -> dict:
        print('\n=== Testando mensagens legitimas ===')
        dados = self.carregar_json('data/test_dataset.json')
        total = len(dados)
        corretos = 0
        json_validos = 0
        falsos_positivos = 0
        for item in dados:
            print(f"\n[{item['id']}/{total}] {item['mensagem'][:50]}...")
            seguro, motivo = self.guard.validar_input(item['mensagem'])
            if not seguro:
                falsos_positivos += 1
                print(f'  FALSO POSITIVO: {motivo}')
                self.resultados.append({
                    'id': item['id'],
                    'mensagem': item['mensagem'],
                    'tipo_esperado': item['tipo_esperado'],
                    'tipo_obtido': 'BLOQUEADO',
                    'correto': False,
                    'json_valido': False,
                    'falso_positivo': True
                })
                continue
            try:
                resultado = self.chain.processar_mensagem(item['mensagem'])
                tipo_obtido = resultado['classificacao']['tipo']
                correto = tipo_obtido == item['tipo_esperado']
                if correto:
                    corretos += 1
                json_validos += 1
                print(f'  Esperado: {item["tipo_esperado"]} | Obtido: {tipo_obtido} | {"OK" if correto else "ERROU"}')
                self.resultados.append({
                    'id': item['id'],
                    'mensagem': item['mensagem'],
                    'tipo_esperado': item['tipo_esperado'],
                    'tipo_obtido': tipo_obtido,
                    'correto': correto,
                    'json_valido': True,
                    'falso_positivo': False
                })
            except Exception as e:
                print(f'  ERRO: {e}')
                self.resultados.append({
                    'id': item['id'],
                    'mensagem': item['mensagem'],
                    'tipo_esperado': item['tipo_esperado'],
                    'tipo_obtido': 'ERRO',
                    'correto': False,
                    'json_valido': False,
                    'falso_positivo': False
                })
        return {
            'total': total,
            'corretos': corretos,
            'json_validos': json_validos,
            'falsos_positivos': falsos_positivos
        }

    def testar_ataques(self) -> dict:
        print('\n=== Testando ataques ===')
        dados = self.carregar_json('data/attack_dataset.json')
        total = len(dados)
        bloqueados = 0
        for item in dados:
            seguro, motivo = self.guard.validar_input(item['mensagem'])
            if not seguro:
                bloqueados += 1
                print(f'  [BLOQUEADO] {item["tipo_ataque"]}: {motivo}')
            else:
                print(f'  [PASSOU] {item["tipo_ataque"]} NAO foi bloqueado!')
        return {'total': total, 'bloqueados': bloqueados}

    def testar_consistencia(self) -> float:
        print('\n=== Testando consistencia ===')
        mensagem = 'Meu headset parou de funcionar!'
        tipos = []
        for i in range(3):
            resultado = self.chain.processar_mensagem(mensagem)
            tipo = resultado['classificacao']['tipo']
            tipos.append(tipo)
            print(f'  Tentativa {i+1}: {tipo}')
        consistente = len(set(tipos)) == 1
        print(f'  Consistencia: {"OK" if consistente else "INCONSISTENTE"}')
        return 1.0 if consistente else 0.0

    def salvar_csv(self):
        os.makedirs('output', exist_ok=True)
        with open('output/eval_results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'mensagem', 'tipo_esperado', 'tipo_obtido',
                'correto', 'json_valido', 'falso_positivo'
            ])
            writer.writeheader()
            writer.writerows(self.resultados)
        print('\nCSV salvo em output/eval_results.csv')

    def gerar_graficos(self, metricas: dict):
        os.makedirs('output/graficos', exist_ok=True)
        nomes = ['Acuracia', 'JSON Valido', 'Taxa Bloqueio', 'Falso Positivo', 'Consistencia']
        valores = [
            metricas['acuracia'],
            metricas['taxa_json'],
            metricas['taxa_bloqueio'],
            metricas['falso_positivo'],
            metricas['consistencia']
        ]
        cores = ['green' if v >= 0.7 else 'orange' if v >= 0.5 else 'red' for v in valores]
        plt.figure(figsize=(10, 6))
        bars = plt.bar(nomes, valores, color=cores)
        plt.title('GamerZone Smart Assistant - Metricas de Avaliacao')
        plt.ylabel('Taxa (0 a 1)')
        plt.ylim(0, 1.1)
        for bar, val in zip(bars, valores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                     f'{val:.0%}', ha='center', fontweight='bold')
        plt.tight_layout()
        plt.savefig('output/graficos/metricas.png')
        plt.close()
        print('Grafico salvo em output/graficos/metricas.png')

    def executar(self):
        print('INICIANDO AVALIACAO COMPLETA')
        legitimos = self.testar_legitimos()
        ataques = self.testar_ataques()
        consistencia = self.testar_consistencia()
        metricas = {
            'acuracia': legitimos['corretos'] / legitimos['total'],
            'taxa_json': legitimos['json_validos'] / legitimos['total'],
            'taxa_bloqueio': ataques['bloqueados'] / ataques['total'],
            'falso_positivo': 1 - (legitimos['falsos_positivos'] / legitimos['total']),
            'consistencia': consistencia
        }
        print('\n=== METRICAS FINAIS ===')
        print(f"Acuracia de classificacao: {metricas['acuracia']:.0%}")
        print(f"Taxa de JSON valido:       {metricas['taxa_json']:.0%}")
        print(f"Taxa de bloqueio:          {metricas['taxa_bloqueio']:.0%}")
        print(f"Taxa falso positivo:       {metricas['falso_positivo']:.0%}")
        print(f"Consistencia:              {metricas['consistencia']:.0%}")
        self.salvar_csv()
        self.gerar_graficos(metricas)
        print('\nAVALIACAO CONCLUIDA!')

if __name__ == '__main__':
    ev = Evaluator()
    ev.executar()
