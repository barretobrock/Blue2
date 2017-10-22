import paramiko
from scp import SCPClient

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.10", username="barretobrock", password="Mjik212")
print("Connected")
scp = SCPClient(ssh.get_transport())
scp.put()
scp.close()