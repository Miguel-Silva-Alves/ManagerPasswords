import requests

def makeRequest(url, type, data=None, header=None):
    if type == 'POST':
        re = requests.post(url=url, json=data)
        return re.json()
    elif type == 'GET':
        re = requests.get(url=url)
        return re.json()
    elif type == 'DELETE':
        re = requests.delete(url=url+'/'+data['id'])
        try:
            return re.json()
        except:
            return re.text
    else:
        return f'Function {type} not implemented yet'