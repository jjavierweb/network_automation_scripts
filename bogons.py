import requests

ipv4_prefixes = requests.get("https://www.team-cymru.org/Services/Bogons/bogon-bn-agg.txt")
ipv6_prefixes = requests.get("https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt")


def print_prefixes(file_name,prefix_list):
    ip_version = file_name[2:]
    with open(f'prefixes_{file_name}.txt','w') as pref:
        pref.write(prefix_list.text)
        pref.close()

    with open(f'prefixes_{file_name}.txt','r') as f:
        for l in f:
            line = l.replace("\n","")
            print(f"{file_name[:2]} prefix-list BOGONS-{ip_version} permit {line} le 32")
        f.close()


print_prefixes("ipv4",ipv4_prefixes)

#print_prefixes("ipv6",ipv6_prefixes)


  
