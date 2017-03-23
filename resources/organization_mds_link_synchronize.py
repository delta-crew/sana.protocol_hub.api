from app.hooks import *
import falcon
import requests
import urllib.parse
from sqlalchemy.orm import joinedload

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLinkProtocol, OrganizationMDSLink, Protocol


class OrganizationMDSLinkSynchronizeResource(object):
    def upload_protocol_to_mds(self, mds, protocol):
        url = urllib.parse.urljoin(mds.url, '/endpoint')
        username = mds.username
        password = mds.password

        # TODO Matt, what do we send here? What HTTP verb? What content type?
        data = {
            'id': protocol.id,
            'xml': protocol.content
        }

        r = requests.post(url + '/user', auth=(username, password), data=data)

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.synchronize_mds))
    def on_post(self, req, res, organization_id, mds_link_id):
        session = req.context['session']

        mds = session.query(OrganizationMDSLink).get(mds_link_id)

        synced_protocols = session.query(OrganizationMDSLinkProtocol).\
                filter_by(
                    organization_id=organization_id,
                    mds_link_id=mds_link_id,
                ).\
                all()

        for synced_protocol in synced_protocols:
            updated_protocol = session.query(Protocol).get(synced_protocol.protocol_id)
            if updated_protocol.version > synced_protocol.synchronized_version:
                self.upload_protocol_to_mds(mds, updated_protocol)

        resp.conext['result'] = {}
        resp.context['type'] = SUCCESS_RESPONSE
