import json
import requests

def get_one_page(page_number):
    url = f'http://thelibrary.adurolife.com/wp-json/wp/v2/posts?page={page_number}'
    response = requests.get(url)

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

    # Get image using the media endpoint
    image_id = post['featured_media']
    url = f'http://thelibrary.adurolife.com/wp-json/wp/v2/media/{image_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        image_url = data['guid']['rendered']
        print(image_url)

# Notes for later

# How to get an image from its post
# http://thelibrary.adurolife.com/wp-json/wp/v2/posts?slug=727989
# post['featured_media'] (8919 in this case)
# http://thelibrary.adurolife.com/wp-json/wp/v2/media/8918
