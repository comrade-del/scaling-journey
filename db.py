import sqlite3
# from dbm import error
# from distutils.log import error


class Database:
    def __init__(self):
        # connect db
        global conn
        conn = sqlite3.connect("newv.db")

        if conn:
            print("Connected Successfully")
        else:
            print("Connection Not Established")

        global cur
        cur = conn.cursor()

    def create_table(self):
        # create admin table
        cur.execute('''DROP TABLE IF EXISTS users''')
        cur.execute('''CREATE TABLE IF NOT EXISTS users (User_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Firstname VARCHAR(50) NOT NULL, 
                    Lastname VARCHAR(50) NOT NULL,
                    Username VARCHAR(50) NOT NULL,
                    Password VARCHAR NOT NULL,
                    Profile_id INT(1) NOT NULL,
                    Validity VARCHAR(50) NOT NULL,
                    Status VARCHAR(50) NOT NULL)''')

        # create candidate table
        cur.execute('''DROP TABLE IF EXISTS candidates''')
        cur.execute('''CREATE TABLE IF NOT EXISTS candidates (candidate_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Firstname VARCHAR(50) NOT NULL,
                    Lastname VARCHAR(50) NOT NULL,
                    Gender VARCHAR(50) NOT NULL,
                    vote_count bigint NOT NULL,
                    Validity VARCHAR(50) NOT NULL)''')
        conn.commit()

    def insert_values(self):
        # inserting default data
        # users
        cur.execute('''INSERT INTO users(User_id, Firstname, Lastname, Username, Password, Profile_id, Validity, Status) VALUES (1000, 'Joe', 'Jay', 'admin1', 1234, 1, 'valid', 'no need')''')
        cur.execute('''INSERT INTO users(Firstname, Lastname, Username, Password, Profile_id, Validity, Status) VALUES ('Jane', 'Joe', 'user1', 1111, 2, 'valid', 'not voted')''')
        cur.execute('''INSERT INTO users(Firstname, Lastname, Username, Password, Profile_id, Validity, Status) VALUES ('Jay', 'Jane', 'user2', 2222, 2, 'valid', 'not voted')''')
        # candidate
        cur.execute('''INSERT INTO candidates(candidate_id, Firstname, Lastname, Gender, vote_count, validity) VALUES (1000, 'John','Doe', 'Male', 0, 'valid')''')
        cur.execute('''INSERT INTO candidates(Firstname, Lastname, Gender, vote_count, validity) VALUES ('Jane', 'Doe', 'Female', 0, 'invalid')''')
        conn.commit()

        # commented out to avoid resetting the tables

    # adding new users, works

    def signup(self):
        f_name = input('Firstname: ')
        l_name = input('Lastname: ')
        u_name = input('Username: ')
        code = int(input('4-6 digit passcode: '))
        profile = 2
        validity = 'pending'
        status = 'not voted'
        try:
            cur.execute('''INSERT INTO users(Firstname, Lastname, Username, Password, Profile_id, Validity, Status) VALUES (?, ?, ?, ?, ?, ?)''', (f_name, l_name, u_name, code, profile, validity, status))
            print('Successfully added')
        except:
            print("Couldn't add to database")

    # login process, works
    """        username = Welcome_Page.username.get()
        password = Welcome_Page.password.get()
        passw = int(password)

        name = cur.execute('''SELECT ? FROM users''', (username,)).fetchone()[0]
        pas = cur.execute('''SELECT Password FROM users WHERE Username=? ''', (name,)).fetchone()[0]
        print(name, pas)
        profile = cur.execute('''SELECT Profile_id FROM users WHERE Username=? ''', (username,)).fetchone()[0]
        validity = cur.execute('''SELECT Validity FROM users WHERE Username=? ''', (username,)).fetchone()[0]"""

    def login(self):
        name = input('Username: ')
        code = input('Password: ')
        profile = cur.execute('''SELECT Profile_id FROM users WHERE Username=? ''', (name,)).fetchone()[0]
        details = cur.execute('''SELECT Password FROM users WHERE Username=? ''', (name,)).fetchone()[0]
        # detail = cur.execute('''SELECT Password FROM users WHERE Profile_id=1''').fetchone()[0]
        validity = cur.execute('''SELECT Validity FROM users WHERE Username=? ''', (name,)).fetchone()[0]
        if details == code:
            print(profile, validity)
            if profile == 1:
                print(f'Welcome {name}')
                self.admin_duties()
            elif profile == 2:
                if validity == 'valid':
                    print(f'Welcome {name}')
                    self.vote()
                else:
                    print(f'Welcome {name}')
                    print('Not eligible to vote')
        else:
            print('Invalid login')

    # admin duties, works
    def admin_duties(self):
        self.action = int(input('''\n[1] Add candidate\n[2] Block or Unblock candidate\n[3] Validate voters\n[4] View results\nWhat would you like to do?: '''))
        if self.action == 1:  # add candidate
            party = input('Party name: ')
            candidate = input('Candidate name: ')
            votes = 0  # till I find a better alternative
            validity = 'valid'
            cur.execute('''INSERT INTO candidates(Firstname, Lastname, Gender, vote_count, validity) VALUES (?,?, ?,?,?)''', (party, candidate, votes, validity))
        elif self.action == 2:  # block candidate
            candidate = input('Candidate name: ')
            choice =input('Do you wish to block or unblock this candidate: ')
            if choice == 'block':
                try:
                    cur.execute('''UPDATE candidates SET validity='invalid' WHERE Firstname=?''', (candidate,))
                    print('Blocked successfully')
                except:
                    cur.execute('''UPDATE candidates SET validity='invalid' WHERE Lastname=?''', (candidate,))
                    print('Blocked successfully')
                finally:
                    print('Not in database')
            elif choice == 'unblock':
                try:
                    cur.execute('''UPDATE candidates SET validity='invalid' WHERE Firstname=?''', (candidate,))
                    print('Blocked successfully')
                except:
                    cur.execute('''UPDATE candidates SET validity='invalid' WHERE Lastname=?''', (candidate,))
                    print('Blocked successfully')
                finally:
                    print('Not in database')
        elif self.action == 3:
            voters = cur.execute('''SELECT * FROM users WHERE Profile_id=2''').fetchall()
            print(voters)
            voter = input('Choose voter to validate: ')
            cur.execute('''UPDATE users SET validity='valid' WHERE Username=?''', (voter,))
        elif self.action == 4:
            results = cur.execute('''SELECT * FROM candidates''').fetchall()
            print(results)

    # voting process, works
    def vote(self):
        na = input('Username: ')
        status = cur.execute('''SELECT Status FROM users WHERE Username=? ''', (na,)).fetchone()[0]
        if status == 'not voted':
            can = cur.execute('''SELECT * FROM candidates WHERE validity='valid' ''').fetchone()
            print(f'These are the candidates you can vote for: {can}')
            self.candidate = input('Choose Candidate: ')
            print(self.candidate)
            if self.candidate in can:
                cur.execute("UPDATE candidates SET vote_count=vote_count+1 WHERE Firstname=?", (self.candidate,))
                print('Vote casted, you may log out now.')
            elif self.candidate not in can:
                print('Candidate cannot be voted for')
            cur.execute('''UPDATE users SET status='voted' WHERE Username=?''', (na,))
        else:
            print("Can't vote again")

        """
         # orrrrrrr
        self.candidate = input('Choose Candidate: ')
        print(self.candidate)
        can = cur.execute('''SELECT validity FROM candidates WHERE candidate_name=?''', (self.candidate,)).fetchone()[0]
        if can == 'valid':
            cur.execute("UPDATE candidates SET vote_count=vote_count+1 WHERE candidate_name=?", (self.candidate,))
        elif can == 'invalid':
            print('Candidate cannot be voted for')
        """


#  main process, finally I see the use of functions
ty = Database()
ty.create_table()
ty.insert_values()

"""choice = input('Login or Sign up?: ')
if choice == 'login':
    ty.login()
elif choice == 'sign up':
    ty.signup()
else:
    print('Invalid')"""


ty.func = cur.execute('''UPDATE users SET Status='not voted' WHERE Profile_id=2''')
ty.func = cur.execute('''UPDATE candidates SET Validity='valid' ''')

# commit
conn.commit()

# close cursor and connection
conn.close()
