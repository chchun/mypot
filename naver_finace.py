import pandas as pd
import requests
from bs4 import BeautifulSoup

import time

base_url = 'https://finance.naver.com/sise/sise_index_day.nhn?code='

def naver_finance_sise_day(code):

    ### 마지막 페이지를 찾는다 ####
    start_url = '{}{}'.format(base_url,code)
    print (start_url)
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    a_tag =soup.find('td','pgRR').find('a')
    href_text =a_tag['href']
    last_page = int(href_text[href_text.find('page=')+5:])
    print(last_page)
    #last_page = 10

    ###  페이지 총 갯수를 구한다.
    url_list = {page_number:"{0}&page={1}".format(start_url,page_number)
                for page_number in list(range(1,last_page+1))}

    table_dfs={}

    for url in range(1,len(url_list)+1):
        pd.read_html(url_list[url])
        table_dfs[url]= pd.read_html(url_list[url],header=0)[0].dropna()

        #time.sleep(1)

    result = pd.concat(table_dfs, ignore_index=True)

    # 전체를 다 합치지 않고, 일부분만 합칠경우
    result2 = pd.concat([table_dfs[num] for num in list(range(1,last_page))], ignore_index=True)

    print(result)



if __name__=="__main__":
    naver_finance_sise_day('FUT')
