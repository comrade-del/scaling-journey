import socket
import pickle
import threading
import sqlite3

IP = socket.gethostbyname(socket.gethostname())
PORT = 2003
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
HEADERSIZE = 10
DISCONNECT_MSG = "DISCONNECT"

conn = sqlite3.connect("newv.db", check_same_thread=False)
cur = conn.cursor()


def handle_client(s, addr):
    print(f"[NEW] {addr}")
    connected = True
    while connected:
        msg = s.recv(SIZE).decode(FORMAT)
        if msg == "sign in":
            print(f"[{addr}] {msg}")
            mg = conn.recv(SIZE).decode(FORMAT)
            mgg = str(mg)
            name = cur.execute('''SELECT ? FROM users''', (mgg,)).fetchone()[0]
            pas = cur.execute('''SELECT Password FROM users WHERE Username=? ''', (name,)).fetchone()[0]
            print(name, pas)
            profile = cur.execute('''SELECT Profile_id FROM users WHERE Username=? ''', (mgg,)).fetchone()[0]
            validity = cur.execute('''SELECT Validity FROM users WHERE Username=? ''', (mgg,)).fetchone()[0]
            s.send(name.encode(FORMAT))
            s.send(pas.encode(FORMAT))
            s.send(str(profile).encode(FORMAT))
            s.send(validity.encode(FORMAT))
        if msg == 'sign up':
            print(f"[{addr}] {msg}")
            firstname = conn.recv(SIZE).decode(FORMAT)
            lastname = conn.recv(SIZE).decode(FORMAT)
            username = conn.recv(SIZE).decode(FORMAT)
            password = conn.recv(SIZE).decode(FORMAT)
            profile = 2
            validity = 'pending'
            status = 'not voted'
            cur.execute(
                '''INSERT INTO users(Firstname, Lastname, Username, Password, Profile_id, Validity, Status) VALUES (?, ?, ?, ?, ?, ?,?)''',
                (firstname, lastname, username, password, profile, validity, status))
            conn.commit()
        if msg == 'admin':
            print(f"[{addr}] {msg}")
            detail = cur.execute('''SELECT Password FROM users WHERE Profile_id=1''').fetchone()[0]
            mss = f"{detail}"
            s.send(mss.encode(FORMAT))
        if msg == 'candidates':
            print(f"[{addr}] {msg}")
            d = cur.execute('''SELECT candidate_id, Firstname, Lastname, Validity FROM candidates WHERE validity='valid' ''').fetchall()
            mgg = pickle.dumps(d)
            s.send(mgg)
        if msg == 'delete voter':
            print(f"[{addr}] {msg}")
            index = conn.recv(SIZE).decode(FORMAT)
            who = cur.execute('''SELECT Firstname, Lastname FROM users WHERE User_id=?''', (index,)).fetchone()
            cur.execute('''UPDATE users SET validity='invalid' WHERE User_id=?''', (index,))
            conn.commit()
            can = cur.execute(
                '''SELECT User_id, Firstname, Lastname, Validity FROM users WHERE Profile_id=2 ''').fetchall()
            mss = f"{who}"
            s.send(mss.encode(FORMAT))
            mgg = pickle.dumps(can)
            s.send(mgg)
    s.close()


def main():
    print("[Started] Yayy")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen()
    print(f"[Listening] {IP}:{PORT}")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE]: {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
