import copy
import re
from datetime import datetime
from typing import Iterator

import requests


def _delete_empty_values(params: dict):
    params_copy = copy.deepcopy(params)
    for key, value in params_copy.items():
        if value is None:
            del params[key]
    return params


class SeekApiResult:
    def __init__(self, data, session):
        self.session = session
        self.data = data

    @classmethod
    def from_id(cls, job_id, session):
        headers = {
            "Host": "www.seek.co.nz",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0",
            "Accept": "*/*",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://www.seek.co.nz/jobs?jobId=86924502&type=promoted",
            "Content-Type": "application/json",
            "X-Seek-EC-SessionId": "c84ac483-ce05-4558-b8dc-77621d55e3e7",
            "X-Seek-EC-VisitorId": "c84ac483-ce05-4558-b8dc-77621d55e3e7",
            "seek-request-brand": "seek",
            "seek-request-country": "NZ",
            "X-Seek-Site": "chalice",
            "Content-Length": "5235",
            "Origin": "https://www.seek.co.nz",
            "Connection": "keep-alive",
            "Cookie": "JobseekerSessionId=d8505197-31c3-4e13-b7e0-4c5ebb8fde09; JobseekerVisitorId=d8505197-31c3-4e13-b7e0-4c5ebb8fde09; last-known-sol-user-id=99e4a5219e4e6d1e96700d29328b825c646d6b87bf73ad9b70a4bf486c3f9793e6fd494a6bc3d02f3e05fd345367f1e8f4d4698e9149eb5e04d0984dd6e46ad84a507bd9cfe4f742a23bd8272612259fda8b2f569234e75d28f193652ae15fb0027cd826e631e3860204c2a49b14b092d9566d49908d2fd956466fa12b819340b97fa79cdcb9855fb3cdac27d0a9eaff0d7421a6a4c53c7a57d367db80e4231ad0d20b8b9ed8; __cf_bm=_bXTaXcZXrPpgiQfXAmZ_wrlrxogsswJhBhXnwJXBNs-1756928485-1.0.1.1-Cd24wdVHb5XjZZ_r6ZH7bFJTAl6f6Afa3O_Pi70AX_L9YBfYT0v8BBO5xgkNB3CwTP..XL4IAno1cflDvBe4lME48vu1N2C_3w2WzxtcPFk; _cfuvid=Rv9BlGxC37t2gHfjS6F1YRNb6i8JfDj9o5LIHBLOWrg-1756927550586-0.0.1.1-604800000; utag_main=v_id:0199110ae52e0028cc6e9dca0f2e0504e002801100bd0$_prevpage:search%20results%3Bexp-1756932086452$_sn:1$_se:2%3Bexp-session$_ss:0%3Bexp-session$_st:1756930285426%3Bexp-session$ses_id:1756927624891%3Bexp-session$_pn:2%3Bexp-session; sol_id=7b9a4c96-ccf4-421c-a821-0090a3c81046; hubble_temp_acq_session=id%3A1756927550768_end%3A1756930327640_sent%3A10; da_cdt=visid_0199110ae52e0028cc6e9dca0f2e0504e002801100bd0-sesid_1756927624891-hbvid_7b9a4c96_ccf4_421c_a821_0090a3c81046-tempAcqSessionId_1756927550768-tempAcqVisitorId_7b9a4c96ccf4421ca8210090a3c81046; da_anz_candi_sid=undefined; _pin_unauth=dWlkPVpEa3pZV0ZpWm1NdE1EQXlNeTAwTVdZeUxXRXpaR010WW1abU1tRmhNV016TXpBeQ; _dd_s=rum=0&expire=1756929431446&logs=0; main=V%7C2~P%7Cjobsearch~WID%7C3001~OSF%7Cquick&set=1756928485682; da_searchTerm=undefined",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "Priority": "u=0",
            "TE": "trailers",
        }
        payload = {
            "operationName": "jobDetails",
            "variables": {
                "jobId": job_id,
                "jobDetailsViewedCorrelationId": "",
                "sessionId": "",
                "zone": "anz-2",
                "locale": "en-NZ",
                "languageCode": "en",
                "countryCode": "NZ",
                "timezone": "Pacific/Auckland",
                "visitorId": "20a995b9-ec84-47cf-891e-b67fdd5ed341",
                "enableApplicantCount": False,
                "enableWorkArrangements": True,
            },
            "query": 'query jobDetails($jobId: ID!, $jobDetailsViewedCorrelationId: String!, $sessionId: String!, $zone: Zone!, $locale: Locale!, $languageCode: LanguageCodeIso!, $countryCode: CountryCodeIso2!, $timezone: Timezone!, $visitorId: UUID!, $enableApplicantCount: Boolean!, $enableWorkArrangements: Boolean!) {\n  jobDetails(\n    id: $jobId\n    tracking: {channel: "WEB", jobDetailsViewedCorrelationId: $jobDetailsViewedCorrelationId, sessionId: $sessionId}\n  ) {\n    ...job\n    insights @include(if: $enableApplicantCount) {\n      ... on ApplicantCount {\n        countLabel(locale: $locale)\n        volumeLabel(locale: $locale)\n        count\n        __typename\n      }\n      __typename\n    }\n    learningInsights(platform: WEB, zone: $zone, locale: $locale) {\n      analytics\n      content\n      __typename\n    }\n    gfjInfo {\n      location {\n        countryCode\n        country(locale: $locale)\n        suburb(locale: $locale)\n        region(locale: $locale)\n        state(locale: $locale)\n        postcode\n        __typename\n      }\n      workTypes {\n        label\n        __typename\n      }\n      company {\n        url(locale: $locale, zone: $zone)\n        __typename\n      }\n      __typename\n    }\n    workArrangements(visitorId: $visitorId, channel: "JDV", platform: WEB) @include(if: $enableWorkArrangements) {\n      arrangements {\n        type\n        label(locale: $locale)\n        __typename\n      }\n      label(locale: $locale)\n      __typename\n    }\n    seoInfo {\n      normalisedRoleTitle\n      workType\n      classification\n      subClassification\n      where(zone: $zone)\n      broaderLocationName(locale: $locale)\n      normalisedOrganisationName\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment job on JobDetails {\n  job {\n    sourceZone\n    tracking {\n      adProductType\n      classificationInfo {\n        classificationId\n        classification\n        subClassificationId\n        subClassification\n        __typename\n      }\n      hasRoleRequirements\n      isPrivateAdvertiser\n      locationInfo {\n        area\n        location\n        locationIds\n        __typename\n      }\n      workTypeIds\n      postedTime\n      __typename\n    }\n    id\n    title\n    phoneNumber\n    isExpired\n    expiresAt {\n      dateTimeUtc\n      __typename\n    }\n    isLinkOut\n    contactMatches {\n      type\n      value\n      __typename\n    }\n    isVerified\n    abstract\n    content(platform: WEB)\n    status\n    listedAt {\n      label(context: JOB_POSTED, length: SHORT, timezone: $timezone, locale: $locale)\n      dateTimeUtc\n      __typename\n    }\n    salary {\n      currencyLabel(zone: $zone)\n      label\n      __typename\n    }\n    shareLink(platform: WEB, zone: $zone, locale: $locale)\n    workTypes {\n      label(locale: $locale)\n      __typename\n    }\n    advertiser {\n      id\n      name(locale: $locale)\n      isVerified\n      registrationDate {\n        dateTimeUtc\n        __typename\n      }\n      __typename\n    }\n    location {\n      label(locale: $locale, type: LONG)\n      __typename\n    }\n    classifications {\n      label(languageCode: $languageCode)\n      __typename\n    }\n    products {\n      branding {\n        id\n        cover {\n          url\n          __typename\n        }\n        thumbnailCover: cover(isThumbnail: true) {\n          url\n          __typename\n        }\n        logo {\n          url\n          __typename\n        }\n        __typename\n      }\n      bullets\n      questionnaire {\n        questions\n        __typename\n      }\n      video {\n        url\n        position\n        __typename\n      }\n      displayTags {\n        label(locale: $locale)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  companyProfile(zone: $zone) {\n    id\n    name\n    companyNameSlug\n    shouldDisplayReviews\n    branding {\n      logo\n      __typename\n    }\n    overview {\n      description {\n        paragraphs\n        __typename\n      }\n      industry\n      size {\n        description\n        __typename\n      }\n      website {\n        url\n        __typename\n      }\n      __typename\n    }\n    reviewsSummary {\n      overallRating {\n        numberOfReviews {\n          value\n          __typename\n        }\n        value\n        __typename\n      }\n      __typename\n    }\n    perksAndBenefits {\n      title\n      __typename\n    }\n    __typename\n  }\n  companySearchUrl(zone: $zone, languageCode: $languageCode)\n  companyTags {\n    key(languageCode: $languageCode)\n    value\n    __typename\n  }\n  restrictedApplication(countryCode: $countryCode) {\n    label(locale: $locale)\n    __typename\n  }\n  sourcr {\n    image\n    imageMobile\n    link\n    __typename\n  }\n  __typename\n}',
        }
        response = session.post(
            "https://www.seek.co.nz/graphql", json=payload, headers=headers
        )
        response.raise_for_status()
        data = response.json()
        return cls(data, session)

    @property
    def title(self):
        return self.data["data"]["jobDetails"]["job"]["title"]

    @property
    def advertiser(self):
        return self.data["data"]["jobDetails"]["job"]["advertiser"]["name"]

    @property
    def categories(self):
        return [
            c["label"]
            for c in self.data["data"]["jobDetails"]["job"]["classifications"]
        ]

    @property
    def description(self):
        raw_description = self.data["data"]["jobDetails"]["job"]["content"]
        return re.sub(r"<.*?>", " ", raw_description)

    @property
    def address(self):
        return self.data["data"]["jobDetails"]["job"]["location"]["label"]

    @property
    def job_id(self):
        return self.data["data"]["jobDetails"]["job"]["id"]

    @property
    def url(self):
        return rf"https://www.seek.co.nz/jobs?jobId={self.job_id}"

    @property
    def employment_type(self):
        return self.data["data"]["jobDetails"]["job"]["workTypes"]["label"]

    @property
    def posted_date(self):
        date_string = self.data["data"]["jobDetails"]["job"]["listedAt"]["dateTimeUtc"]
        return datetime.fromisoformat(date_string).date()

    def get_item(self) -> dict:
        return {
            "title": self.title,
            "advertiser": self.advertiser,
            "categories": self.categories,
            "description": self.description,
            "address": self.address,
            "url": self.url,
            "employment_type": self.employment_type,
            "posted_date": self.posted_date,
        }


