import yaml

def parse_cisco_config(config):
    lines = config.splitlines()
    playbook = {
        'hosts': 'all',
        'tasks': []
    }
    
    current_task = None
    current_interface = None
    current_vlan = None
    current_vrf = None
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('hostname'):
            hostname = line.split()[1]
            playbook['tasks'].append({
                'name': 'Set hostname',
                'hostname': hostname
            })
        
        elif line.startswith('interface'):
            if current_task:
                playbook['tasks'].append(current_task)
            current_interface = line.split()[1]
            current_task = {
                'name': f'Configure interface {current_interface}',
                'interface': current_interface,
                'commands': []
            }
        
        elif line.startswith('vlan'):
            if current_task:
                playbook['tasks'].append(current_task)
            current_vlan = line.split()[1]
            current_task = {
                'name': f'Configure VLAN {current_vlan}',
                'vlan_id': current_vlan,
                'commands': []
            }
        
        elif line.startswith('vrf definition'):
            if current_task:
                playbook['tasks'].append(current_task)
            current_vrf = line.split()[2]
            current_task = {
                'name': f'Configure VRF {current_vrf}',
                'vrf_name': current_vrf,
                'commands': []
            }
        
        elif line.startswith('snmp-server'):
            if current_task:
                playbook['tasks'].append(current_task)
            current_task = {
                'name': 'Configure SNMP',
                'commands': [line]
            }
            playbook['tasks'].append(current_task)
            current_task = None
        
        elif line.startswith('aaa'):
            if current_task:
                playbook['tasks'].append(current_task)
            current_task = {
                'name': 'Configure AAA',
                'commands': [line]
            }
            playbook['tasks'].append(current_task)
            current_task = None
        
        elif line.startswith('router'):
            if current_task:
                playbook['tasks'].append(current_task)
            current_task = {
                'name': 'Configure router',
                'commands': [line]
            }
        
        elif line.startswith('ip vrf'):
            if current_task:
                playbook['tasks'].append(current_task)
            current_task = {
                'name': 'Configure IP VRF',
                'commands': [line]
            }
        
        elif line.startswith('line'):
            if current_task:
                playbook['tasks'].append(current_task)
            current_task = {
                'name': 'Configure line',
                'commands': [line]
            }
        
        elif line:
            if current_task:
                current_task['commands'].append(line)
    
    if current_task:
        playbook['tasks'].append(current_task)
    
    return playbook

# Example Cisco running-config
cisco_config = """
hostname Router1
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
interface GigabitEthernet0/1
 ip address 192.168.2.1 255.255.255.0
 no shutdown
vlan 10
 name Users
vlan 20
 name Guests
router ospf 1
 network 192.168.0.0 0.0.255.255 area 0
snmp-server community public RO
aaa new-model
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
"""

# Parse the Cisco config and convert to Ansible playbook
ansible_playbook = parse_cisco_config(cisco_config)

# Save the Ansible playbook to a YAML file
with open('ansible_playbook.yml', 'w') as file:
    yaml.dump(ansible_playbook, file, default_flow_style=False)

print("Ansible playbook has been generated and saved to 'ansible_playbook.yml'.")