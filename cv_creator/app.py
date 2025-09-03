from datetime import date

from cv_creator.data import Replacements
from cv_creator.documents import AgnosticDocument


class Creator:
    def __init__(self, path: str) -> None:
        self.path = path

    def run(self, replacements: Replacements, output_path: str | None = None):
        if not output_path:
            output_path = self.path

        document = AgnosticDocument()
        document.open_document(self.path)
        for key, value in replacements.to_dict().items():
            document.update_document(key, value)

        document.save_document(output_path)
        document.close_document()
