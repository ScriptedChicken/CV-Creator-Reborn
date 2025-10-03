import re
from datetime import date
from enum import Enum
from os.path import join

from cv_creator_reborn.data import Replacements
from cv_creator_reborn.documents import DocxHandler


class CreatorMode(Enum):
    CV = "cv"
    COVER_LETTER = "cover_letter"


class Creator:
    def __init__(self, path: str) -> None:
        self.path = path

    def run(
        self,
        replacements: Replacements,
        description: str | None = None,
        output_dir: str = ".",
        applicant_name: str | None = None,
        mode: CreatorMode = CreatorMode.COVER_LETTER,
    ):
        ext = self.path.split(".")[-1]
        file_name = f"{mode.value}_{applicant_name}_{replacements.job_title}_{date.today()}.{ext}"
        file_name = (
            file_name.lower().replace(" ", "_").replace("-", "_").replace("/", "_")
        )
        file_name = re.sub(r"_{2,}", "_", file_name)
        output_path = join(output_dir, file_name)

        document = DocxHandler()
        document.open_document(self.path)
        for key, value in replacements.to_dict().items():
            document.update_document(key, value)
        document.execute_chat_gpt_prompts(description)

        document.save_document(output_path)
        document.close_document()
        return output_path
