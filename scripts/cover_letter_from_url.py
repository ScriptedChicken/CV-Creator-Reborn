import glob
import os

from cv_creator_reborn.apis.seek import SeekApi
from cv_creator_reborn.creator import Creator, Replacements

TEMPLATES_DIR = "/home/chook/Documentos/Trabajo/Templates"
OUTPUT_DIR = "/home/chook/Documentos/Trabajo/Outputs"
APPLICANT_NAME = "Angus Hunt"


def pick_template() -> str:
    templates = sorted(glob.glob(os.path.join(TEMPLATES_DIR, "*.docx")))
    if not templates:
        print(f"No .docx templates found in {TEMPLATES_DIR}")
        raise SystemExit(1)

    print("Available templates:")
    for i, t in enumerate(templates, start=1):
        name = os.path.basename(t)
        print(f"  {i}. {name}")

    while True:
        try:
            choice = input(f"\nSelect template (1-{len(templates)}): ")
            index = int(choice) - 1
            if 0 <= index < len(templates):
                return templates[index]
            print(f"Please enter a number between 1 and {len(templates)}")
        except ValueError:
            print("Please enter a valid number")


def main():
    api = SeekApi()
    template_path = pick_template()
    creator = Creator(template_path)

    while True:
        url = input("URL: ")
        for result in api.from_url(url):
            replacements = Replacements.from_result(result)
            path = creator.run(
                replacements,
                description=result.description,
                applicant_name=APPLICANT_NAME,
                output_dir=OUTPUT_DIR,
            )
            print(f"File created at {path}")


if __name__ == "__main__":
    main()