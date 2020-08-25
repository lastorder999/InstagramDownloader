#!/usr/bin/python3
import requests


def url_single_image(content):
    return content['display_url']


def url_single_video(content):
    return content['video_url']


def url_multiple_media(content):
    all_media = content['edge_sidecar_to_children']['edges']
    return [categorise_media(each_media['node']) for each_media in all_media]


def check_is_video(content):
    return content['is_video'] is True


def categorise_media(content):
    if check_is_video(content):
        return url_single_video(content)
    return url_single_image(content)


def go_into_shortcode_media(content):
    return content['graphql']['shortcode_media']


def go_into_type_name(content):
    return content['__typename']


def concatenate_url(url):
    rear = '?__a=1'
    return url + rear


def find_url_media(url_instagram):
    url_instagram_json = concatenate_url(url_instagram)
    content = requests.get(url_instagram_json)
    content_json = content.json()
    content_at_shortcode_media = go_into_shortcode_media(content_json)
    type_file = go_into_type_name(content_at_shortcode_media)

    if type_file == 'GraphImage':
        url_media = [url_single_image(content_at_shortcode_media)]
    elif type_file == 'GraphVideo':
        url_media = [url_single_video(content_at_shortcode_media)]
    elif type_file == 'GraphSidecar':
        url_media = url_multiple_media(content_at_shortcode_media)
    return url_media


def generate_name(url_media):
    name_media = url_media.split('/')[-1].split('?')[0]
    return name_media


def download_media(url_media):
    content_media = requests.get(url_media)
    name_media = generate_name(url_media)

    with open(name_media, 'wb') as file:
        file.write(content_media.content)
    print(f'File name: {name_media}')


def main():
    while True:
        something = input('Enter url instagram >> ').strip()
        url_media = find_url_media(something)
        for url in url_media:
            download_media(url)


if __name__ == '__main__':
    main()
