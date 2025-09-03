import pytest

from cv_creator.app import Creator
from cv_creator.data import Replacements
import os


class TestCreator:
    @pytest.mark.parametrize(
        "path",
        [
            pytest.param(
                "./tests/inputs/cover_letter_template_gpt.odt",
                id="test_run_odt",
            ),
            pytest.param(
                "./tests/inputs/cover_letter_template_gpt.docx",
                id="test_run_docx",
            ),
        ],
    )
    def test_run(self, path):
        replacements = Replacements(
            job_title="Fake Job", company="ACME Products", location="The Moon"
        )
        output_path = path.replace("inputs", "outputs")
        creator = Creator(path)
        creator.run(replacements, output_path)
        assert True
        os.remove(output_path)
