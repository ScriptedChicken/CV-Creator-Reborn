import re
from datetime import date
from os.path import join

from cover_letter_creator.data import Replacements
from cover_letter_creator.documents import DocxHandler


class Creator:
    def __init__(self, path: str) -> None:
        self.path = path

    def run(
        self,
        replacements: Replacements,
        description: str | None = None,
        output_dir: str = ".",
        applicant_name: str | None = None,
    ):
        ext = self.path.split(".")[-1]
        file_name = f"cover_letter_{applicant_name}_{replacements.job_title}_{date.today()}.{ext}"
        file_name = file_name.replace('/', '_')
        output_path = (
            join(output_dir, file_name.lower()).replace(" ", "_").replace("-", "_")
        )
        output_path = re.sub(r"_{2,}", "_", output_path)

        document = DocxHandler()
        document.open_document(self.path)
        for key, value in replacements.to_dict().items():
            document.update_document(key, value)
        document.execute_chat_gpt_prompts(description)

        document.save_document(output_path)
        document.close_document()
        return output_path
