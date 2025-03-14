"""
Module for managing AWS Route 53 hosted zones using boto3.
"""

import boto3
import time


class Route53Manager:
    """
    A class to manage AWS Route 53 hosted zones.
    """

    def __init__(self):
        self.client = boto3.client("route53")

    def create_zone(self, domain_name: str, tags=None):
        """
        Create a hosted zone for the given domain name.

        :param domain_name: The domain name for the hosted zone.
        :param tags: List of tags that should be added for the hosted zone.
        """
        response = self.client.create_hosted_zone(
            Name=domain_name,
            CallerReference=str(time.time()),
            HostedZoneConfig={"Comment": "Subdomain takeover attempt"},
        )

        hosted_zone_id = response["HostedZone"]["Id"]
        name_servers = response["DelegationSet"]["NameServers"]

        if tags is not None:
            self.client.change_tags_for_resource(
                ResourceType="hostedzone",
                ResourceId=hosted_zone_id.split("/")[-1],
                AddTags=tags,
            )

        return hosted_zone_id, name_servers

    def delete_zone(self, zone_id):
        """
        Delete the hosted zone with the given zone ID.

        :param zone_id: The ID of the hosted zone to delete.
        """
        try:
            self.client.delete_hosted_zone(Id=zone_id)
        except self.client.exceptions.NoSuchHostedZone:
            pass

    def update_zone_comment(self, zone_id, new_comment):
        """
        Update comment of a hosted zone.

        :param zone_id: The ID of the hosted zone to update.
        :param new_comment: The new comment to be added.
        """
        response = self.client.update_hosted_zone_comment(
            Id=zone_id.split("/")[-1], Comment=new_comment
        )
        return response
