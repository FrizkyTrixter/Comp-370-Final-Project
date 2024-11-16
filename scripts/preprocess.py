import pandas as pd
import re

file_path = '../data/combined_trump.tsv'

try:
    df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', engine='python')
except Exception as e:
    exit()
df = df.drop_duplicates()

def clean_text(text):
    if pd.isnull(text):
        return ""
    text = re.sub(r'<.*?>', '', text)
    text = text.strip()
    return text

columns_to_clean = ['Title', 'Author', 'Description', 'Content']
for column in columns_to_clean:
    if column in df.columns:
        df[column] = df[column].apply(clean_text)
important_columns = ['Title', 'URL']
df = df.dropna(subset=important_columns)

#finally just add an empty column for "coding"
df['Coding'] = ""

output_file_path = '../data/cleaned_data.tsv'
df.to_csv(output_file_path, sep='\t', index=False)

