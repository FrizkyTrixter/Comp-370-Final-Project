import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# Initialize sentiment analysis pipeline
# Use `device=0` for GPU or `device=-1` for CPU
sentiment_pipeline = pipeline("sentiment-analysis", device=-1)

# Function to classify sentiment with a neutral category based on confidence score
def classify_sentiment_with_neutral(text, neutral_threshold=0.6):
    result = sentiment_pipeline(text[:512])[0]  # Truncate to 512 tokens if text is too long
    label = result['label']
    score = result['score']
    
    # Assign "neutral" if the confidence score is below the threshold
    if score < neutral_threshold:
        return "neutral"
    elif label == "POSITIVE":
        return "positive"
    elif label == "NEGATIVE":
        return "negative"

# Input and output file paths
input_file = "merged_annotated_articles.tsv"  # Replace with your input file path
output_file = "emotion_annotated_articles.tsv"  # Replace with your output file path

# Load the input TSV file
df = pd.read_csv(input_file, sep="\t")

# Apply sentiment classification with progress bar
tqdm.pandas(desc="Processing Sentiments")
df["Sentiment"] = df["Content"].progress_apply(lambda x: classify_sentiment_with_neutral(x))

# Save the results to a new TSV file
df.to_csv(output_file, sep="\t", index=False)

print(f"Sentiment analysis completed. Output saved to {output_file}.")

