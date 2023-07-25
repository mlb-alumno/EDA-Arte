# Importamos las librerías necesarias
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re



# Iniciamos el webdriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://www.lacasaencendida.es/actividades?h=true"
driver.get(url)

driver.find_element(By.CSS_SELECTOR,'#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection').click()


def get_artist(title):
    '''
    función que obtiene el artista de cada evento según el título.
    '''
    splitpatt = r'\,\sde\s|\,\scon\s?'
    try:
        art = re.split(splitpatt,title)[1]
        thistitle = re.split(splitpatt,title)[0]
    except:
        art = "No definido"
        thistitle = title
    return thistitle, art

def collect_page(driver,url):
    """
    función que devuelve el dataframe con los datos de una página individual
    """
    data_dict = dict() 
    description = re.split(r':\s|\n',driver.find_element(By.CLASS_NAME,'item-detail__details').text)
    data_dict["title"] = get_artist(driver.find_element(By.CLASS_NAME,'item-detail__hero__info__title').text)[0]
    data_dict["artist"] = get_artist(driver.find_element(By.CLASS_NAME,'item-detail__hero__info__title').text)[1]
    data_dict["date"] = driver.find_element(By.CLASS_NAME,'item-detail__hero__info__when').text
    try:
        data_dict["description"] = driver.find_element(By.CLASS_NAME,'item-detail__title').find_element(By.TAG_NAME,'p').text
    except:
        data_dict["description"] = driver.find_element(By.CLASS_NAME,'item-detail__title').text
    data_dict["text"] = driver.find_element(By.CLASS_NAME,'item-detail__info__content').text
    data_dict["tags"] = driver.find_element(By.CLASS_NAME,'item-detail__info__tags').text.split(', ')
    try:
        data_dict["group"] = driver.find_element(By.CLASS_NAME,'group-link').text
    except:
        data_dict["group"] = "Not in a group"
    for i in range(0,len(description)-1,2):
        data_dict[description[i]] = description[i+1]
    try:
        data_dict["event"] = driver.find_element(By.CLASS_NAME,'item-detail__list').text
    except:
        data_dict["event"] = "No details"
    
    data_dict["category"] = driver.find_element(By.CLASS_NAME,'tags').text.split(', ')
    data_dict["url"] = url
    data_dict["image"] = re.split(r'\s',driver.find_element(By.CLASS_NAME,'slide__image').get_attribute('srcset'))[0]


    return pd.DataFrame([data_dict])


def extract_items(npage):
    """
    Loop que obtiene los datos de cada página de la primera lista
    """
    data_df = pd.DataFrame()
    results = driver.find_elements(By.CLASS_NAME, 'results-list__item')
    for i in range(len(results)):
        results = driver.find_elements(By.CLASS_NAME, 'results-list__item')
        try:
            url_n = results[i].find_element(By.TAG_NAME,'a').get_attribute('href')
            driver.get(url_n)
            new_data = collect_page(driver,url_n)
            time.sleep(0.2) # a 0.5 funciona
            data_df = pd.concat([data_df,new_data],ignore_index=True,axis=0)

            print(i,"de ",len(results),"completado")
            driver.back()
            time.sleep(0.2) 
        except:
            driver.back()
            continue
    #data_df.to_csv(f"parciales/casaenc_{npage}.csv")
    return data_df

def main():
    """
    Loop que obtiene los datos de todas las listas y los guarda
    """
    url = 'https://www.lacasaencendida.es/actividades?h=true'
    final_df = pd.DataFrame()
    driver.get(url)
    for i in range(0,239):
        print("PÁGINA ",i,":")
        driver.get(url+'&page='+str(i))
        time.sleep(0.3)
        new_df = extract_items(i)
        final_df = pd.concat([final_df,new_df],ignore_index=True,axis=0)
        time.sleep(0.2)
        final_df.to_csv(f"../data/parciales/final1.csv")
    final_df.to_csv(f"../data/parciales/final1.csv")





