output = [
    {'vlan_id': 10, 'name': 'Marketing'},
    {'vlan_id': 20, 'name': 'Sales'},
    {'vlan_id': 10, 'name': 'Finance'},  # Same VLAN ID as the first entry
    {'vlan_id': 30, 'name': 'Engineering'}
]


def main():
    current_vlans_dict={}
    for vlan in output:
        current_vlans_dict[vlan['vlan_id']] = vlan['name']

    print(current_vlans_dict)
    print(type(current_vlans_dict))
if __name__ == "__main__":
    main()