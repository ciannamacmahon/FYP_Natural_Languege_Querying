import spacy

def main():
    nlp= spacy.load("en_core_web_sm")
    stopWords=nlp.Defaults.stop_words

    #stopWords.remove('when')

    doc=nlp("where does Barack Obama live")
    
    list_charc=[]
    for token in doc: 
        characteristics={}   
        characteristics["word"]=token.text   
        characteristics["type of word"]=token.tag_    
        characteristics["The simple UPOS part-of-speech-tag"]=token.pos_    
        characteristics[ "Relationship between tokens"]=token.dep_    
        characteristics["useless word"]=token.is_stop    
 
        list_charc.append(characteristics)
       # print(token.text, token.tag_,token.pos_,token.lemma_,token.is_stop)
    
    print("List of charactertistics associated with each word in sentance: ", list_charc)

    #sentence without the useless/filler words ie.is,the,and
    fileterToekns=[token.text for token in doc if not token.is_stop]
    print(fileterToekns)

    #Finds the named entity and its type
    # "Apple sells an iphone for $1 biliion"
    # Apple= ORG (organisation)
    # 1= Money
    for ent in doc.ents:
        print(ent.text,"Entity Description: ",ent.label_)
    
    #chunk.root.dep describes the relationship from the root to the head
    for chunk in doc.noun_chunks:
        print(chunk.text,  chunk.root.dep_,
            chunk.root.head.text, "end")

if __name__ == '__main__':
    main()