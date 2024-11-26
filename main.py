import psycopg2

from funcs import create_db, add_client, add_phone, change_client, delete_client, delete_phone, find_client

if __name__ == "__main__":
    with psycopg2.connect(database="new_db", user="postgres", password="password") as conn:
        create_db(conn)

        print('\nCREATING DATA FOR 5 CLIENTS:')

        add_client(conn, 1, first_name='Ivan', last_name='Ivanov', email='ivan_ivanov@yandex.ru', phone='+11111111')
        add_client(conn, 2, first_name='Petr', last_name='Petrov', email='petr_petrov@inbox.ru', phone='+222222222')
        add_client(conn, 3, first_name='Sergey', last_name='Sergeev', email='sergey_sergeev@mail.ru')
        add_client(conn, 4, first_name='Alex', last_name='Alexeev', email='alexx@inbox.ru', phone='+4444444')
        add_client(conn, 5, first_name='Bla', last_name='Blabla', email='blablabla@inbox.ru', phone='+0987654321')

        print('\nADDING PHONE TO CLIENT DATA:')

        print('\nTrying to add phone to client data, where we already have their number:')
        add_phone(conn, 4, phone='+333333333')
        print('\nTrying to add phone to client data, where we do not have their number:')
        add_phone(conn, 3, phone='+333333333')

        print('\nCHANGING CLIENT DATA:')

        print('\nTrying to change client data (only name):')
        change_client(conn, 1, first_name='Anton')
        print('\nTrying to change client data (only last name):')
        change_client(conn, 1, last_name='Antonov')
        print('\nTrying to change client data (only email):')
        change_client(conn, 1, email='antonantonov@inbox.ru')
        print('\nTrying to change client data (only phone):')
        change_client(conn, 1, phone='+123')
        print('\nTrying to change client data (first name + last name):')
        change_client(conn, 5, first_name='Name', last_name='Surname')
        print('\nTrying to change client data (email + phone):')
        change_client(conn, 5, email='email', phone='+000000000')
        print('\nTrying to change client data (fist name + phone):')
        change_client(conn, 5, first_name='Newname', phone='+9999999')
        print('\nTrying to change client data (last name + email):')
        change_client(conn, 5, last_name='Newlastname', email='neeeew@yandex.ru')
        print('\nTrying to change ALL client data:')
        change_client(conn, 5, first_name='Viktor', last_name='Viktorov', email='viktorv@inbox.ru', phone='+1234567890')

        print('\nDELETING CLIENT DATA:')

        print('\nTrying to delete client phone number:')
        delete_phone(conn, 3)
        print('\nTrying to delete the same client phone number:')
        delete_phone(conn, 3)
        print('\nTrying to delete ALL client data:')
        delete_client(conn, 4)
        print('\nTrying to delete the same client data:')
        delete_client(conn, 4)

        print('\nFINDING CLIENT DATA:')

        print('\nTrying to find client by first name:')
        find_client(conn, first_name='Anton')
        print('\nTrying to find client by last name:')
        find_client(conn, last_name='Petrov')
        print('\nTrying to find client by email:')
        find_client(conn, email='sergey_sergeev@mail.ru')
        print('\nTrying to find client by phone:')
        find_client(conn, phone='+1234567890')
        print('\nTrying to find client by first name and phone:')
        find_client(conn, first_name='Anton', phone='+123')
        print('\nTrying to find non-existing client:')
        find_client(conn, first_name='Buu')

    conn.close()
