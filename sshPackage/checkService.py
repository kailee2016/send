import paramiko as pik

username='root'
password='Gzhu2018@#$%'
baseHost='202.192.19.4'
port=55555

client=pik.SSHClient()
client.set_missing_host_key_policy(pik.AutoAddPolicy())
client.connect(hostname=baseHost,username=username,password=password,port=port)
print(client)
stdin,stdout,stderr=client.exec_command('ps -ef|grep java')
print(stdout.read())
#host=['4']
