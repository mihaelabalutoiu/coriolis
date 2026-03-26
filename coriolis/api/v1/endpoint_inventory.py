# Copyright 2026 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api import wsgi as api_wsgi
from coriolis.endpoint_resources import api
from coriolis.policies import endpoints as endpoint_policies
from coriolis import utils

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class EndpointInventoryController(api_wsgi.Controller):
    """Returns a VM inventory CSV for endpoints that support it."""

    def __init__(self):
        self._endpoint_resources_api = api.API()
        super(EndpointInventoryController, self).__init__()

    def index(self, req, endpoint_id):
        context = req.environ['coriolis.context']
        context.can("%s:export_inventory" % (
            endpoint_policies.ENDPOINTS_POLICY_PREFIX))

        env = req.GET.get("env")
        if env is not None:
            env = utils.decode_base64_param(env, is_json=True)
        else:
            env = {}

        csv_content = self._endpoint_resources_api.get_endpoint_inventory_csv(
            context, endpoint_id, env)

        req.environ['coriolis.best_content_type'] = 'text/csv'
        resp = api_wsgi.ResponseObject(csv_content)
        resp['content-disposition'] = (
            'attachment; filename="vm_inventory_%s.csv"' % endpoint_id)
        return resp


def create_resource():
    return api_wsgi.Resource(EndpointInventoryController())
