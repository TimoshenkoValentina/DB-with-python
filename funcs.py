from typing import Optional, List
from psycopg2.sql import SQL, Identifier


def create_db(conn):
    cur = conn.cursor()

    cur.execute("""
    DROP TABLE phones;
    DROP TABLE clients;
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
            id INTEGER UNIQUE PRIMARY KEY,
            first_name VARCHAR(40),
            last_name VARCHAR(60),
            email VARCHAR(60)
            );
            """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id),
            phone VARCHAR(12)
            );
            """)
    conn.commit()


def add_client(
        conn,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional = None,
):
    print('\nAdding new client data (client id, first name, last name, email):')
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clients(id, first_name, last_name, email) 
        VALUES(%s, %s, %s, %s) RETURNING id, first_name, last_name, email;
        """, (id, first_name, last_name, email))
    conn.commit()
    print(cur.fetchone())
    if phone is not None:
        print('Their phone number (phone id, client id, phone):')
        cur.execute("""
            INSERT INTO phones(client_id, phone) 
            VALUES(%s, %s) RETURNING id, client_id, phone;
            """, (id, phone))
        conn.commit()
        print(cur.fetchone())
    else:
        print('No phone number yet')


def add_phone(
        conn,
        client_id: int,
        phone: str,
):
    print('Adding phone to client:')
    cur = conn.cursor()
    cur.execute("""
        SELECT phone FROM phones WHERE client_id=%s;
        """, (client_id,))
    phone_info = cur.fetchone()
    if phone_info is None:
        cur.execute("""
            INSERT INTO phones(client_id, phone) 
            VALUES(%s, %s);
            """, (client_id, phone))
        conn.commit()
        cur.execute("""
            SELECT * FROM phones WHERE client_id=%s;
            """, (client_id, ))
        print(cur.fetchone())
        cur.execute("""
            SELECT * FROM clients WHERE id=%s;
            """, (client_id,))
        print(cur.fetchone())
    else:
        print('For this client phone is already in database')


def change_client(
        conn,
        client_id: int,
        first_name: Optional = None,
        last_name: Optional = None,
        email: Optional = None,
        phone: Optional = None
):

    cur = conn.cursor()
    if first_name is not None:
        cur.execute("""
                UPDATE clients SET first_name=%s WHERE id=%s;
                """, (first_name, client_id))
        conn.commit()
    if last_name is not None:
        cur.execute("""
                UPDATE clients SET last_name=%s WHERE id=%s;
                """, (last_name, client_id))
        conn.commit()
    if email is not None:
        cur.execute("""
                UPDATE clients SET email=%s WHERE id=%s;
                """, (email, client_id))
        conn.commit()
    if phone is not None:
        cur.execute("""
                UPDATE phones SET phone=%s WHERE client_id=%s;
                """, (phone, client_id))
        conn.commit()
    cur.execute("""
        SELECT * FROM phones WHERE client_id=%s;
        """, (client_id, ))
    print(cur.fetchone())
    cur.execute("""
        SELECT * FROM clients WHERE id=%s;
        """, (client_id,))
    print(cur.fetchone())


def delete_phone(conn, client_id: int):
    cur = conn.cursor()
    cur.execute("""
        SELECT phone FROM phones WHERE client_id=%s;
        """, (client_id,))
    client_number = cur.fetchone()
    if client_number is not None:
        cur.execute("""
            DELETE FROM phones WHERE client_id=%s;
            """, (client_id, ))
        conn.commit()
        cur.execute("""
            SELECT * FROM phones WHERE client_id=%s;
            """, (client_id,))
        print('Deleted successfully, current client number: ', cur.fetchone())
    else:
        print('Current client has no phone number')


def delete_client(conn,
                  id: int):
    cur = conn.cursor()
    print('Trying to delete phone:')
    delete_phone(conn, id)
    print('Trying to delete client data:')
    cur.execute("""
        SELECT * FROM clients WHERE id=%s;
        """, (id,))
    client_data = cur.fetchone()
    if client_data is not None:
        cur.execute("""
            DELETE FROM clients WHERE id=%s;
            """, (id, ))
        conn.commit()
        cur.execute("""
            SELECT * FROM clients WHERE id=%s;
            """, (id,))
        print('Deleted successfully, current client data: ', cur.fetchone())
    else:
        print('Current client has been already deleted or never has been added to db')


def find_client(
        conn,
        first_name: Optional = None,
        last_name: Optional = None,
        email: Optional = None,
        phone: Optional = None
):

    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM clients c
        LEFT JOIN phones p ON c.id = p.client_id
        WHERE (first_name = %(first_name)s OR %(first_name)s IS NULL)
        AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
        AND (email = %(email)s OR %(email)s IS NULL)
        AND (phone = %(phone)s OR %(phone)s IS NULL);
        """, {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone})

    client = cur.fetchone()
    if client is not None:
        print(client)
    else:
        print('No client data was found')
