from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
from time import sleep

# Função principal para inicializar o Chrome
def iniciar_driver():
    chrome_options = Options()

    arguments = ['--lang=pt-BR', '--start-maximized']
    for argument in arguments:
        chrome_options.add_argument(argument)


    chrome_options.add_experimental_option('prefs', {
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads':1,
    })

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    return driver

# Acessar o site https://search.asf.alaska.edu/
driver = iniciar_driver()
driver.get('https://search.asf.alaska.edu/#/')
driver.implicitly_wait(10)

# Logar na conta de usuário
botoes_logar = driver.find_elements(By.XPATH, "//button[@color='basic']")
botoes_logar[6].click()

# Esperar a nova janela de login abrir
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

# Pega o identificador da janela original
janela_original = driver.current_window_handle

# Troca para a nova janela aberta
for janela in driver.window_handles:
    if janela != janela_original:
        driver.switch_to.window(janela)
        break

campo_usuario = driver.find_element(By.XPATH, "//input[@id='username']")
campo_usuario.send_keys('luizzampronio')

campo_senha = driver.find_element(By.XPATH, "//input[@id='password']")
campo_senha.send_keys('Lpzampronio456')

botao_login = driver.find_element(By.XPATH, "//input[@value='Log in']")
botao_login.click()
sleep(5)

driver.switch_to.window(janela_original)

# Alterar o dataset para Alos-PALSAR
botao_satelite = driver.find_elements(By.XPATH, "//div[@class='button-text']")
botao_satelite[1].click()
sleep(2)

alos_palsar = driver.find_elements(By.XPATH, "//menu[@role='menuitem']")
alos_palsar[3].click()
sleep(2)

# Subir a area de interesse (kml)
botao_subir_kml = driver.find_elements(By.XPATH, "//mat-icon[@role='img']")
sleep(2)
botao_subir_kml[0].click()
sleep(2)

enviar_arquivo = driver.find_elements(By.XPATH, "//button[@class='mdc-button mdc-button--raised mat-mdc-raised-button mat-primary mat-mdc-button-base']")
driver.execute_script('arguments[0].click()', enviar_arquivo[0])
sleep(2)

teclado = Controller()
teclado.type("C:\\Users\\lpzam\\Downloads\\area.kml")
sleep(2)
teclado.press(Key.enter)
teclado.release(Key.enter)
sleep(5)

# Adicionar Start Date
botao_filtro = driver.find_element(By.XPATH, "//span[contains(text(), 'Filters')]")
botao_filtro.click()
sleep(2)

data_inicial = driver.find_element(By.XPATH, "//input[@id='mat-input-2']")
sleep(2)
data_inicial.send_keys('1/1/2011')
sleep(2)

# Adicionar End Date
data_final = driver.find_element(By.XPATH, "//input[@id='mat-input-3']")
sleep(2)
data_final.send_keys('4/21/2011')
sleep(2)

try:
    # Clicar em search
    botao_search = driver.find_elements(By.XPATH, "//button[@class='search-button mdc-button mdc-button--unelevated mat-mdc-unelevated-button mat-primary mat-mdc-button-base']")
    botao_search[1].click()

    # Clicar na primeira imagem encontrada (mais recente)
    primeira_imagem = driver.find_elements(By.XPATH, "//span[@class='mdc-list-item__content']")
    sleep(2)
    primeira_imagem[0].click()
except IndexError:
    print('Sem resultados para o local escolhido')


# Fazer o download de 'Hi-Res Terrain Corrected'
botao_baixar = driver.find_elements(By.XPATH, "//a[@class='link']")
sleep(2)
botao_baixar[1].click()

input('')
driver.close()