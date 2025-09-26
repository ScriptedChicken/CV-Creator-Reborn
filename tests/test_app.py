import os
from os.path import exists

import pytest

from cv_creator.creator import Creator
from cv_creator.data import Replacements


class TestCreator:
    @pytest.mark.parametrize(
        "path",
        [
            pytest.param(
                "./tests/inputs/cover_letter_template.docx",
                id="test_run_docx",
            ),
        ],
    )
    def test_run(self, path):
        replacements = Replacements(
            job_title="Fake Job", company="ACME Products", location="The Moon"
        )
        creator = Creator(path)
        output_path = creator.run(replacements)
        assert exists(output_path)
        os.remove(output_path)
