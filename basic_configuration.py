# import csv

# def (file_path):
#     devices = []

#     with open(file_path, mode="r") as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             filter_row = {key: value for key, value in row.items() if value}

#             if 'create_vlan' in filter_row:
#                 row['create_vlan'] = [int(vlan.strip()) for vlan in filter_row['create_vlan'].split(',') if vlan.strip().isdigit()]
#             else:
#                 row['create_vlan'] = []

#             if 'delete_vlan' in filter_row:
#                 row['delete_vlan'] = [int(vlan.strip()) for vlan in filter_row['delete_vlan'].split(',') if vlan.strip().isdigit()]
#             else:
#                 row['delete_vlan'] = []

#             devices.append(row)

#     return devices

# if __name__ == "__main__":
#     file_path = 'device_details.csv'
#     devices = read_device_details(file_path)
    

#     jinja_template = """
#         {% for device in devices %}
#         {% if create_vlan in device %}
#         {% for vlan_no in device['create_vlan'] %}
#         {%- vlan vlan_no -%}
#         {%- name myvlan vlan_no %} 
        
#         """
    
