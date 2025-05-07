import json

def update_packer_template():
    with open('packer/build_iso.json') as f:
        template = json.load(f)

    # Modify template as needed
    template['variables']['iso_url'] = 'http://mirror.rockylinux.org/iso/Rocky-9.3-x86_64-dvd1.iso'

    with open('packer/build_iso.json', 'w') as f:
        json.dump(template, f, indent=2)

if __name__ == "__main__":
    update_packer_template()
