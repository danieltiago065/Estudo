import pandas as pd
#importando dados 
falhas = pd.read_csv('../Dados/falhas.csv')
maquinas = pd.read_csv('../Dados/maquinas.csv')
producao = pd.read_csv('../Dados/producao.csv')
manutencao = pd.read_csv('../Dados/manutencao.csv')
fmea = pd.read_csv('../Dados/fmea.csv')

#verificando as primeiras linhas de cada tabela
# print(falhas.head())
# print(maquinas.head())
# print(producao.head())
# print(manutencao.head())
# print(fmea.head())
#verificando a quantidade de linhas e colunas de cada tabela
# print(falhas.shape)
# print(maquinas.shape)
# print(producao.shape)
# print(manutencao.shape)
# print(fmea.shape)

#formatando as colunas para minusculo

falhas.columns = falhas.columns.str.strip().str.lower()
maquinas.columns = maquinas.columns.str.strip().str.lower()
producao.columns = producao.columns.str.strip().str.lower()
manutencao.columns = manutencao.columns.str.strip().str.lower()
fmea.columns = fmea.columns.str.strip().str.lower()

#tratar valores nulos

falhas = falhas.dropna()
maquinas = maquinas.dropna()
producao = producao.dropna()
manutencao = manutencao.dropna()
fmea = fmea.dropna()

#verificando os tipos de dados de cada tabela

print(falhas.info())
print(maquinas.info())
print(producao.info())
print(manutencao.info())
print(fmea.info())

#convertendo a coluna data para o formato datetime
falhas['data_falha'] = pd.to_datetime(falhas['data_falha'])
manutencao['data'] = pd.to_datetime(manutencao['data'])
maquinas['data_instalacao'] = pd.to_datetime(maquinas['data_instalacao'])
fmea['data_analise'] = pd.to_datetime(fmea['data_analise'])


#convertendo a coluna tempo para o formato timedelta
falhas['tempo_parado_horas'] = pd.to_timedelta(falhas['tempo_parado_horas'])
producao['horas_operacao'] = pd.to_timedelta(producao['horas_operacao'])



#convertendo a coluna severidade para o formato inteiro
fmea['severidade'] = fmea['severidade'].astype(int)


#convertendo a coluna ocorrencia para o formato inteiro
fmea['ocorrencia'] = fmea['ocorrencia'].astype(int)


#convertendo a coluna detecção para o formato inteiro
fmea['deteccao'] = fmea['deteccao'].astype(int)


#convertendo a coluna rpn para o formato inteiro
fmea['rpn'] = fmea['rpn'].astype(int)


#convertendo a coluna id_maquina para o formato inteiro
fmea['id_maquina'] = fmea['id_maquina'].astype(int)
maquinas['id_maquina'] = maquinas['id_maquina'].astype(int)
manutencao['id_maquina'] = manutencao['id_maquina'].astype(int)
falhas['id_maquina'] = falhas['id_maquina'].astype(int)
producao['id_maquina'] = producao['id_maquina'].astype(int)

print(falhas.columns)
print(maquinas.columns)
print(producao.columns)
print(manutencao.columns)
print(fmea.columns) 


#verificando os tipos de dados de cada tabela pós tratamento

print(falhas.info())
print(maquinas.info())
print(producao.info())
print(manutencao.info())
print(fmea.info())


#verificado ids consistentes entre as tabelas

print(maquinas['id_maquina'].nunique())
print(falhas['id_maquina'].nunique())

#valores nulos criticos
print(falhas['id_maquina'].isna().sum())

#duplicidade
maquinas['id_maquina'].duplicated().sum()

#verificar se existem maquinas com 0 falhas

ids_maquinas = set(maquinas['id_maquina'])
ids_falhas = set(falhas['id_maquina'])

print(ids_maquinas - ids_falhas)


ids_manutencao = set(manutencao['id_maquina'])

print(ids_maquinas - ids_manutencao)


# exportação dos dados tratados para novos arquivos csv

falhas.to_csv('../Dados_tratados/falhas_tratada.csv', index=False)
maquinas.to_csv('../Dados_tratados/maquinas_tratada.csv', index=False)
producao.to_csv('../Dados_tratados/producao_tratada.csv', index=False)
manutencao.to_csv('../Dados_tratados/manutencao_tratada.csv', index=False)
fmea.to_csv('../Dados_tratados/fmea_tratada.csv', index=False)

