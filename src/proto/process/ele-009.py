
import subprocess
import getpass



def run_cmd_w_sudo(passwd):
    # Define the password and the command
    command = 'ps -ef'.split()

    sudocmd = ["sudo", "-s"] + command

    # Create the subprocess
    proc = subprocess.Popen(sudocmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    # Communicate the password to the subprocess
    output, error = proc.communicate(passwd)

    # Print the output and error
    print("Output:", output)
    # print("Error:", error)

if __name__ == "__main__":
    
    passwd = getpass.getpass('Password: ')
    # print('Password entered:', passwd)a
    passwd = (passwd + "\n").encode()
    run_cmd_w_sudo(passwd)




