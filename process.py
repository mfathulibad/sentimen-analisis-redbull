from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd

def add_sentiment_column(df):
    df['sentiment'] = None  # Inisialisasi kolom baru dengan nilai None

    # Loop melalui baris DataFrame dan akses nilai kolom "full_text"
    for index, row in df.iterrows():
        full_text = row['full_text']

        result = sentiment_analysis(full_text)
        status = label_index[result[0]['label']]

        # Menyimpan nilai status ke dalam kolom "sentiment"
        df.at[index, 'sentiment'] = status

pretrained= "mdhugol/indonesia-bert-sentiment-classification"

model = AutoModelForSequenceClassification.from_pretrained(pretrained)
tokenizer = AutoTokenizer.from_pretrained(pretrained)

sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

label_index = {'LABEL_0': 'Positif', 'LABEL_1': 'Netral', 'LABEL_2': 'Negatif'}

KEYWORDS = ["prabowo", "ganjar", "anies"]

for keyword in KEYWORDS:    
    file_path = f'tweet-harvest\\tweets-data\{keyword}_transform.csv'

    # Membaca file CSV
    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")
        # Keluar dari program jika ada kesalahan parser

    # Menambahkan kolom "sentiment" ke DataFrame
    add_sentiment_column(df)
    
    # Menyimpan DataFrame ke dalam file CSV
    output_file_path = f'tweet-harvest\\tweets-data\{keyword}_labelled.csv'
    df.to_csv(output_file_path, index=False, sep=";")  # index=False untuk menghindari menyimpan indeks baris
