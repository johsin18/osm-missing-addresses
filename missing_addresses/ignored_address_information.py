from dataclasses import dataclass
from datetime import date, datetime


@dataclass()
class IgnoredAddressInformation:
    exists: bool
    """Whether the address exists in reality, or not"""
    reason: str
    """Reason for the address being ignored"""
    ignore_date: date
    """Date when the decision to ignore this address was made"""

    @staticmethod
    def parse_ignore_date(param) -> date:
        return datetime.strptime(param, IgnoredAddressInformation.get_date_format()).date()

    @staticmethod
    def get_date_format():
        return '%Y-%m-%d'
