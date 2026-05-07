import random
from datetime import datetime
import pandas as pd

# =============================
# DADOS BASE
# =============================
modos_falha = [
    "Superaquecimento",
    "Falha elétrica",
    "Desalinhamento",
    "Falha pneumática",
    "Sensor defeituoso",
    "Contaminação de processo"
]

causas_falha = [
    "Desgaste de componente",
    "Falta de lubrificação",
    "Falha de sensor",
    "Erro operacional",
    "Variação de processo",
    "Sobrecarga térmica"
]

efeitos_falha = [
    "Parada de linha",
    "Perda de qualidade",
    "Retrabalho",
    "Scrap de material",
    "Redução de produtividade",
    "Aumento de custo operacional"
]

acoes_recomendadas = [
    "Inspeção preventiva",
    "Revisão do sistema",
    "Troca programada de componente",
    "Calibração de sensores",
    "Padronização operacional",
    "Monitoramento preditivo"
]

# =============================
# REGRAS
# =============================
def calcular_severidade(custo):
    if custo <= 2000:
        return 3
    elif custo <= 5000:
        return 5
    elif custo <= 10000:
        return 7
    return 9


def calcular_ocorrencia():
    return random.choice([2, 4, 7, 9])


def calcular_deteccao():
    return random.choice([2, 5, 8])


# =============================
# GERAR DADOS
# =============================
def gerar_fmea(qtd=80, total_maquinas=46):

    dados = []

    for i in range(1, qtd + 1):

        id_maquina = random.randint(1, total_maquinas)
        custo = round(random.uniform(500, 15000), 2)

        severidade = calcular_severidade(custo)
        ocorrencia = calcular_ocorrencia()
        deteccao = calcular_deteccao()
        rpn = severidade * ocorrencia * deteccao

        linha = {
            'id_fmea': i,
            'id_maquina': id_maquina,
            'modo_falha': random.choice(modos_falha),
            'causa_falha': random.choice(causas_falha),
            'efeito_falha': random.choice(efeitos_falha),
            'severidade': severidade,
            'ocorrencia': ocorrencia,
            'deteccao': deteccao,
            'rpn': rpn,
            'acao_recomendada': random.choice(acoes_recomendadas),
            'data_analise': datetime.now().date()
        }

        dados.append(linha)

    return pd.DataFrame(dados)


# =============================
# EXECUÇÃO
# =============================
if __name__ == "__main__":

    fmea = gerar_fmea()

    fmea.to_csv('fmea.csv', index=False)

    print("Arquivo CSV gerado com sucesso!")