@echo off
title ����Ѿ����������
@echo ж�ؾɰ�
pip uninstall mfwScenic
@echo ��װ�µİ�
python setup.py install
@echo ׼�����
pause
python -c "from mafengwo import scenic;scenic.Go()"
pause
