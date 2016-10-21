# 清洗主题

from mysql import mysqlHelp

mysql = mysqlHelp.mysql_help()
qyer = mysql.GetAll(" select subject from j_viewspot where `subject` is not null and `subject`!='' ", ())

list = []
for singelQyer in qyer:
    subjects = singelQyer[0].split(',')
    for singelSubject in subjects:
        if singelSubject.strip() not in list:
            list.append(singelSubject.strip())
            print(singelSubject.strip())

print(len(list))

for targ in list:
    mysql.InsertOrUpdate(" insert into d_subject(subjectName,subjectDescribe) values(%s,%s)", (targ, ''))

print('搞定!')
