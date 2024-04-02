import sqlite3 as sql


class DatabaseManager:

    def __init__(self):
        self.conn = sql.connect('./data/database.db')
        self.cur = self.conn.cursor()

    def CreateTables(self):
        self.query(
            """CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE,
            title TEXT)""")

        self.query(
            """CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT UNIQUE,
            first_name TEXT)""")

        self.query("""CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT 
        UNIQUE)""")

    def query(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchall()

    def getAdminList(self) -> list[str]:
        AdminList = []
        try:
            AdminList = [contain_id[0] for contain_id in self.fetchall('SELECT user_id FROM admins')]
        except sql.OperationalError:
            print('table subscribers is not admins')
        finally:
            return AdminList

    def getSubscribList(self) -> list[str]:
        SubscribList = []
        try:
            SubscribList = [contain_id[0] for contain_id in self.fetchall('SELECT user_id FROM subscribers')]
        except sql.OperationalError:
            print('table subscribers is not subscribers')
        finally:
            return SubscribList

    def getDataChannels(self) -> dict[str]:
        dataChannel = {}
        try:
            dataChannelbd = self.fetchall('SELECT username, title FROM channels')
            dataChannel = dict(zip(('username', 'title'), dataChannelbd[0]))
        except sql.OperationalError:
            print('not DataChannels')
        finally:
            return dataChannel

    def updateDataChannel(self, nameChannel, newDataChannel):
        titleChannel = newDataChannel.title
        try:
            self.query('UPDATE channels set username = ?, title = ? WHERE id = 1', (nameChannel, titleChannel))
        except sql.Error:
            print('Ошибка при обновление данных')
        finally:
            self.conn.close()

    def __del__(self):
        self.conn.close()
