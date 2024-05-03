import phylib
import sqlite3
import os
import math

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_INTERVAL = 0.01

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg (self):
        css_class = ''
        if self.obj.still_ball.number == 0:
            css_class = ' class="cue-ball"'
        return """ <circle%s cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (css_class, self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y), and acceleration (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg (self):
        css_class = ''
        if self.obj.rolling_ball.number == 0:
            css_class = ' class="cue-ball"'
        return """ <circle%s cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (css_class, self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])   

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires position (x,y) as
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;


    # add an svg method here
    def svg (self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires y as
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;


    # add an svg method here
    def svg (self):
        if self.obj.hcushion.y == 0:
            yVal = -25
        else:
            yVal = 2700
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (yVal)

################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires x as
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;


    # add an svg method here
    def svg (self):
        if self.obj.vcushion.x == 0:
            xVal = -25
        else:
            xVal = 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (xVal)

################################################################################
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg (self):
        result = ""
        result += HEADER
        for obj in self:
            if obj is not None:
                result += obj.svg()
        result += FOOTER

        return result
    
    def frame_svg(self, hidden=True):
        result = f'<g style="display: {"none" if (hidden) else "block"};">\n'
        for obj in self:
            if isinstance(obj, (StillBall, RollingBall)):
                result += obj.svg()
        result += "</g>\n"
        return result
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;
            
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y ) );

                # add ball to table
                new += new_ball;
        
        # return table
        return new;

    def get_low_ball_set(self):
        result = []
        for i in range(1, 8):
            # ball = self.getBall(i)
            for obj in self:
                if isinstance(obj, StillBall):
                    if obj.obj.still_ball.number == i:
                        result.append(i)
                elif isinstance(obj, RollingBall):
                    if obj.obj.rolling_ball.number == i:
                        result.append(i)
        return result        


    def get_high_ball_set(self):
        result = []
        for i in range(9, 16):
            # ball = self.getBall(i)
            for obj in self:
                if isinstance(obj, StillBall):
                    if obj.obj.still_ball.number == i:
                        result.append(i)
                elif isinstance(obj, RollingBall):
                    if obj.obj.rolling_ball.number == i:
                        result.append(i)

        return result        


    def cueBall(self):
        cue_ball = None
        for ball in self:
            if isinstance(ball, StillBall):
                if ball.obj.still_ball.number == 0:
                    cue_ball = ball
        return cue_ball
 

    def blackBall(self):
        return self.getBall(8) 

 
    def getBall(self, ball_num):
        result = None
        for obj in self:
            if isinstance(obj, StillBall):
                if obj.obj.still_ball.number == ball_num:
                    result = obj.obj
                    break
            elif isinstance(obj, RollingBall):
                if obj.obj.rolling_ball.number == ball_num:
                    result = obj.obj
                    break
            
        return result
       
