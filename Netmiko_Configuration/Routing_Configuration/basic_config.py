from netmiko import ConnectHandler


device_details = {
    "device_type":"cisco_ios",
    "ip":"192.168.1.11",
    "username":"admin",
    "password":"hackerzone"
}


if __name__ == "__main__":
    netmiko_session = ConnectHandler(**device_details)
    print(netmiko_session.find_prompt())