import time
import base64
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        from config import IMAGENS_PATH
        pasta_destino = IMAGENS_PATH # pasta onde as imagens serão armazenadas localmente
        pasta_destino.mkdir(parents=True, exist_ok=True)

        nome_base = termo_busca.replace(' ', '_')
        nome_base = re.sub(r'[<>:"/\\|?*]', '', nome_base)#Evita erro ao baixar imagens
        nome_arquivo = f"{nome_base}.jpg"
        caminho = pasta_destino / nome_arquivo

        with open(caminho, 'wb') as f:
            f.write(image_data)

        print(f"[✓] Imagem salva em: {caminho}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return str(caminho)

    except (NoSuchElementException, TimeoutException, ValueError) as e:
        print(f"[ERRO] ao buscar imagem para '{termo_busca}': {e}")
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        return None