################################################################################
class Database:
    # Using lab 3 as an example in some parts
    conn = None

    def __init__ (self, reset=False):
        if reset == True:
            # Delete file and make a new empty database
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")
        
        self.conn = sqlite3.connect("phylib.db")

    def tableExistCheck (self, cur, tableName):
        cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name=?""", (tableName,))
        return cur.fetchone() is not None

    def createDB (self):
        cur = self.conn.cursor()

        if self.tableExistCheck(cur, "Ball") == False:
            cur.execute( """CREATE TABLE Ball 
                            ( BALLID INTEGER NOT NULL,
                            BALLNO   INTEGER NOT NULL,
                            XPOS     FLOAT NOT NULL,
                            YPOS     FLOAT NOT NULL,
                            XVEL     FLOAT,
                            YVEL     FLOAT,
                            PRIMARY KEY (BALLID) );""" )
            
        if self.tableExistCheck(cur, "TTable") == False:
            cur.execute( """CREATE TABLE TTable 
                            ( TABLEID INTEGER NOT NULL,
                            TIME      FLOAT NOT NULL,
                            PRIMARY KEY (TABLEID) );""" )
            
        if self.tableExistCheck(cur, "BallTable") == False:
            cur.execute( """CREATE TABLE BallTable 
                            ( BALLID INTEGER NOT NULL,
                            TABLEID  INTEGER NOT NULL,
                            FOREIGN KEY (BALLID) REFERENCES Ball,
                            FOREIGN KEY (TABLEID) REFERENCES TTable );""" )
            
        if self.tableExistCheck(cur, "Shot") == False:
            cur.execute( """CREATE TABLE Shot 
                            ( SHOTID  INTEGER NOT NULL,
                            PLAYERID  INTEGER NOT NULL,
                            GAMEID    INTEGER NOT NULL,
                            PRIMARY KEY (SHOTID),
                            FOREIGN KEY (PLAYERID) REFERENCES Player,
                            FOREIGN KEY (GAMEID) REFERENCES Game );""" )

        if self.tableExistCheck(cur, "TableShot") == False:
            cur.execute( """CREATE TABLE TableShot 
                            ( TABLEID INTEGER NOT NULL,
                            SHOTID    INTEGER NOT NULL,
                            FOREIGN KEY (TABLEID) REFERENCES TTable,
                            FOREIGN KEY (SHOTID) REFERENCES Shot );""" )
            
        if self.tableExistCheck(cur, "Game") == False:
            cur.execute( """CREATE TABLE Game 
                            ( GAMEID INTEGER NOT NULL,
                            GAMENAME VARCHAR(64) NOT NULL,
                            PRIMARY KEY (GAMEID) );""" )
            
        if self.tableExistCheck(cur, "Player") == False:
            cur.execute( """CREATE TABLE Player 
                            ( PLAYERID INTEGER NOT NULL,
                            GAMEID     INTEGER NOT NULL,
                            PLAYERNAME VARCHAR(64) NOT NULL,
                            PRIMARY KEY (PLAYERID), 
                            FOREIGN KEY (GAMEID) REFERENCES Game);""" )
            
        self.conn.commit()
        cur.close()
            
    def readTable (self, tableID):
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM (BallTable INNER JOIN Ball ON BallTable.BALLID=Ball.BALLID)
                    WHERE BallTable.TABLEID=?""", (tableID+1,))
        result = cur.fetchall()

        if result == None:
            return None
        
        table = Table()

        i = 0
        for row in result:
            i = i + 1
            ballno = row[3]
            xpos = row[4]
            ypos = row[5]
            xvel = row[6]
            yvel = row[7]

            if xvel == None:
                xvel = 0.0
            if yvel == None:
                yvel = 0.0

            pos = Coordinate(xpos, ypos)
            # Still ball
            if xvel == 0.0 and yvel == 0.0:
                sb = StillBall(ballno, pos)
                table += sb
            # Rolling ball
            else:
                vel = Coordinate(xvel, yvel)
                acc = Coordinate(0.0, 0.0)

                speed = math.sqrt((vel.x * vel.x) + (vel.y * vel.y))
                if speed > VEL_EPSILON:
                    acc.x = ((vel.x * -1.0) / speed) * DRAG
                    acc.y = ((vel.y * -1.0) / speed) * DRAG

                rb = RollingBall(ballno, pos, vel, acc)
                table += rb

        # Time
        cur.execute("""SELECT TIME FROM TTable WHERE TTable.TABLEID=?""", (tableID+1,))
        timeResult = cur.fetchone()
        if timeResult == None:
            table = None
        else:
            table.time = timeResult[0]
            
        # Close and commit
        #self.conn.commit()
        cur.close()
        return table
    
    def writeTable (self, table):
        cur = self.conn.cursor()

        cur.execute("""INSERT INTO TTable(TIME)
                    VALUES (?)""", (table.time,))
        tableID = cur.lastrowid

        ballData = []
        tableData = []

        for ball in table:
            # Rolling ball
            if isinstance(ball, RollingBall):
                ballno = ball.obj.rolling_ball.number
                xpos = ball.obj.rolling_ball.pos.x
                ypos = ball.obj.rolling_ball.pos.y
                xvel = ball.obj.rolling_ball.vel.x
                yvel = ball.obj.rolling_ball.vel.y

                if (xvel == 0.0):
                    xvel = None
                if (yvel == 0.0):
                    yvel = None

                ballData.append((ballno, xpos, ypos, xvel, yvel))

            # Still ball
            elif isinstance(ball, StillBall):
                ballno = ball.obj.still_ball.number
                xpos = ball.obj.still_ball.pos.x
                ypos = ball.obj.still_ball.pos.y
                
                ballData.append((ballno, xpos, ypos, None, None))

        cur.execute("SELECT MAX(BALLID) FROM Ball")
        firstBallID = cur.fetchone()[0]
        if firstBallID == None:
            firstBallID = 1
        else:
            firstBallID = firstBallID + 1

        cur.executemany("""INSERT INTO Ball(BALLNO, XPOS, YPOS, XVEL, YVEL)
                        VALUES (?, ?, ?, ?, ?)""", ballData)
        
        cur.execute("SELECT MAX(BALLID) FROM Ball")
        lastBallID = cur.fetchone()[0]
        if lastBallID == None:
            lastBallID = 0
            
        for ballID in range(firstBallID, lastBallID+1):
            tableData.append((ballID, tableID))

        cur.executemany("""INSERT INTO BallTable(BALLID, TABLEID)
                        VALUES (?, ?)""", tableData)
        
        # Close and commit
        #self.conn.commit()
        cur.close()
        return tableID-1
    
    def close (self):
        self.conn.commit()
        self.conn.close()

    def getGame (self, gameID):
        cur = self.conn.cursor()
        gameID = gameID + 1

        cur.execute("""SELECT GAMENAME, PLAYERNAME, PLAYERID FROM (Game INNER JOIN Player ON Game.GAMEID=Player.GAMEID)
                    WHERE Game.GAMEID=?""", (gameID,))
        result = cur.fetchall()

        if (result == []):
            # Close and commit, no game found with that ID
            self.conn.commit()
            cur.close()
            return None

        gameName = result[0][0] # gameName is the same in both rows (only 2 rows should be produced)

        # Getting playerIDs
        playerIDs = []
        for row in result:
            playerIDs.append(row[2])
        
        # Comparing playerIDs to get correct name
        if playerIDs[0] < playerIDs[1]:
            player1Name = result[0][1]
            player2Name = result[1][1]
        else:
            player1Name = result[1][1]
            player2Name = result[0][1]

        # Close and commit
        self.conn.commit()
        cur.close()
        return gameName, player1Name, player2Name
    
    def setGame (self, gameName, player1Name, player2Name):
        cur = self.conn.cursor()

        cur.execute("""INSERT INTO Game(GAMENAME)
                    VALUES (?)""", (gameName,))
        gameID = cur.lastrowid

        cur.execute("""INSERT INTO Player(GAMEID, PLAYERNAME)
                    VALUES (?, ?)""", (gameID, player1Name,))
        cur.execute("""INSERT INTO Player(GAMEID, PLAYERNAME)
                    VALUES (?, ?)""", (gameID, player2Name,))
        
        # Close and commit
        self.conn.commit()
        cur.close()
        return gameID
    
    def newShot (self, gameName, playerName):
        cur = self.conn.cursor()

        cur.execute("""SELECT GAMEID FROM Game WHERE Game.GAMENAME=?""", (gameName,))
        gameID = cur.fetchone()

        cur.execute("""SELECT PLAYERID FROM Player WHERE Player.GAMEID=? AND Player.PLAYERNAME=?""", (gameID[0], playerName,))
        playerID = cur.fetchone()

        cur.execute("""INSERT INTO Shot(PLAYERID, GAMEID)
                    VALUES (?, ?)""", (playerID[0], gameID[0],))
        shotID = cur.lastrowid

        # Close and commit
        self.conn.commit()
        cur.close()
        return shotID
    
    def updateTableShot (self, tableShotData):
        cur = self.conn.cursor()

        cur.executemany("""INSERT INTO TableShot(TABLEID, SHOTID)
                        VALUES (?, ?)""", tableShotData)

        # Close and commit
        self.conn.commit()
        cur.close()

    def getMaxTableID (self):
        cur = self.conn.cursor()

        cur.execute("SELECT MAX(TABLEID) FROM TTable")
        maxTableID = cur.fetchone()[0]
        if maxTableID == None:
            maxTableID = 0

        cur.close()
        return maxTableID

