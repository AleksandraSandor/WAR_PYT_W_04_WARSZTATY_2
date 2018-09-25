from models.users import User
from models.messages import Message
from controlers.connection import create_connection
import datetime


ala = User()
ala.username = "Agata2"
ala.email = "agata23@o2.pl"
ala.set_password("passwd",'12')
conn = create_connection("users_db")
cursor = conn.cursor()
ala.save_to_db(cursor)

msg1 = Message()
msg1.from_id = 5
msg1.to_id = 3
msg1.text = 'test w drugą stronę11'
msg1.creation_date = datetime.datetime.now()
conn = create_connection("users_db")
cursor = conn.cursor()
msg1.save_to_db(cursor)



conn = create_connection("users_db")
cursor = conn.cursor()
msg = Message.load_all_messages_for_user(cursor,1)
for row in msg:
    print(f'Message to {row[0]} from {row[1]}. Sent on {row[3]}. Text: "{row[2]}"')

