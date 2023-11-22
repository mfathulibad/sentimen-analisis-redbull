import subprocess

KEYWORDS = ["prabowo", "ganjar", "anies"]

SINCE = since
UNTIL = until

for keyword in KEYWORDS:
    filename = f'{topicId}_{keyword}.csv'

    search_keyword = f"{keyword} until:{UNTIL} since:{SINCE}"

    command = f'npx --yes tweet-harvest@2.2.7 -o "{filename}" -s "{search_keyword}" -l {amount} --token "34e252d65ac27a217ea6fa7de24720061040a6c0"'

    try:    
        subprocess.run(command, shell=True, check=True)
        print('Crawling data berhasil!')
    except subprocess.CalledProcessError as e:
        print(f'Gagal melakukan crawling data: {e}')