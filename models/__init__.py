from models import hasher

class User:

    __id = None
    email = None
    username = None
    __hashed_password = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt):
        self.__hashed_password = hasher.password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO "user"(username, email, hashed_password)
                      VALUES(%s, %s, %s) RETURNING id;"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE "user" SET username=%s, email=%s, hashed_password=%s WHERE id=%s;"""
            values = (self.username, self.email, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True


    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = """SELECT id, username, email, hashed_password FROM "user" WHERE id=%s;"""
        cursor.execute(sql, (user_id, ))
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            print("No user with that id found.")
            return None


    @staticmethod
    def load_all_users(cursor):
        sql = """SELECT id, username, email, hashed_password FROM "user" ;"""
        result = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            result.append(loaded_user)
        return result

    @staticmethod
    def load_all_ids_usernames(cursor):
        sql = """SELECT id, username FROM "user";"""
        result = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            result.append(loaded_user)
        return result

    def delete(self, cursor):
        sql = """DELETE FROM "user" WHERE id=%s"""
        try:
            cursor.execute(sql, (self.__id, ))
            self.__id = -1
            return True
        except AttributeError:
            print("No user with that id found for deletion.")
            return False

    @staticmethod
    def list_usernames(cursor):
        sql = """SELECT username FROM "user";"""
        result = []
        cursor.execute(sql)

        for row in cursor.fetchall():
            result.append(row[0])
        return result


class Message:
    __id = None
    __from_id = None
    __to_id = None
    __message_content = None
    __creation_date = None

    def __init__(self):
        self.__id = -1
        self.__from_id = ""
        self.__message_content = ""
        self.__creation_date = ""


    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = """SELECT id, from_id, to_id, text, creation_date FROM "message" WHERE id=%s;"""
        cursor.execute(sql, (message_id,))
        data = cursor.fetchone()
        if data:
            loaded_mssg = Message()
            loaded_mssg.__id = data[0]
            loaded_mssg.__from_id = data[1]
            loaded_mssg.__to_id = data[2]
            loaded_mssg.__message_content = data[3]
            loaded_mssg.__creation_date = data[4]
            return loaded_mssg
        else:
            print("No message with that id found.")
            return None


    @staticmethod
    def load_all_messages_for_user(cursor, user_id):
        sql = """SELECT message.id, from_id, to_id, text, creation_date, username AS from_user FROM "message"
                    JOIN "user" ON message.from_id="user".id
                    WHERE to_id=%s
                    ORDER BY creation_date DESC;"""
        result = []
        cursor.execute(sql, (user_id,))
        for row in cursor.fetchall():
            loaded_mssg = Message()
            loaded_mssg.__id = row[0]
            loaded_mssg.__from_id = row[1]
            loaded_mssg.__to_id = row[2]
            loaded_mssg.__message_content = row[3]
            loaded_mssg.__creation_date = row[4]
            loaded_mssg.from_user = row[5]
            result.append(loaded_mssg)
        return result


    @staticmethod
    def load_all_messages(cursor):
        sql = """SELECT id, from_id, to_id, text, creation_date FROM "message" 
                  ORDER BY creation_date ASC;"""

        result = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_mssg = Message()
            loaded_mssg.__id = row[0]
            loaded_mssg.__from_id = row[1]
            loaded_mssg.__to_id = row[2]
            loaded_mssg.__message_content = row[3]
            loaded_mssg.__creation_date = row[4]
            result.append(loaded_mssg)
        return result

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO "message"(from_id, to_id, text, creation_date)
                              VALUES(%s, %s, %s, to_timestamp(%s, 'yyyy-mm-dd hh24:mi:ss')) RETURNING id"""
            values = (self.__from_id, self.__to_id, self.__message_content, self.__creation_date)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]
            return True
        else:
            return False

    @property
    def id(self):
        return self.__id

    @property
    def from_id(self):
        return self.__from_id

    @from_id.setter
    def from_id(self, id):
        self.__from_id = id

    @property
    def to_id(self):
        return self.__to_id

    @to_id.setter
    def to_id(self, id):
        self.__to_id = id

    @property
    def creation_date(self):
        return self.__creation_date

    @creation_date.setter
    def creation_date(self, date):
        self.__creation_date = date

    @property
    def message_content(self):
        return self.__message_content

    @message_content.setter
    def message_content(self, content):
        self.__message_content = content
