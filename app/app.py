import falcon
from falcon_cors import CORS
import json

from app.middleware import SessionWrapper, JSendTranslator
from resources import (
    MeResource,
    UsersResource,
    ProtocolsResource,
    ProtocolResource,
    SharedProtocolsResource,
    SharedProtocolResource,
    PublicProtocolsResource,
    ProtocolVersionsResource,
    ProtocolVersionResource,
    OrganizationsResource,
    OrganizationResource,
    OrganizationMembersResource,
    OrganizationMemberResource,
    OrganizationGroupsResource,
    OrganizationGroupResource,
    OrganizationGroupMembersResource,
    OrganizationGroupMemberResource,
    OrganizationMDSLinksResource,
    OrganizationMDSLinkResource,
    OrganizationMDSLinkProtocolsResource,
    OrganizationMDSLinkProtocolResource,
    OrganizationMDSLinkSynchronizeResource,
)

cors = CORS(allow_all_origins=True)

app = falcon.API(
    middleware=[
        SessionWrapper(),
        JSendTranslator(),
        cors.middleware,
    ]
)

# Users
me = MeResource()
users = UsersResource()

app.add_route('/users/', users)
app.add_route('/users/me', me)

# Protocols
protocol = ProtocolResource()
protocols = ProtocolsResource()

app.add_route('/protocols/', protocols)
app.add_route('/protocols/{protocol_id}', protocol)

# Public Protocols
public_protocols = PublicProtocolsResource()
app.add_route('/protocols/public', public_protocols)

# Shared Protocols
shared_protocol = SharedProtocolResource()
shared_protocols = ProtocolsResource()
app.add_route('/organizations/{organization_id}/protocols/', shared_protocols)
app.add_route('/organizations/{organization_id}/protocols/{protocol_id}', shared_protocol)


# Protocol Versions
protocol_versions = ProtocolVersionsResource()
protocol_version = ProtocolVersionResource()

app.add_route('/protocols/{protocol_id}/versions/', protocol_versions)
app.add_route('/protocols/{protocol_id}/versions/{version_id}', protocol_version)


# Organizations
organizations = OrganizationsResource()
organization = OrganizationResource()

app.add_route('/organizations/', organizations)
app.add_route('/organizations/{organization_id}', organization)


# Organization Members
organization_members = OrganizationMembersResource()
organization_member = OrganizationMemberResource()

app.add_route('/organizations/', organization_members)
app.add_route('/organizations/{organization_id}', organization_member)


# Organization Groups
organization_group = OrganizationGroupResource()
organization_groups = OrganizationGroupsResource()

app.add_route('/organizations/{organization_id}/groups', organization_groups)
app.add_route('/organizations/{organization_id}/groups/{group_id}', organization_group)


# Organization Group Members
organization_group_member = OrganizationGroupMemberResource()
organization_group_members = OrganizationGroupMembersResource()

app.add_route(
    '/organizations/{organization_id}/groups/{group_id}/members',
    organization_group_members
)
app.add_route(
    '/organizations/{organization_id}/groups/{group_id}/members/{member_id}',
    organization_group_member
)


# Organization MDS Links
organization_mds_link = OrganizationMDSLinkResource()
organization_mds_links = OrganizationMDSLinksResource()

app.add_route(
    '/organizations/{organization_id}/mds_links/',
    organization_mds_links
)
app.add_route(
    '/organizations/{organization_id}/mds_links/{mds_link_id}',
    organization_mds_link
)


# Organization MDS Link Protocols
organization_mds_link_protocols = OrganizationMDSLinkProtocolsResource()
organization_mds_link_protocol = OrganizationMDSLinkProtocolResource()
organization_mds_link_synchronize = OrganizationMDSLinkSynchronizeResource()

app.add_route(
    '/organizations/{organization_id}/mds_links/{mds_link_id}/protocols/',
    organization_mds_link_protocols
)
app.add_route(
    '/organizations/{organization_id}/mds_links/{mds_link_id}/protocols/{protocol_id}',
    organization_mds_link_protocol
)
app.add_route(
    '/organizations/{organization_id}/mds_links/{mds_link_id}/synchronize',
    organization_mds_link_synchronize
)
