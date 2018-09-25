from models import users
from models import messages
from controlers import connection
import datetime


ala = users.User()
ala.username = "Agata2"
ala.email = "agata23@o2.pl"
ala.set_password("passwd",'12')
conn = connection.create_connection("users_db")
cursor = conn.cursor()
ala.save_to_db(cursor)

msg1 = messages.Message()
msg1.from_id = 5
msg1.to_id = 3
msg1.text = 'test w drugą stronę11'
msg1.creation_date = datetime.datetime.now()
conn = connection.create_connection("users_db")
cursor = conn.cursor()
msg1.save_to_db(cursor)



conn = connection.create_connection("users_db")
cursor = conn.cursor()
msg = messages.Message.load_all_messages_for_user(cursor,1)
for row in msg:
    print(f'Message to {row[0]} from {row[1]}. Sent on {row[3]}. Text: "{row[2]}"')

