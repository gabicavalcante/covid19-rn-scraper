import scrapy
from urllib.parse import urljoin
from pathlib import Path
import rows

SUSPEITOS = "CASOS SUSPEITOS"
DESCARTADOS = "CASOS DESCARTADOS"
CONFIRMADOS = "CASOS CONFIRMADOS"

BULLETIN_TAG = (
    "boletimcovid_19"
    "epidemiologicosemana_epidemiologica_"
    "01_a_17_de_2020"
)


def clean(text):
    if text:
        return text.replace("\n", " ").strip()
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
                SUSPEITOS in clean(row["field_1"])
                and DESCARTADOS in clean(row["field_2"])
                and CONFIRMADOS in clean(row["field_3"])
            ):
                can_read = True
                continue

            if can_read:
                city = clean(list(row.values())[0])
                data["municipio"] = city
                data["suspeitos"] = row["field_1"].split("\n")[0]
                data["descartados"] = row["field_2"]
                data["confirmados"] = row["field_3"].split("\n")[0]
                yield data

            if city and city == "RN":
                break
