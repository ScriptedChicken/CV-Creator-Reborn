import pytest

from cover_letter_creator.api import create_cover_letter, template_response_to_file
from tests.utils import text_to_docx_response_simple

import os
from os.path import exists
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from cover_letter_creator.api import app

client = TestClient(app)

class TestGenerateCoverLetter:
    test_text = """
    Cover Letter for JOB_TITLE Position at COMPANY_NAME

    LOCATION_NAME
    DATE

    Dear Hiring Manager,

    I am writing to express my enthusiastic interest in the JOB_TITLE position at COMPANY_NAME, as advertised on your company website. With my background and skills in [relevant field], I am confident that I would be a valuable asset to your team in LOCATION_NAME.

    Throughout my career, I have developed strong [key skill 1] and [key skill 2] abilities that align perfectly with the requirements of the JOB_TITLE role. My experience in [relevant experience] has prepared me to make significant contributions to COMPANY_NAME from day one.

    I am particularly drawn to COMPANY_NAME because of your reputation for [company quality or achievement]. Your commitment to [specific value or mission] resonates with my own professional values, and I would be thrilled to contribute to your ongoing success.

    Thank you for considering my application. I have attached my resume for your review and would welcome the opportunity to discuss how my skills and experience can benefit COMPANY_NAME. I am available for an interview at your earliest convenience.

    Sincerely,
    [Your Name]
    [Your Contact Information]
    """

    def test_create_cover_letter(self):
        url = "https://www.seek.co.nz/job/87348029"
        response = text_to_docx_response_simple(self.test_text)
        template_path = template_response_to_file(response)
        cover_letter_path = create_cover_letter(url, "Test User", template_path)
        assert cover_letter_path

    def test_api_generate_cover_letter(self):
        """Test successful cover letter generation"""
        with patch('cover_letter_creator.api.get_template_from_id') as mock_get_template:
            response = text_to_docx_response_simple(self.test_text)
            template_path = template_response_to_file(response)
            mock_get_template.return_value = template_path

            payload = {
                "url": "https://www.seek.co.nz/job/87348029",
                "name": "John Doe",
                "template_id": "template_123"
            }
            
            response = client.post("http://0.0.0.0:8000/generate-cover-letter/", json=payload)
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/octet-stream"

            mock_get_template.assert_called_once_with("template_123")
            if exists(template_path):
                os.remove(template_path)