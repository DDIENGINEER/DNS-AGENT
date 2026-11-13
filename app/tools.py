import json
from pathlib import Path

# Locate project data directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_dataset(filename):
    """Load mock DNS data from JSON."""
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def search_private_dns(hostname):
    """Search for a hostname in private DNS."""

    records = load_dataset("private_dns.json")

    return [
        record for record in records
        if record["hostname"].lower() == hostname.lower()
    ]


def search_public_dns(hostname):
    """Search for a hostname in public DNS."""

    records = load_dataset("public_dns.json")

    return [
        record for record in records
        if record["hostname"].lower() == hostname.lower()
    ]


def validate_regional_dns(hostname):
    """Check DNS resolution across regions."""

    records = load_dataset("regional_resolution.json")

    return [
        record for record in records
        if record["hostname"].lower() == hostname.lower()
    ]


def identify_dns_hosting(hostname):
    """Identify the hosting platform and DNS zone."""

    inventory = load_dataset("hosting_inventory.json")

    matching_records = []

    for record in inventory:
        zone = record["zone"].lower()

        if hostname.lower() == zone or hostname.lower().endswith("." + zone):
            matching_records.append(record)

    return matching_records