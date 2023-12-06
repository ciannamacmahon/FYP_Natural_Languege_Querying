import requests
import json

def main():
    testList=[]
    findingCIDOCNotation(testList)

def findingCIDOCNotation(list):
    response=requests.get("https://lov.linkeddata.es/dataset/lov/api/v2/term/search?q=birth&vocab=crm")
    if response.status_code==200:
        data=response.json()

        # formatting
        if 'results' in data:
            results=data['results']
            cidocNotation= [result.get('prefixedName',[]) for result in results]
            formatted= json.dumps(cidocNotation, indent=2)
            print(formatted)
    else:
        print(f"Error: {response.status_code}")

if __name__ == '__main__':
    main()