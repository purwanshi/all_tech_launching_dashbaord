import os
import subprocess
import google.generativeai as genai # type: ignore

# Gemini API key
google_gemini_api = "AIzaSyBHRBlq6nzFhp8ieBY4pVH10p2ITnwnvN4"

# Configure Gemini
genai.configure(api_key=google_gemini_api)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

def linux_gemini_model(myprompt):
    prompt = f"""
You are an AI assistant. Your task is to understand the user's prompt and return a single valid Linux shell command (like date, pwd, ls, etc). 
DO NOT include quotation marks in your response — only output the shell command.

Prompt: {myprompt}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def ssh_execute_command(username, ip, command):
    final_command = f"ssh {username}@{ip} {command}"
    result = subprocess.getoutput(final_command)
    return result

# Collect remote details
print("\n🎛️  Welcome to the Linux Command Executor 🎛️")
username = input("Enter username of remote account: ")
ip = input("Enter your remote server IP: ")

# Display Menu
print("\nChoose an option:")
print("1. Run 'date' command")
print("2. Run 'cal' command")
print("3. Run 'uptime' command")
print("4. Run 'whoami' command")
print("5. Run 'uname -a' command")
print("6. Run 'df -h' command")
print("7. Run 'free -m' command")
print("8. Run 'ls' command")
print("9. Run 'pwd' command")
print("10.run 'dnf; command")
print("11. Run 'chmod 755 filename' command               ➝ Change file permission")
print("12. Run 'chown user:group filename' command        ➝ Change file ownership")
print("13. Run 'mkdir newdir' command                     ➝ Create directory")
print("14. Run 'rmdir dir' command                        ➝ Remove directory")
print("15. Run 'rm filename' command                      ➝ Remove file")
print("16. Run 'mv oldfile newfile' command               ➝ Rename/move file")
print("17. Run 'touch file' command                       ➝ Create empty file")
print("18. Run 'zip archive.zip file' command             ➝ Compress file")
print("19. Run 'unzip archive.zip' command                ➝ Unzip archive")
print("20. Run 'ping -c 4 google.com' command             ➝ Ping test")
print("21. Run 'ip a' command                              ➝ Show IP addresses")
print("22. Run 'curl http://example.com' command           ➝ Download content")
print("23. Run 'wget http://example.com/file' command      ➝ Download file")
print("24. Run 'netstat -tulnp' command                    ➝ Show open ports")
print("25. Run 'ss -tulnp' command                         ➝ Show socket status")
print("26. Run 'traceroute google.com' command             ➝ Trace route to host")
print("27. Run 'nslookup google.com' command               ➝ DNS query")
print("28. Run 'head -n 5 file.txt' command                ➝ First 5 lines of file")
print("29. Run 'tail -n 5 file.txt' command                ➝ Last 5 lines of file")
print("30. Run 'cut -d: -f1 /etc/passwd' command           ➝ Cut fields by delimiter")
print("31. Run 'grep \"root\" /etc/passwd' command          ➝ Search pattern in file")
print("32. Run 'sort file.txt' command                     ➝ Sort lines alphabetically")
print("33. Run 'uniq file.txt' command                     ➝ Remove duplicate lines")
print("34. Run 'wc -l file.txt' command                    ➝ Count lines")
print("35. Run 'awk \"{print $1}\" file.txt' command         ➝ Print first word of each line")
print("36. Run 'sed \"s/old/new/g\" file.txt' command        ➝ Replace text")
print("37. Run 'uname -r' command                          ➝ Kernel version")
print("38. Run 'df -Th' command                            ➝ Disk filesystems & usage")
print("39. Run 'top -b -n 1' command                       ➝ Show process list")
print("40. Run 'ps aux' command                            ➝ Show running processes")
print("41. Run 'history' command                           ➝ Command history")
print("42. Run 'hostname' command                          ➝ Show hostname")
print("43. Run 'uptime' command                            ➝ Show uptime again")
print("44. Run 'nmap -sS -p 80 127.0.0.1' command          ➝ Port scan")
print("45. Run 'locate passwd' command                     ➝ Locate file")
print("46. Run 'find / -name passwd' command               ➝ Find file")
print("47. Run 'man ls' command                            ➝ Manual page of ls")
print("48. Run 'kill -9 PID' command                       ➝ Kill process by PID")
print("49. Run 'ifconfig' command                          ➝ Network interfaces")
print("50. Run 'uname -m' command                          ➝ Machine architecture")
print("51. Run 'ip link' command                           ➝ List network interfaces")
print("52. Run 'systemctl status sshd' command             ➝ Service status")
print("53. Run 'sudo systemctl restart sshd' command       ➝ Restart service")
print("54. Run 'echo \"Hello\" | tee file.txt' command       ➝ Write output to file")
print("55. Run 'df -i' command                             ➝ Show inode usage")
print("56. Run 'lsblk' command                             ➝ Block devices")
print("57. Run 'lsmod' command                             ➝ Kernel modules")
print("58. Run 'vmstat' command                            ➝ System performance")
print("59. Run 'iostat' command                            ➝ CPU & IO stats")
print("60. Run 'watch date' command                        ➝ Auto-refresh command")
print("61. Run 'shutdown -h now' command                   ➝ Shutdown system")
print("62. Run 'reboot' command                            ➝ Reboot system")
print("63. Run 'who' command                               ➝ Logged in users")
print("64. Run 'users' command                             ➝ Current users")
print("65. Run 'groups' command                            ➝ Groups of current user")
print("66. Run 'alias l=\"ls -la\"' command                 ➝ Create alias")
print("67. Run 'unalias l' command                         ➝ Remove alias")
print("68. Run 'echo \"password\" | passwd --stdin username' command ➝ Set password")
print("69. Run 'useradd testuser' command                  ➝ Add new user")
print("70. Run 'userdel -r testuser' command               ➝ Delete user")
print("71. Run 'passwd testuser' command                   ➝ Change password")
print("72. Run 'lsblk' command                             ➝ List block devices (disks, partitions)")
print("73. Run 'fdisk -l' command                          ➝ List all disk partitions (MBR-based systems)")
print("74. Run 'parted -l' command                         ➝ List all partitions (including GPT systems)")
print("75. Run 'df -h' command                              ➝ Show disk space usage in human-readable format")
print("76. Run 'df -i' command                              ➝ Show inode usage on filesystems")
print("77. Run 'mount' command                              ➝ Show all mounted filesystems")
print("78. Run 'umount /dev/sdX1' command                    ➝ Unmount a filesystem")
print("79. Run 'mkfs.ext4 /dev/sdX1' command                 ➝ Format partition with ext4 filesystem")
print("80. Run 'blkid' command                               ➝ List block device UUIDs and filesystem types")
print("81. Run 'tune2fs -l /dev/sdX1' command                ➝ Show detailed info of ext2/ext3/ext4 filesystem")
print("82. Run 'mount /dev/sdX1 /mnt' command                ➝ Mount partition to /mnt directory")
print("83. Run 'swapoff -a' command                          ➝ Disable all swap areas")
print("84. Run 'swapon -a' command                           ➝ Enable all swap areas")
print("85. Run 'mkswap /dev/sdX2' command                    ➝ Create swap area on partition")
print("86. Run 'ls -lh /dev/disk/by-uuid/' command           ➝ List disks by UUID (device identifiers)")




choice = input("\nEnter your choice: ")

# Predefined menu options
if choice == "1":
    print(ssh_execute_command(username, ip, "date"))

elif choice == "2":
    print(ssh_execute_command(username, ip, "cal"))

elif choice == "3":
    print(ssh_execute_command(username, ip, "uptime"))

elif choice == "4":
    print(ssh_execute_command(username, ip, "whoami"))

elif choice == "5":
    print(ssh_execute_command(username, ip, "uname -a"))

elif choice == "6":
    print(ssh_execute_command(username, ip, "df -h"))

elif choice == "7":
    print(ssh_execute_command(username, ip, "free -m"))

elif choice == "8":
    print(ssh_execute_command(username, ip, "ls"))

elif choice == "9":
    print(ssh_execute_command(username, ip, "pwd"))

elif choice == "11":
    print(ssh_execute_command(username, ip, "chmod 755 filename"))

elif choice == "12":
    print(ssh_execute_command(username, ip, "chown user:group filename"))

elif choice == "13":
    print(ssh_execute_command(username, ip, "mkdir newdir"))

elif choice == "14":
    print(ssh_execute_command(username, ip, "rmdir dir"))

elif choice == "15":
    print(ssh_execute_command(username, ip, "rm filename"))

elif choice == "16":
    print(ssh_execute_command(username, ip, "mv oldfile newfile"))

elif choice == "17":
    print(ssh_execute_command(username, ip, "touch file"))

elif choice == "18":
    print(ssh_execute_command(username, ip, "zip archive.zip file"))

elif choice == "19":
    print(ssh_execute_command(username, ip, "unzip archive.zip"))

elif choice == "20":
    print(ssh_execute_command(username, ip, "ping -c 4 google.com"))

elif choice == "21":
    print(ssh_execute_command(username, ip, "ip a"))

elif choice == "22":
    print(ssh_execute_command(username, ip, "curl http://example.com"))

elif choice == "23":
    print(ssh_execute_command(username, ip, "wget http://example.com/file"))

elif choice == "24":
    print(ssh_execute_command(username, ip, "netstat -tulnp"))

elif choice == "25":
    print(ssh_execute_command(username, ip, "ss -tulnp"))

elif choice == "26":
    print(ssh_execute_command(username, ip, "traceroute google.com"))

elif choice == "27":
    print(ssh_execute_command(username, ip, "nslookup google.com"))

elif choice == "28":
    print(ssh_execute_command(username, ip, "head -n 5 file.txt"))

elif choice == "29":
    print(ssh_execute_command(username, ip, "tail -n 5 file.txt"))

elif choice == "30":
    print(ssh_execute_command(username, ip, "cut -d: -f1 /etc/passwd"))

elif choice == "31":
    print(ssh_execute_command(username, ip, "grep 'root' /etc/passwd"))

elif choice == "32":
    print(ssh_execute_command(username, ip, "sort file.txt"))

elif choice == "33":
    print(ssh_execute_command(username, ip, "uniq file.txt"))

elif choice == "34":
    print(ssh_execute_command(username, ip, "wc -l file.txt"))

elif choice == "35":
    print(ssh_execute_command(username, ip, "awk '{print $1}' file.txt"))

elif choice == "36":
    print(ssh_execute_command(username, ip, "sed 's/old/new/g' file.txt"))

elif choice == "37":
    print(ssh_execute_command(username, ip, "uname -r"))

elif choice == "38":
    print(ssh_execute_command(username, ip, "df -Th"))

elif choice == "39":
    print(ssh_execute_command(username, ip, "top -b -n 1"))

elif choice == "40":
    print(ssh_execute_command(username, ip, "ps aux"))

elif choice == "41":
    print(ssh_execute_command(username, ip, "history"))

elif choice == "42":
    print(ssh_execute_command(username, ip, "hostname"))

elif choice == "43":
    print(ssh_execute_command(username, ip, "uptime"))

elif choice == "44":
    print(ssh_execute_command(username, ip, "nmap -sS -p 80 127.0.0.1"))

elif choice == "45":
    print(ssh_execute_command(username, ip, "locate passwd"))

elif choice == "46":
    print(ssh_execute_command(username, ip, "find / -name passwd"))

elif choice == "47":
    print(ssh_execute_command(username, ip, "man ls"))

elif choice == "48":
    print(ssh_execute_command(username, ip, "kill -9 PID"))

elif choice == "49":
    print(ssh_execute_command(username, ip, "ifconfig"))

elif choice == "50":
    print(ssh_execute_command(username, ip, "uname -m"))

elif choice == "51":
    print(ssh_execute_command(username, ip, "ip link"))

elif choice == "52":
    print(ssh_execute_command(username, ip, "systemctl status sshd"))

elif choice == "53":
    print(ssh_execute_command(username, ip, "sudo systemctl restart sshd"))

elif choice == "54":
    print(ssh_execute_command(username, ip, "echo 'Hello' | tee file.txt"))

elif choice == "55":
    print(ssh_execute_command(username, ip, "df -i"))

elif choice == "56":
    print(ssh_execute_command(username, ip, "lsblk"))

elif choice == "57":
    print(ssh_execute_command(username, ip, "lsmod"))

elif choice == "58":
    print(ssh_execute_command(username, ip, "vmstat"))

elif choice == "59":
    print(ssh_execute_command(username, ip, "iostat"))

elif choice == "60":
    print(ssh_execute_command(username, ip, "watch date"))

elif choice == "61":
    print(ssh_execute_command(username, ip, "shutdown -h now"))

elif choice == "62":
    print(ssh_execute_command(username, ip, "reboot"))

elif choice == "63":
    print(ssh_execute_command(username, ip, "who"))

elif choice == "64":
    print(ssh_execute_command(username, ip, "users"))

elif choice == "65":
    print(ssh_execute_command(username, ip, "groups"))

elif choice == "66":
    print(ssh_execute_command(username, ip, "alias l='ls -la'"))

elif choice == "67":
    print(ssh_execute_command(username, ip, "unalias l"))

elif choice == "68":
    print(ssh_execute_command(username, ip, "echo 'password' | passwd --stdin username"))

elif choice == "69":
    print(ssh_execute_command(username, ip, "useradd testuser"))

elif choice == "70":
    print(ssh_execute_command(username, ip, "userdel -r testuser"))

elif choice == "71":
    print(ssh_execute_command(username, ip, "passwd testuser"))

elif choice == "72":
    print(ssh_execute_command(username, ip, "lsblk"))

elif choice == "73":
    print(ssh_execute_command(username, ip, "fdisk -l"))

elif choice == "74":
    print(ssh_execute_command(username, ip, "parted -l"))

elif choice == "75":
    print(ssh_execute_command(username, ip, "df -h"))

elif choice == "76":
    print(ssh_execute_command(username, ip, "df -i"))

elif choice == "77":
    print(ssh_execute_command(username, ip, "mount"))

elif choice == "78":
    partition = input("Enter partition to unmount (e.g. /dev/sdX1): ")
    print(ssh_execute_command(username, ip, f"umount {partition}"))

elif choice == "79":
    partition = input("Enter partition to format (e.g. /dev/sdX1): ")
    print(ssh_execute_command(username, ip, f"mkfs.ext4 {partition}"))

elif choice == "80":
    print(ssh_execute_command(username, ip, "blkid"))

elif choice == "81":
    partition = input("Enter partition to inspect (e.g. /dev/sdX1): ")
    print(ssh_execute_command(username, ip, f"tune2fs -l {partition}"))

elif choice == "82":
    partition = input("Enter partition to mount (e.g. /dev/sdX1): ")
    mount_point = input("Enter mount point directory (e.g. /mnt): ")
    print(ssh_execute_command(username, ip, f"mount {partition} {mount_point}"))

elif choice == "83":
    print(ssh_execute_command(username, ip, "swapoff -a"))

elif choice == "84":
    print(ssh_execute_command(username, ip, "swapon -a"))

elif choice == "85":
    partition = input("Enter swap partition (e.g. /dev/sdX2): ")
    print(ssh_execute_command(username, ip, f"mkswap {partition}"))

elif choice == "86":
    print(ssh_execute_command(username, ip, "ls -lh /dev/disk/by-uuid/"))


# Custom task via GenAI
elif choice == "87":
    mycmd = input("Describe your task in natural language: ")
    command = linux_gemini_model(mycmd)
    print(f"\nGemini generated command: {command}\n")
    result = ssh_execute_command(username, ip, command)
    print(result)

else:
    print(" Invalid choice.")
