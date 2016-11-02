from distutils.core import setup

# 发布马蜂窝景点抓取代码
setup(
    name="mfwScenic",
    version="1.0",
    py_modules=['mafengwo.scenic', 'mafengwo.clearSql', 'mysql.mysqlHelp'],
    data_files=[('do', ['Go.bat'])],
)
