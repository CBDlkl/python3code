@echo off
title ����Ѿ����������
@echo ж�ؾɰ�
pip uninstall mfwScenic
@echo ��װ�µİ�
python setup.py install
@echo ׼���ɹ�
pause
python -c "from mafengwo import clearSql;clearSql.ClearSubjectAndViewSpot()"
pause
