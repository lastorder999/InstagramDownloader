import os
import requests


def check_file_exists(name):
    """Check if a file exist."""
    return os.path.isfile(name)


def create_name_pattern(name):
    """Create a name pattern.

    Arge:
        name: 'file.jpg'

    Returns:
        name: 'file-{}.jpg'
    """
    file_name, file_type = name.split('.')
    new_file_name = file_name + '-{}.'
    return new_file_name + file_type


def increment_file_name(name_pattern):
    """Find file name which does not exist.

    Arge:
        name_pattern: 'file-{}.jpg'

    Returns:
        file-1.jpg
        file-2.jpg
    """
    i = 1
    while os.path.exists(name_pattern.format(i)):
        i += 1
    return name_pattern.format(i)


def url_single_image(content):
    """Find image URL."""
    return content['display_url']


def url_single_video(content):
    """Find video URL."""
    return content['video_url']


def url_multiple_media(content):
    all_media = content['edge_sidecar_to_children']['edges']
    return [categorise_media(each_media['node']) for each_media in all_media]


def check_is_video(content):
    """Check content if is video."""
    return content['is_video'] is True


def categorise_media(content):
    """Make sure the content is video or image if it's video call function find
    video URL, but if it's image call function find image URL."""
    if check_is_video(content):
        return url_single_video(content)
    return url_single_image(content)


def go_into_shortcode_media(content):
    return content['graphql']['shortcode_media']


def go_into_type_name(content):
    """Find content type."""
    return content['__typename']


def concatenate_url(url):
    rear = '?__a=1'
    return url + rear


def find_url_media(url_instagram):
    """Classify"""
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
    """Separate the name from URL."""
    name_media = url_media.split('/')[-1].split('?')[0]
    return name_media


def download_media(name_media, url_media):
    """Save image or video by write binary."""
    content_media = requests.get(url_media)

    with open(name_media, 'wb') as file:
        file.write(content_media.content)
    print('File name: {}'.format(name_media))


def main():
    while True:
        something = input('Enter url instagram >> ').strip()
        url_medias = find_url_media(something)
        if not url_medias:
            continue
        for url in url_medias:
            name_media = generate_name(url)
            if check_file_exists(name_media):
                print('keep/ replace/ skip')
                choice = input('>> ')
                if choice == 'keep':
                    download_media(increment_file_name(create_name_pattern(name_media)), url)
                if choice == 'replace':
                    download_media(name_media, url)
                else:
                    continue
            else:
                download_media(name_media, url)


if __name__ == '__main__':
    main()
