import os
try:
	os.chdir(os.path.join(os.getcwd(), 'jupyters'))
	print(os.getcwd())
except:
	pass


from icrawler.builtin import GoogleImageCrawler
import os
from tqdm import tqdm_notebook
import pandas as pd
from datetime import date


folder_to_save = '/media/congvm/DATA/additional_data_33_classes/'

 
name_list = [
#     'đám cưới việt nam',
]

id_list = [1]



for kw, cls_id in zip(name_list, id_list):
    # Create data folders
    data_folder = os.path.join(folder_to_save, str(cls_id))
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    google_crawler = GoogleImageCrawler(
        feeder_threads=4,
        parser_threads=4,
        downloader_threads=4,

    storage={'root_dir': data_folder})

    for i in range(5):
        filters = dict(date=((2013 + i, 1, 1), 
                             (2013 + i, 12, 31)))
        #             size='large',
        #             color='orange',
        #             license='commercial,modify',

        google_crawler.crawl(keyword=kw, 
                            filters=filters, 
                            max_num=1000, 
                            file_idx_offset='auto',
                            overwrite=True)


