from cv_creator_reborn.apis.seek import SeekApi
from cv_creator_reborn.creator import Creator, Replacements

api = SeekApi()
url = "https://www.seek.co.nz/job/86924490?cid=company-profile&ref=company-profile"
creator = Creator("templates/cover_letter_template.docx")
for result in api.from_url(url):
    replacements = Replacements.from_result(result)
    output_path = creator.run(replacements, description=result.description)
