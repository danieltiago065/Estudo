import pandas as pd
import requests
import os
import re
import logging
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

DATE_FORMAT    = "%Y-%m-%d"
CONTEXTO_DIAS  = 60   # dias recentes usados no contexto detalhado
CAMPOS_ESPERADOS = ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"]


# ─────────────────────────────────────────────
# 0. CLIENTE OPENAI
# ─────────────────────────────────────────────

def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "❌ Variável de ambiente OPENAI_API_KEY não encontrada.\n"
            "Crie um arquivo .env com: OPENAI_API_KEY=sua_chave_aqui"
        )
    return OpenAI(api_key=api_key)


# ─────────────────────────────────────────────
# 1. GEOCODIFICAÇÃO
# ─────────────────────────────────────────────

def buscar_localizacao(query: str) -> list | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": query, "count": 5, "language": "pt", "format": "json"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("results")
    except requests.exceptions.RequestException as e:
        log.error("Erro na geocodificação: %s", e)
        return None


def formatar_nome_local(local: dict) -> str:
    partes = [local.get("name", "")]
    if local.get("admin1"):
        partes.append(local["admin1"])
    if local.get("country"):
        partes.append(local["country"])
    return ", ".join(p for p in partes if p)


def selecionar_localizacao(query: str) -> dict | None:
    print(f"\n🔍 Buscando '{query}'...")
    resultados = buscar_localizacao(query)

    if not resultados:
        print("❌ Nenhuma localização encontrada. Tente novamente.")
        return None

    if len(resultados) == 1:
        local = resultados[0]
        print(f"✅ Localização encontrada: {formatar_nome_local(local)}")
        return local

    print(f"\n📍 {len(resultados)} resultados encontrados. Escolha um:\n")
    for i, r in enumerate(resultados, 1):
        print(f"  [{i}] {formatar_nome_local(r)} (lat {r['latitude']:.2f}, lon {r['longitude']:.2f})")

    while True:
        escolha = input(f"\nDigite o número (1-{len(resultados)}): ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(resultados):
            return resultados[int(escolha) - 1]
        print("Opção inválida. Tente novamente.")


def obter_csv_para_local(local: dict) -> str:
    nome_safe = re.sub(r"[^\w\-]", "_", formatar_nome_local(local)).strip("_")
    return f"weather_{nome_safe}.csv"


# ─────────────────────────────────────────────
# 2. CARREGAR OU CRIAR BASE
# ─────────────────────────────────────────────

def carregar_dados(csv_file: str) -> pd.DataFrame:
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        log.info("CSV carregado: %d registros", len(df))
    else:
        df = pd.DataFrame(columns=["date", "temp_max", "temp_min", "temp_mean"])
        log.info("Novo dataset criado para esta localização")
    return df


# ─────────────────────────────────────────────
# 3. ÚLTIMA DATA
# ─────────────────────────────────────────────

def obter_ultima_data(df: pd.DataFrame) -> datetime:
    if df.empty:
        return datetime.strptime("2000-01-01", DATE_FORMAT)
    return df["date"].max() + timedelta(days=1)


# ─────────────────────────────────────────────
# 4. EXTRAÇÃO INCREMENTAL
# ─────────────────────────────────────────────

def extrair_dados(start_date: datetime, local: dict) -> pd.DataFrame:
    hoje = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    if start_date >= hoje:
        log.info("Dados já atualizados — nada novo a buscar.")
        return pd.DataFrame()

    start_str = start_date.strftime(DATE_FORMAT)
    hoje_str  = hoje.strftime(DATE_FORMAT)
    nome      = formatar_nome_local(local)

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={local['latitude']}&longitude={local['longitude']}"
        f"&start_date={start_str}&end_date={hoje_str}"
        "&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean"
        f"&timezone={local.get('timezone', 'auto')}"
    )

    log.info("Buscando dados de %s até %s para %s...", start_str, hoje_str, nome)

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        log.error("Timeout ao acessar a API Open-Meteo.")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        log.error("Erro na requisição: %s", e)
        return pd.DataFrame()

    daily = data.get("daily", {})
    campos_ausentes = [c for c in CAMPOS_ESPERADOS if c not in daily]
    if campos_ausentes:
        log.error("Campos ausentes na resposta da API: %s", campos_ausentes)
        return pd.DataFrame()

    novos = pd.DataFrame({
        "date":      daily["time"],
        "temp_max":  daily["temperature_2m_max"],
        "temp_min":  daily["temperature_2m_min"],
        "temp_mean": daily["temperature_2m_mean"],
    })
    novos["date"] = pd.to_datetime(novos["date"])

    log.info("%d novos registros recebidos.", len(novos))
    return novos


