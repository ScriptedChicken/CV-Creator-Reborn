import requests
url = "https://www.seek.co.nz/graphql"
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZWcG9mM0dXQTN3cWVrTDV6ODVFZyJ9.eyJodHRwOi8vc2Vlay9jbGFpbXMvY291bnRyeSI6Ik5aIiwiaHR0cDovL3NlZWsvY2xhaW1zL2JyYW5kIjoic2VlayIsImh0dHA6Ly9zZWVrL2NsYWltcy9leHBlcmllbmNlIjoiY2FuZGlkYXRlIiwiaHR0cDovL3NlZWsvY2xhaW1zL3VzZXJfaWQiOiIzNTI3ODgwMCIsImlzcyI6Imh0dHBzOi8vbG9naW4uc2Vlay5jb20vIiwic3ViIjoiYXV0aDB8NWIwMGU3YTUxMzA0YjEyOTQzYmYyNDg5ZjE0MmI2NmUiLCJhdWQiOlsiaHR0cHM6Ly9zZWVrL2FwaS9jYW5kaWRhdGUiLCJodHRwczovL3NlZWthbnoub25saW5lYXV0aC5wcm9kLm91dGZyYS54eXovdXNlcmluZm8iXSwiaWF0IjoxNzAyMTg2OTEyLCJleHAiOjE3MDIxOTA1MTIsImF6cCI6ImdVMDdjc3BqQ0dZNElvNnJFT1c3a2FaTzZTY1E4SlVXIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBvZmZsaW5lX2FjY2VzcyJ9.DhU7dk-D_JVt2FlcWVD14r_9lo41rwGB2p1Uv1lTw4IO1L4PpE7d6tGDrBl4EL3XhEIbO3ZOC1m1U61zJBbCaEDHWn5ixNgr8ZH6r-l5MQUWnO4rWkIAx4lOPFlXnpUd3s0hIVGNNm7_jnUl08vrGHNWCR8BJqHN_oR0qrHvHsTCus97vFeyDJJDLXLxiSwV8PbdUQmwc9HXULc2xg8y2lIBF-I6zn77Cz2LcwR29eVoMvqyyxsulsR50nDLuF79tLEh5bZcQyyVTiw2Jfbw7r2AeD_udmXfV8Mm7iXurtkLXylegRMNxSlT0KrUQwqBMjr5mi8kKDCO8M3ZEdLsvg",
    "content-type": "application/json",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "seek-request-brand": "seek",
    "seek-request-country": "NZ",
    "x-seek-ec-sessionid": "b469ca6d-ed9a-4016-8a71-7a9eb4293370",
    "x-seek-ec-visitorid": "b469ca6d-ed9a-4016-8a71-7a9eb4293370",
    "x-seek-site": "chalice",
    "cookie": "JobseekerSessionId=b469ca6d-ed9a-4016-8a71-7a9eb4293370; JobseekerVisitorId=b469ca6d-ed9a-4016-8a71-7a9eb4293370; sol_id=e626743e-302d-4c15-9d77-aa128844b59b; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22qW13PrH4MnmvlnMvkik8%22%7D; _pin_unauth=dWlkPU1EY3hZV0poTlRFdE5EZzBNQzAwTlRZNUxXRTFNRFV0T0RObU5UVXhNakZrTURKaw; _hjSessionUser_335909=eyJpZCI6ImM1NjhkZjE2LTJmMzMtNTNhYi05Njk4LWE3OGEzYzU0ODlhNSIsImNyZWF0ZWQiOjE2ODc3Njc0ODkxMTcsImV4aXN0aW5nIjp0cnVlfQ==; __gads=ID=cdd21657055a77d9:T=1687768150:RT=1687768150:S=ALNI_MYK7zgadra6jJ2tsXiwHZ4pkcyhAw; __gpi=UID=00000c184add8091:T=1687768150:RT=1687768150:S=ALNI_MYAVlsREhZglYUVF9ngGPdRDRFyAQ; _gcl_au=1.1.1462053643.1697535682; _gcl_aw=GCL.1697614892.Cj0KCQjwhL6pBhDjARIsAGx8D59z43j7Z5bP5fWklcb0jhgJE1T1_iNkrAir4v-vGHDpRHyA3lkyr8MaAh4nEALw_wcB; _gcl_dc=GCL.1697614892.Cj0KCQjwhL6pBhDjARIsAGx8D59z43j7Z5bP5fWklcb0jhgJE1T1_iNkrAir4v-vGHDpRHyA3lkyr8MaAh4nEALw_wcB; _gac_UA-63910946-1=1.1697614892.Cj0KCQjwhL6pBhDjARIsAGx8D59z43j7Z5bP5fWklcb0jhgJE1T1_iNkrAir4v-vGHDpRHyA3lkyr8MaAh4nEALw_wcB; sol_id=e626743e-302d-4c15-9d77-aa128844b59b; _hjSessionUser_2818040=eyJpZCI6ImEzMzdiY2FhLWIyYzgtNWE2ZS1hMTZiLTNkMGM4MzRiYjZhNSIsImNyZWF0ZWQiOjE3MDE1Nzk3MjMwOTgsImV4aXN0aW5nIjpmYWxzZX0=; _ga_JYC9JXRYWC=GS1.1.1701579722.1.1.1701579813.34.0.0; last-known-sol-user-id=8ab4c8d46981c3009bf4afe05e4831aeab833ab923113ce2389132c6b13f4d09783f4649d340a143147988295853a0a721bce7b8bfe5488f9eb2a820d1c0badf17c398bf0c294908a552fbcdc6b3c96f36d397df211ee60fa130e0daa7abeddb9ac2fdbf95360feb76b3910ca657cd8278c5755f7e0822cd9c6b1abb018f8c149e7574e4df56aa465a777dc11758a441613f0af1c95557dc9794f5e628cd557f823af116e15c; _legacy_auth0.gU07cspjCGY4Io6rEOW7kaZO6ScQ8JUW.is.authenticated=true; auth0.gU07cspjCGY4Io6rEOW7kaZO6ScQ8JUW.is.authenticated=true; _gid=GA1.3.1307198124.1702026966; main=V%7C2~P%7Cjobsearch~K%7Cpython~WH%7CAll%20Australia~WID%7C3000~L%7C3000~OSF%7Cquick&set=1702097948335/V%7C2~P%7Cjobsearch~K%7Cpython~WH%7CAustralia~WID%7C3001~L%7C3001~OSF%7Cquick&set=1702060729852/V%7C2~P%7Cjobsearch~K%7Cpython~OSF%7Cquick&set=1702060719427; __cf_bm=yr5.u3jm6ePIJ1q9W.Mc.Z__YwIslsD2MXLPvuJ5aqg-1702185796-1-ASdyTi0f1CkhG1amKa10GIFgaoRA9k+9L0wwtn5+k4ufCqgWCPs862koHC6x/jQ0JsdT6mE7jyaWs84AfALf3Ow=; da_cdt=visid_0188f6c819f7002ee02f87b1ed260506f001706700fb8-sesid_1702185797805; _hjIncludedInSessionSample_335909=0; _hjSession_335909=eyJpZCI6IjQ4MDExYTZjLTU0NTUtNDhiNS1hYWI3LWI3YWZjNTQ5NmI1OSIsImNyZWF0ZWQiOjE3MDIxODU3OTgzMjcsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; _hjAbsoluteSessionInProgress=0; da_anz_candi_sid=1702185797805; utag_main=v_id:0188f6c819f7002ee02f87b1ed260506f001706700fb8$_sn:19$_se:4$_ss:0$_st:1702187689089$dc_visit:19$ses_id:1702185797805%3Bexp-session$_pn:2%3Bexp-session$_prevpage:home%3Bexp-1702189489092$dc_event:4%3Bexp-session$krux_sync_session:1702185797805%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session; _ga=GA1.1.1224671429.1687767489; _ga_SEQK0YEJZZ=GS1.1.1702185802.19.1.1702186480.60.0.0; _dd_s=rum=0&expire=1702187811768",
    "Referer": "https://www.seek.co.nz/",
    "Referrer-Policy": "no-referrer-when-downgrade"
}
payload = {
    "operationName": "searchLocationsSuggest",
    "variables": {
        "query": "a",
        "recentLocation": "",
        "count": 16,
        "locale": "en-NZ",
        "country": "nz",
        "visitorId": "e626743e-302d-4c15-9d77-aa128844b59b"
    },
    "query": "query searchLocationsSuggest($query: String!, $count: Int!, $recentLocation: String!, $locale: Locale, $country: CountryCodeIso2, $visitorId: UUID) {\n  searchLocationsSuggest(\n    query: $query\n    count: $count\n    recentLocation: $recentLocation\n    locale: $locale\n    country: $country\n    visitorId: $visitorId\n  ) {\n    __typename\n    suggestions {\n      ... on LocationSuggestion {\n        __typename\n        text\n        highlights {\n          start\n          end\n          __typename\n        }\n      }\n      ... on LocationSuggestionGroup {\n        __typename\n        label\n        suggestions {\n          text\n          highlights {\n            start\n            end\n            __typename\n          }\n          __typename\n        }\n      }\n      __typename\n    }\n  }\n}\n"
}
res = requests.post(url, data=payload, headers=headers)
print(res.status_code)
print(res.text)
res_data = res.json().get('data')
location_list = [suggestion['text'] for suggestion in res_data['searchLocationsSuggest']['suggestions']]
print(location_list)
