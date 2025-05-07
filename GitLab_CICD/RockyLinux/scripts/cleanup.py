import os
import shutil

def collect_error_logs():
    error_log_dir = './error-logs'
    os.makedirs(error_log_dir, exist_ok=True)
    
    # Collect error logs from the project directory
    for root, dirs, files in os.walk('.'):
        for file in files:
            if 'error' in file.lower() or file.endswith('.log'):
                src = os.path.join(root, file)
                dst = os.path.join(error_log_dir, os.path.basename(file))
                shutil.copy(src, dst)

def clean_up_project():
    # List of directories and files to be deleted
    items_to_delete = ['output', '.venv', 'packer', 'ansible', 'scripts', 'requirements.txt', '.gitlab-ci.yml']
    
    for item in items_to_delete:
        if os.path.isdir(item):
            shutil.rmtree(item, ignore_errors=True)
        elif os.path.isfile(item):
            os.remove(item)

    # Optionally remove any .pyc or .log files left behind
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc') or file.endswith('.log'):
                try:
                    os.remove(os.path.join(root, file))
                except Exception:
                    pass

if __name__ == "__main__":
    collect_error_logs()
    clean_up_project()
