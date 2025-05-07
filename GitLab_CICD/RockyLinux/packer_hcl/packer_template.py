import subprocess

def run_packer():
    packer_command = ["packer", "build", "packer_template.hcl"]
    process = subprocess.run(packer_command, capture_output=True, text=True)

    if process.returncode == 0:
        print("Packer build succeeded!")
    else:
        print(f"Packer build failed: {process.stderr}")

if __name__ == "__main__":
    run_packer()