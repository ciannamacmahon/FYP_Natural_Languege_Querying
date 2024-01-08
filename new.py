import difflib
from sentence_transformers import SentenceTransformer, util

# Load the text file containing the list of questions
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

text_file_path = 'q.txt'
with open(text_file_path, 'r', encoding='utf-8') as file:
    question_list = file.read().splitlines()

# User input
user_input = input("Question")

# Function to find the closest match
def find_closest_match(user_input, question_list):
    userEmbeddings=sbert_model.encode(user_input,convert_to_tensor=True)
    questionEmbeddings=sbert_model.encode(question_list,convert_to_tensor=True)

    cosineSim= util.pytorch_cos_sim(userEmbeddings,questionEmbeddings)[0]
    mostSimiliarIndex=cosineSim.argmax()
    
    return mostSimiliarIndex,cosineSim

# Find the closest match
closest_question_index,sim = find_closest_match(user_input, question_list)

# Print the result
print(f"User Input: {user_input}")
print(f"Closest Match: {question_list[closest_question_index]}")
print(f"Similarity Score: {sim[closest_question_index].item()}")