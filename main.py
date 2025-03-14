from dnsquery import DNSResolver
from route53 import Route53Manager
from takeover import brute_force

def main():
    dns_resolver = DNSResolver()
    manager = Route53Manager()
    name_servers = dns_resolver.get_aws_ns_servers("sub.example.com")
    print(name_servers)
    result = brute_force(manager, "sub.example.com", name_servers, 1000)
    print(result)


if __name__ == "__main__":
    main()
