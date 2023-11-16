import pandas as pd

keywords = ["prabowo", "ganjar", "anies"]

def trim_field(keywords):
  for keyword in keywords:
    file_path = f'{keyword}.csv'
    
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

      specific_fields.to_csv(f'{keyword}_trimmed.csv', index=False)
    except pd.errors.ParserError as e:
      print(f"ParserError: {e}")