from netmiko import ConnectHandler


device_details = {
    "device_type":"cisco_ios",
    "ip":"192.168.1.125",
    "username":"admin",
    "password":"hackerzone"
}

def main():
    session = ConnectHandler(**device_details)
    print(f"Connected to the device {session.host}")


if __name__ == "__main__":
    main()