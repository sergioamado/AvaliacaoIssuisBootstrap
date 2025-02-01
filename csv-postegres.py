import psycopg2
import pandas as pd

# Configuração do banco de dados PostgreSQL
db_config = {
    "host": "localhost",
    "database": "github_issues",
    "user": "postegres",
    "password": "cl0ud$"
}

# Conexão com o banco de dados
def connect_db(config):
    try:
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        exit()

# Função para salvar issues do CSV no banco
def salvar_issues_csv_no_banco(conn, csv_file):
    df = pd.read_csv(csv_file, encoding='utf-8')  # Lê o arquivo CSV
    with conn.cursor() as cursor:
        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO issues (id, numero_issue, titulo, estado, data_abertura, data_atualizacao, 
                                data_conclusao, usuario_atribuido, milestone, url, refatoracao, 
                                testes_regressao, prioridade, tempo_resolucao_dias)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, (
                row['id'],
                row['number'],
                row['title'],
                row['state'],
                row['created_at'],
                row['updated_at'],
                row['closed_at'],
                row['assignee'],
                row['milestone'],
                row['html_url'],
                row['refatoracao'],
                row['testes_regressao'],
                row['prioridade'],
                row['tempo_resolucao_dias']
            ))
        conn.commit()
    print("Dados do arquivo CSV salvos no banco de dados com sucesso.")

# Carregar CSV para o banco
conn = connect_db(db_config)
salvar_issues_csv_no_banco(conn, "issues.csv")
conn.close()
