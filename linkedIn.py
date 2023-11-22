from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import re
from datetime import datetime, timedelta
import parameters, csv, os.path, time
import random

short_random = random.randint(5, 20)
medium_random = random.randint(20, 60)
long_random = random.randint(60, 100)
compteur = 0
mon_message = "Bonjour, contente faire parti de votre réseaux"


def open_profile(ignore_list=[]):   
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
    wait = WebDriverWait(driver, 10)
    
    # Localisez la div qui contient les éléments li
    div_containing_lis = driver.find_element(By.ID, 'ember1375')  # Remplacez 'id_de_la_div' par l'ID réel de la div

    # Trouvez tous les éléments li à l'intérieur de cette div
    list_items = div_containing_lis.find_elements(By.TAG_NAME, 'li')

    # Créez un objet WebDriverWait pour gérer les attentes
    wait = WebDriverWait(driver, 10)

# Itérez sur chaque élément li
    for index, li in enumerate(list_items, start=1):
        try:
            # À l'intérieur de chaque li, trouvez le bouton à cliquer
            # Remplacez 'selector_du_bouton' par le sélecteur approprié pour le bouton
            button = li.find_elements(By.CSS_SELECTOR, '.scaffold-finite-scroll.scaffold-finite-scroll--finite')
        
            # Attendez que le bouton soit cliquable et cliquez dessus
            wait.until(EC.element_to_be_clickable(button)).click()
        
            # Ajoutez ici un délai ou une autre logique si nécessaire, par exemple pour fermer une fenêtre modale qui pourrait apparaître
        
        except TimeoutException:
            print(f"Le bouton dans le li numéro {index} n'est pas devenu cliquable dans le temps imparti.")
        except ElementClickInterceptedException:
            print(f"Le clic sur le bouton dans le li numéro {index} a été intercepté par un autre élément.")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la tentative de clic sur le bouton dans le li numéro {index}: {e}")

'''
    message_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[aria-label*='Send a message to']")))
    mon_message = "Bonjour, contente faire parti de votre réseaux"
    for button in message_buttons:
        try:
            # Scrollez jusqu'au bouton si nécessaire
            driver.execute_script("arguments[0].scrollIntoView();", button)
            # Attendez que le bouton soit cliquable et cliquez dessus
            wait.until(EC.element_to_be_clickable(button)).click()
            #time.sleep(10)
            #message_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='textbox'][@aria-label='Write a message…']")))
            #message_box.send_keys(mon_message)
            time.sleep(10)
            # Envoyer la touche ESCAPE
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            #time.sleep(10)
        except Exception as e:
            print("Erreur lors du clic sur le bouton de message:", e)
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)
    time.sleep(5)
    # Incrémenter la variable globale
    global compteur   
    compteur += 1
    print(compteur)
    driver.close()  
    driver.switch_to.window(driver.window_handles[0])  
'''
def parse_time(time_string):
    # Cette fonction convertit le texte de temps en un objet datetime
    # Assurez-vous que cette fonction gère tous les formats de temps que LinkedIn peut afficher
    numbers = re.findall(r'\d+', time_string)
    if 'minute' in time_string:
        return datetime.now() - timedelta(minutes=int(numbers[0]))
    elif 'hour' in time_string:
        return datetime.now() - timedelta(hours=int(numbers[0]))
    elif 'day' in time_string:
        return datetime.now() - timedelta(days=int(numbers[0]))
    else:
        return datetime.now()  # Retourne le temps actuel si le format est inconnu


# Functions
def search_and_send_request(till_page, writer, ignore_list=[]):
    for page in range(1):
        print('\nINFO: Checking on page %s' % (page))
        driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
        time.sleep(short_random)
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(short_random)
        linkedin_urls = driver.find_elements(By.CSS_SELECTOR, '.mn-connection-card.artdeco-list')
        print('INFO: %s connections found on page %s' % (len(linkedin_urls), page))
        connections_with_time = []
        for index, result in enumerate(linkedin_urls, start=1):
            text = result.text.split('\n')[0]
            if text in ignore_list or text.strip() in ignore_list:
                print("%s ) IGNORED: %s" % (index, text))
                continue
            
            time_elements = result.find_elements(By.CLASS_NAME, 'time-badge')
            if time_elements:
                time_text = time_elements[0].text
                connection_time = parse_time(time_text)
                connections_with_time.append((connection_time, result))

        connections_with_time.sort(key=lambda x: x[0])

        for connection_time, result in connections_with_time:

                # Vérifier si le temps de connexion est inférieur à 23 heures
            if connection_time > datetime.now() - timedelta(days=7):
                print("%s ) TIME OK: %s" % (index, text))
                    # Trouver le bouton Message
                message_button = result.find_element(By.CSS_SELECTOR, "button[aria-label*='Send a message to']")
                if message_button:
                    try:
                        # Cliquez sur le bouton Message
                        message_button.click()
                        # Attendre que la popup de message soit visible
                        message_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.msg-form__contenteditable")))

                        # Extraire le prénom de la personne à partir de la div des détails de la connexion
                        name_element = result.find_element(By.CSS_SELECTOR, "span.mn-connection-card__name")
                        full_name = name_element.text
                        first_name = full_name.split(' ')[0] 
                        time.sleep(10)

                        personalized_message = f"Bonjour {first_name}, \nMerci pour la connexion.\n\nAs-tu déjà entendu parler du portage salarial ?"
                        message_box.send_keys(personalized_message)

                        #message_box.send_keys('Bonjour, contente de faire parti de votre réseaux')
                        #message_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='textbox'][@aria-label='Write a message…']")))
                        time.sleep(10)
                        
                        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.msg-form__send-button")))
                        send_button.click()
                        time.sleep(10)
                        
                        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        time.sleep(10)
                        print("%s ) MESSAGE SENT: %s" % (index, text))
                    except Exception as e:
                        print('%s ) ERROR: %s' % (index, text))
                        time.sleep(short_random)
                else:
                    print("%s ) NO MESSAGE BUTTON: %s" % (index, text))
                    time.sleep(short_random)


try:
    # Login
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.linkedin.com/login')
    driver.find_element('id', 'username').send_keys(parameters.linkedin_username)
    driver.find_element('id', 'password').send_keys(parameters.linkedin_password)
    driver.find_element('xpath', '//*[@type="submit"]').click()
    time.sleep(20)
    # CSV file loging
    file_name = parameters.file_name
    file_exists = os.path.isfile(file_name)
    writer = csv.writer(open(file_name, 'a'))
    if not file_exists: writer.writerow(['Connection Summary'])
    ignore_list = parameters.ignore_list
    if ignore_list:
        ignore_list = [i.strip() for i in ignore_list.split(',') if i]
    else:
        ignore_list = []
    # Search
    search_and_send_request(till_page=parameters.till_page, writer=writer,
                            ignore_list=ignore_list)
except KeyboardInterrupt:
    print("\n\nINFO: User Canceled\n")
except Exception as e:
    print('ERROR: Unable to run, error - %s' % (e))
finally:
    # Close browser
    driver.quit()