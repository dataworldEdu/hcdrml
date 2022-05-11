import configparser
import json


config = configparser.ConfigParser()
config.read('app/config.ini')

cFlag = 1   # 1: 개발서버, 2: 로컬

DBSETTING = {}

if cFlag == 1:
    DBSETTING = {
        'host': config['DEVDB']['HOST'],
        'port': config['DEVDB']['PORT'],
        'user': config['DEVDB']['USER'],
        'passwd': config['DEVDB']['PASSWD'],
        'database': config['DEVDB']['DATABASE'],
        'charset': config['DEVDB']['CHARSET']
    }
else:
    DBSETTING = {
        'host': config['LOCALDB']['HOST'],
        'port': config['LOCALDB']['PORT'],
        'user': config['LOCALDB']['USER'],
        'passwd': config['LOCALDB']['PASSWD'],
        'database': config['LOCALDB']['DATABASE'],
        'charset': config['LOCALDB']['CHARSET']
    }