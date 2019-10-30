#!/bin/bash
backup_dir=/data/mongo_backup
backup_log=/data/mongo_backup/backup.log
hostname=127.0.0.1
db_user="mongoadmin"
db_pass="secret"
db_port=17017
db_name="statistic_job"
mongodump=/bin/mongodump

#echo "#backup mongodb" >>/var/spool/cron/root
#echo "0 9 * * * sh /data/backup-mongodb.sh" >> /var/spool/cron/root

if [ ! -d $backup_dir ]
then
    mkdir $backup_dir -p
fi

$mongodump --host $hostname --port $db_port -u $db_user -p $db_pass -d $db_name --archive=$backup_dir/${db_name}-$(date +%F-%H).gz &>> $backup_log

if [ $? -eq 0 ]
then
    echo -e "$(date +%F-%T)\t mongodb backup success !" >> $backup_log
else
    echo -e "$(date +%F-%T)\t mongodb backup failed !" >> $backup_log
fi
