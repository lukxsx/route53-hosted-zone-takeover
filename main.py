import argparse
from dnsquery import DNSResolver
from takeover import brute_force
from logger_config import setup_logging

logger = setup_logging()

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

args = parser.parse_args()



def main():
    dns_resolver = DNSResolver()
    #manager = Route53Manager()
    name_servers = dns_resolver.get_aws_ns_servers(args.domain)
    logger.info(name_servers)
    result = brute_force(args.domain, name_servers, args.max_attempts)
    print(result)


if __name__ == "__main__":
    main()
