import subprocess

KEYWORDS = ["prabowo", "ganjar", "anies"]

SINCE = since
UNTIL = until

for keyword in KEYWORDS:
    filename = f'{topicId}_{keyword}.csv'

    search_keyword = f"{keyword} until:{UNTIL} since:{SINCE}"

    command = f'npx --yes tweet-harvest@2.2.7 -o "{filename}" -s "{search_keyword}" -l {amount} --token "433af3c9bbc460a4aebe4f88ba037aada1dbadc7"'

    try:    
        subprocess.run(command, shell=True, check=True)
        print('Crawling data berhasil!')
    except subprocess.CalledProcessError as e:
        print(f'Gagal melakukan crawling data: {e}')