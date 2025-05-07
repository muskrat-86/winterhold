
import os
import subprocess

def setup_venv():
    # Create a virtual environment
    subprocess.run(['python3', '-m', 'venv', '.venv'])

    # Activate the virtual environment and install dependencies
    activate_script = '.venv/bin/activate'
    if os.name == 'nt':
        activate_script = '.venv\\Scripts\\activate.bat'

    # Upgrade pip and install requirements
    subprocess.run(['pip', 'install', '--upgrade', 'pip'])
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

if __name__ == "__main__":
    setup_venv()
