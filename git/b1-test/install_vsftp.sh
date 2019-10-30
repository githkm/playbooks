#!/bin/bash
yum install -y vsftpd.x86_64
# 用户名
read -p "Input a username：" user
pwd=`openssl rand -base64 8 | cut -c1-10`
read -p "Input FTP path: " ftppath

# ftp搭建脚本
useradd vsftpd -s /sbin/nologin
useradd virtusers  -s /sbin/nologin
cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.backup.conf

cat > /etc/vsftpd/vsftpd.conf << EOF
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
anon_upload_enable=NO
anon_mkdir_write_enable=NO
dirmessage_enable=YES
xferlog_enable=YES
chown_uploads=NO
xferlog_file=/var/log/vsftpd.log
xferlog_std_format=YES
accept_timeout=36000
connect_timeout=36000
idle_session_timeout=36000
data_connection_timeout=36000

listen_port=6666
nopriv_user=vsftpd
ftpd_banner=Welcome to FTP service.
chroot_list_enable=YES
allow_writeable_chroot=YES
chroot_local_user=NO
ls_recurse_enable=NO
listen=YES
pasv_enable=YES
pasv_min_port=3500
pasv_max_port=3501
pasv_promiscuous=YES
listen_ipv6=NO
pam_service_name=vsftpd
tcp_wrappers=YES
guest_enable=YES
guest_username=virtusers
userlist_enable=YES
virtual_use_local_privs=YES
user_config_dir=/etc/vsftpd/VirUserConfig
reverse_lookup_enable=NO
EOF

### 日志文件
touch /var/log/vsftpd.log
chown vsftpd.vsftpd /var/log/vsftpd.log

### 虚拟用户配置目录
mkdir /etc/vsftpd/VirUserConfig

### 虚拟用户名单文件
cat > /etc/vsftpd/viruser_passwd << EOF
$user
$pwd
EOF


# 生成虚拟用户数据
db_load -T -t hash -f   /etc/vsftpd/viruser_passwd  /etc/vsftpd/viruser_passwd.db

### pam配置
cat > /etc/pam.d/vsftpd << EOF
#%PAM-1.0

auth    sufficient      /lib64/security/pam_userdb.so     db=/etc/vsftpd/viruser_passwd
account sufficient      /lib64/security/pam_userdb.so     db=/etc/vsftpd/viruser_passwd
#

session    optional     pam_keyinit.so    force revoke
auth       required	pam_listfile.so item=user sense=deny file=/etc/vsftpd/ftpusers onerr=succeed
auth       required	pam_shells.so
auth       include	password-auth
account    include	password-auth
session    required     pam_loginuid.so
session    include	password-auth
EOF

cat > /etc/vsftpd/VirUserConfig/$user << EOF
local_root=${ftppath}
anonymous_enable=NO
write_enable=YES
local_umask=022
anon_upload_enable=NO
anon_mkdir_write_enable=NO
idle_session_timeout=36000
data_connection_timeout=36000
max_clients=0
max_per_ip=0
local_max_rate=0
EOF

### 修改FTP目录权限
chown virtusers:virtusers ${ftppath}
chmod 755 ${ftppath}


###
systemctl start vsftpd.service