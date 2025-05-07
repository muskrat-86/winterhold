import requests

VCENTER_SERVER = "your-vcenter-server"
USERNAME = "your-username"
PASSWORD = "your-password"

session = requests.Session()
session.auth = (USERNAME, PASSWORD)

def create_vm():
    url = f"https://{VCENTER_SERVER}/rest/vcenter/vm"
    payload = {
        "name": "CustomVM",
        "guest_os": "CENTOS_7_64",
        "placement": {
            "datacenter": "your-datacenter",
            "datastore": "your-datastore"
        },
        "boot": {
            "type": "iso",
            "iso_path": "[datastore] custom.iso"
        }
    }
    response = session.post(url, json=payload)
    
    if response.status_code == 201:
        print("VM created successfully!")
    else:
        print(f"Error creating VM: {response.text}")

if __name__ == "__main__":
    create_vm()