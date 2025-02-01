import os
import requests
import pandas as pd
from datetime import datetime

# Função para ler o token do arquivo github_token.txt
def ler_token_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r") as arquivo:
            return arquivo.read().strip()  # Remove espaços e quebras de linha extras
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        exit()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        exit()

# Lendo o token do arquivo github_token.txt
token_path = "github_token.txt"  # Nome do arquivo no diretório do projeto
token = ler_token_arquivo(token_path)
headers = {"Authorization": f"token {token}"}

# URL do repositório
url = "https://api.github.com/repos/twbs/bootstrap/issues"

# Configuração para coletar issues
total_limit = 350
per_page = 100
all_issues = []
page = 1

# Função para limpar strings com caracteres problemáticos
def clean_string(value):
    if isinstance(value, str):
        return value.encode('utf-8', 'ignore').decode('utf-8')  # Remove caracteres inválidos
    return value

# Função para calcular tempo de resolução
def calcular_tempo_resolucao(created_at, closed_at):
    if pd.notna(created_at) and pd.notna(closed_at):
        return (closed_at - created_at).days
    return None

# Coletar issues da API do GitHub
while len(all_issues) < total_limit:
    print(f"Buscando página {page}...")
    params = {
        "state": "closed",  # Apenas issues fechadas
        "per_page": per_page,
        "page": page,
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            issues = response.json()
            if not issues:
                print("Não há mais issues para coletar.")
                break

            for issue in issues:
                created_at = pd.to_datetime(issue["created_at"]) if "created_at" in issue else None
                closed_at = pd.to_datetime(issue["closed_at"]) if "closed_at" in issue else None
                tempo_resolucao = calcular_tempo_resolucao(created_at, closed_at)

                all_issues.append({
                    "id": issue["id"],
                    "number": issue["number"],
                    "title": clean_string(issue["title"]),
                    "state": issue["state"],
                    "created_at": created_at,
                    "updated_at": pd.to_datetime(issue["updated_at"]) if "updated_at" in issue else None,
                    "closed_at": closed_at,
                    "assignee": clean_string(issue["assignee"]["login"]) if issue["assignee"] else None,
                    "milestone": clean_string(issue["milestone"]["title"]) if issue["milestone"] else None,
                    "html_url": clean_string(issue["html_url"]),
                    "refatoracao": "refactor" in issue["title"].lower(),
                    "testes_regressao": "test" in issue["title"].lower() or "regression" in issue["title"].lower(),
                    "prioridade": "alta" if "urgent" in issue["title"].lower() else (
                        "baixa" if "minor" in issue["title"].lower() else "média"
                    ),
                    "tempo_resolucao_dias": tempo_resolucao
                })

            if len(all_issues) >= total_limit:
                break
            page += 1
        else:
            print(f"Erro ao buscar dados: {response.status_code}")
            print(response.json())
            break
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        break

print(f"Total de issues coletadas: {len(all_issues)}")

# Salvar em arquivo CSV
if all_issues:
    output_file = "issues-closed.csv"
    df = pd.DataFrame(all_issues)
    df.to_csv(output_file, index=False, encoding='utf-8')  # Salva o arquivo como UTF-8
    print(f"Dados salvos no arquivo '{output_file}' com sucesso.")
