from cv_creator.seek_api import SeekApi

api = SeekApi()
# url = input("Paste URL: ")
url = r'https://www.seek.co.nz/jobs?jobId=86448735&type=promoted'
for result in api.from_url(url):
    print(result.description)