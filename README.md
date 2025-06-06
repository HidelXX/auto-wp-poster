# 🛠️ Automação de Postagem de Produtos no WordPress

Este projeto tem como objetivo automatizar a publicação de produtos no WordPress a partir de dados estruturados em planilhas, com foco em futuras integrações via API e facilidades de uso.

---

## ✅ Funcionalidades Implementadas

- 📄 Leitura de produtos a partir de planilha Excel
- 🧠 Formatação de títulos
- 🌐 Download automático de imagem principal via scraping (Google Imagens)
- 💬 Postagem automatizada no WordPress usando Selenium
- 💾 Publicação de produtos como **rascunhos**
- 🔐 Configuração por arquivo `.env` e `config.py`

---

## 🚧 Funcionalidades em Desenvolvimento

- 🔄 Integração com API REST do WordPress (sem Selenium)
- 🖼️ Upload de **múltiplas imagens** por produto
- 🗂️ Categorização automática baseada em regras ou planilhas
- 🖥️ Interface gráfica (GUI) para uso manual e não técnico

---

## ⚙️ Tecnologias Utilizadas

- Python 3.10+
- `selenium`
- `pandas`
- `python-dotenv`
- `openpyxl`
- `pathlib`

---

## 📂 Estrutura do Projeto


C:\caminho\para\os\arquivos

├── imagens/      ← onde as imagens são salvas

├── planilhas/    ← onde está o Excel com os produtos

└── script/       ← onde está o código Python do projeto

        ├── main.py
        ├── config.py
        ├── utils.py
        ├── .env
        └── README.md


---

## 🚀 Como Usar

1. **Clone o repositório:**

        git clone https://github.com/HidelXX/automacao-reffinato.git


Crie o arquivo .env
    
        CHROMEDRIVER_PATH=C:/caminho/para/chromedriver.exe
        EXCEL_PATH=C:/caminho/para/planilhas/estoque.xlsx
        IMAGENS_PATH=C:/caminho/para/imagens

        WP_USERNAME=seu_usuario
        WP_PASSWORD=sua_senha
        WP_LOGIN_URL=https://seudominio.com.br/wp-admin/
        WP_NOVA_POSTAGEM_URL=https://seudominio.com.br/wp-admin/post-new.php?post_type=produtos
🔐 Importante: não inclua esse arquivo no GitHub. Ele deve estar no seu `.gitignore`.


Instale as dependências:

    pip install -r requirements.txt

 Configure o limite de produtos no config.py:

ex:    `LIMITE_PRODUTOS = 100`

Execute o script principal:

    python main.py

👨‍💻 Autor

Hidelbrando Tavares
GitHub: @HidelXX
