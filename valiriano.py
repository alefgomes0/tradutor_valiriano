import json
from validator_collection import checkers


class ValirianoInfo:
    texto: str
    dicionario: dict
    palavra: str
    tradução: str


class Valiriano:
    def __init__(self):
        with open("dicio_final.txt", "r", encoding="utf-8") as file:
            dicionario = json.load(file)
            dicionario = dict(sorted(dicionario.items()))

        pontuação = [
            ".",
            "...",
            ",",
            "!",
            "?",
            ":",
            "-",
            "_",
            "[",
            "]",
            "{",
            "}",
            "(",
            ")",
        ]
        texto = ""
        tradução = ""
        sinal = ""

        self.texto = texto
        self._dicionario = dicionario
        self.pontuação = pontuação
        self.sinal = sinal
        self.tradução = tradução
        

    def __str__(self):
        return f"Tradutor de Português(BR) para Alto Valiriano(High Valirian)"

    @property
    def dicionario(self):
        return self._dicionario

    def traduzir(self, texto=None):
        if not texto:
            texto = input("Texto: ").strip()
        self.verificar(texto)
        self.texto = texto.strip()
        self.decididor()

    def verificar(self, frase):
        is_valid = checkers.is_string(frase, minimum_length=2, maximum_length=500)
        if not is_valid:
            raise TypeError("Seu texto deve ter entre 2-500 caracteres.")
        return frase.strip()

    def decididor(self):
        for i, palavra in enumerate(self.texto.split()):
            if palavra.istitle() and i != 0 or palavra.isdigit():
                self.não_traduzir(palavra)
            elif not any(sinal in palavra for sinal in self.pontuação):
                self.traduzir_sem_pontuação(palavra.lower())
            else:
                self.encontrar_pontuação(palavra.lower())

    def não_traduzir(self, palavra):
        self.tradução += (palavra.title()) + " "
        return self.tradução

    def traduzir_sem_pontuação(self, verbete):
        if verbete in self._dicionario:
            verbete = self._dicionario[verbete]
        else:
            verbete = self.encontrar_parecido(verbete)
        self.tradução += (verbete + self.sinal) + " "
        self.sinal = ""
        return self.tradução
  
    def encontrar_parecido(self, item):
        diminuidor = 0
        while True:
            for s in self._dicionario:
                if s.count(item[0 : len(item) + diminuidor]):
                    return self._dicionario[s]
            diminuidor -= 1

    def encontrar_pontuação(self, termo):
        for substring in termo:
            for sinal in self.pontuação:
                if substring == sinal:
                    index = termo.find(substring)
                    palavra_cortada = termo[:index]
                    self.sinal = termo[index:]
                    return self.traduzir_sem_pontuação(palavra_cortada)

    def print(self):
        return print(f"{self.tradução}")


valiriano = Valiriano()
valiriano.traduzir()
valiriano.print()
