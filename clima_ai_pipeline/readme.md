# 🌤️ Weather Pipeline CLI

Pipeline incremental de dados climáticos com análise por IA via terminal.

Coleta automaticamente dados históricos de temperatura de **qualquer cidade, estado ou país do mundo** usando a API gratuita [Open-Meteo](https://open-meteo.com/), armazena localmente em CSV e permite consultas em linguagem natural respondidas pelo `gpt-4o-mini`.

---

## ✨ Funcionalidades

- **Localização livre** — digite qualquer cidade, estado ou país; o sistema busca as coordenadas automaticamente via geocodificação
- **Extração incremental** — baixa apenas os dias ainda não registrados, sem reprocessar o histórico
- **CSV por localização** — cada local tem seu próprio arquivo de histórico, permitindo alternar entre cidades sem perder dados
- **Contexto inteligente** — a IA recebe automaticamente o recorte de dados mais adequado à pergunta feita (veja detalhes abaixo)
- **Comparação de períodos** — compare dois intervalos de datas diretamente, sem custo de tokens
- **Logging estruturado** — logs com timestamp para rastreabilidade completa
- **Tratamento robusto de erros** — falhas de rede, campos ausentes na API e entradas inválidas tratadas com mensagens claras

---

## 🧠 Contexto inteligente

A maior limitação de pipelines com IA é o limite de tokens. Este projeto resolve isso detectando automaticamente o escopo da pergunta e enviando o recorte ideal:

| Tipo de pergunta | Dados enviados à IA |
|---|---|
| *"Qual foi a temp. esta semana?"* | Dados diários — últimos 60 dias |
| *"Como foi o verão de 2022?"* | Dados diários — ano completo mencionado |
| *"Qual o ano mais quente da história?"* | Resumo mensal — todo o histórico |
| *"Tendência de temperatura nos últimos anos?"* | Resumo mensal — todo o histórico |
| 4 datas `YYYY-MM-DD` na pergunta | Comparação local — **sem chamar a IA** |

O resumo mensal agrega máxima, mínima, média, pico absoluto e vale absoluto por mês — permitindo responder perguntas históricas de décadas com apenas ~300 linhas de contexto.

---

## 🚀 Instalação

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/weather-pipeline.git
cd weather-pipeline
```

**2. Crie e ative um ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure a API Key da OpenAI**

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_aqui
```

> ⚠️ Nunca comite o arquivo `.env`. Ele já está no `.gitignore`.

---

## ▶️ Uso

```bash
python weather_pipeline.py
```

Ao iniciar, o sistema pede a localização desejada:

```
🌍 Weather Pipeline — Análise Climática com IA
────────────────────────────────────────────────
Digite uma cidade, estado ou país para análise.
Exemplos: Tokyo  |  Minas Gerais  |  Portugal

📍 Localização: Paris

🔍 Buscando 'Paris'...

📍 3 resultados encontrados. Escolha um:

  [1] Paris, Île-de-France, França (lat 48.85, lon 2.35)
  [2] Paris, Texas, Estados Unidos (lat 33.66, lon -95.55)
  [3] Paris, Kentucky, Estados Unidos (lat 38.20, lon -84.25)

Digite o número (1-3): 1

✅ Usando: Paris, Île-de-France, França
   Coordenadas : lat 48.8534, lon 2.3488
   Fuso horário: Europe/Paris
   Arquivo CSV : weather_Paris_Île-de-France_França.csv
```

Em seguida, os dados são carregados/atualizados e o sistema entra no loop de perguntas:

```
🧠 Sistema pronto! Digite sua pergunta ou 'sair' para encerrar.

Pergunta: Qual foi o mês mais frio de 2018?
Pergunta: Houve algum dia acima de 40°C em 2022?
Pergunta: Qual a tendência de temperatura nos últimos 10 anos?
Pergunta: 2023-06-01 2023-08-31 2024-06-01 2024-08-31
```

> Para **comparar dois períodos**, inclua exatamente 4 datas no formato `YYYY-MM-DD`. A comparação é feita localmente, sem chamar a IA e sem custo de tokens.

---

## 📁 Estrutura do Projeto

```
weather-pipeline/
├── weather_pipeline.py          # Script principal
├── weather_Paris_(...).csv      # Histórico por localização (gerado automaticamente)
├── requirements.txt
├── .env                         # Variáveis de ambiente (não versionado)
├── .gitignore
└── README.md
```

---

## 📦 Dependências

```
pandas
requests
openai
python-dotenv
```

Instale direto ou gere o `requirements.txt` com:

```bash
pip freeze > requirements.txt
```

---

## 🔒 Segurança

- A API Key da OpenAI é carregada **exclusivamente** via variável de ambiente (`.env`)
- O arquivo `.env` nunca deve ser versionado
- Sugestão de `.gitignore`:

```
.env
weather_*.csv
__pycache__/
venv/
```

---

## 🌐 APIs utilizadas

| API | Uso | Custo |
|---|---|---|
| [Open-Meteo Archive](https://open-meteo.com/en/docs/historical-weather-api) | Dados históricos de temperatura | Gratuita |
| [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) | Busca de coordenadas por nome | Gratuita |
| [OpenAI](https://platform.openai.com/) | Análise e respostas em linguagem natural | Pago (gpt-4o-mini) |

---

## 📄 Licença

MIT License. Veja [LICENSE](LICENSE) para detalhes.
