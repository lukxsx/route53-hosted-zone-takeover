# AWS Route 53 Hosted Zone Takeover

This tool attempts to take over AWS Route 53 hosted zones by brute-forcing the zones until a zone with the desired AWS nameservers is reached. It allows testing of NS assignments and adding DNS records upon successful takeover.

The tool is utilizing the takeover method described in [this blogpost](https://www.form3.tech/blog/engineering/dangling-danger).

## Features

- Brute force AWS Route 53 hosted zones.
- Specify maximum attempts for takeover.
- Add DNS records upon successful takeover.
- Logging of operations.

## Installation

It is recommended to use the [`uv`](https://github.com/astral-sh/uv) package manager for Python to run this project.

    uv sync

Alternatively, you can use `pip` with the included `requirements.txt`. In the later usage steps, replace `uv run` with `python`.

    pip install -r requirements.txt

## Usage

    uv run main.py [options] <domain>

### Options

- `domain`: The domain name for the hosted zone.
- `--max_attempts VALUE`: Maximum attempts to try to perform takeover (default: 1000).
- `--record_type VALUE`: The type of the DNS record (A, AAAA, CNAME, MX, NS, PTR, SOA, SPF, SRV, TXT).
- `--record_name VALUE`: The name of the DNS record.
- `--record_value VALUE`: The value of the DNS record.
- `--tags TAGS`: AWS tags in key=value format.

### Example

    uv run main.py --max_attempts 1000 --record_type A --record_name sub.example.com --record_value 192.0.2.1 --tags Project=Takeover sub.example.com

