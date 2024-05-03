import math
import random
import Physics

TABLE_CENTER_X = Physics.TABLE_WIDTH / 2.0
BALL_DIAMETER = Physics.BALL_DIAMETER + 5.0
BALL_RADIUS = Physics.BALL_RADIUS + 2.5
ADJUSTMENT = math.sqrt(3.0)/2.0

class GameEngine:
    def __init__(self):
        self.game: Physics.Game = None
        self.table: Physics.Table = None
        self.table_id = 0
        self.current_player = 1
        self.shoot_animation_data = []
        self.player_one_ball_set = None
        self.player_two_ball_set = None
        self.game_over = False
        self.winner = 0
        self.switch_player = False
        self.player_one_ball_set_name = ""
        self.player_two_ball_set_name = ""

    def shoot(self, params):
        # self.table_id = 0  #  for debug only
        self.game.shoot(
            self.game.gameName, self.get_current_player_name(), self.table, params['xvel'], params['yvel'])
        print("Preparing shot data...")
        self.playGame()
        
        
    def playGame(self):
        self.switch_player = False
        self.collect_shoot_frames(self.table_id)
        
        self.table = self.shoot_animation_data[len(self.shoot_animation_data) - 1]
        
        if len(self.shoot_animation_data) == 0 and self.table:
            # something is wrong. Physics returned no frames after shot
            self.shoot_animation_data.append(self.table)

        low_set = self.table.get_low_ball_set()
        high_set = self.table.get_high_ball_set()
        blackBall = self.table.blackBall()

        # it is not defined yet which player plays high or low
        if self.player_one_ball_set is None or self.player_two_ball_set is None:
            if len(low_set) < len(high_set):
                self.set_ball_set_to_players(low_set, high_set)
            elif len(low_set) > len(high_set):
                self.set_ball_set_to_players(high_set, low_set)
            elif len(low_set) == len(high_set) and len(low_set) < 7: # equal balls sunk. Need to find from what set ball was sunk first
                first_set, second_set = self.get_first_sunk_set(self.shoot_animation_data, low_set, high_set)
                self.set_ball_set_to_players(first_set, second_set)
        
        currentPlayerBallSet = self.player_one_ball_set if self.current_player == 1 else self.player_two_ball_set
        
        if self.player_one_ball_set is not None and self.player_two_ball_set is not None:
            if self.player_one_ball_set_name == "" or self.player_two_ball_set_name == "":
                self.player_one_ball_set_name = "High" if self.arrays_are_equal(self.player_one_ball_set, high_set) else "Low"
                self.player_two_ball_set_name = "High" if self.arrays_are_equal(self.player_two_ball_set, high_set) else "Low"
            
            start_frame = self.shoot_animation_data[0]
            start_low_set = start_frame.get_low_ball_set()
            start_high_set = start_frame.get_high_ball_set()
            start_player_ball_set = start_high_set if self.arrays_are_equal(currentPlayerBallSet, high_set) else start_low_set
            if currentPlayerBallSet is not None and start_player_ball_set is not None:
                if len(currentPlayerBallSet) == len(start_player_ball_set):
                    self.switch_player = True

        # let's check for the game end
        if (currentPlayerBallSet is None or len(currentPlayerBallSet) > 0) and blackBall is None:
            self.game_over = True
            self.winner = 1 if (self.current_player == 1) else 2
            return

        if (currentPlayerBallSet is None or len(currentPlayerBallSet) == 0) and blackBall is None:
            self.game_over = True
            self.winner = self.current_player
            return
        
        # if cue ball sunk, need to return it to initial position
        cueBall = self.table.cueBall()
        if cueBall is None:
            self.table += Physics.StillBall(0, Physics.Coordinate(TABLE_CENTER_X, Physics.TABLE_LENGTH - TABLE_CENTER_X))
            
        self.table_id = self.table_id + len(self.shoot_animation_data) - 1
        
        
    def get_first_sunk_set(self, shoot_frames, low_set, high_set):
        for frame in shoot_frames:
            l_set = frame.get_low_ball_set()
            h_set = frame.get_high_ball_set()
            if len(l_set) < len(h_set):
                return low_set, high_set
            elif len(l_set) > len(h_set):
                return high_set, low_set

        return low_set, high_set
     
    def arrays_are_equal(self, arr1, arr2):
        if arr1 is None or arr2 is None:
            return False
        if len(arr1) != len(arr2):
            return False
        for i in range(len(arr1)):
            if arr1[i] != arr2[i]:
                return False
        return True

    def set_ball_set_to_players(self, ball_set, another_set):
        if self.current_player == 1:
            self.player_one_ball_set = ball_set
            self.player_two_ball_set = another_set
        else:
            self.player_one_ball_set = another_set
            self.player_two_ball_set = ball_set

    def get_current_player_name(self):
        return self.get_player_name(self.current_player)
       
    def get_player_name(self, player):
        return self.game.player1Name if (player == 1) else self.game.player2Name
       
    def collect_shoot_frames(self, start_id):
        self.shoot_animation_data = []
        db = Physics.Database()
        table = db.readTable(start_id)
        if table:
            self.shoot_animation_data.append(table)
        while table:
            start_id += 1
            table = db.readTable(start_id)
            if table:
                self.shoot_animation_data.append(table)
        db.close()
    
    def get_next_player(self):
        if self.switch_player:
            return 2 if (self.current_player == 1) else 1
        else:
            return self.current_player
        
    def create_new_game(self, game_name, player_one, player_two):
        self.table_id = 0
        self.current_player = random.randint(1, 2)
        self.shoot_animation_data = []
        self.player_one_ball_set = None
        self.player_two_ball_set = None
        self.player_one_ball_set_name = ""
        self.player_two_ball_set_name = ""
        self.game_over = False
        self.winner = 0
        self.switch_player = False

        db = Physics.Database(reset=True)  # clear database
        db.close()
        
        self.table = Physics.Table()

        # 1 ball (Yellow)
        pos = Physics.Coordinate(TABLE_CENTER_X, TABLE_CENTER_X)
        self.table += Physics.StillBall(1, pos)

