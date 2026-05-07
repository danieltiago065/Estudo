import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

fake = Faker("pt_BR")
random.seed(42)

# =============================
# DADOS BASE - COIL COATING
# =============================
linhas = [
    # Seção de Entrada
    "Desbobinador 1",
    "Desbobinador 2",
    "Suporte de Passagem",
    "Grampeadora (Joiner)",
    "Pisador de Chapa",
    "Freio de Chpa",
    "Pré-Cleaner",
    "Rolos Tensionadores Entrada",
    "Acumulador de Entrada",
    "Guia-Alinhador 1",

    # Seção de Tratamento Químico
    "Tanque de Desengraxe 1",
    "Tanque de Lavagem 1",
    "Tanque de Lavagem 2",
    "Vaso Comunicante Desengraxe 1",
    "Vaso Comunicante Lavagem 2",
    "Tanque de Desengraxe 2 (Reserva)",
    "Tanque de Lavagem 3 (Reserva)",
    "Bridle 1",
    "Facas de Ar para Secagem",
    "Suporte de Rolos Defletores",
    "Pintadora Química",
    "Mesa de Motores Pintadora Química",
    "Estufa Tratamento Químico",
    "Guia-Alinhador 2",
    "Rolo de Curva",

    # Seção de Pintura
    "Suporte de Rolos Defletores Primer",
    "Pintadora Primer",
    "Mesa de Motores Primer",
    "Estufa Primer",
    "Base de Rolos Cromados Primer",
    "Guia-Alinhador 3",
    "Bridle 2",
    "Suporte de Rolos Defletores Acabamento",
    "Pintadora Acabamento",
    "Estufa Acabamento",
    "Base de Rolos Cromados Acabamento",
    "Guia-Alinhador 4",

    # Seção de Aplicação de Filme
    "Desbobinador de Filme",
    "Aplicador de Filme",
    "Bridle 3",

    # Seção de Saída
    "Acumulador de Saída",
    "Rolos Tensionadores Saída",
    "Tesoura Guilhotina",
    "Sensor Guia de Alinhamento",
    "Rebobinador de Chapa"
]

setores = [
    "Preparação de Superfície",
    "Pintura",
    "Cura Térmica",
    "Utilidades",
    "Movimentação",
    "Qualidade"
]

tipos_falha = [
    "Falha elétrica",
    "Falha mecânica",
    "Parada hidráulica",
    "Sensor defeituoso",
    "Superaquecimento",
    "Falha pneumática",
    "Problema de alinhamento",
    "Contaminação de processo"
]

tipos_manutencao = [
    "Preventiva",
    "Corretiva",
    "Preditiva",
    "Inspeção"
]

tecnicos = [
    "Carlos Silva",
    "Mariana Costa",
    "João Pereira",
    "Fernanda Rocha",
    "Lucas Martins"
]


def random_date(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))


# =============================
# GERAÇÃO DE DADOS
# =============================
def gerar_maquinas():
    maquinas = []

    mapa_setores = {
        # Entrada
        "Desbobinador 1": "Seção de Entrada",
        "Desbobinador 2": "Seção de Entrada",
        "Suporte de Passagem": "Seção de Entrada",
        "Grampeadora (Joiner)": "Seção de Entrada",
        "Pisador de Chapa": "Seção de Entrada",
        "Freio de Chpa": "Seção de Entrada",
        "Pré-Cleaner": "Seção de Entrada",
        "Rolos Tensionadores Entrada": "Seção de Entrada",
        "Acumulador de Entrada": "Seção de Entrada",
        "Guia-Alinhador 1": "Seção de Entrada",

        # Tratamento Químico
        "Tanque de Desengraxe 1": "Seção de Tratamento Químico",
        "Tanque de Lavagem 1": "Seção de Tratamento Químico",
        "Tanque de Lavagem 2": "Seção de Tratamento Químico",
        "Vaso Comunicante Desengraxe 1": "Seção de Tratamento Químico",
        "Vaso Comunicante Lavagem 2": "Seção de Tratamento Químico",
        "Tanque de Desengraxe 2 (Reserva)": "Seção de Tratamento Químico",
        "Tanque de Lavagem 3 (Reserva)": "Seção de Tratamento Químico",
        "Bridle 1": "Seção de Tratamento Químico",
        "Facas de Ar para Secagem": "Seção de Tratamento Químico",
        "Suporte de Rolos Defletores": "Seção de Tratamento Químico",
        "Pintadora Química": "Seção de Tratamento Químico",
        "Mesa de Motores Pintadora Química": "Seção de Tratamento Químico",
        "Estufa Tratamento Químico": "Seção de Tratamento Químico",
        "Guia-Alinhador 2": "Seção de Tratamento Químico",
        "Rolo de Curva": "Seção de Tratamento Químico",

        # Pintura
        "Suporte de Rolos Defletores Primer": "Seção de Pintura",
        "Pintadora Primer": "Seção de Pintura",
        "Mesa de Motores Primer": "Seção de Pintura",
        "Estufa Primer": "Seção de Pintura",
        "Base de Rolos Cromados Primer": "Seção de Pintura",
        "Guia-Alinhador 3": "Seção de Pintura",
        "Bridle 2": "Seção de Pintura",
        "Suporte de Rolos Defletores Acabamento": "Seção de Pintura",
        "Pintadora Acabamento": "Seção de Pintura",
        "Estufa Acabamento": "Seção de Pintura",
        "Base de Rolos Cromados Acabamento": "Seção de Pintura",
        "Guia-Alinhador 4": "Seção de Pintura",

        # Filme
        "Desbobinador de Filme": "Seção de Aplicação de Filme",
        "Aplicador de Filme": "Seção de Aplicação de Filme",
        "Bridle 3": "Seção de Aplicação de Filme",

        # Saída
        "Acumulador de Saída": "Seção de Saída",
        "Rolos Tensionadores Saída": "Seção de Saída",
        "Tesoura Guilhotina": "Seção de Saída",
        "Sensor Guia de Alinhamento": "Seção de Saída",
        "Rebobinador de Chapa": "Seção de Saída"
    }

    for i, nome in enumerate(linhas, start=1):
        maquinas.append((
            i,
            nome,
            mapa_setores.get(nome, "Não Classificado"),
            nome,
            random_date(datetime(2015, 1, 1), datetime(2022, 12, 31)).date()
        ))

    return maquinas


