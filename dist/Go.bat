@echo off
title 马蜂窝景点爬虫程序
@echo 卸载旧包
pip uninstall mfwScenic
@echo 安装新的包
python setup.py install
@echo 准备成功
pause
python -c "from mafengwo import clearSql;clearSql.ClearSubjectAndViewSpot()"
pause
