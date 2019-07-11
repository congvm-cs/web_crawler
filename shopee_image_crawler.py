
#%%
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from tqdm import tqdm
import ailabtools


SAVE_FOLDER = '/media/congvm/DATA/shopee_data'
#%%
def get_url(result):
    if result.value_of_css_property('background-image') != 'none':
        return result.value_of_css_property('background-image')
    else:
        return get_url(result.find_element_by_tag_name('div'))
    
def get_parsed_url(css_val):
    css_val = css_val.replace('url("', "")
    url = css_val.replace('")', "")
    return url

def download_image(url, save_folder=None):
    img = np.array(Image.open(urlopen(url)))
    
    if save_folder != None:
        img = img[:, :, ::-1]
        cv2.imwrite(os.path.join(save_folder, url.split('/')[-1]) + '.jpg', 
                   img)
    return img


#%%

options = Options()  
options.add_argument("--headless")  

destination_url = 'https://shopee.vn/'
driver = webdriver.Chrome(executable_path='./driver/chromedriver', chrome_options=options)

#%%
keywords = [
    'máy ảnh'
]

#%%
total_images = 0

#%%
for kw in keywords:
    driver.get(destination_url)
    time.sleep(0.5)
    elem = driver.find_element_by_class_name("shopee-searchbar-input__input")
    elem.send_keys(kw)
    elem.send_keys(Keys.ENTER)
    time.sleep(0.5)
    
    #===============================================================
    total = driver.find_element_by_class_name('shopee-mini-page-controller__total')
    total = int(total.text)
    
    save_folder='{}/{}'.format(SAVE_FOLDER, kw)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)    
    
    for i in range(total):
        results = driver.find_elements_by_class_name("shopee-search-item-result__item")
        successful = 0
        for idx, item in enumerate(tqdm(results)):
            try:
                url_ccs_val = get_url(item)
                _ = download_image(get_parsed_url(url_ccs_val), save_folder=save_folder)
                successful += 1
                total_images += successful
                
                if idx % 10 == 0:
                    step = 700*(idx//10)
                    driver.execute_script("window.scrollTo({},{});".format(step, step+700))
#                     time.sleep(1)
            except:
                pass
        print('Downloaded: {}/{}'.format(successful, len(results)))
        results.clear()
        next_button = driver.find_element_by_class_name('shopee-mini-page-controller__next-btn')
        next_button.click()
        # time.sleep(0.5)


#%%
# ailabtools.ailab_multiprocessing.pool_worker(target=download, inputs=keywords, num_worker=1)



