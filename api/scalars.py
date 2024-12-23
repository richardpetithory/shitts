from datetime import date

from ariadne import ScalarType

date_scalar = ScalarType("Date")


@date_scalar.serializer
def date_serialize(value: date):
    """
    Datetime serializer iso8601
    designed to replace iso8601 decorator
    """
    if hasattr(value, "isoformat"):
        return value.isoformat()

    return ""


@date_scalar.value_parser
def date_parse(value):
    return date.fromisoformat(value)


scalars = [date_scalar]