# *******************************************

        # 2 ball (BLUE)
        pos = Physics.Coordinate(TABLE_CENTER_X - BALL_RADIUS,
                                 TABLE_CENTER_X - ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(2, pos)

        # 9 ball (LIGHTYELLOW)
        pos = Physics.Coordinate(TABLE_CENTER_X + BALL_RADIUS,
                                 TABLE_CENTER_X - ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(9, pos)

# *******************************************
        # 3 ball (RED)
        pos = Physics.Coordinate(TABLE_CENTER_X - BALL_DIAMETER,
                                 TABLE_CENTER_X - 2 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(3, pos)

        # 8 ball (BLACK)
        pos = Physics.Coordinate(TABLE_CENTER_X,
                                 TABLE_CENTER_X - 2 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(8, pos)

        # 10 ball (LIGHTBLUE)
        pos = Physics.Coordinate(TABLE_CENTER_X + BALL_DIAMETER,
                                 TABLE_CENTER_X - 2 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(10, pos)

# *******************************************

        # 4 ball (PURPLE)
        pos = Physics.Coordinate(TABLE_CENTER_X - BALL_DIAMETER - BALL_RADIUS,
                                 TABLE_CENTER_X - 3 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(4, pos)

        # 14 ball (LIGHTGREEN)
        pos = Physics.Coordinate(TABLE_CENTER_X - BALL_RADIUS, TABLE_CENTER_X - 3 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(14, pos)

        # 7 ball (BROWN)
        pos = Physics.Coordinate(TABLE_CENTER_X + BALL_RADIUS, TABLE_CENTER_X - 3 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(7, pos)

        # 11 ball (PINK)
        pos = Physics.Coordinate(TABLE_CENTER_X + BALL_DIAMETER + BALL_RADIUS,
                                 TABLE_CENTER_X - 3 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(11, pos)

# *******************************************

        # 12 ball (MEDIUMPURPLE)
        pos = Physics.Coordinate(TABLE_CENTER_X - 2 * BALL_DIAMETER, TABLE_CENTER_X - 4 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(12, pos)

        # 6 ball (GREEN)
        pos = Physics.Coordinate(TABLE_CENTER_X - BALL_DIAMETER, TABLE_CENTER_X - 4 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(6, pos)

        # 15 ball (SANDYBROWN)
        pos = Physics.Coordinate(TABLE_CENTER_X, TABLE_CENTER_X - 4 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(15, pos)

        # 13 ball (LIGHTSALMON)
        pos = Physics.Coordinate(TABLE_CENTER_X + BALL_DIAMETER, TABLE_CENTER_X - 4 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(13, pos)

        # 5 ball (ORANGE)
        pos = Physics.Coordinate(TABLE_CENTER_X + 2 * BALL_DIAMETER, TABLE_CENTER_X - 4 * ADJUSTMENT * BALL_DIAMETER)
        self.table += Physics.StillBall(5, pos)


# *******************************************
# *******************************************
        # cue ball
        pos = Physics.Coordinate(TABLE_CENTER_X, Physics.TABLE_LENGTH - TABLE_CENTER_X)
        self.table += Physics.StillBall(0, pos)

        self.game = Physics.Game(gameName=game_name, player1Name=player_one, player2Name=player_two)

