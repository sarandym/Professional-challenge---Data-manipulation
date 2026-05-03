import pandas as pd     # IMPORTAÇÃO DE BIBLIOTECAS
import numpy as np
import matplotlib.pyplot as plt

arquivo = r'C:/Users/Matheus Sarandy/Desktop/dados_vendas_bigdata.csv'  # LEITURA DO CSV
df = pd.read_csv(arquivo, sep=';')

#------------------------------------------------------------
# TRATAMENTO DE DADOS
#------------------------------------------------------------

# Corrige formato da hora (troca '-' por ':' apenas na parte da hora)
df['Data_Hora'] = df['Data_Hora'].str.replace(r'(\d{2})-(\d{2})$', r'\1:\2', regex=True)

# Converte para datetime com formato definido (evita erro e melhora performance)
df['Data_Hora'] = pd.to_datetime(df['Data_Hora'], format='%d-%m-%Y %H:%M', errors='coerce')

# Garante tipo numérico
df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

#---------------------------------------
# FILTRAGEM - TOTAL DE VENDAS
#---------------------------------------

df_compras = df[df['Tipo_de_atividade'] == 'compra']
total_vendas = df_compras.shape[0]


# AGREGAÇÃO - TOP 10 PRODUTOS
top_produtos = df[df['Tipo_de_atividade'] == 'visualizacao']['Produto'].value_counts().head(10)
total_top10_produtos = top_produtos.sum()


# AGREGAÇÃO EXTRA - TOP 10 MAIS VENDIDOS (COMPRA)
top10_vendidos = df[df['Tipo_de_atividade'] == 'compra']['Produto'].value_counts().head(10)
total_top10_vendidos = top10_vendidos.sum()


# AGREGAÇÃO EXTRA - TOP 10 MAIS NO CARRINHO
top10_carrinho = (df[df['Tipo_de_atividade'] == 'carrinho']['Produto'].value_counts().head(10))
total_top10_carrinho = top10_carrinho.sum()


# AGREGAÇÃO - VALOR MÉDIO POR HORA
df_compras['Hora'] = df_compras['Data_Hora'].dt.hour

media_por_hora = (
    df_compras
    .groupby('Hora')['Valor']
    .mean()
    .sort_index()
)


#--------------------------------
# VISUALIZAÇÃO
#--------------------------------

# Gráfico 1 - VALOR MÉDIO POR HORA
plt.figure()
plt.plot(media_por_hora.index, media_por_hora.values)
plt.title('Valor Médio das Compras por Hora')
plt.xlabel('Hora')
plt.ylabel('Valor Médio')
plt.grid()

# Gráfico 2 - TOP 10 PRODUTOS MAIS VISUALIZADOS
plt.figure()
plt.bar(top_produtos.index, top_produtos.values)
plt.title('Top 10 Produtos Mais Visualizados')
plt.xlabel('Produto')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)

# GRÁFICO 3 - TOP 10 MAIS VENDIDOS
plt.figure()
plt.bar(top10_vendidos.index, top10_vendidos.values)
plt.title('Top 10 Produtos Mais Vendidos')
plt.xlabel('Produto')
plt.ylabel('Quantidade de Vendas')
plt.xticks(rotation=45)


# GRÁFICO 4 - TOP 10 CARRINHO
plt.figure()
plt.bar(top10_carrinho.index, top10_carrinho.values)
plt.title('Top 10 Produtos Mais Adicionados ao Carrinho')
plt.xlabel('Produto')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)

# ==============================
# PREPARAÇÃO EXTRA (MINUTOS + CONTAGEM)
# ==============================

# Extrai minuto (enriquecimento)
df_compras['Minuto'] = df_compras['Data_Hora'].dt.minute

# Quantidade de compras por hora
qtd_por_hora = df_compras.groupby('Hora').size()


#------------------------------------
# RESULTADOS
#------------------------------------

print(f'Total de vendas: {total_vendas}')
print('\nTop 10 Produtos Visualizados:')
print(top_produtos)


print('\nTOP 10 PRODUTOS MAIS VENDIDOS')
print(top10_vendidos)


print('\nTOP 10 PRODUTOS MAIS ADICIONADOS AO CARRINHO')
print(top10_carrinho)

print('-' * 40)
print(f'total top10 carrinho: {total_top10_carrinho}')
print(f'total top10 vendidos: {total_top10_vendidos}')
print(f'total top10 visualizados: {total_top10_produtos}')

plt.show()