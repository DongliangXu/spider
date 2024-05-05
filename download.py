from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bs4 import BeautifulSoup
import re
import os
import time 





def download_page(uuid):
    cnt = 0
    while cnt <= 5:
        cnt += 1
        try:
            driver.get('https://portal.gdc.cancer.gov/files/{}'.format(uuid))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td/a[contains(@href, 'bioId')]")))
        except:
            continue
        else:
            page = driver.page_source
            with open('{}.html'.format(uuid), 'w', encoding='utf-8') as fp:
                fp.write(page)
            print("{} download success!\n".format(uuid))
            return
        time.sleep(2)
    print("{} download failed!\n".format(uuid))
    time.sleep(2)


def check_html(html):
    with open(html) as fp:
        page = fp.read()
    soup = BeautifulSoup(page, 'lxml')
    flag = 0
    if soup.main.table:
        flag = 1
    else:
        print(html)
    return(flag)

accession = []


with open("gdc_sample_sheet.2024-01-23.tsv") as fp:
    for line in fp:
        if line.startswith("File"):
            continue
        arr = line.strip().split("\t")
        accession.append(arr[0])


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('user-agent=Mozilla/5.0 (Windows 98; Win 9x 4.90) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/23.0.862.0 Safari/532.0')
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# driver = webdriver.Chrome(options=options, executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#       "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#           get: () => undefined
#         })
#       """
# })
# driver.implicitly_wait(10)


def parse_html(html, cnt):
    with open(html) as fp:
        page = fp.read()
    soup = BeautifulSoup(page, 'lxml')
    tables = soup.main.find_all('table')

    head = []
    res = []

    for tr in tables[0].find_all("tr"):
        head.append(tr.th.text)
        res.append(tr.td.text)

    for tr in tables[1].find_all("tr"):
        head.append(tr.th.text)
        res.append(tr.td.text)

    for th in tables[2].find_all("th"):
        head.append(th.text)

    for td in tables[2].find_all("td"):
        res.append(td.text)

    line = "\t".join(head)
    if cnt == 1:
        print(line)

    line = "\t".join(res)
    print(line)


cnt = 0
for entry in accession:
    cnt += 1
    html = "{}.html".format(entry)
    # download_page(entry)
    parse_html(html, cnt)






