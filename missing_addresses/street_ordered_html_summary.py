import locale
from pathlib import Path
from yattag import Doc, indent
from missing_addresses import Address, StreetDiff, AddressDiff, AddressDiffMetaData
from typing import Dict
from datetime import datetime

script_path = Path(__file__).parent.absolute()


class StreetOrderedHtmlSummary:
    def __housenumbers_order(self, info: tuple) -> tuple:
        return info[0].housenumber.sort_key()

    def __format_date(self, dt: datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def write(self, streets: Dict[str, StreetDiff], diff: AddressDiff, metadata: AddressDiffMetaData, file_path: str):
        locale.setlocale(locale.LC_ALL, "")
        ordered_streets = sorted(streets.keys(), key=locale.strxfrm)

        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                doc.stag('meta', charset='utf-8')
                with tag('title'):
                    text(f'Missing Addresses of {metadata.area_name}')
                with tag('style'):
                    doc.asis(Path(script_path, "main.css").read_text())
            with tag('body'):
                with tag('h1'):
                    text(f'Missing Addresses of {metadata.area_name}')
                with tag('p'):
                    text(f'Generated on ')
                    with tag('span', id="generationDatetime"):
                        text(f'{self.__format_date(metadata.generation_date)}')
                    text(f', ',
                         f'OpenStreetMap data from {self.__format_date(metadata.actual_date)}, '
                         f'reference data from {self.__format_date(metadata.reference_date)}')

                doc.asis(Path(script_path, "toolbox.html").read_text())

                with tag('table', id='mainTable', klass='sticky'):
                    with tag('thead'):
                        with tag('tr'):
                            with tag('th'):
                                text('Street Name')
                            with tag('th', klass='matches'):
                                text('matches')
                            with tag('th', klass='missing'):
                                text('missing')
                            with tag('th', klass='surplus'):
                                text('surplus')
                    with tag('tbody'):
                        name: str
                        for name in ordered_streets:
                            with tag('tr', name=name):
                                a: Address
                                with tag('td'):
                                    doc.asis(name)
                                with tag('td', klass='matches'):
                                    with tag('span'):
                                        text(f'{len(streets[name].matches)}: ')
                                    for (a, m) in sorted(streets[name].matches.items(), key=self.__housenumbers_order):
                                        with tag('a-i', p=f'{m.osm_primitive.type[0:1]}{m.osm_primitive.id}',
                                                        c=f'{m.coordinate.lat},{m.coordinate.lon}'):
                                            text(f"{str(a.housenumber)}")
                                with tag('td', klass='missing'):
                                    with tag('span'):
                                        text(f'{streets[name].num_missing_not_ignored}: ')
                                    for (a, m) in sorted(streets[name].missing.items(), key=self.__housenumbers_order):
                                        if m.ignore_information is None:
                                            attributes = ()
                                        else:
                                            attributes = ('ignored', ('reason', m.ignore_information.reason))
                                        with tag('a-m', c=f'{m.coordinate.lat},{m.coordinate.lon}', *attributes):
                                            text(f"{str(a.housenumber)}")
                                with tag('td', klass='surplus'):
                                    with tag('span'):
                                        text(f'{streets[name].num_surplus_not_ignored}: ')
                                    for (a, s) in sorted(streets[name].surplus, key=self.__housenumbers_order):
                                        if s.ignore_information is None:
                                            attributes = ()
                                        else:
                                            attributes = ('ignored', ('reason', s.ignore_information.reason))
                                        with tag('a-s', p=f'{s.osm_primitive.type[0:1]}{s.osm_primitive.id}', *attributes):
                                            text(f"{str(a.housenumber)}")
                    with tag('tfoot'):
                        with tag('tr'):
                            with tag('th'):
                                text('Total')
                            with tag('th', klass='matches'):
                                text(str(diff.num_matches))
                            with tag('th', klass='missing'):
                                text(f'{diff.num_missing_not_ignored} ({len(diff.missing) - diff.num_missing_not_ignored})')
                            with tag('th', klass='surplus'):
                                text(f'{diff.num_surplus_not_ignored} ({len(diff.surplus) - diff.num_surplus_not_ignored})')
                        with tag('tr'):
                            with tag('th'):
                                text(str(diff.num_reference))
                            with tag('th', klass='matches'):
                                text(f'{diff.coverage_in_percent: 3.1f}%')
                            with tag('th', klass='missing'):
                                text(f'{diff.num_missing_not_ignored / diff.num_reference * 100.0: 3.1f}%')
                            with tag('th', klass='surplus'):
                                text(f'{diff.num_surplus_not_ignored / diff.num_reference * 100.0: 3.1f}%')

                with tag('script'):
                    doc.asis(Path(script_path, "main.js").read_text())

        html: str = indent(doc.getvalue(), indentation=' ')  # do not indent, just add line breaks

        f = open(file_path, "w+", encoding='utf-8')
        f.write(html)
        f.close()

