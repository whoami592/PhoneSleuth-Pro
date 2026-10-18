"""Phone number parsing and metadata. No subscriber lookup is performed."""
from dataclasses import asdict, dataclass
from phonenumbers import (
    NumberParseException, PhoneNumberFormat, format_number, is_possible_number,
    is_valid_number, parse, region_code_for_number, carrier, geocoder, timezone,
)

@dataclass
class NumberAnalysis:
    input_number: str
    international_format: str | None
    national_format: str | None
    country_code: int | None
    region: str | None
    possible: bool
    valid_numbering_plan: bool
    number_type: str
    carrier_metadata: str | None
    location_metadata: str | None
    time_zones: list[str]
    note: str = "Metadata only; does not identify a subscriber, owner, live status, or location."

def analyze_number(raw: str, default_region: str | None = None) -> dict:
    raw = (raw or "").strip()
    if not raw:
        raise ValueError("Enter a phone number.")
    try:
        n = parse(raw, default_region)
    except NumberParseException as exc:
        raise ValueError(f"Could not parse phone number: {exc}") from exc
    possible = is_possible_number(n)
    valid = is_valid_number(n)
    type_name = str(__import__("phonenumbers").number_type(n)).replace("PhoneNumberType.", "")
    result = NumberAnalysis(
        input_number=raw,
        international_format=format_number(n, PhoneNumberFormat.INTERNATIONAL),
        national_format=format_number(n, PhoneNumberFormat.NATIONAL),
        country_code=n.country_code,
        region=region_code_for_number(n),
        possible=possible,
        valid_numbering_plan=valid,
        number_type=type_name,
        carrier_metadata=carrier.name_for_number(n, "en") or None,
        location_metadata=geocoder.description_for_number(n, "en") or None,
        time_zones=list(timezone.time_zones_for_number(n)),
    )
    return asdict(result)
