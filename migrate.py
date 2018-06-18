import json
import requests
import csv
import re
import html
import os.path

csvfile = 'challenges.csv'

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

if not os.path.exists(csvfile):
    # Create csv with headers
    with open(csvfile, 'a') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows([headers])


def get_one_page(page):
    url = f'http://thelibrary.adurolife.com/wp-json/wp/v2/posts?page={page}'
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


# Library has 91 pages
for page_number in range(1, 92):
    print(f'Fetching page {page_number}', end='', flush=True)
    page = get_one_page(page_number)

    for post in page:
        print('.', end='', flush=True)
        title = html.unescape(post['title']['rendered'])

        content = post['content']['rendered']

        pattern = '(?<=<script type="application\/json">\s).*(?=\s<\/script>)'
        r = re.search(pattern, content)
        if r is None:
            json_data = None
        else:
            json_data = json.loads(r.group())['defaults']

        r = re.search('(?<=<div id="shD">\s).*(?=\s<\/div>)', content)
        if r is None:
            instructions = ''
        else:
            instructions = html.unescape(r.group())

        r = re.search('(?<=<pre id="fvch-code-0">)[\s\S]*(?=<\/pre>)', content)
        if r is None:
            more_information = ''
        else:
            more_information = html.unescape(r.group())

        if 125 in post['categories']:
            category = 'Health and Fitness'
        elif 126 in post['categories']:
            category = 'Growth and Development'
        elif 127 in post['categories']:
            category = 'Money and Prosperity'
        elif 128 in post['categories']:
            category = 'Contribution and Sustainability'
        else:
            category = ''

        if json_data:
            limeade_dimensions = ','.join(json_data['dimensions'])
            limeade_dimensions = html.unescape(limeade_dimensions)
        else:
            limeade_dimensions = ''

        if json_data:
            limeade_image_url = json_data['imgUrl']
        else:
            limeade_image_url = ''

        if json_data:
            team_activity = 'yes' if json_data['team'] == 'Team' else 'no'
        else:
            team_activity = ''

        if json_data:
            if 'Weekly' in json_data['tracking']:
                reward_occurrence = 'Weekly'
            else:
                reward_occurrence = 'Once'
        else:
            reward_occurrence = ''

        if json_data:
            if 'Units' in json_data['tracking']:
                activity_tracking_type = 'Units'
                activity_goal = json_data['required']
            elif 'Days' in json_data['tracking']:
                activity_tracking_type = 'Days'
                activity_goal = json_data['required']
            else:
                activity_tracking_type = 'Event'
                activity_goal = ''
        else:
            activity_tracking_type = ''
            activity_goal = ''

        if json_data:
            if 'device' in json_data:
                device_enabled = json_data['device']
            else:
                device_enabled = 'no'

            if device_enabled == 'yes':
                activity_goal_text = json_data['text'].split(' | ')[1]
                device_units = json_data['text'].split(' | ')[0]
            else:
                if 'text' in json_data:
                    activity_goal_text = json_data['text']
                else:
                    activity_goal_text = ''

                if activity_goal_text == '0':
                    activity_goal_text = ''
                device_units = ''
        else:
            activity_goal_text = ''
            device_enabled = ''
            device_units = ''

        one_line = [title, instructions, more_information, category,
                    limeade_dimensions, limeade_image_url, team_activity,
                    reward_occurrence, activity_tracking_type, activity_goal,
                    activity_goal_text, device_enabled, device_units]

        # Get image using the media endpoint
        image_id = post['featured_media']
        url = f'http://thelibrary.adurolife.com/wp-json/wp/v2/media/{image_id}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            image_url = data['guid']['rendered']
            one_line.append(image_url)

        # Encode every column in the row
        for i in one_line:
            i = i.encode('utf-8')

        # Append result to CSV
        with open(csvfile, 'a') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows([one_line])

    print('')
