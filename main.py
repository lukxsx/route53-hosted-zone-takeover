from dnsquery import DNSResolver
from takeover import brute_force
from logger_config import setup_logging

logger = setup_logging()

def main():
    dns_resolver = DNSResolver()
    #manager = Route53Manager()
    name_servers = dns_resolver.get_aws_ns_servers("example.com")
    logger.info(name_servers)
    result = brute_force("example.com", name_servers, 1000)
    print(result)


if __name__ == "__main__":
    main()
