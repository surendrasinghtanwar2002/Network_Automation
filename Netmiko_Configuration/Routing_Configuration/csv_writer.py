import csv

# Correctly define the records as a list of lists
rec = [
    ["device_ip", "device_type", "username", "password"],
    ["192.168.1.100", "cisco_ios", "admin", "hackerzone"],
    ["192.168.1.105", "cisco_ios", "admin", "hackerzone"],
    ["192.168.1.110", "cisco_ios", "admin", "hackerzone"],
    ["192.168.1.115", "cisco_ios", "admin", "hackerzone"]
]

def main():
    # Open the file and write the records
    with open("device_details.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rec)  # Indent this line to be part of the with block
    print("CSV created")

if __name__ == "__main__":
    main()