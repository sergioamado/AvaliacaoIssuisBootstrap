import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Lendo o arquivo CSV
df = pd.read_csv('issuis-closed.csv')

# Preenchendo dados vazios com valores padrão
df['tempo_resolucao_dias'].fillna(0, inplace=True)
df['prioridade'].fillna('Desconhecida', inplace=True)

# Convertendo colunas para tipos adequados
df['tempo_resolucao_dias'] = pd.to_numeric(df['tempo_resolucao_dias'], errors='coerce')
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

# Filtro de dados (por exemplo, apenas issues com estado 'closed')
df = df[df['state'] == 'closed']

# Pergunta ao usuário qual gráfico ele quer gerar
print("Escolha o gráfico que você deseja gerar:")
print("1 - Gráfico de Barras (Quantidade de Issues por Prioridade)")
print("2 - Gráfico de Linhas (Tempo Médio de Resolução ao Longo do Tempo)")
print("3 - Gráfico de Pizza (Proporção de Issues por Estado)")
grafico_escolhido = int(input("Digite o número do gráfico desejado (1, 2 ou 3): "))

# Perguntar ao usuário quais colunas usar para o gráfico
colunas_disponiveis = df.columns
print("\nColunas disponíveis para análise:")
for i, coluna in enumerate(colunas_disponiveis, start=1):
    print(f"{i} - {coluna}")

# Perguntando as colunas para o eixo X e Y
coluna_x = int(input("\nEscolha a coluna para o eixo X (digite o número): ")) - 1
coluna_y = int(input("Escolha a coluna para o eixo Y (digite o número): ")) - 1

# Filtra as colunas que o usuário escolheu
coluna_x = colunas_disponiveis[coluna_x]
coluna_y = colunas_disponiveis[coluna_y]

# Geração do gráfico baseado na escolha do usuário
if grafico_escolhido == 1:
    # Gráfico de Barras: Quantidade de Issues por Prioridade
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=coluna_y, palette='viridis')
    plt.title(f'Quantidade de Issues por {coluna_y}')
    plt.xlabel(coluna_y)
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    plt.show()

elif grafico_escolhido == 2:
    # Gráfico de Linhas: Tempo de Resolução ao Longo do Tempo
    if pd.api.types.is_datetime64_any_dtype(df[coluna_x]):
        df_grouped = df.groupby(df[coluna_x].dt.date)[coluna_y].mean().reset_index()
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df_grouped, x=coluna_x, y=coluna_y, marker='o', color='blue')
        plt.title(f'{coluna_y} ao Longo do Tempo')
        plt.xlabel(coluna_x)
        plt.ylabel(coluna_y)
        plt.xticks(rotation=45)
        plt.show()
    else:
        print(f"A coluna '{coluna_x}' não é de data, não é possível gerar gráfico de linhas.")

elif grafico_escolhido == 3:
    # Gráfico de Pizza: Proporção de Issues por Estado
    if coluna_y == 'state':
        plt.figure(figsize=(7, 7))
        df[coluna_y].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='Set3')
        plt.title(f'Proporção de {coluna_y}')
        plt.ylabel('')  # Remove label do eixo Y para clareza no gráfico de pizza
        plt.show()
    else:
        print(f"A coluna '{coluna_y}' não é adequada para um gráfico de pizza.")

else:
    print("Opção de gráfico inválida!")
