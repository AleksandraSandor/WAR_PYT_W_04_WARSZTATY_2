import argparse
import models.hasher
from models import User
from psycopg2 import connect, OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



def establish_connection(cnx_cursor):
    username = "aleksandrasandor"
    passwd = "1987lukas"
    hostname = "localhost"
    db_name = "users_db"

    try:
        cnx_cursor[0] = connect(user=username, password=passwd, host=hostname, database=db_name)
        cnx_cursor[0].set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cnx_cursor[1] = cnx_cursor[0].cursor()
        print("Connection established.")
        return cnx_cursor

    except OperationalError:
        print("Failed to connect.")
        return


def end_connection(cnx_cursor_pair):

    cnx_cursor_pair[0].close()
    cnx_cursor_pair[1].close()
    print("Connection closed.")
    return


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        dest="username", default=False,
                        help="Takes input as user's login.")
    parser.add_argument("-p", "--password",
                        dest="password", default=False,
                        help="Takes input as user's password. Checks if there are at least 8 characters.")
    parser.add_argument("-n", "--newpass",
                        dest="newpass", default=False,
                        help="Accepts new password for a user.")
    parser.add_argument("-l", "--list",
                        action="store_true", dest="list", default=False,
                        help="Lists all users.")
    parser.add_argument("-d", "--delete",
                        action="store_true", dest="delete", default=False,
                        help="Deletes provided user login.")
    parser.add_argument("-e", "--edit", action="store_true",
                        dest="edit", default=False,
                        help="Modifies provided user login.")

    options = parser.parse_args()

    return options


def solution(options):

    # -u and -p parameters only (Create user)
    if options.username and options.password and not options.newpass and not options.delete and not options.list and not options.edit:

        user_collection = []
        try:
            user_collection = User.load_all_ids_usernames(cnx_cursor[1])
        except:
            print("Failed to load user data.")

        if len(options.password) < 8:
            return "Password too short. Provide at least 8 characters."
        else:
            for item in user_collection:
                if options.username == item.username:
                    return "Error: User already exists."


            new_user = User()
            new_user.username = options.username
            new_user.email = options.username + "@test.com"
            new_user.set_password(options.password, models.hasher.generate_salt())
            new_user.save_to_db(cnx_cursor[1])
            return "User created."

    # -u -p -e and -n parameters (Modify user password)
    elif options.username and options.password and options.edit and options.newpass and not options.delete and not options.list:

        user_collection = []
        try:
            user_collection = User.load_all_ids_usernames(cnx_cursor[1])
        except:
            print("Failed to load user data.")

        # Check login
        for item in user_collection:
            if options.username == item.username:

                # Load one user
                user_data = User.load_user_by_id(cnx_cursor[1], item.id)

                # Check if password is correct
                if models.hasher.check_password(options.password, user_data.hashed_password) is True:
                    if len(options.newpass) < 8:
                        return "New password too short. Provide at least 8 characters."
                    # Perform operation
                    user_data.set_password(options.newpass, models.hasher.generate_salt())
                    user_data.save_to_db(cnx_cursor[1])
                    return "Password changed."
                else:
                    return "Wrong password."
        return "No such user found. Create new user using parameters: --username and --password"

    # -u -p and -d parameters (Delete user)
    elif options.username and options.password and options.delete and not options.newpass and not options.list and not options.edit:

        user_collection = []
        try:
            user_collection = User.load_all_ids_usernames(cnx_cursor[1])
        except:
            print("Failed to load user data.")

        # Check login
        for item in user_collection:
            if options.username == item.username:

                # Load one user
                user_data = User.load_user_by_id(cnx_cursor[1], item.id)

                # Check if password is correct
                if models.hasher.check_password(options.password, user_data.hashed_password) is True:
                    # Perform operation
                    user_data.delete(cnx_cursor[1])
                    return "User deleted."
                else:
                    return "Wrong password."
        return "No such user found."

    # -l parameter (List all users)
    elif options.list and not options.username and not options.password and not options.delete and not options.newpass and not options.edit:
        user_list = User.list_usernames(cnx_cursor[1])
        user_list.sort()
        print("### List of users ###")
        for username in user_list:
            print(username)
        return "### List ended ###"


    else:
        return "No function for those parameters found. Write '-h' "


if __name__ == "__main__":


    cnx_cursor = ["", ""]
    establish_connection(cnx_cursor)

    print(solution(set_options()))

    end_connection(cnx_cursor)
