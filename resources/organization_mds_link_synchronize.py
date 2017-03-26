from app.hooks import *
import falcon
import requests
import urllib.parse
import tempfile
from sqlalchemy import desc 
from sqlalchemy.orm import joinedload

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import (
    OrganizationMDSLinkProtocol,
    OrganizationMDSLink,
    Protocol,
    SharedProtocol
)


class OrganizationMDSLinkSynchronizeResource(object):
    def upload_protocol_to_mds(self, user, session, mds, protocol, old_protocol):
        url = urllib.parse.urljoin(mds.url, '/mds/core/procedure/')

        # TODO Matt, what do we send here? What HTTP verb? What content type?
        with tempfile.TemporaryFile() as src:
            src.write(str.encode(protocol.protocol.content))
            src.seek(0)

            data = {
                'title': protocol.protocol.title,
                'version': protocol.protocol_version,
                'author': '{} {}'.format(user.first_name, user.last_name),
                'description': 'Uploaded from Protocol Hub',
            }
            files = {
                'src': src,
            }

            r = requests.post(url, data=data, files=files)
            if r.status_code == 200:
                old_protocol.synchronized_version = protocol.protocol_version
                session.add(old_protocol)
                session.commit()
                return True
            return False

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.synchronize_mds))
    def on_post(self, req, resp, organization_id, mds_link_id):
        session = req.context['session']
        user = req.context['user']

        mds_link = session.query(OrganizationMDSLink).get(mds_link_id)

        if mds_link == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'mds': 'no mds link with id {}'.format(mds_link_id),
            }
            return

        synced_protocols = session.query(OrganizationMDSLinkProtocol).\
                join(OrganizationMDSLink).\
                filter(
                    OrganizationMDSLink.organization_id==organization_id,
                    OrganizationMDSLinkProtocol.mds_link_id==mds_link_id).\
                all()

        successfully_synced = []
        for synced_protocol in synced_protocols:
            updated_protocol = session.query(SharedProtocol).\
                    filter(
                        SharedProtocol.protocol_id==synced_protocol.protocol_id,
                        SharedProtocol.organization_id==organization_id).\
                    order_by(desc(SharedProtocol.protocol_version)).\
                    first()
            if updated_protocol.protocol_version > synced_protocol.synchronized_version:
                success = self.upload_protocol_to_mds(
                    user, session, mds_link, updated_protocol, synced_protocol)
                if success:
                    successfully_synced.append(updated_protocol.protocol_id)


        resp.context['result'] = {
            'synced_protocols': successfully_synced,
        }
