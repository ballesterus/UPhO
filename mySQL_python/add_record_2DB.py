#! /usr/bin/env python
""" This Script CONTAINS THE FUCTIONS DEFINITION TO POPULATE AND QUERY MYSPECIMENS DATA BASE
"""
import MySQLdb
import re
import tabulate


Mydb = MySQLdb.connect(host="localhost", user="root", passwd="", db="mySpecimens", charset='utf8')
Mycursor = Mydb.cursor()

def db_close():
    Mydb.close()
    Mycursor.close()

def are_there(sql):
    if Mycursor.execute(sql) > 0:
        return True
    else:
        return False


def query_and_print(sql):
    if are_there(sql):
        col_names = [i[0] for i in Mycursor.description]
        records = Mycursor.fetchall()
        print tabulate.tabulate(records, headers = col_names, tablefmt="orgtbl" )
            
    else:
        print "No records found with that search criterion"
        
            
def show_existing_records(table):
    sql = "SELECT * FROM %s;" % table
    numRecs = Mycursor.execute(sql)
    query_and_print(sql)
    print "There are %d records" % numRecs
    
def last_record(table):
    sql = "SELECT * FROM %s WHERE  id%s  = (SELECT MAX(id%s) FROM %s);" % (table, table, table, table)
    query_and_print(sql)

def search_personel(keyword):
    sql= """SELECT * FROM Personel WHERE
    LastName LIKE '%%%s%%' 
    OR FirstName LIKE '%%%s%%'
    OR MiddleName LIKE '%%%s%%' 
    ORDER BY idPersonel;
    """ % (keyword, keyword, keyword)
    query_and_print(sql)

def search_species(keyword):
    sql = """SELECT * FROM SPECIES WHERE
    Family LIKE '%%%s%%'
    OR Genus LIKE  '%%%s%%'
    OR Species LIKE  '%%%s%%'
    OR Author LIKE  '%%%s%%'
    """ % (keyword, keyword, keyword, keyword)
    query_and_print(sql)


def search_locality(keyword):
    sql= """SELECT idLocality,
    LocalityName,
    Country,
    State,
    County
    FROM LOCALITY WHERE
    Country  LIKE '%%%s%%' 
    OR LocalityName LIKE '%%%s%%'
    OR State LIKE '%%%s%%'
    OR County Like '%%%s%%'
    OR Notes LIKE '%%%s%%';
    """ % (keyword, keyword, keyword, keyword, keyword)
    query_and_print(sql)

def search_collection(keyword):
    sql = """SELECT * FROM collection_view
    WHERE LocalityName LIKE '%%%s%%'
    OR Country LIKE '%%%s%%'
    OR State LIKE '%%%s%%'
    OR Collected_by LIKE '%%%s%%'
    OR DATE_FORMAT(CollectionDate, '%%Y %%m') = '%s'
    OR DATE_FORMAT(CollectionDate, '%%Y') = '%s'
    ORDER BY idNUM;
    """ %  (keyword, keyword, keyword, keyword, keyword, keyword)
    query_and_print(sql)

def search_determination(keyword):
    sql = """SELECT * FROM determination_view
    WHERE Binomen LIKE '%%%s%%' 
    OR Determined_by LIKE '%%%s%%'
    ORDER BY DetDate;
    """ % (keyword, keyword)
    query_and_print(sql)

def add_personel():
    LastName = raw_input('Type last name: ')
    FirstName = raw_input('Type first name: ')
    MiddleName = raw_input('Type middle Name: ')
    print "New person to add is %s %s %s" % (LastName, FirstName, MiddleName)
    sql = """INSERT INTO Personel SET
    LastName ='%s',
    FirstName = '%s',
    MiddleName = '%s';
    """% (LastName, FirstName, MiddleName)
    Mycursor.execute(sql)
    Mydb.commit()
    last_record("Personel")