class Game:
    def __init__ (self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        db = Database()
        db.createDB()

        # Only GameID provided
        if (isinstance(gameID, int) and gameName == None and player1Name == None and player2Name == None):
            results = db.getGame(gameID)
            if results != None:
                self.gameID = gameID + 1
                self.gameName = results[0]
                self.player1Name = results[1]
                self.player2Name = results[2]

        # Only 3 strings are provided
        elif (gameID == None and isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str)):
            result = db.setGame(gameName, player1Name, player2Name)
            
            self.gameID = result
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

        # Invalid constructor  
        else:
            raise TypeError("Invalid arguments")
        
        db.close()

    def shoot (self, gameName, playerName, table, xvel, yvel):
        db = Database()
        tableShotData = []

        shotID = db.newShot(gameName, playerName)

        # Finding the cue ball and making it a rolling ball
        cue_ball = table.cueBall()

        xpos = cue_ball.obj.still_ball.pos.x
        ypos = cue_ball.obj.still_ball.pos.y

        cue_ball.type = phylib.PHYLIB_ROLLING_BALL
        cue_ball.obj.rolling_ball.number = 0
        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel

        speed = math.sqrt((xvel * xvel) + (yvel * yvel))
        if speed > VEL_EPSILON:
            cue_ball.obj.rolling_ball.acc.x = ((xvel * -1.0) / speed) * DRAG
            cue_ball.obj.rolling_ball.acc.y = ((yvel * -1.0) / speed) * DRAG

        # Using tempTable as the table to determine interval times and newTable to write to database
        tempTable = phylib.phylib_copy_table(table)
        newTable = phylib.phylib_copy_table(table)
        while (tempTable != None):
            timeBefore = tempTable.time
            tempTable = tempTable.segment()
            if (tempTable == None):
                tableID = db.writeTable(table)
                tableShotData.append((tableID+1, shotID))
                db.updateTableShot(tableShotData)
                return table
            timeAfter = tempTable.time
            timeDifference = timeAfter - timeBefore
            intervalCount = math.floor(timeDifference / FRAME_INTERVAL)

            for num in range(intervalCount):
                currentTime = num * FRAME_INTERVAL
                newTable = table.roll(currentTime)
                newTable.time = timeBefore + currentTime
                tableID = db.writeTable(newTable)
                
                tableShotData.append((tableID+1, shotID))
                
            table = table.segment()
        
        db.close()
