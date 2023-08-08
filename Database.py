import pyodbc

# I know I did alot of this explanation in my first readme file explaining how this works,
# but I figured I should go through a more thorough walkthrough in how this works.

# This is where our Server information goes, for testing purposes this will be unique per each of us.
# In the final implementation we will probably use somthing called a .env file to store this information.
# That way the program can access it, but any random person who happens upon our repository won't be able to just have
# the access information for the 3DHoloGroup server.
server = 'MATTHEWSPC'
database = 'Dummy Database'
username = 'python'
password = '123'
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database +
    ';ENCRYPT=no; UID=' + username + ';PWD=' + password)

# These are our SQL statements, you can write SQL in Python just like a normal Query and then you can just
# send it to the database to run the SQL on their end, with the values we send it.
INSERT_ESTABLISHMENT = "INSERT INTO Establishment(Latitude, Longitude, DateLastModified, EstablishmentName, " \
                       "EstablishmentType, DateCreated, MostUsedSentenceHistoryId) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?);"
# When you pick your values for the database, Pyodbc has us use ? for user input.
# The order that you set this up in is important, so keep track when you assign variables down the line.
UPDATE_ESTABLISHMENT = "UPDATE Establishment SET Latitude = ?, Longitude = ?, DateLastModified = ?, " \
                       "EstablishmentName = ?, EstablishmentType = ? WHERE EstablishmentId = ?;"
# Potentially change above statement to be WHERE MostUsedSentenceHistoryId = ? instead of EstablishmentId.

FIND_ESTABLISHMENT = "SELECT * FROM Establishment WHERE EstablishmentType = ?;"

FIND_ESTABLISHMENT_TYPES = "SELECT EstablishmentId, EstablishmentType FROM Establishment;"

INSERT_SENTENCE = "INSERT INTO SentenceByEstablishment(Sentence, EstablishmentId) VALUES (?, ?);"


RECEIVE_MOSTUSEDSENTENCEHISTORYID = "SELECT MostUsedSentenceHistoryId, Longitude, Latitude " \
                                    "FROM MostUsedSentenceHistory;"

RECEIVE_COORDINATES = "SELECT Longitude, Latitude FROM MostUsedSentenceHistory;"


# Notice here that I have the variables in the same order as listed in the SQL itself.
# That is important, because that is the data it expects to receive.
# If your variables are in the wrong order/are the wrong type then it won't get an error on this side,
# but it will be an error on the Server side, so the data won't be added to the tables.
def create_establishment(latitude, longitude, datemodified, name, type, datecreated, mostusedsentencehistoryid):
    cursor = conn.cursor()  # Every time you interact with the database you will create a cursor.
    # That Cursor will be what you use to execute you SQL.
    cursor.execute(INSERT_ESTABLISHMENT, (latitude, longitude, datemodified, name, type, datecreated, mostusedsentencehistoryid))
    # Whenever you add something to the database you need to make sure you commit it,
    # otherwise it won't actually save server side.
    cursor.commit()


def update_establishment(latitude, longitude, datemodified, name, type, id):  # TODO Probably to be changed.
    cursor = conn.cursor()
    cursor.execute(UPDATE_ESTABLISHMENT, (latitude, longitude, datemodified, name, type, id))
    cursor.commit()


def find_data(type):
    cursor = conn.cursor()
    cursor.execute(FIND_ESTABLISHMENT, (type))
    # When you want to retrieve something from the database, you use either fetchall, for all values in the column,
    # or fetchone for a single value.
    return cursor.fetchall()


def get_establishment_type():
    cursor = conn.cursor()
    cursor.execute(FIND_ESTABLISHMENT_TYPES)
    return cursor.fetchall()


def create_sentence(text, Id):
    cursor = conn.cursor()
    cursor.execute(INSERT_SENTENCE, (text, Id))
    cursor.commit()


def get_mostusedid():
    cursor = conn.cursor()
    cursor.execute(RECEIVE_MOSTUSEDSENTENCEHISTORYID)
    return cursor.fetchall()

def get_coordinates():
    cursor = conn.cursor()
    cursor.execute(RECEIVE_COORDINATES)
    return cursor.fetchall()
