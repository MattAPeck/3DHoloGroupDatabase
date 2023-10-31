import pyodbc

server = 'server'
database = 'Dummy Database'
username = 'python'
password = '123'
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database +
    ';ENCRYPT=no; UID=' + username + ';PWD=' + password)

INSERT_ESTABLISHMENT = "INSERT INTO Establishment(Latitude, Longitude, DateLastModified, EstablishmentName, " \
                       "EstablishmentType, DateCreated, MostUsedSentenceHistoryId) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?);"

UPDATE_ESTABLISHMENT = "UPDATE Establishment SET Latitude = ?, Longitude = ?, DateLastModified = ?, " \
                       "EstablishmentName = ?, EstablishmentType = ? WHERE EstablishmentId = ?;"

FIND_ESTABLISHMENT = "SELECT * FROM Establishment WHERE EstablishmentType = ?;"

FIND_ESTABLISHMENT_TYPES = "SELECT EstablishmentId, EstablishmentType FROM Establishment;"

INSERT_SENTENCE = "INSERT INTO SentenceByEstablishment(Sentence, EstablishmentId) VALUES (?, ?);"


RECEIVE_MOSTUSEDSENTENCEHISTORYID = "SELECT MostUsedSentenceHistoryId, Longitude, Latitude " \
                                    "FROM MostUsedSentenceHistory;"

RECEIVE_COORDINATES = "SELECT Longitude, Latitude FROM MostUsedSentenceHistory;"


def create_establishment(latitude, longitude, datemodified, name, type, datecreated, mostusedsentencehistoryid):
    cursor = conn.cursor()
    cursor.execute(INSERT_ESTABLISHMENT, (latitude, longitude, datemodified, name, type, datecreated, mostusedsentencehistoryid))
    cursor.commit()


def update_establishment(latitude, longitude, datemodified, name, type, id):  # TODO Probably to be changed.
    cursor = conn.cursor()
    cursor.execute(UPDATE_ESTABLISHMENT, (latitude, longitude, datemodified, name, type, id))
    cursor.commit()


def find_data(type):
    cursor = conn.cursor()
    cursor.execute(FIND_ESTABLISHMENT, (type))
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
