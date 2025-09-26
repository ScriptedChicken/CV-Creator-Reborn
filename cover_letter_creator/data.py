from dataclasses import dataclass
from datetime import date

from cover_letter_creator.seek_api import SeekApiResult


@dataclass
class Replacements:
    job_title: str
    company: str
    location: str

    @classmethod
    def from_result(cls, result: SeekApiResult):
        return cls(
            job_title=result.title, company=result.advertiser, location=result.address
        )

    def to_dict(self):
        return {
            "JOB_TITLE": self.job_title,
            "COMPANY_NAME": self.company,
            "LOCATION_NAME": self.location,
            "DATE": date.today().strftime("%d/%m/%Y"),
        }
