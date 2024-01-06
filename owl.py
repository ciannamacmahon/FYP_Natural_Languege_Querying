from owlready2 import *
from sentence_transformers import SentenceTransformer, util


def match_nat_lang(query,classes):
        sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        input_embedding = sbert_model.encode(query, convert_to_tensor=True)

        # Calculate cosine similarity with each ontology class
        similarity_scores = {}
        for ontology_class in classes:
            class_label = ontology_class.label.first()
            class_embedding = sbert_model.encode(class_label, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(input_embedding, class_embedding)
            similarity_scores[class_label] = similarity.item()

        # Return the ontology class with the highest similarity score
        best_match = max(similarity_scores, key=similarity_scores.get)
        print(best_match)
    
def main():
        onto_path.append("/ontology/")
        onto=get_ontology("http://erlangen-crm.org/231027/").load()
       # print(onto)
        ontologyClasess=list(onto.classes())
        print(ontologyClasess)
        print("????????????????????????")
        ontologyProp=list(onto.properties())
        print(ontologyProp)
        print("????????????????????????")
        ontologyPropD=list(onto.disjoint_properties())
        print(ontologyPropD)

        query=input("ask your query: ")
        match_nat_lang(query,ontologyProp)



if __name__ == '__main__':
    main()