# ─────────────────────────────────────────────
# 5. TRANSFORM + LOAD
# ─────────────────────────────────────────────

def atualizar_base(df: pd.DataFrame, novos: pd.DataFrame, csv_file: str) -> pd.DataFrame:
    if novos.empty:
        return df

    df = pd.concat([df, novos], ignore_index=True)
    df = df.drop_duplicates(subset="date")
    df = df.sort_values("date").reset_index(drop=True)
    df.to_csv(csv_file, index=False)

    log.info("Base atualizada e salva em '%s' (%d registros totais).", csv_file, len(df))
    return df


# ─────────────────────────────────────────────
# 6. COMPARAÇÃO DE PERÍODOS
# ─────────────────────────────────────────────

def comparar_periodos(
    df: pd.DataFrame,
    inicio1: str, fim1: str,
    inicio2: str, fim2: str,
) -> str:
    try:
        dt_inicio1 = pd.to_datetime(inicio1)
        dt_fim1    = pd.to_datetime(fim1)
        dt_inicio2 = pd.to_datetime(inicio2)
        dt_fim2    = pd.to_datetime(fim2)
    except Exception:
        return "⚠️ Formato de data inválido. Use YYYY-MM-DD."

    p1 = df[(df["date"] >= dt_inicio1) & (df["date"] <= dt_fim1)]
    p2 = df[(df["date"] >= dt_inicio2) & (df["date"] <= dt_fim2)]

    if p1.empty or p2.empty:
        return "⚠️ Dados insuficientes para um ou ambos os períodos solicitados."

    media1    = p1["temp_mean"].mean()
    media2    = p2["temp_mean"].mean()
    diferenca = media2 - media1
    direcao   = "➡️ Mais quente no segundo período." if diferenca > 0 else "➡️ Mais frio no segundo período."

    return (
        f"\n📊 Comparação de Períodos\n"
        f"{'─' * 35}\n"
        f"Período 1 ({inicio1} → {fim1}): {media1:.2f}°C\n"
        f"Período 2 ({inicio2} → {fim2}): {media2:.2f}°C\n"
        f"Diferença: {diferenca:+.2f}°C\n"
        f"{direcao}\n"
    )


# ─────────────────────────────────────────────
# 7. AGREGAÇÃO INTELIGENTE DO CONTEXTO
# ─────────────────────────────────────────────

def extrair_anos_pergunta(pergunta: str) -> list[int]:
    """Extrai anos de 4 dígitos mencionados na pergunta (ex: 2020, 2023)."""
    return [int(a) for a in re.findall(r"\b(20\d{2}|19\d{2})\b", pergunta)]


def detectar_escopo(pergunta: str, df: pd.DataFrame) -> str:
    """
    Decide qual granularidade de dados enviar para a IA:

    - Pergunta menciona anos específicos     → dados diários daqueles anos
    - Pergunta parece histórica/comparativa  → resumo mensal de todo o histórico
    - Caso contrário                         → dados diários dos últimos 60 dias
    """
    pergunta_lower = pergunta.lower()

    # Palavras que indicam escopo histórico amplo
    palavras_historicas = [
        "ano", "anos", "anual", "histórico", "historia", "história",
        "decada", "década", "longo prazo", "tendencia", "tendência",
        "mais quente", "mais frio", "recorde", "média anual",
        "todo", "todos", "geral", "evolução", "comparar anos"
    ]

    anos_mencionados = extrair_anos_pergunta(pergunta)

    if anos_mencionados:
        return "anos_especificos"

    if any(p in pergunta_lower for p in palavras_historicas):
        return "historico"

    return "recente"


def montar_contexto(pergunta: str, df: pd.DataFrame) -> tuple[str, str]:
    """
    Retorna (contexto_texto, descricao) de acordo com o escopo detectado.
    """
    if df.empty:
        return "", "vazio"

    escopo = detectar_escopo(pergunta, df)

    # ── Escopo: anos específicos mencionados na pergunta ──
    if escopo == "anos_especificos":
        anos = extrair_anos_pergunta(pergunta)
        filtro = df["date"].dt.year.isin(anos)
        recorte = df[filtro]

        if recorte.empty:
            # fallback para histórico mensal
            escopo = "historico"
        else:
            # dados diários dos anos mencionados
            contexto = recorte[["date", "temp_max", "temp_min", "temp_mean"]].to_string(index=False)
            descricao = f"dados diários dos anos: {', '.join(map(str, anos))}"
            return contexto, descricao

    # ── Escopo: resumo mensal de todo o histórico ──
    if escopo == "historico":
        resumo = (
            df.assign(
                ano=df["date"].dt.year,
                mes=df["date"].dt.month
            )
            .groupby(["ano", "mes"])
            .agg(
                media_max=("temp_max",  "mean"),
                media_min=("temp_min",  "mean"),
                media_med=("temp_mean", "mean"),
                max_abs=  ("temp_max",  "max"),
                min_abs=  ("temp_min",  "min"),
            )
            .round(2)
            .reset_index()
        )
        contexto  = resumo.to_string(index=False)
        descricao = f"resumo mensal de {df['date'].dt.year.min()} a {df['date'].dt.year.max()}"
        return contexto, descricao

    # ── Escopo padrão: dados diários recentes ──
    recorte   = df.tail(CONTEXTO_DIAS)
    contexto  = recorte[["date", "temp_max", "temp_min", "temp_mean"]].to_string(index=False)
    descricao = f"dados diários dos últimos {CONTEXTO_DIAS} dias"
    return contexto, descricao


