import scrapy
from urllib.parse import urljoin
from pathlib import Path
import rows
import itertools as it

SUSPECTED = "CASOS SUSPEITOS"
DISCARDED = "CASOS DESCARTADOS"
CONFIRMED = "CASOS CONFIRMADOS"


tokens = ["RN", "Total Geral"]


def clean_cities(cities):
    cities_it = iter(cities.replace("\n", ",").split(","))
    ct = []
    for city in cities_it:
        if "(" in city and ")" not in city:
            city = f"{city} {next(cities_it)}"
        ct.append(city)
    return ct


def clean(text):
    if text:
        return text.replace("\n", " ").strip()
    return ""


def change_format(number):
    if number:
        return number.replace(",", ".")
    return ""


class CovidRNSpider(scrapy.Spider):
    name = "covid-rn"

    start_urls = [
        "http://www.saude.rn.gov.br/Conteudo.asp?TRAN=ITEM&TARG=7549&ACT=&PAGE=0&PARM=&LBL=Boletins+Epidemiol%F3gicos"
    ]

    def parse(self, response):
        bulletins = response.xpath(
            "//div[@id='P000']/ul[1]/li/descendant-or-self::*[self::a[contains(@href, '.PDF')]]"
        )

        for bulletin in bulletins[:1]:
            data = {
                "bulletin_titulo": bulletin.xpath(".//text()").extract_first(),
                "bulletin_url": urljoin(
                    response.url, bulletin.xpath(".//@href").extract_first()
                ),
            }
            self.logger.info(str(data))

            yield scrapy.Request(
                data.get("bulletin_url"), meta={"row": data}, callback=self.read_pdf
            )

    def read_pdf(self, response):
        path = f"download/{Path(response.url).name}"
        self.logger.info("Saving PDF %s from %s", path, response.url)

        with open(path, "wb") as f:
            f.write(response.body)

        can_read = False
        data = {}
        city = None

        for row in rows.import_from_pdf(path):
            row = row._asdict()
            if (
                SUSPECTED in clean(row["field_1"])
                and DISCARDED in clean(row["field_2"])
                and CONFIRMED in clean(row["field_3"])
            ):
                can_read = True
                continue

            if can_read:
                city = list(row.values())[0]
                if len(city.split("\n")) > 3:
                    cities, suspected, discarded, confirmed = row.values()
                    cities = clean_cities(cities)
                    discarded = discarded.split("\n")

                    suspected = list(it.islice(suspected.split("\n"), 0, None, 2))
                    confirmed = list(it.islice(confirmed.split("\n"), 0, None, 2))

                    dt = list(zip(cities, suspected, discarded, confirmed))
                    for (a, b, c, d) in dt:
                        yield {
                            "municipio": a,
                            "suspeitos": change_format(b),
                            "descartados": change_format(c),
                            "confirmados": change_format(d),
                        }
                else:
                    city = clean(city)
                    data["municipio"] = city
                    data["suspeitos"] = row["field_1"].split("\n")[0]
                    data["descartados"] = row["field_2"]
                    data["confirmados"] = row["field_3"].split("\n")[0]
                yield data

            if city and any(city in text for text in tokens):
                break
