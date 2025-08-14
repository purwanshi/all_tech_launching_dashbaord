import streamlit as st
import subprocess

# Menu definition
menu = {
    "1": ("Show current date and time", "date"),
    "2": ("Display calendar", "cal"),
    "3": ("Show system uptime", "uptime"),
    "4": ("Show logged-in user", "whoami"),
    "5": ("Show system info", "uname -a"),
    "6": ("Check disk usage", "df -h"),
    "7": ("Check memory usage", "free -m"),
    "8": ("List files in current directory", "ls -l"),
    "9": ("List files including hidden", "ls -la"),
    "10": ("Show current directory path", "pwd")
    # ... Add more if you want
}

st.title("🖥️ Linux Dashboard")
st.write("Run Linux commands remotely via SSH")

username = st.text_input("Enter SSH username")
ip = st.text_input("Enter remote IP address")
choice = st.selectbox("Select a command", options=list(menu.keys()), format_func=lambda x: f"{x}. {menu[x][0]}")

if st.button("Run Command"):
    if username and ip:
        command = menu[choice][1]
        ssh_command = f"ssh {username}@{ip} '{command}'"
        try:
            output = subprocess.check_output(ssh_command, shell=True, text=True)
            st.code(output)
        except subprocess.CalledProcessError as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter both username and IP.")
