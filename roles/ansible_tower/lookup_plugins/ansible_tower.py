#
#  Copyright 2018 Red Hat | Ansible
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
"""

EXAMPLES = """
"""

RETURN = """
"""
import json

from ansible.plugins.lookup import LookupBase
from ansible.module_utils.urls import Request
from ansible.errors import AnsibleLookupError


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        base_url = "https://%s/api/v2" % variables['tower_host']
        headers = {'Content-type': 'application/json'}

        username = variables['tower_username']
        password = variables['tower_password']
        verify_ssl = variables.get('tower_verify_ssl')

        req = Request(headers=headers, url_username=username,
                      url_password=password, validate_certs=verify_ssl,
                      force_basic_auth=True)

        url = "%s/%s" % (base_url, terms[0])

        resp = req.get(url)
        resp = json.loads(resp.read())

        return resp['results']
