import pandas as pd #Trabalhar com dados em formato de tabela
import matplotlib.pyplot as plt #Criar gráficos
import matplotlib #Configuração de gráficos

# Garantir suporte a acentuação em gráficos
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

#Leitura do arquivo CSV
caminho = "dados/gastos.csv" #Define o caminho do aqrquivo
df = pd.read_csv(caminho, encoding='utf-8') #Lê o arquivo CSV e armazena em um DataFrame


#Converter a coluna 'Data' para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'], errors='coerce') #Converte a coluna 'Data' para o tipo datetime

#Checar valores ausentes
print(df.isnull().sum()) #Verifica se há valores nulos

#Criar coluna de mês para análise mensal
df['Mes'] = df['Data'].dt.to_period('M') #Cria uma nova coluna 'Mes' a partir da coluna 'Data'

#Agrupar por categoria e mês 
gastos_categoria = df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False) #Agrupa os dados por categoria e soma os valores, ordenando em ordem decrescente
gastos_mes = df.groupby('Mes')['Valor'].sum() #Agrupa os dados por mês e soma os valores

#Exibir as análises no terminal
print('\nGastos por Categorias:')
print(gastos_categoria) #Exibe os gastos por categoria
print('\nGastos Mensais:')
print(gastos_mes) #Exibe os gastos mensais

#Gráfico de pizza(Distribuição dos gastos por categoria)
plt.figure(num='Gastos por Categoria', figsize=(8,6)) #Cria uma nova figura para o gráfico de pizza e nomeia a janela
gastos_categoria.plot.pie(autopct='%1.1f%%') #Cria o gráfico de pizza com porcentagens 
plt.title('Distribuição dos Gastos por Categoria') #Título do gráfico
plt.ylabel('') #Remove o rótulo do eixo y
plt.tight_layout() #Ajusta o layout do gráfico
plt.savefig('imagens/gastos_categoria.png') #Salva o gráfico em um arquivo PNG dentro da pasta imagens
plt.show() #Exibe o gráfico

#Converter o período para o formato de mês
gastos_mes.index = gastos_mes.index.strftime('%B') #Converte os meses para o formato de nome completo (ex: Janeiro, Fevereiro, etc.)

#Gráfico de barras(Distribuição dos gastos por mês)
plt.figure(num='Gastos Mensais', figsize=(10, 6)) #Define o tamanho da figura
gastos_mes.plot.bar(color='skyblue') #Cria o gráfico de barras
plt.title('Distribuição dos Gastos por Mês') #Define o título do gráfico
plt.xlabel('Mês') #Define o rótulo do eixo x
plt.ylabel('Valor Total') #Define o rótulo do eixo y
plt.tight_layout() #Ajusta o layout
plt.savefig('imagens/gastos_mensais.png') #Salva o gráfico em um arquivo PNG dentro da pasta imagens
plt.show() #Exibe o gráfico

#Gera o aqruivo em Excel
with pd.ExcelWriter('relatorios/relatorio_gastos.xlsx') as writer:
    df.to_excel(writer, index=False, sheet_name="Gastos Originais")# Exporta os dados originais para uma planilha
    gastos_categoria.to_frame("Total por Categoria").to_excel(writer, sheet_name="Resumo Categoria")# Exporta os dados agrupados por categoria para uma planilha
    gastos_mes.to_frame("Total por Mês").to_excel(writer, sheet_name="Resumo Mês")# Exporta os dados agrupados por mês para uma planilha

print("✅ Relatório Excel exportado com sucesso!")# Exibe mensagem de sucesso