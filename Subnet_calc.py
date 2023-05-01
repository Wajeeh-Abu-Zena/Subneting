import re

# Input ip address
def get_ip_address():
    while True:
        ip_address = input("Enter IP address: ")
        pattern = r'^(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)$'
        if re.match(pattern, ip_address):
            return ip_address
        else:
            print("Invalid IP address format. Please try again.")

# input cidr number
def calc_cidr(ip_address):
    while True:
        input_cidr = input("Enter CIDR number : ")
        if str(input_cidr).isdigit():
            if (input_cidr == ''):
                ip_class = int(ip_address.split('.')[0])
                if ip_class <= 126:
                    cidr = 8
                    return cidr
                elif ip_class >= 128 and ip_class <= 191:
                    cidr = 16
                    return cidr
                elif ip_class >= 192 and ip_class <= 223:
                    cidr = 24
                    return cidr
            else:
                if int(input_cidr) > 0 and int(input_cidr) <= 32:
                    return int(input_cidr)
                else:
                    print("Invalid CIDR format. Please try again.")
        else:
            print('Please enter valid CIDR number from 1 to 32 ')

# input host or subnet
def get_partition_type():
    while True:
        partition_type = input("Enter partition type (hosts or subnets): ")
        p = partition_type.lower()
        if p in ['hosts', 'subnets']:
            return p
        else:
            print("Invalid partition type. Please enter 'hosts' or 'subnets'.")

# number of hosts or subnets
def get_partition_number(par_type, cidr):
    while True:
        partition_number = int(input(f"Enter number of {par_type}: "))

        if str(partition_number).isdigit():
            if par_type == 'subnets':
                # max subnets number
                part_type_num = 2 ** (30 - int(cidr))
            else:
                # max hosts number
                part_type_num = calc_hosts_num(cidr)
            if partition_number > part_type_num and partition_number > 0:
                print(f'Please enter valid {par_type} number , The max {par_type} number is {part_type_num}')
            else:
                break
        else:
            print("Invalid number format. Please enter a positive integer.")
    return partition_number


def binary_subnet_mask(cidr):
    binary_subnet_mask = [0] * 32

    for i in range(int(cidr)):
        binary_subnet_mask[i] = 1
    return binary_subnet_mask

def decimal_subnet_mask(binary_subnet_mask):
    # Convert the subnet mask from a list of 32 bits to dotted decimal notation
    subnet_mask_octets = []

    for i in range(0, 32, 8):
        subnet_mask_octet = int(''.join(map(str, binary_subnet_mask[i:i + 8])), 2)
        subnet_mask_octets.append(str(subnet_mask_octet))

    subnet_mask_dotted_decimal = '.'.join(subnet_mask_octets)
    return subnet_mask_dotted_decimal

def calc_hosts_num(cidr):
    hosts_num = 2 ** (32 - int(cidr)) - 2
    return hosts_num

def calc_subnets_num(cidr):
    """Calculate the number of possible subnets based on the input IP address."""

    remaining_bits = 8 - ((32 - cidr) % 8)
    if remaining_bits == 8:
        max_subnets = 2 ** 0
    else:
        max_subnets = 2 ** remaining_bits
    return max_subnets

def calc_network_address(ip_address, subnet_mask):
    # Split IP address and subnet mask into octets
    ip_octets = ip_address.split('.')
    subnet_octets = subnet_mask.split('.')
    ID_address = []

    for i in range(4):
        ip_octet = int(ip_octets[i])
        subnet_octet = int(subnet_octets[i])
        ID = bin(ip_octet & subnet_octet)
        ID_address.append(ID[2:])

    # Convert each binary octet to decimal
    decimal_address = [str(int(octet, 2)) for octet in ID_address]

    return '.'.join(decimal_address)


def calc_BC_address(ip_address, subnet_mask):
    # Split IP address and subnet mask into octets
    ip_octets = ip_address.split('.')
    subnet_octets = subnet_mask.split('.')
    BC = []
    for i in range(4):
        if subnet_octets[i] == '255':
            BC.append(ip_octets[i])
        elif subnet_octets[i] == '0':
            BC.append('255')
        else:
            skips = 256 - int(subnet_octets[i])
            s = skips
            while s <= int(ip_octets[i]):
                s += skips
            BC.append(str(s-1))

    broadcast = '.'.join(BC)
    return broadcast


def calc_partition_user_divide(par_type, par_num, phas):
    if phas == 'first':
        if par_type == 'subnets':
            num_bits = 1
            while (2 ** num_bits) < par_num:
                num_bits += 1
            new_cidr = 32 - num_bits

        else:
            num_bits = 0
            while (2 ** num_bits) < par_num + 2:
                num_bits += 1
            new_cidr = 32 - num_bits
    else:

        new_cidr = '30'

    return new_cidr

def calc_first_last(ip_address, subnet_mask):
    # Convert IP address and subnet mask to binary strings
    ip_bin = ''.join([bin(int(x) + 256)[3:] for x in ip_address.split('.')])
    subnet_bin = ''.join([bin(int(x) + 256)[3:] for x in subnet_mask.split('.')])

    # Calculate the network address and broadcast address using bitwise AND and OR operations
    network_bin = ''.join([str(int(ip_bin[i]) & int(subnet_bin[i])) for i in range(len(ip_bin))])
    broadcast_bin = ''.join([str(int(network_bin[i]) | int(subnet_bin[i]) ^ 1) for i in range(len(network_bin))])

    # Convert binary strings back to decimal format
    network_address = '.'.join([str(int(network_bin[i:i + 8], 2)) for i in range(0, len(network_bin), 8)])
    broadcast_address = '.'.join([str(int(broadcast_bin[i:i + 8], 2)) for i in range(0, len(broadcast_bin), 8)])

    return broadcast_address


def main():
    ip_address = get_ip_address()
    cidr = calc_cidr(ip_address)
    par_type = get_partition_type()
    par_num = get_partition_number(par_type, cidr)
    binary_mask = binary_subnet_mask(cidr)
    mask = decimal_subnet_mask(binary_mask)
    print('The subnet mask is : ', mask)
    host = calc_hosts_num(cidr)
    print('The hosts number is : ', host) 
    sub = calc_subnets_num(cidr)
    print('Numbers of subnetting : ', sub)

    print('The first subnet:')
    new_cidr = calc_partition_user_divide(par_type, par_num, 'first')
    new_binary_mask = binary_subnet_mask(new_cidr)
    new_mask = decimal_subnet_mask(new_binary_mask)
    net_id = calc_network_address(ip_address, new_mask)
    print('The Network Address is :', net_id)
    bc = calc_BC_address(ip_address, new_mask)
    print('The braodcost address is :', bc)

    print('The last subnet:')
    new_cidr = calc_partition_user_divide(par_type, par_num, 'last')
    new_binary_mask = binary_subnet_mask(new_cidr)
    new_mask = decimal_subnet_mask(new_binary_mask)
    net_id = calc_network_address(ip_address, new_mask)
    print('The Network Address is :', net_id)
    bc = calc_first_last(ip_address, mask)
    print('The braodcost address is :', bc)

if __name__ == '__main__':
    main()