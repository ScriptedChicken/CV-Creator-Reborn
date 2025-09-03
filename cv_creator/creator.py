from datetime import date
from os.path import join

from cv_creator.data import Replacements
from cv_creator.documents import DocxHandler


class Creator:
    def __init__(self, path: str) -> None:
        self.path = path

    def run(self, replacements: Replacements, description: str|None = None, output_dir: str = "."):
        ext = self.path.split(".")[-1]
        file_name = f"{replacements.job_title}_{date.today()}.{ext}".lower()
        output_path = join(output_dir, file_name)

        document = DocxHandler()
        document.open_document(self.path)
        for key, value in replacements.to_dict().items():
            document.update_document(key, value)
        document.execute_chat_gpt_prompts(replacements)

        document.save_document(output_path)
        document.close_document()
        return output_path
