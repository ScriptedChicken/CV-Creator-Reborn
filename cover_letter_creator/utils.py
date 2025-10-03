import os
import tempfile
import uuid

import requests

def template_response_to_file(response: requests.Response):
    temp_dir = tempfile.gettempdir()
    filename = f"cover_letter_{uuid.uuid4().hex[:8]}.docx"
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, "wb") as file:
        file.write(response.content)
    return filepath


def get_template_from_id(template_id: str):
    response = requests.get(TEMPLATE_API_ENDPOINT, params={"template_id": template_id})
    response.raise_for_status()
    return template_response_to_file(response)