class SeekApi:
    def __init__(self, session=requests.Session()):
        self.api_url = "https://www.seek.co.nz/api/jobsearch/v5/search"
        self.session = session

    def search(
        self,
        query: str = None,
        id: str = None,
        where: str = "All New Zealand",
        page: int = 1,
    ) -> Iterator[SeekApiResult]:
        params = {
            "iteKey": "NZ-Main",
            "sourcesystem": "houston",
            "where": where,
            "page": f"{page}",
            "keywords": query,
            "jobId": id,
            "pageSize": "22",
            "include": "",
            "locale": "en-NZ",
            "source": "SEARCH_ENG",
            "relatedSearchesCount": "12",
            "queryHints": "spellingCorrection",
            "facets": "salaryMin,workArrangement,workType",
        }

        params = _delete_empty_values(params)

        response = self.session.get(self.api_url, params=params)
        response.raise_for_status()
        for data in response.json().get("data", []):
            job_id = data["id"]
            yield SeekApiResult.from_id(job_id, self.session)

    def from_url(self, url: str, **kwargs):
        """
        eg: https://www.seek.co.nz/jobs?jobId=86448735&type=promoted
        """
        patterns = [r"jobId=(\d+)", r"job\/(\d+)"]
        import re

        for pattern in patterns:
            results = re.findall(pattern, url)
            for result in results:
                yield from self.search(query=None, id=result, **kwargs)
