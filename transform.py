import pandas as pd
import mongodb

KEYWORDS = ["prabowo", "ganjar", "anies"]


def compare_length(topicId):
    amount = mongodb.getAmount(topicId)

    limit = amount
    for keyword in KEYWORDS:
        file_path = f'tweet-harvest/tweets-data/{topicId}_{keyword}.csv'

        encodings = ['utf-8', 'latin-1', 'utf-16']  # Add more encodings if needed
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                    lines = file.readlines()
                    length_of_records = len(lines)
                    break  # Break if the file is read successfully
            except UnicodeDecodeError:
                continue  # Continue to try the next encoding if this one fails
        
        if length_of_records < limit:
            limit = length_of_records

    for keyword in KEYWORDS:
        file_path = f'tweet-harvest/tweets-data/{topicId}_{keyword}.csv'
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')  # Try reading with utf-8 encoding

        # Memilih hanya 10 record pertama
        df_subset = df.head(limit)

        # Menyimpan subset ke dalam file CSV baru
        file_path_subset = f'tweet-harvest/tweets-data/{topicId}_{keyword}_transform.csv'
        df_subset.to_csv(file_path_subset, sep=';', encoding='utf-8', index=False, mode='w')


def trim_field(topicId):
  for keyword in KEYWORDS:
    file_path = f'tweet-harvest/tweets-data/{topicId}_{keyword}_transform.csv'
    
    try:
      df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

      specific_fields = df[['created_at', 
                            'id_str', 
                            'full_text',
                            'quote_count', 
                            'reply_count', 
                            'retweet_count', 
                            'favorite_count', 
                            'username', 
                            'tweet_url']]

      specific_fields.to_csv(f'tweet-harvest/tweets-data/{topicId}_{keyword}_transform.csv', index=False, sep=';')
    except pd.errors.ParserError as e:
      print(f"ParserError: {e}")


def convert_datetime(topicId):
  for keyword in KEYWORDS:
    # Read the CSV file into a DataFrame
    file_path = f'tweet-harvest/tweets-data/{topicId}_{keyword}_transform.csv'

    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")

    # Convert the "created_at" column to datetime
    df['created_at'] = pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S %z %Y')

    # Save the updated DataFrame back to the same CSV file
    df.to_csv(file_path, index=False, mode='w')


def add_keyword(topicId):
    for keyword in KEYWORDS:
        file_path = f'tweet-harvest/tweets-data/{topicId}_{keyword}_transform.csv'

        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Add a new column called 'keyword' with the value 'prabowo'
        df['keyword'] = keyword

        # Save the DataFrame back to the CSV file
        df.to_csv(file_path, index=False, mode='w', sep=';')