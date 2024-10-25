from netmiko import ConnectHandler

device_Details = {
    "device_type":"cisco_ios",
    "ip":"192.168.1.60",
    "username":"admin",
    "password":"hackerzone",
    "secret":"hackerzone"
}

if __name__ == "__main__":
    # session = ConnectHandler(**device_Details)
    # output = session.secret
    # print(output)
    atual_data  = [("192.168.1.100",True),("192.168.1.105",False),("192.168.1.110",True),("192.168.1.115",True)]
    output = list(filter(lambda x : False not in x,atual_data))
    print(output)
    