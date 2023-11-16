from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd

pretrained= "mdhugol/indonesia-bert-sentiment-classification"

model = AutoModelForSequenceClassification.from_pretrained(pretrained)
tokenizer = AutoTokenizer.from_pretrained(pretrained)

sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

label_index = {'LABEL_0': 'Positif', 'LABEL_1': 'Netral', 'LABEL_2': 'Negatif'}

file_path = 'tweet-harvest\\tweets-data\prabowo_transform.csv'

try:
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
    df.head(5)
except pd.errors.ParserError as e:
    print(f"ParserError: {e}")

# df.head(5)

# Loop melalui baris DataFrame dan akses nilai kolom "full_text"
for index, row in df.iterrows():
    full_text = row['full_text']

    result = sentiment_analysis(full_text)
    status = label_index[result[0]['label']]
    score = result[0]['score']

    row['sentimen'] = status
    print(f'Text: {full_text} | Label : {status} ({score * 100:.3f}%)')
