#!/root/.pyenv/versions/3.6.3/bin/python
# coding: utf-8
# RDS备份

import subprocess
import time

user = "root"
pwd = "IlcjbiLP4Y4Yvmp"

mysqlip_dic = {"172.16.6.10": [str(x) for x in range(0, 4)],   #MYSQL01
               "172.16.6.14": [str(x) for x in range(4, 8)],   #MYSQL02
               "172.16.6.6": ["8", "9", "a", "b"],             #MYSQL03
               "172.16.6.4": ["c", "d", "e", "f"]              #MYSQL04
               }

flag_list = []


def backup():
    current_time = None
    for ip in mysqlip_dic:
        current_time = time.ctime()
        data_id_list = mysqlip_dic[ip]   # ['0','1','2','3']
        for dbid in data_id_list:
            ### 清空本地mysql数据库
#            print('######################################## alice_prd_%s ########################################' % dbid)
#            cmd1 = '''mysql -uroot -proot -e \"drop database if exists alice_prd_%s;\"''' % dbid
#            print('cmd1：', cmd1)
#            p1 = subprocess.Popen(cmd1, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#            out1, err1 = p1.communicate()
#            # print('out1', out1.decode())
#            if err1.decode() is not "":
#                print('err1', err1.decode())
#                flag_list.append("%s alice_prd_%s db delete wrong\n" % (current_time, dbid))
#                continue
            ### 备份
#            cmd2 = "mysqldump -h%s -u%s -p%s --databases alice_prd_%s " \
#                   "--single-transaction --master-data=2 > /data/rds_backup/SQL/alice_prd_%s.sql" \
#                   % (ip, user, pwd, dbid, dbid)
            cmd2 = "mysqldump -h%s -u%s -p%s --databases alice_prd_%s " \
                   "-n --single-transaction --master-data=2 | gzip > /data/rds_backup/SQL/alice_prd_%s.sql.gz" \
                   % (ip, user, pwd, dbid, dbid)
            print('cmd2：', cmd2)
            p2 = subprocess.Popen(cmd2, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            out2, err2 = p2.communicate()
            # print('out2', out2.decode())
            if err2.decode() is not "":
                print('err2', err2.decode())
                flag_list.append("%s alice_prd_%s backup wrong\n" % (current_time, dbid))
                continue
            ### 导入
#            cmd3 = '''mysql -uroot -proot < /data/rds_backup/SQL/alice_prd_%s.sql''' % dbid
#            print('cmd3：', cmd3, '\n')
#            p3 = subprocess.Popen(cmd3, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#            out3, err3 = p3.communicate()
#            # print('out3', out3.decode())
#            if err3.decode() is not "":
#                print('err3', err3.decode())
#                flag_list.append("%s alice_prd_%s db import wrong\n" % (current_time, dbid))
#                continue
    return current_time, flag_list


def status(current_time, flag_list):
    flag_string = ''.join(flag_list)
    with open('/data/rds_backup/backup.log', 'w') as f:
        if flag_list:
            f.write(flag_string)
        else:
            f.write("%s DONE" % current_time)


if __name__ == "__main__":
    current_time, flag_list = backup()
    status(current_time, flag_list)

