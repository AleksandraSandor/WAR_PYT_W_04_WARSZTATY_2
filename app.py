from models import User
from controlers import connection

ala = User()
ala.username = "Agata"
ala.email = "agata@o2.pl"
ala.set_password("passwd",'12')
conn = connection.create_connection("users_db")
cursor = conn.cursor()
ala.save_to_db(cursor)
