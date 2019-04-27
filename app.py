# from pathlib import Path
from tqdm import tqdm
from unsync import unsync
import requests
import os
import re


myfile = os.fspath('data/requirements.txt')

def openfile():
    with open(myfile,'r') as openfile:
        piprequirements = openfile.readlines()
    return piprequirements

def write_new_file(updates):
    f = open('data/new_requirements.txt', 'w+')
    for i in tqdm(updates):
        if i['newVersion'] != i['currentVersion']:
            line = f"{i['library']}=={i['newVersion']} # Change from {i['currentVersion']}"
        else:
            line = f"{i['library']}=={i['currentVersion']}"
        f.write(line + '\n')

    return 'done'

def loop_calls(itemList):
    results = []
    for i in tqdm(itemList):
        url = f"https://pypi.org/pypi/{i['library']}/json"
        resp = call_pypi(url)
        pip_info = {'library': i['library']
                    ,'currentVersion': i['currentVersion']
                    ,'newVersion': resp['newVersion']}

        results.append(pip_info)
    
    return results

def call_pypi(url):
    r = requests.get(url)
    resp = r.json()
    if r.status_code != 200:
        result = {'newVersion': resp['info']['version']}
    else:
        resp = r.json()
        result = {'newVersion': resp['info']['version']}
    return result

def clean_item(items):
    results = []
    for i in items:
        l1 = i.replace(">=", " ")
        l2 = l1.replace("==", " ")
        l3 = re.sub("[\(\[].*?[\)\]]", "", l2)
        # print(l3)
        m = l3
        pipItem = m.split()
        library = pipItem[0]
        try:
            currentVersion = pipItem[1]
        except Exception:
            currentVersion = "None"

        cleaned_lib = {'library': library
                        ,'currentVersion': currentVersion}
        # print(cleaned_lib)

        results.append(cleaned_lib)
    # print(results)
    return results

def main():
    file_data = openfile()
    # print(file_data)
    cleaned_data = clean_item(file_data)
    # print(cleaned_data)
    fulllist = loop_calls(cleaned_data)
    # print(len(fulllist))
    written = write_new_file(fulllist)
    # print (written)

if __name__ == '__main__':
    main()