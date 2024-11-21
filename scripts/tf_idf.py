import pandas as pd
import string
import math
from collections import defaultdict


df = pd.read_csv('../data/final/merged_annotated_articles.tsv', sep='\t')
with open('stopwords.txt', 'r') as f:
    stopwords = set(f.read().split())
df['Text'] = df['Title'].fillna('') + ' ' + df['Description'].fillna('') + ' ' + df['Content'].fillna('')

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation + string.digits))
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return words
df['Tokens'] = df['Text'].apply(preprocess)
words = set()
document_frequencies = defaultdict(int)
total_documents = len(df)
for tokens in df['Tokens']:
    unique_tokens = set(tokens)
    words.update(unique_tokens)
    for token in unique_tokens:
        document_frequencies[token] += 1
idf = {}
for term, df_t in document_frequencies.items():
    idf[term] = math.log(total_documents / (1 + df_t)) 

df['TF_IDF'] = df['Tokens'].apply(lambda tokens: {term: tokens.count(term) * idf[term] for term in tokens})





categories = df['Coding'].unique()

for category in categories:
    category_docs = df[df['Coding'] == category]
    category_tf_idf = defaultdict(float)
    
    for tf_idf_dict in category_docs['TF_IDF']:
        for term, score in tf_idf_dict.items():
            category_tf_idf[term] += score
    sorted_terms = sorted(category_tf_idf.items(), key=lambda x: x[1], reverse=True)
    top_10_terms = sorted_terms[:10]
    
    print(f"Category: {category}")
    print("Top 10 words:")
    for term, score in top_10_terms:
        print(f"{term} (TF-IDF Score: {score:.4f})")
    print()
    with open('../data/final/tf_idf_output.txt', 'a') as f:
        f.write(f"Category: {category}\n")
        f.write("Top 10 words:\n")
        for term, score in top_10_terms:
            f.write(f"{term} (TF-IDF Score: {score:.4f})\n")
        f.write('\n')


