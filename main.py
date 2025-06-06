from tqdm import tqdm
from pathlib import Path
import subprocess
from config import EXCEL_PATH
from utils import (
    iniciar_driver_e_login,
    carregar_dados,
    formatar_titulo_bruto,
    baixar_primeira_imagem_google,
    postar_produto,
)

def verificar_e_criar_estrutura():
    estrutura_criada = Path("estrutura.criada")

    if not estrutura_criada.exists():
        print("[!] Estrutura não encontrada. Executando setup.bat...")
        subprocess.call(["script/setup.bat"], shell=True)

        estrutura_criada.touch()
        print("[✓] Setup inicial concluído.")

verificar_e_criar_estrutura()

def main():
    df = carregar_dados(EXCEL_PATH)
    driver, wait = iniciar_driver_e_login()

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Postando produtos"):
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
