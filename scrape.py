import os

def crawl_data(amount, until, since):
    target_directory = "tweet-harvest"
    try:
        current_directory = os.getcwd()
        os.chdir(target_directory)

        file_path = "scrape.py"
        try:
            with open(file_path, 'r') as file:
                code = file.read()

            exec_globals = globals().copy()
            exec_globals.update({'amount': amount, 'until': until, 'since': since})

            exec(code, exec_globals)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    finally:
        os.chdir(current_directory)