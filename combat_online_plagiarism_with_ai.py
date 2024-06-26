# -*- coding: utf-8 -*-
"""Combat Online Plagiarism with AI

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j7Q41RRmc6zikMiVZt6VP1GS1QP6-qyA
"""

pip install transformers torch numpy sklearn nltk

import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel

# Download necessary NLTK resources (run this once)
nltk.download('punkt')

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name, output_hidden_states=True)

# Function to tokenize and get BERT embeddings
def get_bert_embeddings(text):
    # Tokenize text
    tokens = tokenizer.encode(text, add_special_tokens=True)

    # Get BERT model output
    with torch.no_grad():
        outputs = model(torch.tensor(tokens).unsqueeze(0))
        hidden_states = outputs.hidden_states

    # Concatenate the last 4 hidden states (as recommended in BERT paper)
    concatenated_hidden_states = torch.cat(hidden_states[-4:], dim=-1)

    # Take the average of token embeddings to get sentence embedding
    sentence_embedding = torch.mean(concatenated_hidden_states, dim=1).squeeze()

    return sentence_embedding.numpy()

# Function to calculate cosine similarity between two embeddings
def calculate_similarity(embedding1, embedding2):
    embedding1 = np.expand_dims(embedding1, axis=0)
    embedding2 = np.expand_dims(embedding2, axis=0)
    return cosine_similarity(embedding1, embedding2)[0][0]

# Example usage to detect plagiarism
def detect_plagiarism(text1, text2, threshold=0.9):
    # Get embeddings for both texts
    embedding1 = get_bert_embeddings(text1)
    embedding2 = get_bert_embeddings(text2)

    # Calculate cosine similarity between embeddings
    similarity_score = calculate_similarity(embedding1, embedding2)

    # Determine plagiarism based on similarity score and threshold
    if similarity_score >= threshold:
        return True, similarity_score
    else:
        return False, similarity_score

# Example texts
document1 = """
Machine learning is the scientific study of algorithms and statistical models that
computer systems use to perform a specific task without using explicit instructions,
relying on patterns and inference instead. It is seen as a subset of artificial
intelligence.
"""

document2 = """
Machine learning is the study of algorithms and statistical models that computer
systems use to perform a specific task without using explicit instructions, relying
on patterns and inference instead. It is seen as a subset of artificial intelligence.
"""

document3 = """
Deep learning is a subset of machine learning in artificial intelligence (AI) that
has networks capable of learning unsupervised from data that is unstructured or
unlabeled.
"""

# Detect plagiarism between document1 and document2
plagiarized, similarity = detect_plagiarism(document1, document2)
print(f"Documents 1 and 2 are plagiarized: {plagiarized}, Similarity score: {similarity:.4f}")

# Detect plagiarism between document1 and document3
plagiarized, similarity = detect_plagiarism(document1, document3)
print(f"Documents 1 and 3 are plagiarized: {plagiarized}, Similarity score: {similarity:.4f}")