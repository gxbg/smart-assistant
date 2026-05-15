
import json
import re
from src.llm_client import LLMClient
from src.prompts import prompt_classificar, prompt_processar, prompt_responder
from src.schemas import ClassificacaoSchema, ProcessamentoSchema, RespostaSchema


def extrair_json(texto: str) -> dict:
    """
    Extrai JSON de uma resposta do LLM.
    O LLM as vezes retorna texto antes ou depois do JSON.
    Esta funcao encontra e extrai apenas o JSON.
    """
    # Tenta fazer parse direto primeiro
    try:
        return json.loads(texto)
    except:
        pass

    # Tenta encontrar JSON entre chaves
    try:
        inicio = texto.find("{")
        fim = texto.rfind("}") + 1
        if inicio != -1 and fim > inicio:
            json_str = texto[inicio:fim]
            return json.loads(json_str)
    except:
        pass

    # Tenta remover markdown (```json ... ```)
    try:
        limpo = re.sub(r"```json|```", "", texto).strip()
        return json.loads(limpo)
    except:
        pass

    return {}


class AssistantChain:
    """
    Pipeline multi-etapa do assistente GamerZone.
    Conecta LLM + Prompts + Schemas em 3 etapas sequenciais.
    """

    def __init__(self):
        self.cliente = LLMClient()
        self.system_prompt = self._carregar_system_prompt()

    def _carregar_system_prompt(self) -> str:
        """Carrega o system prompt defensivo do arquivo txt."""
        try:
            with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
                return f.read()
        except:
            return "Voce e Maya, assistente da GamerZone Store."

    def etapa1_classificar(self, mensagem: str) -> ClassificacaoSchema:
        """
        Etapa 1 — Classifica a mensagem do cliente.
        Retorna: tipo, urgencia, tema, resumo
        """
        print("\n[Etapa 1] Classificando mensagem...")

        prompt = prompt_classificar(mensagem)

        # Tenta ate 3 vezes (retry)
        for tentativa in range(3):
            resposta = self.cliente.enviar_mensagem(
                system_prompt=self.system_prompt,
                user_message=prompt
            )

            dados = extrair_json(resposta)

            if dados:
                try:
                    schema = ClassificacaoSchema(**dados)
                    print(f"[Etapa 1] OK! tipo={schema.tipo}, urgencia={schema.urgencia}")
                    return schema
                except Exception as e:
                    print(f"[Etapa 1] Tentativa {tentativa+1} falhou: {e}")

        # Fallback se todas tentativas falharem
        print("[Etapa 1] Usando fallback!")
        return ClassificacaoSchema(
            tipo="duvida",
            urgencia="media",
            tema="nao identificado",
            resumo=mensagem[:100]
        )

    def etapa2_processar(self, mensagem: str, classificacao: ClassificacaoSchema) -> ProcessamentoSchema:
        """
        Etapa 2 — Processa conforme o tipo detectado.
        MUDA comportamento conforme resultado da Etapa 1!
        """
        print(f"\n[Etapa 2] Processando como: {classificacao.tipo}...")

        prompt = prompt_processar(mensagem, classificacao.model_dump())

        for tentativa in range(3):
            resposta = self.cliente.enviar_mensagem(
                system_prompt=self.system_prompt,
                user_message=prompt
            )

            dados = extrair_json(resposta)

            if dados:
                try:
                    # Garante que dados_extraidos e um dict
                    if isinstance(dados.get("dados_extraidos"), str):
                        dados["dados_extraidos"] = {"info": dados["dados_extraidos"]}

                    schema = ProcessamentoSchema(**dados)
                    print(f"[Etapa 2] OK! sentimento={schema.sentimento}")
                    return schema
                except Exception as e:
                    print(f"[Etapa 2] Tentativa {tentativa+1} falhou: {e}")

        # Fallback
        print("[Etapa 2] Usando fallback!")
        return ProcessamentoSchema(
            tipo_detectado=classificacao.tipo,
            dados_extraidos={"mensagem": mensagem},
            analise="Nao foi possivel processar completamente",
            sentimento="neutro",
            prioridade=classificacao.urgencia
        )

    def etapa3_responder(self, mensagem: str, classificacao: ClassificacaoSchema, processamento: ProcessamentoSchema) -> RespostaSchema:
        """
        Etapa 3 — Gera a resposta final formatada para o cliente.
        """
        print("\n[Etapa 3] Gerando resposta final...")

        prompt = prompt_responder(
            mensagem,
            classificacao.model_dump(),
            processamento.model_dump()
        )

        for tentativa in range(3):
            resposta = self.cliente.enviar_mensagem(
                system_prompt=self.system_prompt,
                user_message=prompt
            )

            dados = extrair_json(resposta)

            if dados:
                try:
                    schema = RespostaSchema(**dados)
                    print(f"[Etapa 3] OK! confianca={schema.confianca}")
                    return schema
                except Exception as e:
                    print(f"[Etapa 3] Tentativa {tentativa+1} falhou: {e}")

        # Fallback
        print("[Etapa 3] Usando fallback!")
        return RespostaSchema(
            resposta="Obrigado pelo contato! Nossa equipe ira analisar sua solicitacao.",
            confianca="baixa",
            acao_sugerida="Encaminhar para atendimento humano",
            tempo_resolucao="1 dia util"
        )

    def processar_mensagem(self, mensagem: str) -> dict:
        """
        Executa o pipeline completo das 3 etapas.
        Este e o metodo principal que sera chamado pelo main.py
        """
        print("\n" + "="*50)
        print(f"MENSAGEM: {mensagem}")
        print("="*50)

        # Etapa 1
        classificacao = self.etapa1_classificar(mensagem)

        # Etapa 2 — comportamento muda conforme tipo!
        processamento = self.etapa2_processar(mensagem, classificacao)

        # Etapa 3
        resposta = self.etapa3_responder(mensagem, classificacao, processamento)

        # Resultado final
        resultado = {
            "mensagem_original": mensagem,
            "classificacao": classificacao.model_dump(),
            "processamento": processamento.model_dump(),
            "resposta_final": resposta.model_dump()
        }

        print("\n[Pipeline] Concluido!")
        return resultado
