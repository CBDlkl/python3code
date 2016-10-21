import json

import time

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


# 填充主题和景点的外键关系表
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


# 解析价格(price)
def ClearPrice():
    allInfo = mysql.GetAll(" select viewspotid,source,price,youpujson,mfwjson,qyerjson,mfwdetailjson from j_viewspot ",
                           ())

    for singelRow in allInfo:

        if singelRow[1] == 'mafengwo':
            mfwJson = json.loads(singelRow[6])
            mfwPrice = mfwJson['门票']
            if mfwPrice != "":
                mysql.InsertOrUpdate(" update j_viewspot set price=%s where viewspotid=%s  ",
                                     (mfwPrice, singelRow[0]))

        if singelRow[1] == 'youpu':
            if singelRow[3] != '' and singelRow[3] != None:
                youpuJson = json.loads(singelRow[3])
                youpuPrice = youpuJson['price']
                if youpuPrice != "":
                    mysql.InsertOrUpdate(" update j_viewspot set price=%s where viewspotid=%s  ",
                                         (youpuPrice, singelRow[0]))



print('ok!', time.localtime())
