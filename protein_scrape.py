import requests
from bs4 import BeautifulSoup
import html_to_json
from urllib.parse import urlparse
from pprint import pprint as pp
import os

class ProteinGetter:
    def __init__(self) -> None:
        self.domain = None
        self.deal_meta_data_list = []
    
    def __repr__(self) -> str:
        self.deal_meta_data

    def get_url(self, uri, headers=None, payload=None) -> requests.Response:
        self.domain = urlparse(uri).netloc
        default_headers = {
            "User-Agent": "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        }
        if not headers:
            headers = default_headers
        if not payload:
            payload = {}
        get_page = requests.get(url=f"{uri}", headers=headers, params=payload)
        return get_page

    def __create_static_file_2_parse(self, requests_response_obj) -> None:
        # use domain name as file name
        "TODO: error check incoming object type, add meta data to init for reuse, for __read_in_static_file it should have file name already"
        with open(f"{self.domain}.html", "w") as htmlfile:
            soup = BeautifulSoup(requests_response_obj.content, "html.parser")
            soup_content = soup.prettify()
            htmlfile.write(soup_content)

    def __read_in_static_file(self) -> None:
        with open(f"{self.domain}.html", "r") as htmlfile:
            output_json = html_to_json.convert(htmlfile)

    def parse_results(self, requests_response_obj: requests.Response):
        raise NotImplementedError


class MuscleAndStrengthProtein(ProteinGetter):
    def __init__(self) -> None:
        super().__init__()
        self.uri = os.environ.get("MuscleAndStrengthProtein")

    def get_url(self, headers=None, payload=None) -> requests.Response:
        return super().get_url(self.uri, headers, payload)

    def parse_results(self, requests_response_obj: requests.Response):
        assert isinstance(requests_response_obj, requests.Response)
        soup = BeautifulSoup(requests_response_obj.content, "html.parser").prettify()
        output_json = html_to_json.convert(soup)
        try:
            deals_section = output_json["html"][0]["body"][0]["main"][0]["article"][0][
                "section"
            ]
        except Exception as err:
            raise KeyError(
                "Top level args changed, either body, main, article, or section have changed."
            )
        try:
            iterable_deals = deals_section[0]["div"][0]["div"][0]["div"]
        except Exception as err:
            raise KeyError("Second level args changed, trying to access 3 nested divs.")
        for protein_deal in iterable_deals:
            try:
                individual_deal_attributes = protein_deal["div"][0]["div"]
            except Exception as err:
                raise KeyError(
                    "Individual deal attributes failing to parse 2 divs at deal level."
                )
            try:
                price = individual_deal_attributes[2]["div"][1]["span"][0]["_value"]
            except Exception as err:
                raise KeyError("Could not retrieve price, structure changed.")
            try:
                link = self.domain + individual_deal_attributes[2]["div"][2]["a"][0]["_attributes"][
                    "href"
                ]
            except Exception as err:
                raise KeyError("Could not retrieve link to item, structure changed.")
            try:
                product_description = individual_deal_attributes[1]["div"][0]["_value"]
            except Exception as err:
                raise KeyError(
                    "Could not retrieve product description, structure changed."
                )
            try:
                deal = individual_deal_attributes[2]["span"][0]["_value"]
            except Exception as err:
                raise KeyError(
                    "Could not retrieve deal banner details, structure changed."
                )
            deal_dict = dict({product_description: {"Price": price, "Link": link, "Deal": deal}})
            self.deal_meta_data_list.append(deal_dict)

        return self.deal_meta_data_list


