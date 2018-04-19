import os
import time
import re
from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error
import datetime

def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

def writeToDatabase(title, description):
    query = "INSERT INTO happy_minute(title,description,`time`) " \
            "VALUES(%s,%s, NOW());"
    args = (title, description)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        cursor.execute(query, args)
        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

def checkTime(hour, minute):
    # if hour == minute:
    writeToDatabase(str(hour) + ":" + str(minute), "Matched")

def checkKernelTime(hour, minute):
    kernel_info = os.uname()
    regex = r"(\S{3} \S{3} \d+ (\d+):(\d+):\d+ \S{3} \d+)"
    matches = re.findall(regex, kernel_info[3])
    if matches[0][1] == hour and matches[0][2] == minute:
        writeToDatabase(matches[0][1] + ":" + matches[0][2], "Happy birthminute! " + matches[0][1])

def run():
    now = datetime.datetime.now()
    checkTime(now.hour, now.minute)
    checkKernelTime(now.hour, now.minute)

if __name__ == '__main__':
    run()