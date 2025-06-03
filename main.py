from config import EXCEL_PATH
from scraping_img import baixar_primeira_imagem_google
from utils_titulo import formatar_titulo_bruto
from wordpress_login import iniciar_driver_e_login
from wordpress_post import postar_produto
from excel_loader import carregar_dados

def main():
    df = carregar_dados(EXCEL_PATH)
    driver, wait = iniciar_driver_e_login()

    for _, row in df.iterrows():
        titulo_original = row['Titulo']
        descricao = row['Descrição']
        titulo_formatado = formatar_titulo_bruto(titulo_original)

        print(f"Buscando imagem para: {titulo_original}")
        imagem_path = baixar_primeira_imagem_google(driver, titulo_original)

        if not imagem_path:
            imagem_path = None

        postar_produto(driver, wait, titulo_formatado, descricao, imagem_path, titulo_original)

if __name__ == "__main__":
    main()