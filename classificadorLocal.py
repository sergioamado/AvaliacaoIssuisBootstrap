import requests
import pandas as pd

# 1. Carregar os dados
df = pd.read_csv("issues-closed.csv")

# 2. Converter para JSON para envio
data_json = df.to_json(orient="records")

# 3. Simulação de envio para processamento
url = "https://sua-api-de-classificacao.com/processar"  # Você precisaria de uma API real
response = requests.post(url, json={"data": data_json})

if response.status_code == 200:
    # 4. Receber os dados categorizados
    df_classificado = pd.DataFrame(response.json()["data"])
    
    # 5. Salvar o novo arquivo classificado
    df_classificado.to_csv("issues_bootstrap_classificado.csv", index=False)
    print("Classificação concluída! Arquivo salvo como 'issues_bootstrap_classificado.csv'.")
else:
    print("Erro ao processar os dados:", response.text)
