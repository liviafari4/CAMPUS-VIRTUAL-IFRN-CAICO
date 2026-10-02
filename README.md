# Campus Virtual IFRN Caicó

TODO

## Como executar

1. Clone este repositório.
    ```
    git clone link_para_este_repositorio
    ```

2. Crie um ambiente virtual Python.
    ```
    python -m venv env
    ```

3. Ative o ambiente virtual.

    No Windows:
    
    ```
    env\Scripts\activate
    ```

    No Linux:

    ```
    source envcampus/bin/activate
    ```

4. Instale todos os requerimentos.
    ```
    pip install -r requirements.txt
    ```

5. Execute o Flask.
    ```
    flask run --debug
    ```

## Banco de Dados

O sistema utiliza um banco de dados SQLite (`vagas.db`).

Na primeira execução do projeto, o arquivo `vagas.db` é criado automaticamente pela função `criar_tabelas()` presente no arquivo `app.py`.

Como esse arquivo é gerado localmente e armazena apenas os dados de execução da aplicação, ele não faz parte do repositório e está configurado para ser ignorado pelo Git através do `.gitignore`.