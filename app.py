# from pathlib import Path
from tqdm import tqdm
from unsync import unsync
import requests
import os
import re
import asyncio

myfile = os.fspath('data/requirements.txt')

def openfile():
    with open(myfile,'r') as openfile:
        piprequirements = openfile.readlines()
    return piprequirements

def write_new_file(updates):
    f = open('data/new_requirements.txt', 'w+')
    sorted_list = sorted(updates, key = lambda i: i['library'])
    # print(sorted_list)

    for v in sorted_list:
        
        if v['newVersion'] != v['currentVersion']:
            line = f"{v['library']}=={v['newVersion']} # Change from {v['currentVersion']}"
        else:
            line = f"{v['library']}=={v['currentVersion']}"
        f.write(line + '\n')

    return 'done'


def loop_calls(itemList):
    results = []
    for i in tqdm(itemList,desc='PyPi calls', total=len(itemList),ascii=True,unit=' pypiCall'):
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
        
        comment = i.startswith("#")
        recur_file = i.startswith("-")
        empty_line =  False
        if i:
            empty_line =  False

        if len(i.strip()) != 0 and comment == False and recur_file == False and empty_line == False:
            # print(i)
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
            print(cleaned_up_i)
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
            # print(cleaned_lib['library'])
            lib = cleaned_lib['library']
            if not any(l['library']==lib for l in results):
                results.append(cleaned_lib)


    # print(results)
    return results

def main():
    file_data = openfile()
    # print(file_data)
    cleaned_data = clean_item(file_data)
    # print(cleaned_data)
    fulllist = loop_calls(cleaned_data)
    # print(fulllist)
    written = write_new_file(fulllist)
    # print (written)

if __name__ == '__main__':
    main()