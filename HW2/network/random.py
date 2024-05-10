import netifaces

# Get a dictionary containing information about all network interfaces
interfaces = netifaces.interfaces()

# Print information about each network interface
for interface in interfaces:
    print(f"Interface: {interface}")
    addresses = netifaces.ifaddresses(interface)
    for address_family, addresses_info in addresses.items():
        print(f"  Address Family: {address_family}")
        for address_info in addresses_info:
            print(f"    Address: {address_info.get('addr')}")
