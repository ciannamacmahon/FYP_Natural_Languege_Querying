import spacy 
from spacy import displacy
import requests
import json


def NLPProcess(userQuery):
    nlp= spacy.load("en_core_web_sm")
    #stopWords.remove('when')

    doc=nlp(userQuery)
    questionWord=""
    root=""
    rootLemma=""
    verb=""
    verbLemma=""
    noun=""
    nounLemma=""
    
    input_char=[]
    for token in doc: 
        characteristics={}   
        characteristics["word"]=token.text   
        characteristics["type of word"]=token.tag_    
        if token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
            questionWord=token.text
        characteristics["The simple UPOS part-of-speech-tag"]=token.pos_   
        if token.pos_=="VERB":
            verb=token.text
            verbLemma=token.lemma_
        elif token.pos_=="NOUN":
            noun=token.text
            nounLemma=token.lemma_

        characteristics[ "Relationship between tokens"]=token.dep_  
        if token.dep_== "ROOT":
            root=token.text
            rootLemma=token.lemma_

        #characteristics["lemma"]=token.lemma_ 
        characteristics["useless word"]=token.is_stop    
 
        input_char.append(characteristics)
       # print(token.text, token.tag_,token.pos_,token.lemma_,token.is_stop)
    breakdown=[
        {"Root":root, "Lemma":rootLemma},
        {"Verb": verb,"Lemma":verbLemma},
        {"Noun":noun,"Lemma":nounLemma},
        {"Question": questionWord}
    ]
    print("List of charactertistics associated with each word in sentance: ", breakdown)

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
        #findingCIDOCNotation(ent.label, chunk.root.head.text)

def depParsing(doc):
    char=[]
    
    
  #  sentence=input("whats you question? ")
    print ("{:<15} | {:<8} |{:<8}| {:<15} | {:<20}".format('Token','Type','Relation','Head', 'Children'))
    print ("-" * 70)

    fileterToekns=[token.text for token in doc if not token.is_stop]
    print(fileterToekns)

    for ent in doc.ents:
        print(ent.text,"Entity Description: ",ent.label_)

    for chunk in doc.noun_chunks:
        print(chunk.text,  chunk.root.dep_,"Relationship: ",
            chunk.root.head.text, "end")

    for token in doc:
        word={}
    # Print the token, dependency nature, head and all dependents of the token
        print ("{:<15} |{:<8} | {:<8} | {:<15} | {:<20}"
            .format(str(token.text), str(token.pos_),str(token.dep_), str(token.head.text), str([child for child in token.children])))
        word["word"]=token.text 
        word["relation"]=token.dep_
        char.append(word)
  
    # Use displayCy to visualize the dependency 
    #displacy.serve(doc, style='dep', options={'distance': 130})
    print(char)
    tripleExtraction(char)

def tripleExtraction(char):
    subject=[]
    predicate=[]
    object=[]

    for prop in char:
        text=prop["word"]
        relation=prop["relation"]

        #nominal sentence- statement sentence (she is happy)
        if "nsubj" in relation:
            print("test")
            if "dobj" in relation:
                subject.append(text)
                predicate.append("prep")
                object.append("dobj")
            elif "pobj" in relation:
                subject.append(text)
                predicate.append("prep")
                object.append("pobj")
            else:
                subject.append(text)
                predicate.append("prep")
                object.append("xcomp")

            print("Subject: ", subject, "Predicate: ", predicate, "Object: ",object)

        #passive sentence- fpcuses on the action happening to the noun/subject (The cake is baked by adam)
        elif "nsubjpass" in relation:
            subject.append("agent")
            predicate.append("root")
            object.append("nsubjpass")


def main():
    global userQuestion
    global input_char
    nlp= spacy.load("en_core_web_sm")
    #stopWords.remove('when')

    userQuestion=input("Please enter your query")
    doc=nlp(userQuestion)
    depParsing(doc)

    #NLPProcess(userQuestion)

    
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