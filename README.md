## Employee Attrition Project: Análise Preditiva e Data Pipeline

Este projeto, originado em uma dinâmica de Análise Preditiva de RH (Employee Attrition), evoluiu para uma Prova de Conceito (PoC) de Engenharia de Dados. O objetivo principal é estabelecer uma infraestrutura de dados integrada e automatizada entre o Google Drive e um Banco de Dados SQL, servindo de blueprint para futuros projetos da Empresa Júnior.


## ⚙️ Arquitetura do Projeto (Data Pipeline)

O fluxo de trabalho do projeto é estruturado em um pipeline que garante a ingestão, transformação e destino dos dados (ETL simplificado):

| Fase | Descrição | Tecnologias Chave |
| :--- | :--- | :--- |
| **Source (Fonte)** | Arquivos de dados CSV hospedados no Google Drive. | Google Drive, `gspread` |
| **Transform** | O Notebook Jupyter executa a lógica de limpeza, padronização e cálculo das **Taxas de Rotatividade (Attrition Rates)**. | Python, Pandas |
| **Load (Carga)** | Os resultados são carregados em destinos estratégicos para consumo. | PostgreSQL (`SQLAlchemy`), Google Sheets |

## 🚀 Instalação e Configuração

Para rodar este projeto localmente, siga os passos abaixo para configurar o ambiente virtual e as dependências.

### 1. Criar o Ambiente Virtual

Abra o terminal na pasta raiz do projeto e crie o ambiente virtual:

```bash
python3 -m venv venv
````

### 2\. Ativar o Ambiente

| Sistema Operacional | Comando |
| :--- | :--- |
| **Linux / macOS** | `source venv/bin/activate` |
| **Windows** | `venv\\Scripts\\activate` |

### 3\. Instalar as Dependências

Com o ambiente ativado, instale todas as bibliotecas necessárias:

```bash
venv/bin/pip install -r requirements.txt
```

## 🔐 Configuração de Variáveis de Ambiente

Este projeto utiliza variáveis de ambiente para gerenciar credenciais sensíveis e URLs de conexão. Crie um arquivo chamado `.env` na **raiz** do projeto e preencha com suas configurações:

```env
# Configurações do Banco de Dados
DB_URL="postgresql://user:pass@localhost:5432/nome_do_seu_banco"

# Configurações do Google Drive/Sheets
DRIVE_FOLDER_ID="o_id_da_sua_pasta_no_drive"
CREDS_PATH="./service_account_creds.json"
```

## 📁 Estrutura do Projeto

A lógica de execução reside primariamente na pasta `analysis/`.

```
.
├── analysis/
│   ├── .env                       # Variáveis de ambiente para o Notebook
│   ├── credentials.json           # 👈 Credenciais do Google Sheets/Drive
│   └── notebooks.ipynb            # 👈 O Notebook principal de análise e execução
├── models/
├── pipeline/
│   ├── data_transform.py          # Lógica de limpeza e transformação de dados
│   └── main.py                    # Funções de utilidade (Ex: save_data_to_postgres)
├── utils/
│   └── google_drive_utils.py      # Funções de upload para o Drive/Sheets
├── .gitignore
└── requirements.txt
```

## 💻 Como Executar a Análise

1.  Certifique-se de que o ambiente virtual está ativado.
2.  Inicie o Jupyter Notebook (ou JupyterLab):
    ```bash
    jupyter notebook
    ```
3.  Abra o arquivo `analysis/analysis.ipynb`.
4.  **Execute as células em ordem.** O notebook irá:
      * Carregar as variáveis `.env`.
      * Aplicar transformações nos dados (`pandas`).
      * Calcular todas as taxas de rotatividade necessárias para o Dashboard.
      * **Salvar os DataFrames de resumo** no Google Sheets e no PostgreSQL.

Ao final, seu banco de dados estará alimentado com as tabelas de resumo para que você possa conectar o Power BI.

-----

*Desenvolvido com o intuito de aplicar conceitos de Data Engineering em uma análise de Data Science clássica.*
"""

