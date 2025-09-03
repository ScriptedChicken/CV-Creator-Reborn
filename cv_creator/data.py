from dataclasses import dataclass
from datetime import date


@dataclass
class Replacements:
    job_title: str
    company: str
    location: str

    def to_dict(self):
        return {
            "JOB_TITLE": self.job_title,
            "COMPANY_NAME": self.company,
            "LOCATION_NAME": self.location,
            "DATE": date.today().strftime("%d/%m/%Y"),
        }
