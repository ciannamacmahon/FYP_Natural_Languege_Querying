import openai
import nlp
import os
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON

cidocDict=[
    {}
]
personFinder={}
personFinder['name']="crm:P1_is_identified_by"
personFinder['readable']="rdfs:label"
cidocDict.append(personFinder)

bearChar={}
bearChar["class"]= "?birth rdf:type crm:E67_Birth"
bearChar["birthDate properties"]="crm:P4_has_time-span ?timespanA, crm:P98_brought_into_life ?person. ?timespanA crm:P82a_begin_of_the_begin ?birthDate"
bearChar["birthPlace property"]=" crm:P4_has_time-span X crm:P7_took_place_at X"
cidocDict.append(bearChar)

def load_api_keys():
    load_dotenv()
    openai_key=os.getenv("OPENAI_APi_KEY")
    return openai_key

def connect_OPENAI():
    openai_key=load_api_keys()
    openai.api_key=openai_key

def construct_SPARQL():
    # SPARQL query executed on endpoint
    # {query_parameter} is replaced by the term entered into the interface
    #query_person=input("who?: ")
    print("This is going to allow you to find all the people born within a specified time frame are their respective death dates")
    startDate=input("Enter the name date of the timeframe: ")
    endDate=input("Enter the end date of the time frame: ")
    start_SPARQL = """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX crm: <http://erlangen-crm.org/current/>
        PREFIX vt: <https://kb.virtualtreasury.ie/>
        PREFIX vt_ont: <https://ont.virtualtreasury.ie/ontology#>

        select distinct ?person_name ?birth_date 

        where {
                #Get appellation (surname-forename) of person
                ?person crm:P1_is_identified_by ?appellation.
                ?appellation rdfs:label ?person_name.


            """
    

    end_SPARQL="""
"""

    endSPARQLFilter="""
        FILTER(?birthDate= {birth})
    """

    query=start_SPARQL+end_SPARQL

    search_graph(query)
def search_graph(sparql_query):
    # only endpoint is VRTI graph
    graph_uri = "https://blazegraph.virtualtreasury.ie/blazegraph/namespace/b2022/sparql"
   # print(graph_uri)

   # sparql_query = sparql_query.replace("{query_parameter}", query_parameter.lower())
    table_rows = {}
    try:
        sparql = SPARQLWrapper(graph_uri)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        row_count = 0
        sparql_variables = sorted(results["head"]["vars"])
        print(f"The following variables are returned by the SPARQL query: {sparql_variables}")
        for result in results["results"]["bindings"]:
            new_row = {}
            for variable in sparql_variables:
                if result.get(variable):
                    current_value = result.get(variable).get("value")
                    new_row[variable] = current_value
            table_rows[row_count] = new_row
            row_count += 1
        print(f"The results of the query: {table_rows}")
        chat_chatGPT(table_rows)
        #print(f"The SPARQL query executed:\n {sparql_query}")
        return table_rows
    except Exception as e:
        exception_message = f"Exception: {e}"
        print(exception_message)
        return exception_message

def main():
    connect_OPENAI()
  #  search_graph()

def chat_chatGPT(SPARQL_answer): #SAPRQL result is currently stored as dict not string
    framing_text="turn this entire SPARQL result into a natural language sentence;"
    string_SPARQL_Result=str(SPARQL_answer)
    chatGPT_Question=framing_text+string_SPARQL_Result
    print(f"The question you are asking CHAT-GPT is: ",chatGPT_Question)
    messages=[{"role":"user","content":chatGPT_Question}]
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    result=response.choices[0].message["content"]
    print(result)

#if __name__ == '__main__':
  #  main()