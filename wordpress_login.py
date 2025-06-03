from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import config

def iniciar_driver_e_login():
    options = webdriver.ChromeOptions()
    service = Service(config.CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    driver.get("https://reffinato.com.br/wp-admin/")
    if "wp-login.php" in driver.current_url or "login" in driver.title.lower():
        try:
            wait.until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(config.WP_USERNAME)
            wait.until(EC.presence_of_element_located((By.ID, "user_pass"))).send_keys(config.WP_PASSWORD)
            wait.until(EC.element_to_be_clickable((By.ID, "wp-submit"))).click()
            wait.until(EC.presence_of_element_located((By.ID, "wpadminbar")))
            print("[✓] Login realizado com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha no login: {e}")
            driver.quit()
            exit(1)

    return driver, wait
