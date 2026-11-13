from app.tools import (
    search_private_dns,
    search_public_dns,
    validate_regional_dns,
    identify_dns_hosting
)

hostname = "api.example.com"

print("\n===== PRIVATE DNS =====")
print(search_private_dns(hostname))

print("\n===== PUBLIC DNS =====")
print(search_public_dns(hostname))

print("\n===== REGIONAL VALIDATION =====")
print(validate_regional_dns(hostname))

print("\n===== DNS HOSTING =====")
print(identify_dns_hosting(hostname))