def add_locality():
    Country = raw_input('Type the country of the new Locality: ' )
    State = raw_input('Type the state or province: ' )
    County = raw_input('Type the county or municipality: ')
    LocalityName = raw_input('Type the name of the locality: '  )
    DecimalLong = float(raw_input('Type the longitude in decimal format: '))
    DecimalLat =  float(raw_input('Type the latitude in decimal format: '))
    Elevation =  int(raw_input('Type the elvation in meters: '))
    Notes = raw_input('Type any notes you want to add: ')
    sql = """ INSERT INTO Locality SET
    Country = '%s',
    State = '%s',
    County = '%s',
    LocalityName = '%s',
    DecimalLong = %f,
    DecimalLat = %f,
    Elevation = %d,
    Notes = '%s';
    """ % (Country, State, County, LocalityName, DecimalLong, DecimalLat, Elevation, Notes)
    Mycursor.execute(sql)
    Mydb.commit()
    last_record("Locality")

def add_collection_event():
    while True:
        print "Search for the locality where the collection event ocurred"
        search_locality(raw_input('Search term: '))
        print "Type the localityID  to use, type 'r' to search again or 'n' to add a new locality."
        answer = raw_input('Selection: ')
        if  answer == 'n':
            add_locality()
            break
        elif answer == 'r':
            print 'Try another seacrh term'
        else:
            idLocality = int(answer)
            CollectionDate = raw_input('Type the collection day in YYYY-MM-DD format: ' )
            CollectionMethod = raw_input('Add a collection method: ')
            Notes =raw_input('Add notes if necesary: ')
            sql = """INSERT INTO CollectionEvent SET
            CollectionDate = '%s',
            CollectionMethod = '%s',
            Notes = '%s',
            idLocality = %d;
            """ % (CollectionDate, CollectionMethod, Notes, idLocality)
            Mycursor.execute(sql)
            Mydb.commit()
            last_record('CollectionEvent')
            print "Go to add collectors"
            add_collectors()
            break
        
def add_collectors():
    idColl = int(raw_input('Confirm collection event: '))
    select = 'add'
    while True:
        search_personel(raw_input('Search collector: '))
        answer = raw_input("Select the person ID or type 'n' to add a new one :")
        if answer == 'n':
            add_personel()
        else:
            idPers = int(answer)
            sql = """INSERT INTO Collectors SET
            idCollectionEvent = %d,
            idPersonel =%d;
            """ % (idColl, idPers)
            Mycursor.execute(sql)
            Mydb.commit()
            sql2= """SELECT * FROM collection_view
            WHERE idNum = %d
            """ % (idColl)
            query_and_print(sql2)
            question = raw_input("continue adding collectors?(y/n): ")
            if question == 'n':
                break
            else:
                print 'Adding another collector'

def add_species():
    Family = raw_input('Insert family: ')
    Genus = raw_input('Insert Genus: ')
    Species = raw_input('Insert pecies epithet: ')
    Author = raw_input('Insert species author: ')
    Notes = raw_input('Insert notes: ')
    sql="""INSERT INTO Species SET
    Family = '%s',
    Genus = '%s',
    Species = '%s',
    Author = '%s',
    Notes = '%s';
    """ % (Family, Genus, Species, Author, Notes)
    Mycursor.execute(sql)
    Mydb.commit()
    last_record("Species")

def add_determination():
    DetDate = raw_input('Insert determination date as YYYY-MM-DD or YYYY-MM-00: ')
    while True:
        print 'Searching species name'
        search_species(raw_input('Seach term: '))
        print "Type tye species code to use that species name, or 'r' to retry the search or 'n to add a new species to the species table."
        answer = raw_input('Selection: ')
        if answer =='n':
            add_species()
        elif answer == 'r':
            print 'Try another seacrh term'
        else:
            idSpecies = int(answer)
            break
    while True:
        print "Searching for determiner"
        search_personel(raw_input('Search people: '))
        print "Type tye personId to use, or 'r' to retry the search or 'n to add a new person to the Personel table."
        answer = raw_input("Select the person ID or type 'new' to add a new one :")
        if answer =='n':
            add_personel()
            break
        elif answer == 'r':
            print 'Try another seacrh term'
        else:
            idPersonel = int(answer)
            break
    sql = """INSERT INTO Determination SET
    DetDate = '%s',
    idSpecies = %d,
    idPersonel = %d ;
    """ % (DetDate, idSpecies, idPersonel)
    Mycursor.execute(sql)
    Mydb.commit()
    sqlc = "SELECT * FROM determination_view  WHERE  iddetermination  = (SELECT MAX(iddetermination) FROM determination_view);"
    query_and_print(sqlc)

