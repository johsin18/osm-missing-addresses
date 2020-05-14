from dataclasses import dataclass
from datetime import date, datetime


@dataclass()
class IgnoredAddressInformation:
    exists: bool
    reason: str
    ignore_date: date

    @staticmethod
    def parse_ignore_date(param) -> date:
        return datetime.strptime(param, IgnoredAddressInformation.get_date_format()).date()

    @staticmethod
    def get_date_format():
        return '%Y-%m-%d'
