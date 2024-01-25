import os
import csv
import logging

from rigour.data import DATA_PATH
from rigour.langs.util import normalize_code

# https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab
log = logging.getLogger(__name__)

TEMPLATE = """# This file is automatically generated, do not edit it.
from typing import Dict, Set

ISO3_ALL: Set[str] = set(%r)  # noqa
ISO3_MAP: Dict[str, str] = %r  # noqa
ISO2_MAP: Dict[str, str] = %r  # noqa
"""


def update_data():
    iso3_ids = set()
    iso2_map = {}
    iso3_map = {}

    lang_path = DATA_PATH / "langs"
    path = os.path.dirname(__file__)
    source_file = os.path.join(path, lang_path / "iso-639-3.tab")
    with open(source_file, "r", encoding="utf-8") as ufh:
        for row in csv.DictReader(ufh, delimiter="\t"):
            iso3 = normalize_code(row.pop("Id"))
            if iso3 is None or len(iso3) != 3:
                continue
            iso3_ids.add(iso3)

            part1 = normalize_code(row.pop("Part1"))
            if part1 is not None:
                iso3_map[part1] = iso3
                iso2_map[iso3] = part1

            part2b = normalize_code(row.pop("Part2B"))
            if part2b is not None:
                iso3_map[part2b] = iso3

            part2t = normalize_code(row.pop("Part2T"))
            if part2t is not None:
                iso3_map[part2t] = iso3

            ref_name = normalize_code(row.pop("Ref_Name"))
            if ref_name is not None and len(ref_name) > 3:
                iso3_map[ref_name] = iso3

            # print(row)

    with open(lang_path / "iso639.py", "w", encoding="utf-8") as ofh:
        data = TEMPLATE % (list(sorted(iso3_ids)), iso3_map, iso2_map)
        ofh.write(data)

    # doc = html.fromstring(res.content)
    # for row in doc.findall('.//table//table/tr'):
    #     cells = [c.text_content().strip() for c in row.findall('.//td')]
    #     if len(cells) != 5:
    #         continue
    #     iso3, iso2, english, french, german = cells
    #     if not len(iso2):
    #         iso2 = None
    #     iso3 = iso3.split(')')
    #     iso3 = [c.split('(')[0].strip() for c in iso3]
    #     iso3 = [c for c in iso3 if len(c)]
    #     print(iso3, iso2)


if __name__ == "__main__":
    update_data()
