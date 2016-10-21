from mysql import mysqlHelp

mysql = mysqlHelp.mysql_help()


# 清洗主题
def ClearSubject():
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


def ClearSubjectAndViewSpot():
    qyers = mysql.GetAll(" select viewspotid,subject from j_viewspot where source='qyer' ", ())
    for singelQyer in qyers:
        try:
            subjects = singelQyer[1].split(',')
            for singelSubject in subjects:
                subId = mysql.GetAll(" select id from d_subject where subjectName=%s ", (singelSubject.strip()))[0]
                print('查询到景点%s,主题%s的ID为:%s' % (singelQyer[0], singelSubject.strip(), subId[0]))
                mysql.InsertOrUpdate(" insert into j_viewspot_subject(viewspotid,subjectid) values(%s,%s) ",
                                     (singelQyer[0], subId[0]))
        except Exception as e:
            print('系统发生一次错误:', e)


ClearSubjectAndViewSpot()
print('ok!')
