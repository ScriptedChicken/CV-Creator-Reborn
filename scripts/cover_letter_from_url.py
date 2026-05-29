from cv_creator_reborn.apis.seek import SeekApi
from cv_creator_reborn.creator import Creator, Replacements

api = SeekApi()
template_path = '/home/chook/Documentos/Trabajo/cover_letter_angus_hunt_python_developer_2026_template.docx'
output_dir = '/home/chook/Documentos/Trabajo/Outputs'
creator = Creator(template_path)

while True:
    url = input("URL: ")
    for result in api.from_url(url):
        replacements = Replacements.from_result(result)
        path = creator.run(replacements, description=result.description, applicant_name="Angus Hunt", output_dir=output_dir)
        print(f"File created at {path}")