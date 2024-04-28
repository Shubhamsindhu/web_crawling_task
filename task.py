from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import csv,json,re


driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://packaging.python.org/en/latest/guides/section-install/"
driver.get(url)
html_content = driver.page_source
tree = html.fromstring(html_content)
try:
    links_data = tree.xpath("//div[@class='toctree-wrapper compound']/ul/li/a")
    anchor_data = [(a.text_content(), a.get('href')) for a in links_data]
    data = pd.DataFrame({'Anchor_Text': [x[0] for x in anchor_data], 'Href': ['https://packaging.python.org/en/latest/guides/'+x[1].replace('..','') for x in anchor_data]})
    data.to_csv('data.csv', index=False)
except:
    links_data="NotFound"
print(links_data)

driver.quit()

def extract_data(count,url, text):
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html_content = driver.page_source
    tree = html.fromstring(html_content)
    with open(str(count) + '.json') as f:
        productData = json.load(f)
    attributeNameList = productData.keys()
    for attribute in attributeNameList:

        if attribute=='heading':
           heading_data=tree.xpath(productData[attribute])[0].text_content().replace('#','').replace('\n','')
        else:
            heading_list=[heading_data]
            subheading_list=[]
            code_list=[]
            for index,sub_section in enumerate(tree.xpath(productData[attribute])):
                
                subheading_xpath=productData[attribute]+f"[{index+1}]"+"/h3"
                code_xpath=productData[attribute]+f"[{index+1}]"+"//label[contains(.,'Unix/macOS')]/following-sibling::div[1]//pre"
                try:
                    
                  subheading_data=tree.xpath(subheading_xpath)[0].text_content().replace('#','').replace('\n','')
                  subheading_list.append(subheading_data)
                except:
                    subheading_data="NotFound"
                    subheading_list.append(subheading_data)
                try:
                    subheading_code=tree.xpath(code_xpath)[0].text_content().replace('#','').replace('\n','')
                    code_list.append(subheading_code)
                except:
                    subheading_code="NotFound"
                    code_list.append(subheading_code)
    return heading_list,subheading_list,code_list,text

def add_data_to_csv(data, filename):
    file_name=re.sub(r'[^\w\s]', '', filename).replace(' ', '_')
    df = pd.DataFrame(data)
    print(df)
    df.to_csv(f'{file_name}.csv', index=False)

with open('data.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  
    for index, row in enumerate(reader):
        Anchor_Text, Href = row
        heading_list,sub_heading_list,code_list,file_name=extract_data(index+1,Href,Anchor_Text)
        combined_data = [{'heading': heading_list[0], 'sub_heading': value2, 'code': value3} for  value2, value3 in zip( sub_heading_list, code_list)]
        add_data_to_csv(combined_data, file_name)
        

        