# ─────────────────────────────────────────────
# 8. EXTRAIR DATAS DA PERGUNTA
# ─────────────────────────────────────────────

def extrair_datas(pergunta: str) -> list[str] | None:
    datas = re.findall(r"\d{4}-\d{2}-\d{2}", pergunta)
    return datas if len(datas) == 4 else None


# ─────────────────────────────────────────────
# 9. RESPONDER COM IA
# ─────────────────────────────────────────────

def responder_com_ia(pergunta: str, df: pd.DataFrame, nome_local: str, client: OpenAI) -> str:
    # Comparação direta de períodos (sem IA)
    datas = extrair_datas(pergunta)
    if datas:
        return comparar_periodos(df, datas[0], datas[1], datas[2], datas[3])

    if df.empty:
        return "⚠️ Nenhum dado disponível para análise."

    contexto, descricao = montar_contexto(pergunta, df)

    prompt = (
        f"Você é um analista climático especializado.\n\n"
        f"Use SOMENTE os dados abaixo referentes a {nome_local}. "
        f"Não invente informações. Se não souber, diga claramente.\n\n"
        f"Contexto enviado: {descricao}\n\n"
        f"{contexto}\n\n"
        f"Pergunta: {pergunta}\n\n"
        f"Responda em português, de forma clara e objetiva."
    )

    log.info("Contexto enviado à IA: %s", descricao)

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.3,
        )
        return resposta.choices[0].message.content
    except Exception as e:
        log.error("Erro na chamada à API OpenAI: %s", e)
        return f"❌ Erro ao consultar a IA: {e}"


# ─────────────────────────────────────────────
# 10. EXECUÇÃO PRINCIPAL
# ─────────────────────────────────────────────

def main():
    log.info("Iniciando pipeline incremental de dados climáticos...")

    try:
        client = get_openai_client()
    except EnvironmentError as e:
        print(e)
        return

    # ── Seleção de localização ──
    print("\n🌍 Weather Pipeline — Análise Climática com IA")
    print("─" * 48)
    print("Digite uma cidade, estado ou país para análise.")
    print("Exemplos: Tokyo  |  Minas Gerais  |  Portugal\n")

    local = None
    while local is None:
        query = input("📍 Localização: ").strip()
        if not query:
            print("Por favor, digite uma localização.")
            continue
        local = selecionar_localizacao(query)

    nome_local = formatar_nome_local(local)
    csv_file   = obter_csv_para_local(local)

    print(f"\n✅ Usando: {nome_local}")
    print(f"   Coordenadas : lat {local['latitude']:.4f}, lon {local['longitude']:.4f}")
    print(f"   Fuso horário: {local.get('timezone', 'auto')}")
    print(f"   Arquivo CSV : {csv_file}\n")

    # ── Pipeline de dados ──
    df          = carregar_dados(csv_file)
    ultima_data = obter_ultima_data(df)
    novos_dados = extrair_dados(ultima_data, local)
    df          = atualizar_base(df, novos_dados, csv_file)

    print("\n🧠 Sistema pronto! Digite sua pergunta ou 'sair' para encerrar.")
    print("💡 Dicas:")
    print("   • Perguntas recentes  → dados diários dos últimos 60 dias")
    print("   • Mencione um ano     → dados diários daquele ano completo")
    print("   • Perguntas históricas → resumo mensal de todo o histórico")
    print("   • 4 datas YYYY-MM-DD  → comparação de períodos (sem IA)\n")

    try:
        while True:
            pergunta = input("Pergunta: ").strip()

            if not pergunta:
                continue

            if pergunta.lower() in ("sair", "exit", "quit"):
                print("Encerrando. Até logo!")
                break

            resposta = responder_com_ia(pergunta, df, nome_local, client)
            print(f"\n📊 Resposta:\n{resposta}\n")

    except KeyboardInterrupt:
        print("\n\nEncerrado pelo usuário (Ctrl+C). Até logo!")


if __name__ == "__main__":
    main()