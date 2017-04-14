# Object for store the content of gameboard
import numpy as np
import pymysql.cursors
from time import gmtime, strftime

class GameBoard:

    m, n, k = 6, 7, 4
    n_players = 2

    def __init__(self, db, room_id, shape = (6,7)):
        # Set the default value of the class    
        self._array = -np.ones(shape=shape, dtype=int)
        self._db = db
        self._room_id = room_id
        self._updated_board = 0
        self._lastplayer = ''

        # Get the room information from database
        try:
            with db.cursor() as cursor:
                sql = "SELECT * FROM game_room WHERE room_id = %s"
                cursor.execute(sql, (room_id))

                result = cursor.fetchone()
                print(result)
                if len(result) > 0:
                    self._holder = result['holder']
                    self._room_create = result['create_datetime']
                    self._room_stage = result['room_stage']
                    self._room_guest = result['guest']
                    self._game_start = result['game_starttime']
                    self._game_status = result['room_stage']
                else:
                    raise ValueError('Room ID does not exists')

        except ValueError:
            print("Error occurs")

    @property
    def room_status(self):
        return self._game_status


    def get_chessstatus(self, myusername):
        # Get the position of the chess from database
        last_user = ''
        try:
            with self._db.cursor() as cursor:
                sql = "SELECT * FROM game_connect4board WHERE room_id = %s ORDER BY step_id"
                cursor.execute(sql, (self._room_id))

                result = cursor.fetchall()
                if len(result) > 0:
                    for steps in range(len(result)):
                        my_step = (result[steps]['username'] != myusername) * 1
                        self._array[result[steps]['row']-1, result[steps]['column']-1] = my_step
                        last_user = result[steps]['username']

                    self._updated_board


                if last_user != '':
                    self._lastplayer = last_user

        except    Exception as error:
            print(error)

        return {'game_board': self._array, 'game_status': self._game_status}

    #TODO: Fail to insert move into Mysql Database
    def set_chessstatus(self, myusername, col, row=0):
        # Get new move
        if self._updated_board == 0:
            self.get_chessstatus

        # Check the last user
        if self._lastplayer == myusername or \
            (self._lastplayer == '' and self._holder != myusername):
            return {'my_turn': False, 'game_board': self._array, 'valid_move': False}

        if self._game_status == "end_game" or \
            self._game_status == "win_game":
            return {'my_turn': False, 'game_board': self._array, 'valid_move': False}
        elif self._room_guest == myusername or self._holder == myusername:
            check_valid = self.checkposition(col, row)
            if check_valid > 0:
                sql = """INSERT INTO game_connect4board (`username`, `game_side`, `room_id`, `row`, 
                `column`, `move_time`) VALUES (%s, %s, %s, %s, %s, %s)"""

                current_game_side = (self._room_guest == myusername) * 1
                current_move_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                row = check_valid

                print("Col" + str(col))
                try:
                    with self._db.cursor() as cursor:
                        cursor.execute(sql, (myusername, current_game_side, self._room_id, 
                            row, col, current_move_time))

                        print(cursor.lastrowid)

                    self._db.commit()

                    self._array[row - 1, col - 1] = 0

                except ValueError:
                    print("Error occurs")

            return {'my_turn' : True, 'game_board': self._array, 'valid_move': (check_valid > 0)}


    def checkposition(self, col, row=0):
        avaliable = -1
        current_col = self._array[:, col-1]

        for cols in range(len(current_col)):
            if current_col[cols] == -1:
                avaliable = cols + 1
                break

        return avaliable

    def find_winner(self, myusername, row=None, col=None):
        # Check if someone has won
        for l in self.get_lines(row=row, col=col):
            if len(l) < self.k:
                pass
            else:
                count = 0
                for x in l:
                    if x == 0:
                        count += 1
                        if count == self.k:
                            try:
                                with self._db.cursor() as cursor:
                                    sql = """INSERT INTO game_roomstage (`room_id`, `room_stage`, 
                                        `username`, `event_datetime`) 
                                        VALUES(%s, %s, %s, %s)"""
                                    current_move_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                    cursor.execute(sql, (self._room_id, "win_game", myusername, current_move_time))

                                    sql = """UPDATE game_room SET room_stage = 'win_game' WHERE 
                                        room_id = %s"""
                                    cursor.execute(sql, (self._room_id))
                                self._db.commit()
                            except ValueError:
                                print("Error occurs")
                            return 0
                    else:
                        count = 0
        # If no one won, check if it is a draw game.
        if self.is_full:
            self._game_status = "end_game"
            try:
                with self._db.cursor() as cursor:
                    sql = """INSERT INTO game_roomstage (`room_id`, `room_stage`, `username`, `event_datetime`) 
                        VALUES(%s, %s, %s, %s)"""
                    current_move_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    cursor.execute(sql, (self._room_id, "end_game", myusername, current_move_time))
                    sql = """UPDATE game_room SET room_stage = 'end_game' WHERE 
                        room_id = %s"""
                    cursor.execute(sql, (self._room_id))
                self._db.commit()
            except ValueError:
                print("Error occurs")
            return -1
        else:
                return None

    def get_lines(self, row=None, col=None):
        board_array = self._array
        n_row, n_col = board_array.shape
        if row is None or col is None:
            # All horizontal lines
            for i in range(n_row):
                yield board_array[i, :]
            # All vertical lines
            for j in range(n_col):
                yield board_array[:, j]
            # All diagonal & anti-diagonal lines
            for i in range(-n_row + 1, n_col):
                yield np.diagonal(board_array, offset=i)
                yield np.diagonal(board_array[:, ::-1], offset=i)
        else:
            # Horizontal line (-) passing (row, col)
            yield board_array[row, :]
            # Vertical line (|) passing (row, col)
            yield board_array[:, col]
            # Diagonal line (\) passing (row, col)
            yield np.diagonal(board_array, offset=col - row)
            # Anti-diagonal line (/) passing (row, col)
            yield np.diagonal(board_array[:, ::-1], offset=n_col - col - 1 - row)

    @property
    def is_full(self):
        return np.all(self._array != -1)