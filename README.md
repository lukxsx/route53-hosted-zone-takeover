# AWS Route 53 Hosted Zone Takeover

This tool attempts to take over AWS Route 53 hosted zones by brute-forcing the zones until a zone with the desired AWS nameservers is reached. It allows testing of NS assignments and adding DNS records upon successful takeover.

## Features

- Brute force AWS Route 53 hosted zones.
- Specify maximum attempts for takeover.
- Add DNS records upon successful takeover.
- Logging of operations.

## Usage

python3 main.py [options] <domain>

### Options

- `domain`: The domain name for the hosted zone.
- `--max_attempts VALUE`: Maximum attempts to try to perform takeover (default: 1000).
- `--record_type VALUE`: The type of the DNS record (A, AAAA, CNAME, MX, NS, PTR, SOA, SPF, SRV, TXT).
- `--record_name VALUE`: The name of the DNS record.
- `--record_value VALUE`: The value of the DNS record.
- `--tags TAGS`: AWS tags in key=value format.

### Example

    python3 main.py --max_attempts 1000 --record_type A --record_name sub.example.com --record_value 192.0.2.1 --tags Project=Takeover sub.example.com

