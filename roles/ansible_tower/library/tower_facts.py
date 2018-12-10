from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import Request


def get(resource):
    base_url = 'https://10.8.38.187/api/v2/%s' % resource
    headers = {'Content-Type': 'application/json'}

    req = Request(headers=headers, url_username='admin', url_password='ansible',
                  validate_certs=False, force_basic_auth=True)

    resp = req.get(base_url)
    return resp.read()


def get_organization_from_id(module, organization_id):
    resp = get('organizations/%s' % organization_id)
    data = module.from_json(resp)
    return data['name']


def get_inventory(module):
    resp = get('inventories')
    data = module.from_json(resp)

    objects = list()
    for item in data['results']:
        objects.append({
            'name': item['name'],
            'description': item['description'],
            'organization': get_organization_name_from_id(module, item['organization'])
        })
    return objects


def main():
    """ main entry point for module execution
    """
    argument_spec = {
        'subset': dict(type='list'),
        'name': dict()
    }

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    name = module.params['name']

    result = {'changed': False}

    facts = {
        'inventories': get_inventory(module)
    }

    if name:
        result['ansible_facts'] = {name: facts}
    else:
        result['ansible_facts'] = facts

    module.exit_json(**result)

if __name__ == '__main__':
    main()
