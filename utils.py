import re
import base64
import time
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import config


def iniciar_driver_e_login():
    options = webdriver.ChromeOptions()
    service = Service(config.CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    driver.get(config.WP_LOGIN_URL)
    if "wp-login.php" in driver.current_url or "login" in driver.title.lower():
        try:
            wait.until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(config.WP_USERNAME)
            wait.until(EC.presence_of_element_located((By.ID, "user_pass"))).send_keys(config.WP_PASSWORD)
            wait.until(EC.element_to_be_clickable((By.ID, "wp-submit"))).click()
            wait.until(EC.presence_of_element_located((By.ID, "wpadminbar")))
            print("[\u2713] Login realizado com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha no login: {e}")
            driver.quit()
            exit(1)

    return driver, wait


def carregar_dados(caminho):
    return pd.read_excel(caminho).head(config.LIMITE_PRODUTOS)


def formatar_titulo_bruto(titulo: str) -> str:
    titulo = titulo.strip()
    titulo = re.sub(r"\bRef\.?\s*\S*", "", titulo, flags=re.IGNORECASE)
    titulo = re.sub(r"\s*\([^)]*\)", "", titulo)
    titulo = re.sub(r"[\u201C\"']([a-zA-Z])[\u201D\"']", lambda m: f'“Tipo {m.group(1).upper()}”', titulo)
    titulo = re.sub(r"\s*-\s*[\w\s,\.]+$", "", titulo)
    titulo = re.sub(r"(\d+)[,\.]?(\d*)\s*[mM][²2]?", lambda m: f"{m.group(1)}.{m.group(2)}m²" if m.group(2) else f"{m.group(1)}m²", titulo)
    titulo = re.sub(r"(\d+)[xX×](\d+)", r"\1x\2", titulo)
    titulo = re.sub(r"m²m", "m²", titulo, flags=re.IGNORECASE)

    especiais = {"HD", "C/", "P/", "Q/", "S/", "A", "O", "BR", "GL"}
    palavras = titulo.split()
    palavras_formatadas = [palavra.upper() if palavra.upper() in especiais else palavra.capitalize() for palavra in palavras]

    return " ".join(palavras_formatadas).strip()


def baixar_primeira_imagem_google(driver, termo_busca):
    try:
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(f"https://www.google.com/search?tbm=isch&q={termo_busca}")
        time.sleep(2)

        wait = WebDriverWait(driver, 10)
        div_imagem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "H8Rx8c")))
        img_tag = div_imagem.find_element(By.TAG_NAME, "img")
        src = img_tag.get_attribute("src")

        if not src or not src.startswith("data:image"):
            raise ValueError("Imagem não encontrada ou inválida.")

        header, base64_data = src.split(",", 1)
        image_data = base64.b64decode(base64_data)

        pasta_destino = config.IMAGENS_PATH
        pasta_destino.mkdir(parents=True, exist_ok=True)

        nome_base = termo_busca.replace(' ', '_')
        nome_base = re.sub(r'[<>:"/\\|?*]', '', nome_base)
        nome_arquivo = f"{nome_base}.jpg"
        caminho = pasta_destino / nome_arquivo

        with open(caminho, 'wb') as f:
            f.write(image_data)

        print(f"[\u2713] Imagem salva em: {caminho}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return str(caminho)

    except (NoSuchElementException, TimeoutException, ValueError) as e:
        print(f"[ERRO] ao buscar imagem para '{termo_busca}': {e}")
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        return None


def postar_produto(driver, wait, titulo_formatado, descricao, imagem_path, titulo_original):
    try:
        driver.get(config.WP_NOVA_POSTAGEM_URL)

        wait.until(EC.presence_of_element_located((By.ID, "title"))).send_keys(titulo_formatado)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "content_ifr")))
        wait.until(EC.presence_of_element_located((By.ID, "tinymce"))).send_keys(descricao)
        driver.switch_to.default_content()

        if imagem_path and Path(imagem_path).exists():
            try:
                wait.until(EC.element_to_be_clickable((By.ID, "set-post-thumbnail"))).click()
                wait.until(EC.element_to_be_clickable((By.ID, "menu-item-upload"))).click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))).send_keys(imagem_path)
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".media-button-select"))).click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#set-post-thumbnail img")))
                print("[\u2713] Imagem destacada adicionada com sucesso.")
            except Exception as e:
                print(f"[ERRO] ao adicionar imagem destacada para: {titulo_formatado} -> {e}")
        else:
            print(f"[!] Imagem não encontrada para: {titulo_original}")

        save_button = wait.until(EC.element_to_be_clickable((By.ID, "save-post")))
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        save_button.click()

        print(f"[\u2713] Produto postado como rascunho: {titulo_formatado}")
    except Exception as e:
        print(f"[ERRO] ao postar produto '{titulo_formatado}': {e}")