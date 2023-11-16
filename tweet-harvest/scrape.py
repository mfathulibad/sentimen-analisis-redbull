import subprocess

filename = 'prabowo.csv'
search_keyword = 'prabowo'
limit = 50

command = f'npx --yes tweet-harvest@2.2.7 -o "{filename}" -s "{search_keyword}" -l {limit} --token "34e252d65ac27a217ea6fa7de24720061040a6c0"'

try:
    subprocess.run(command, shell=True, check=True)
    print('Crawling data berhasil!')
except subprocess.CalledProcessError as e:
    print(f'Gagal melakukan crawling data: {e}')
