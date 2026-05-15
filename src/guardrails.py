import re

class GuardrailSystem:

    def __init__(self):
        self.max_chars = 500
        self.padroes_ataque = [
            r'ignore todas',
            r'ignore instrucoes',
            r'ignore as instru',
            r'ignore all previous',
            r'esqueca tudo',
            r'forget previous',
            r'you are now',
            r'voce agora e',
            r'act as if',
            r'jailbreak',
            r'dan mode',
            r'modo dan',
            r'sem restricoes',
            r'without restrictions',
            r'revele o',
            r'revele seu',
            r'reveal your',
            r'reveal prompt',
            r'mostre suas instrucoes',
            r'print your instructions',
            r'nova personalidade',
            r'finja que',
            r'pretend you',
            r'system prompt',
        ]
        self.chars_proibidos = ['<', '>', '{', '}']
        self.termos_sensiveis = [
            'system prompt',
            'instrucoes do sistema',
            'minhas instrucoes',
            'fui programado',
            'meu prompt',
            'ignore anteriores',
        ]

    def validar_input(self, texto: str) -> tuple:
        if not texto or not texto.strip():
            return False, 'Mensagem vazia'
        if len(texto) > self.max_chars:
            return False, f'Mensagem muito longa (max {self.max_chars} caracteres)'
        for char in self.chars_proibidos:
            if char in texto:
                return False, f'Caractere nao permitido: {char}'
        texto_lower = texto.lower()
        for padrao in self.padroes_ataque:
            if padrao in texto_lower:
                return False, f'Tentativa de ataque detectada: {padrao}'
        return True, 'OK'

    def validar_output(self, resposta: str) -> tuple:
        if not resposta or not resposta.strip():
            return False, 'Resposta vazia'
        if len(resposta) < 10:
            return False, 'Resposta muito curta'
        resposta_lower = resposta.lower()
        for termo in self.termos_sensiveis:
            if termo in resposta_lower:
                return False, f'Resposta vazou informacao sensivel: {termo}'
        return True, 'OK'

    def sanitizar_input(self, texto: str) -> str:
        texto = ' '.join(texto.split())
        return texto.strip()
