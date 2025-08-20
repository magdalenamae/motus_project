class User: 
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.hash_pw = None
        self.email = email
        self.last_login = None
        self.created_on = None

    def save(self, conn):
        if self.user_id is None: 
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO motus_users (username, email, hash_pw) VALUES (%s, %s, %s) '
                'RETURNING user_id, username, email',
                [self.username, self.email, self.hash_pw]
            )
            new_user = cur.fetchone()
        else: 
            self.update(self, conn)

    def update(self, conn):
        cur = conn.cursor()
        cur.execute(
            'UPDATE motus_users SET username=%s, email=%s, hash_pw=%s WHERE user_id=%s',
            [self.username, self.email, self.hash_pw, self.user_id]
        )

    @classmethod
    def get_user_via_email(cls, email, conn):
        cur = conn.cursor()
        cur.execute(
            "SELECT email, hash_pw, user_id, username, last_login, created_on FROM motus_users WHERE email = %s",
            [email]
        )
        row = cur.fetchone()
        if row is None:
            return None
        
        user = User(
            email=row[0],
            user_id=row[2],
            username=row[3]
        )
        user.hash_pw = row[1]
        user.last_login = row[4]
        user.created_on = row[5]
        return user


class Ride:
    def __init__(self, ride_id, user_id, ride_description, ride_start, ride_end):
        self.ride_id = ride_id
        self.user_id = user_id
        self.ride_description = ride_description
        self.ride_start = ride_start
        self.ride_end = ride_end

    def save(self, conn):
        if self.ride_id is not None:
            self.update(conn)
        else:
            self.insert(conn)

    def update(self, conn):
        cur = conn.cursor()
        cur.execute(
            'UPDATE rides SET user_id=%s, ride_description=%s, ride_start=%s, ride_end=%s WHERE ride_id=%s',
            [self.user_id, self.ride_description, self.ride_start, self.ride_end, self.ride_id]
        )

    def insert(self, conn):
        cur = conn.cursor()
        cur.execute(
            '''
            INSERT INTO rides (user_id, ride_description, ride_start, ride_end)
            VALUES (%s, %s, %s, %s)
            RETURNING ride_id
            ''',
            [self.user_id, self.ride_description, self.ride_start, self.ride_end]
        )
        self.ride_id = cur.fetchone()[0]

    @classmethod
    def get_rides_for_user(cls, user_id, conn):
        cur = conn.cursor()
        cur.execute(
            '''
            SELECT ride_id, user_id, ride_description, ride_start, ride_end
            FROM rides
            WHERE user_id = %s
            ORDER BY ride_id DESC
            ''',
            [user_id]
        )
        return cur.fetchall()
    
    @classmethod
    def delete_ride(cls, ride_id, conn):
        cur = conn.cursor()
        cur.execute('DELETE FROM rides WHERE ride_id = %s', [ride_id])
        