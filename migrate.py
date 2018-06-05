import json
import requests

def get_one_page(page_number):
    url = f'http://thelibrary.adurolife.com/wp-json/wp/v2/posts?page={page_number}'
    headers = ''

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

first_page = get_one_page(1)

for post in first_page:
    slug = post['slug']
    title = post['title']['rendered']
    url = post['link']
    date = post['date']
    modified = post['modified']

    print(slug)
    print(title)
    print(url)
    print(date)
    print(modified)
