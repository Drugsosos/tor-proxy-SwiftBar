#!/usr/bin/env python3
#
# Tor proxy
#
# <bitbar.title>Tor proxy</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>drugsosos</bitbar.author>
# <bitbar.author.github>drugsosos1</bitbar.author.github>
# <bitbar.desc>Displays proxy status (country flag) and allows toggling it on and off and reloading proxy</bitbar.desc>
# <bitbar.dependencies>python3,tor,obfs4proxy</bitbar.dependencies>

from os import popen, path, getenv
from dotenv import load_dotenv

load_dotenv()  # Loads ENVs from .env file

interface = "wi-fi"  # You can also set this to e.g. "ethernet"

proxy_type = "SOCKS"
proxy_get = "-getsocksfirewallproxy"
proxy_set = "-setsocksfirewallproxystate"

port = '9150'  # Tor port (≥ 1024)
token = ''  # Your token from ipinfo.io

python_location = '/opt/homebrew/opt/python@3.10/bin/python3.10'
file_location = path.realpath(__file__)


def get_state() -> bool:
    if 'No' in popen(f'networksetup {proxy_get} {interface}').read():
        return True
    return False


def get_flag() -> str | None:
    import requests
    from flag import flag
    if token:
        params = {'token': token}
        proxy = {'https': f'socks5://127.0.0.1:{port}'}
        country = requests.get('https://ipinfo.io', params=params, proxies=proxy).json().get('country')
        return flag(country)
    return


def get_icon(state: bool) -> tuple:
    if state:
        state_icon = "🌍"
        action_toggle = "Enable"
    else:
        try:
            state_icon = get_flag()
            if not state_icon:
                state_icon = "🧦"
        except Exception:
            state_icon = "🧦"
        action_toggle = "Disable"
    return state_icon, action_toggle


def toggle(state: bool) -> None:
    from os import system
    if state:
        system(f'/opt/homebrew/bin/tor --SocksPort {port}')
        system(f'networksetup {proxy_set} {interface} on')
    else:
        system('killall tor')
        system(f'networksetup {proxy_set} {interface} off')


def reload() -> None:
    from os import system
    system('killall tor')
    system(f'networksetup {proxy_set} {interface} off')
    system(f'/opt/homebrew/bin/tor --SocksPort {port}')
    system(f'networksetup {proxy_set} {interface} on')


def menu(state_icon: str, action_toggle: str, state: bool) -> None:
    print(f'{state_icon} | dropdown=false')

    print('---')

    print(
        f'{action_toggle} Proxy | refresh=true bash={python_location} param1={file_location} param2=toggle terminal=false shortcut=CMD+F8'
    )
    if not state:
        print(
            f'Reload | refresh=true bash={python_location} param1={file_location} param2=reload terminal=false shortcut=CMD+F9')


def main(args: list, state: bool):
    if 'toggle' in args:
        toggle(state)

    if 'reload' in args:
        reload()

    state_icon, action_toggle = get_icon(state)

    menu(state_icon, action_toggle, state)


if __name__ == "__main__":
    from sys import argv
    _state = get_state()
    main(argv, _state)
