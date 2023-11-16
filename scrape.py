import subprocess


def crawl_data():
    filename = 'piala.csv'
    search_keyword = 'piala dunia u-20 until:2023-03-28 since:2023-03-01'
    limit = 50

    command = f'npx --yes tweet-harvest@latest -o "{filename}" -s "{search_keyword}" -l {limit} --token ""'

    try:
        subprocess.run(command, shell=True, check=True)
        return 'Crawling data berhasil!'
    except subprocess.CalledProcessError as e:
        return f'Gagal melakukan crawling data: {e}'