def add_specimen():
   while True:
        print "Search for the collection event  using a locality descriptor (Country, Sate, locality name, etc.) or the date of collection as year (YYYY), year-month (YYYY-MM) or full date (YYYYY-MM-DD)"
        search = search_collection(raw_input('Search term: '))
        print "Type the Collection Event ID to use that collection event, type 'r' to retry the search with other term, or 'n' to add a new collection event."
        answer = raw_input('Selection: ')
        if  answer == 'n' :
            print 'Adding a new Collection event'
            add_collection_event()
        elif answer == 'r':
            print 'search again'
        else:
            idColl = int(answer)
            GH_number = raw_input("GH number:"  )
            otherCatalogNumber = raw_input("Type the additional catalog number: " )  
            Preparation_Type = raw_input('What type of preparation: '  )
            femaleCount = int(raw_input('Amount of females: '))
            maleCount =  int(raw_input('Amount of males: '))
            juvenilesCount =  int(raw_input('Amount of Juveniles: '))
            subAdultMaleCount = int(raw_input('Amount of sub-females: '))
            subAdultFemaleCount = int(raw_input('Amount of sub-males: '))
            Notes = raw_input('Add notes if necesary: ')
            q_add_det = raw_input('Do you wanna add determination? (y/n)' ) 
            if q_add_det == 'n':
                sql = """INSERT INTO Specimen SET
                GH_number = '%s',
                otherCatalogNumber = '%s',
                Preparation_Type = '%s',
                femaleCount = %d,
                maleCount = %d,
                juvenilesCount = %d,
                subAdultMaleCount = %d,
                subAdultFemaleCount = %d,
                Notes = '%s'
                idCollectionEvent = %d ;
                """ % (GH_number, otherCatalogNumber, Preparation_Type, femaleCount, maleCount, juvenilesCount, subAdultMaleCount, subAdultFemaleCount, Notes, idColl)
                break
            if q_add_det =='y':
                while True:
                    print 'Searching determination'
                    search_determination(raw_input('Seach term: '))
                    print "Type the deterimination id to use, or 'r' to retry the search or 'n to add a new species to the species table."
                    answer = raw_input('Selection: ')
                    if answer == 'r':
                        print 'Try another term'
                    elif answer == 'n':
                        print 'Adding a new determination'
                        add_determination()
                    else:
                        idDet = int(answer)
                        sql = """INSERT INTO Specimen SET
                        GH_number = '%s',
                        otherCatalogNumber = '%s',
                        Preparation_Type = '%s',
                        femaleCount = %d,
                        maleCount = %d,
                        juvenilesCount = %d,
                        subAdultMaleCount = %d,
                        subAdultFemaleCount = %d,
                        Notes = '%s',
                        idDetermination = %d,
                        idCollectionEvent = %d ;
                        """ % (GH_number, otherCatalogNumber, Preparation_Type, femaleCount, maleCount, juvenilesCount, subAdultMaleCount, subAdultFemaleCount, Notes, idDet, idColl)
                        break
            Mycursor.execute(sql)
            Mydb.commit()
            sqlc = "SELECT * FROM specimen_view  WHERE  idSpecimen  = (SELECT MAX(idSpecimen) FROM Specimen);"
            query_and_print(sqlc)
            break
