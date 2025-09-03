from cv_creator.seek_api import SeekApi
from cv_creator.app import Creator, Replacements

api = SeekApi()
# url = input("Paste URL: ")
url = r'https://www.seek.co.nz/jobs?jobId=86448735&type=promoted'
creator = Creator('templates/cover_letter_template_gpt.docx')
for result in api.from_url(url):
    replacements = Replacements.from_result(result)
    creator.run(replacements=replacements, output_path='test.docx')