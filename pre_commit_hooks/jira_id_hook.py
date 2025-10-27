import subprocess
import sys
import re
import os

def get_current_branch_name():
    result = subprocess.run(['git', 'symbolic-ref', '--short', 'HEAD'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Unable to get the current branch name.")
        sys.exit(1)
    return result.stdout.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: python add_branch_name.py <commit_msg_file>")
        sys.exit(1)
    print(f"usage 1:{sys.argv[0]} 2:{sys.argv[1]}End")
    commit_msg_file=sys.argv[1]
    branch_name = get_current_branch_name()

    # Check for a pattern matching 'something_' after a '/'
    if re.search(r'\/.+-', branch_name) and ('feature' in branch_name or 'bugfix' in branch_name):
        # Extract the prefix from the branch name (everything after the first '/' and before the first '_')
        match = re.search(r'.*\/([A-Z]+-\d+).*', branch_name)
        if match:
            prefix = match.group(1)

            # Check if the commit message file exists and is non-empty
            if os.path.exists(commit_msg_file) and os.path.getsize(commit_msg_file) > 0:
                with open(commit_msg_file, 'r+') as file:
                    commit_msg = file.read().strip()

                    if commit_msg.startswith(prefix):
                        print("Prefix already set, it's good")
                    elif commit_msg:
                        # Prefix the commit message with the branch prefix
                        print("Update commit message")
                        file.seek(0)
                        file.write(f"{prefix} {commit_msg}\n")
                        file.truncate()
                    else:
                        print("Please set a comment for commit")
                        sys.exit(1)

