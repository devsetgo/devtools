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
    # print(r.status_code)
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
        logicList = ['==','>=','<=','>','<']
        if '==' in i:
            new_i = i.replace("==", " ")        
        elif ">=" in i:
            new_i = i.replace(">=", " ")
        elif "<=" in i:
            new_i = i.replace("<=", " ")
        elif ">" in i:
            new_i = i.replace(">", " ")
        elif "<" in i:
            new_i = i.replace("<", " ")
        else:
            new_i = i
        
        bracketList =  ['[',']','(',')']
        cleaned_up_i = re.sub("[\(\[].*?[\)\]]", "", new_i)
        # print(cleaned_up_i)
        m = cleaned_up_i
        pipItem = m.split()
        # print(pipItem)
        library = pipItem[0]
        try:
            currentVersion = pipItem[1]
        except Exception:
            currentVersion = "Empty Version in requirements.txt"

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