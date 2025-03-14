"""
Module for making DNS queries to find the authoritative AWS name servers.
"""
import dns.resolver
import dns.message
import dns.query
import dns.rdatatype
import dns.name


class DNSResolver:
    """
    A class to manage DNS resolution and delegation chain lookups.
    """

    ROOT_NS = "198.41.0.4"  # IP of a.root-servers.net

    def resolve_ns_ip(self, nameserver):
        """
        Resolve a nameserver hostname to its IP address.

        :param nameserver: The nameserver hostname.
        :return: The IP address of the nameserver or None if resolution fails.
        """
        try:
            answer = dns.resolver.resolve(nameserver, "A")
            return answer[0].to_text() if answer else None
        except Exception:
            return None

    def non_recursive_lookup(self, name, nameserver, rtype):
        """
        Perform a non-recursive lookup.

        :param name: The domain name to query.
        :param nameserver: The nameserver to query.
        :param rtype: The record type to query.
        :return: The DNS response or None if the query fails.
        """
        try:
            query = dns.message.make_query(name, rtype)
            response = dns.query.udp(query, nameserver, timeout=3)
            return response
        except Exception as e:
            print(f"Error querying {nameserver} for {name}: {e}")
            return None

    def find_delegation_chain(self, domain, max_depth=40):
        """
        Follow the delegation chain from the root to the target domain.

        :param domain: The target domain.
        :param max_depth: The maximum depth to follow the delegation chain.
        :return: A list of delegation nameservers.
        """
        delegation_ns = [{"name": ".", "ns": self.ROOT_NS}]
        domain = dns.name.from_text(domain)

        for depth in range(max_depth):
            if not delegation_ns:
                return []
            current_ns = delegation_ns[0]["ns"]
            print(f"[{depth+1}] Querying {current_ns} for NS records of {domain}")

            response = self.non_recursive_lookup(
                domain.to_text(), current_ns, dns.rdatatype.NS
            )
            if not response or response.rcode() != dns.rcode.NOERROR:
                return delegation_ns

            new_delegation_ns = []
            for rrset in response.authority:
                if rrset.rdtype == dns.rdatatype.NS:
                    for ns in rrset:
                        ns_domain = ns.to_text().rstrip(".")
                        ns_ip = self.resolve_ns_ip(ns_domain)
                        if ns_ip:
                            new_delegation_ns.append(
                                {
                                    "name": rrset.name.to_text(),
                                    "ns": ns_ip,
                                    "ns_domain": ns_domain,
                                }
                            )

            delegation_ns = new_delegation_ns if new_delegation_ns else delegation_ns

        return delegation_ns

    def get_aws_ns_servers(self, domain):
        """
        Retrieve AWS nameservers from the delegation chain.

        :param domain: The target domain.
        :return: A list of AWS nameservers.
        """
        aws_ns_servers = []
        for ns in self.find_delegation_chain(domain):
            ns_domain = ns["ns_domain"].rstrip(".")
            if ns_domain.startswith("ns-") and "awsdns" in ns_domain:
                aws_ns_servers.append(ns_domain)
        return aws_ns_servers
