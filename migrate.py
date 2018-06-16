import json
import requests
import csv

csvfile = "challenges.csv"

headers = [
    'Title',
    'Instructions',
    'More Information Html',
    'Category',
    'Limeade Dimensions',
    'Limeade Image Url',
    'Team Activity',
    'Reward Occurrence',
    'Activity Tracking Type',
    'Activity Goal',
    'Activity Goal Text',
    'Device Enabled',
    'Device Units',
    'Header Image'
]

result = [headers]


def get_one_page(page):
    url = f'http://thelibrary.adurolife.com/wp-json/wp/v2/posts?page={page}'
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


# # Library has 91 pages
# for page_number in range(1, 91):
#     get_one_page(page_number)

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

    # After putting it all in a list, push the list to the result list
    # result.append(new_list)

    # Get image using the media endpoint
    image_id = post['featured_media']
    url = f'http://thelibrary.adurolife.com/wp-json/wp/v2/media/{image_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        image_url = data['guid']['rendered']
        print(image_url)

# Output result to CSV
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(result)

# Notes for later

# How to get an image from its post
# http://thelibrary.adurolife.com/wp-json/wp/v2/posts?slug=727989
# post['featured_media'] (8919 in this case)
# http://thelibrary.adurolife.com/wp-json/wp/v2/media/8918
