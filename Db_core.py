import pymssql

server = 'IPv4 address'
database = 'tg_bot_company'
username = 'username_bd'
password = 'password_bd'

connect = pymssql.connect(server, username, password, database)
cursor = connect.cursor()
cursor_2 = connect.cursor()
