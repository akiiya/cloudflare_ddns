import codecs
import json
import os

import requests


current_folder = os.path.abspath(os.path.dirname(__file__))


def get_config():
    config_path = os.path.join(current_folder,'cf_config.json')
    with codecs.open(config_path,'rb',encoding='utf-8') as f:
        return json.load(f)


def get_ip(ip_get_url):
    """
    get the ip address of whoever executes the script
    """
    response = requests.get(ip_get_url)
    return str(response.text)


def set_ip(the_ip):
    """
    sets the ip in via cloudflare api
    """

    config = get_config()

    url = (
        "https://api.cloudflare.com/client/v4/zones/%(zone_id)s/dns_records/%(record_id)s"
        % {"zone_id": config.get("ZONE_ID"), "record_id": config.get("RECORD_ID")}
    )

    headers = {
        "Authorization":"Bearer "+config.get("API_KEY"),
        "Content-Type": "application/json",
    }

    payload = {
        "type": "A",
        "name": config.get("RECORD_NAME"),
        "content": the_ip,
        "proxied":False
    }
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    print(response.content)
    print(response.status_code)


def main():
    ip_get_url = "http://ip.42.pl/raw"
    the_ip = get_ip(ip_get_url)
    set_ip(the_ip)


if __name__ == "__main__":
    main()
