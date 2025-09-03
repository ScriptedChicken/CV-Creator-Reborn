from cv_creator.seek_api import SeekApi
from cv_creator.app import Creator, Replacements

api = SeekApi()
# url = input("Paste URL: ")
url = r'https://www.seek.co.nz/jobs?jobId=86448735&type=promoted'
for result in api.from_url(url):
    creator = Creator('templates/cover_letter_template_gpt.docx')
    replacements = Replacements(
        job_title=result.title, company=result.advertiser, location=result.address
    )
    creator.run(replacements=replacements, output_path='test.docx')