import os
from os.path import exists

import pytest

from cv_creator_reborn.creator import Creator, CreatorMode
from cv_creator_reborn.data import Replacements
from tests.utils import extract_document_text


class TestCreator:
    @pytest.mark.parametrize(
        "path, mode",
        [
            pytest.param(
                "./tests/inputs/cover_letter_template.docx",
                CreatorMode.COVER_LETTER,
                id="test_run_docx_cover_letter",
            ),
            pytest.param(
                "./tests/inputs/cv_template.docx",
                CreatorMode.COVER_LETTER,
                id="test_run_docx_cv",
            ),
        ],
    )
    def test_run(self, path, mode):
        job_title = "Fake Job"
        company = "ACME Products"
        location = "The Moon"
        replacements = Replacements(
            job_title=job_title, company=company, location=location
        )
        creator = Creator(path)
        output_path = creator.run(replacements, mode=mode)
        assert exists(output_path)

        document_text = extract_document_text(output_path)
        assert job_title in document_text
        assert company in document_text
        assert location in document_text

        os.remove(output_path)
