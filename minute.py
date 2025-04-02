from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys 

from success_data import add_to_wins

from bs4 import BeautifulSoup
import requests

import time

import sys

import os
from dotenv import load_dotenv


current_time = time.time()
current_struct_time = time.localtime(current_time)

# Extract the date components from the struct_time object
year = current_struct_time.tm_year
month = current_struct_time.tm_mon
day = current_struct_time.tm_mday

curr_date = (f"Current date: {month:02}/{day:02}/{year:02}")

date_line = ''

with open('string.txt', 'r') as f:
    content = f.readlines()  
    if len(content) == 0:  
        check_today = False
    else:
        date_line = (content[0][:-1] )

check_today = (date_line == curr_date)

if not check_today:

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver = webdriver.Chrome()

    driver.get('https://www.minutecryptic.com/')
    play_button = driver.find_element(By.TAG_NAME, 'button')

    play_button.click()

    time.sleep(2)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find('p').text
    print(element)
    index = element.find('(')
    end_index = element.find(')')

    number = int(element[index+1: end_index])
    
    s = ''.join(element[:index].strip().split(' ') )
    with open('string.txt', 'w') as f:
        f.write(curr_date)
        f.write('\n')
        
        f.write(s)
        f.write('\n')
        
        f.write(str(number) )
        f.write('\n')
        f.write( element[:-3] ) 
        
    driver.close()

with open('string.txt', 'r') as f:
    readlist = f.readlines()
    s = readlist[1][:-1]
    number = int( readlist[2][:-1] )
    element_list = readlist[3].split(' ')[:-1]
    
print( s )
print( number )
print( element_list )

j = [i for i in s.lower() if i in 'qwertyuiopasdfghjklzxcvbnm']

x = ''.join(j)
print(x)
answer_list =[]
for i in range(0, len(x)-number+1):
    print(x[i:i+number].lower() )
    answer_list.append( x[i:i+number].lower() )



firlas_word = (element_list[0], element_list[-1])

def api_call(word): 

    load_dotenv()

    api_key = os.environ.get("API_KEY")

    api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        return response.json() 
    else:
        print("Error:", response.status_code, response.text)

r1 = api_call(firlas_word[0])
r2 = api_call(firlas_word[1])

print(r1)
print(r2)

def find_right_word(json):
    if json is None:
        json = {'synonyms' : []}
    ret_list = []
    for word in json['synonyms']:
        item = ''.join([i for i in word if i in 'qwertyuiopasdfghjklzxcvbnm'])
        if len(item) == number:
            ret_list.append(item)
    
    return list(set(ret_list))

slist1 = find_right_word(r1)
slist2 = find_right_word(r2)

for word in slist1:
    answer_list.append(word)
for word in slist2:
    answer_list.append(word)
    
    
    
    
def submit_attempts(answer_list):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get('https://www.minutecryptic.com/')
    play_button = driver.find_element(By.TAG_NAME, 'button')

    play_button.click()
    time.sleep(2)
    
    for item in answer_list:
    
        text_box = driver.find_element(By.XPATH, "/html/body/main/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/button[1]")
        text_box.send_keys(item)
        
        check_button = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[3]/div[1]/button[3]' ) 
        check_button.click()
        
        try:
            x_button = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/button')
            x_button.click()
        except:
            return (f'THIS IS THE CORRECT ANSWER: {item}')
            
        
        time.sleep(1)
        
        # try:
        #     text_box = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/button[8]')
        #     text_box.click()
        # except:
        #     print('skip')
        

        for i in range(0, number):
            text_box.send_keys(Keys.BACKSPACE)
            
    return 'Cannot BS it' 

# Access the arguments passed from the terminal
arguments = sys.argv

# Access other arguments
if len(arguments) > 1:
    result = submit_attempts(answer_list)
    print(result)
    full_string = (' '.join(element_list))
    if result == 'Cannot BS it':
        add_to_wins(curr_date, full_string, 0)
    else:
        add_to_wins(curr_date, full_string, 1)







