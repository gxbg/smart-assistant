import requests
import tiktoken
import os
from dotenv import load_dotenv

load_dotenv()


class LLMClient:

    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.max_input_length = int(os.getenv("MAX_INPUT_LENGTH", "500"))
        self.endpoint = f"{self.base_url}/api/chat"
        self.encoder = tiktoken.get_encoding("cl100k_base")
        print(f"[LLMClient] Modelo: {self.model}")
        print(f"[LLMClient] URL: {self.base_url}")

    def contar_tokens(self, texto: str) -> int:
        tokens = self.encoder.encode(texto)
        return len(tokens)

    def enviar_mensagem(self, system_prompt: str, user_message: str) -> str:
        mensagens = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        payload = {
            "model": self.model,
            "messages": mensagens,
            "stream": False
        }
        try:
            resposta = requests.post(self.endpoint, json=payload, timeout=60)
            resposta.raise_for_status()
            dados = resposta.json()
            return dados["message"]["content"]
        except requests.exceptions.ConnectionError:
            print("[ERRO] Ollama nao esta rodando.")
            return ""
        except requests.exceptions.Timeout:
            print("[ERRO] Timeout.")
            return ""
        except Exception as e:
            print(f"[ERRO] {e}")
            return ""

    def testar_conexao(self) -> bool:
        try:
            resposta = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if resposta.status_code == 200:
                print("[OK] Ollama esta rodando!")
                return True
            return False
        except:
            print("[ERRO] Ollama nao acessivel.")
            return False
