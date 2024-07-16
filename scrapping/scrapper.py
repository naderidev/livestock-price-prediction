from bs4 import BeautifulSoup
import requests
import dataclasses
from persiantools import digits


@dataclasses.dataclass
class DataRow:
    province_title: str
    product_type: str
    min_price: int
    max_price: int
    date: list

    def get_mean_price(self) -> float:
        return (
            (self.min_price + self.max_price) / 2
            if self.min_price != 0 and self.max_price != 0.0
            else 0
        )

    def to_csv_row(self):
        return f"{self.province_title},{self.get_mean_price()},{self.product_type},{self.date[0]},{self.date[1]},{self.date[2]}"


class Scrapper:
    PAGE_URL: str = (
        "https://www.itpnews.com/price/show/%D8%AF%D8%A7%D9%85+%D8%B2%D9%86%D8%AF%D9%87/301"
    )
    session: requests.Session

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.cookies.update({"_mj_vwport_": "1536"})

    def _make_request(self, date: list[int] = None) -> requests.Response:
        return self.session.request(
            method="POST",
            url=Scrapper.PAGE_URL,
            files=(
                [
                    ("price_d", (None, str(date[2]))),
                    ("price_m", (None, str(date[1]))),
                    ("price_y", (None, str(date[0]))),
                ]
            ),
        )

    def get_data(self, product_types: list[str], date: list) -> list[DataRow]:
        req = self._make_request(date)
        if not req.ok:
            raise ConnectionError("The Request wasn't successful!")

        soup = BeautifulSoup(req.content.decode(), features="html.parser")
        return (
            sum(self.__parse_table(soup, date, product_types) , [])
            if self.__is_valid_date(soup, date)
            else []
        )

    def __parse_table(
        self, soup: BeautifulSoup, date: list[int], product_types: list[str]
    ) -> list:
        return list(
            map(
                lambda r: list(
                    filter(
                        lambda x: x != None,
                        [
                            (
                                DataRow(
                                    province_title=list(r.children)[1].text,
                                    product_type="گوسفند",
                                    min_price=int(
                                        list(r.children)[3].text.replace(",", "")
                                    ),
                                    max_price=int(
                                        list(r.children)[4].text.replace(",", "")
                                    ),
                                    date=date,
                                )
                                if "گوسفند" in product_types
                                else None
                            ),
                            (
                                DataRow(
                                    province_title=list(r.children)[1].text,
                                    product_type="گوساله",
                                    min_price=int(
                                        list(r.children)[5].text.replace(",", "")
                                    ),
                                    max_price=int(
                                        list(r.children)[6].text.replace(",", "")
                                    ),
                                    date=date,
                                )
                                if "گوساله" in product_types
                                else None
                            ),
                        ],
                    )
                ),
                soup.find("table", attrs={"class", "price_table"}).find_all("tr")[2:-1],
            )
        )

    def __is_valid_date(self, soup: BeautifulSoup, date:list) -> list[int]:
        return soup.text.find(digits.en_to_fa(f"{str(date[0])[-2:]}/{date[1]:02d}/{date[2]:02d}")) != -1
