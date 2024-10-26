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
    session = ConnectHandler(**device_Details)
    if session:
        print(f"We are connected to the device {session.host}")
        device_prompt = session.find_prompt()
        print(f"This is the current device prompt {device_prompt}")
        if session.enable():
            current_prompt = session.find_prompt()
            print(f'This is the current prompt of the device {current_prompt}')
            vlan_output = session.send_command("show vlan",use_textfsm=True)             ## This command is used to send the show vlan details
            print(f"This is the output of the vlan {vlan_output} ")

 

    