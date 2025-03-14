from route53 import Route53Manager
import time
from logger_config import setup_logging

logger = setup_logging()


def brute_force(domain_name, target_ns, attempt_limit):
    """
    Perform brute force attempts to generate and delete Route 53 hosted zones.

    :param domain_name: The domain name for the hosted zone.
    :param target_ns: List of target name servers (max 4 items).
    :param attempt_limit: Maximum number of attempts.
    :return: Status object indicating success, domain name, target name servers, found name server, attempt count, and elapsed time.
    """
    manager = Route53Manager()
    parent_domain = ".".join(domain_name.rstrip(".").split(".")[1:])
    attempts = 0
    start_time = time.time()
    ns_seen = {}

    while attempts < attempt_limit:
        attempts += 1
        logger.info("Attempt %d: Creating hosted zone for %s", attempts, parent_domain)

        zone_id, name_servers = manager.create_zone(parent_domain)
        formatted_ns = ", ".join(f"{ns} ({ns_seen[ns]})" for ns in name_servers)
        logger.info("Zone ID: %s, got AWS name servers: %s", zone_id, formatted_ns)

        found_ns = [ns for ns in target_ns if ns in name_servers]
        for ns in found_ns:
            if ns in ns_seen:
                ns_seen[ns] += 1
            else:
                ns_seen[ns] = 1

        if found_ns:
            elapsed_time = time.time() - start_time
            result_obj = {
                "success": True,
                "domain_name": domain_name,
                "target_ns": target_ns,
                "found_ns": found_ns,
                "attempts": attempts,
                "elapsed_time": elapsed_time,
                "unique_ns": len(ns_seen.keys()),
            }
            logger.info(result_obj)
            return result_obj

        logger.info(
            "No match found. Deleting... Encountered %d unique AWS name servers so far.",
            len(ns_seen.keys()),
        )
        manager.delete_zone(zone_id)
        time.sleep(1)

    if attempts >= attempt_limit:
        logger.info("Maximum number of attempts tried")

    elapsed_time = time.time() - start_time
    result_obj = {
        "success": False,
        "domain_name": domain_name,
        "target_ns": target_ns,
        "found_ns": None,
        "attempts": attempts,
        "elapsed_time": elapsed_time,
        "unique_ns": len(ns_seen.keys()),
    }
    logger.info(result_obj)
    return result_obj
