import os

def crawl_data():
    target_directory = "tweet-harvest"
    try:
        current_directory = os.getcwd()  # Menyimpan direktori saat ini
        os.chdir(target_directory)  # Mengubah direktori kerja ke folder yang diinginkan

        file_path = "scrape.py"
        try:
            with open(file_path, 'r') as file:
                code = file.read()
                exec(code)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    finally:
        os.chdir(current_directory)
