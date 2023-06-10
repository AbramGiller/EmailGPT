import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Load emails from the pickle file
with open('emails.pkl', 'rb') as file:
    emails = pickle.load(file)

def extract_keywords(query):
    # For now, we'll just split the query into words.
    # This can be improved using NLP techniques to better handle phrases, etc.
    return query.split()

def get_embedding(text):
    try:
        response = requests.post(
            'https://api.openai.com/v1/embeddings',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer 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'
            },
            json={
                'input': text,
                'model': 'text-embedding-ada-002'
            }
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response was: {response.text}")
        raise
    except Exception as err:
        print(f"Other error occurred: {err}")
        raise
    else:
        return np.array(response.json()['data'][0]['embedding'])

def process_query(query):
    # Get the query keywords and their embeddings
    query_keywords = extract_keywords(query)
    query_embeddings = np.array([get_embedding(keyword) for keyword in query_keywords])

    # Find the emails that best match the query
    best_emails = []
    for email in emails:
        email_embedding = get_embedding(email['Body'])
        similarity = cosine_similarity([email_embedding], query_embeddings)
        if np.mean(similarity) > 0.5:  # Threshold to consider an email as matching
            best_emails.append(email)

    return best_emails

# Test with a query
query = input("Enter your query: ").strip()
matching_emails = process_query(query)
for email in matching_emails:
    print(email)