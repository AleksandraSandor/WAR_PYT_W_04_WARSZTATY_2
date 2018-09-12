from connection import create_connection
from users import User


class Message(object):
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = ""
        self.to_id = ""
        self.text = ""
        self.creation_date = ""

    @property
    def id(self):
        return self.__id

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = '''INSERT INTO message (from_id, to_id, text, creation_date) VALUES(%s, %s, %s, %s) RETURNING id;'''
            values = (self.from_id, self.to_id, self.text, self.creation_date)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        else:
            sql = '''UPDATE message SET from_id=%s, to_id=%s, text=%s, creation_date=%s WHERE id=%s;'''
            values = (self.from_id, self.to_id, self.text, self.creation_date, self.id)
            cursor.execute(sql, values)
            return True
        return False

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = '''SELECT id, from_id, to_id, text, creation_date FROM message WHERE id=%s;'''
        cursor.execute(sql, (message_id,))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data[0]
            loaded_message.from_id = data[1]
            loaded_message.to_id = data[2]
            loaded_message.text = data[3]
            loaded_message.creation_date = data[4]
            return loaded_message
        else:
            return None

    @staticmethod
    def load_all_messages_for_user(cursor, user_id):
        sql = '''select t.username, u.username, m.text, m.creation_date  
                  from message m join "user" u on m.from_id = u.id join "user" t on m.to_id=t.id
                  where m.from_id = %s order by m.creation_date;'''
        ret = []
        cursor.execute(sql, (user_id,))
        for row in cursor.fetchall():
            ret.append(row)
        return ret

    @staticmethod
    def load_all_messages(cursor):
        sql = '''SELECT id, from_id, to_id, text, creation_date FROM message;'''
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.creation_date = row[4]
            ret.append(loaded_message)
        return ret

    def message(self, cursor):
        sql = '''DELETE FROM message WHERE id=%s;'''
        cursor.execute(sql, (self.__id,))
        self.__id = -1
        return True
