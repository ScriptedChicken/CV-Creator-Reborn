from cv_creator.creator import Creator, Replacements
from cv_creator.seek_api import SeekApi

api = SeekApi()
url = "https://www.seek.co.nz/job/86924490?cid=company-profile&ref=company-profile"
creator = Creator("templates/cover_letter_template_gpt.docx")
for result in api.from_url(url):
    replacements = Replacements.from_result(result)
    print(creator.run(replacements, description=result.description))