def gerar_falhas(qtd=120):
    falhas = []
    for i in range(1, qtd + 1):
        falhas.append((
            i,
            random.randint(1, len(linhas)),
            random_date(datetime(2024, 1, 1), datetime(2025, 12, 31)).date(),
            random.choice(tipos_falha),
            round(random.uniform(1, 18), 2),
            round(random.uniform(500, 15000), 2)
        ))
    return falhas


def gerar_producao(qtd=250):
    producao = []
    for i in range(1, qtd + 1):
        producao.append((
            i,
            random.randint(1, len(linhas)),
            random_date(datetime(2024, 1, 1), datetime(2025, 12, 31)).date(),
            round(random.uniform(8, 24), 2),
            random.randint(20, 300)
        ))
    return producao


def gerar_manutencoes(qtd=100):
    manutencoes = []
    for i in range(1, qtd + 1):
        manutencoes.append((
            i,
            random.randint(1, len(linhas)),
            random_date(datetime(2024, 1, 1), datetime(2025, 12, 31)).date(),
            random.choice(tipos_manutencao),
            round(random.uniform(800, 20000), 2),
            random.choice(tecnicos)
        ))
    return manutencoes


# =============================
# EXPORTAÇÃO PARA CSV
# =============================
def exportar_csv():
    print("Gerando arquivos CSV...")

    df_maquinas = pd.DataFrame(
        gerar_maquinas(),
        columns=[
            "id_maquina",
            "nome_maquina",
            "setor",
            "tipo",
            "data_instalacao"
        ]
    )

    df_falhas = pd.DataFrame(
        gerar_falhas(),
        columns=[
            "id_falha",
            "id_maquina",
            "data_falha",
            "tipo_falha",
            "tempo_parado_horas",
            "custo_manutencao"
        ]
    )

    df_producao = pd.DataFrame(
        gerar_producao(),
        columns=[
            "id_producao",
            "id_maquina",
            "data",
            "horas_operacao",
            "unidades_produzidas"
        ]
    )

    df_manutencoes = pd.DataFrame(
        gerar_manutencoes(),
        columns=[
            "id_manutencao",
            "id_maquina",
            "data",
            "tipo_manutencao",
            "custo",
            "tecnico"
        ]
    )

    df_maquinas.to_csv("maquinas.csv", index=False, encoding="utf-8-sig")
    df_falhas.to_csv("falhas.csv", index=False, encoding="utf-8-sig")
    df_producao.to_csv("producao.csv", index=False, encoding="utf-8-sig")
    df_manutencoes.to_csv("manutencoes.csv", index=False, encoding="utf-8-sig")

    print("Arquivos CSV gerados com sucesso.")
    print("Arquivos criados:")
    print("- maquinas.csv")
    print("- falhas.csv")
    print("- producao.csv")
    print("- manutencoes.csv")


if __name__ == "__main__":
    exportar_csv()
