import spacy
import requests
import json
def main():
    nlp= spacy.load("en_core_web_sm")
    #stopWords.remove('when')

    doc=nlp("Who was born in 1600?")
    questionWord=""
    
    list_charc=[]
    for token in doc: 
        characteristics={}   
        characteristics["word"]=token.text   
        characteristics["type of word"]=token.tag_    
        if token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
            questionWord=token.text
        characteristics["The simple UPOS part-of-speech-tag"]=token.pos_   
        characteristics[ "Relationship between tokens"]=token.dep_  
        characteristics["lemma"]=token.lemma_ 
        characteristics["useless word"]=token.is_stop    
 
        list_charc.append(characteristics)
       # print(token.text, token.tag_,token.pos_,token.lemma_,token.is_stop)
    
    print("List of charactertistics associated with each word in sentance: ", list_charc)

    #sentence without the useless/filler words ie.is,the,and
    fileterToekns=[token.text for token in doc if not token.is_stop]
    print(fileterToekns)
    print(questionWord)

    #Finds the named entity and its type
    # "Apple sells an iphone for $1 biliion"
    # Apple= ORG (organisation)
    # 1= Money
    filterOption=""
    for ent in doc.ents:
        print(ent.text,"Entity Description: ",ent.label_)
        filterOption=ent.text
    
    #chunk.root.dep describes the relationship from the root to the head
    for chunk in doc.noun_chunks:
        print(chunk.text,  chunk.root.dep_,"Relationship: ",
            chunk.root.head.text, "end")
        findingCIDOCNotation(ent.label, chunk.root.head.text)

def findingCIDOCNotation(querysubject,queryObject):
    x="birthdate"

    url="https://lov.linkeddata.es/dataset/lov/api/v2/term/search?q={}&vocab=ecrm".format(x)
    print(url)
    response=requests.get(url)
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