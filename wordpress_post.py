from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

def postar_produto(driver, wait, titulo_formatado, descricao, imagem_path, titulo_original):
    try:
        driver.get("https://reffinato.com.br/wp-admin/post-new.php?post_type=produtos")

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
                print("[✓] Imagem destacada adicionada com sucesso.")
            except Exception as e:
                print(f"[ERRO] ao adicionar imagem destacada para: {titulo_formatado} -> {e}")
        else:
            print(f"[!] Imagem não encontrada para: {titulo_original}")

        save_button = wait.until(EC.element_to_be_clickable((By.ID, "save-post")))
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        save_button.click()

        print(f"[✓] Produto postado como rascunho: {titulo_formatado}")
    except Exception as e:
        print(f"[ERRO] ao postar produto '{titulo_formatado}': {e}")
