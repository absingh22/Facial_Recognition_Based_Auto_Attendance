from imutils import paths
import mysql.connector
import os

from datetime import date

def mysqlfunc():
    mydb = mysql.connector.connect(
        host="LAPTOP-76O3CEHF",
        user="root",
        passwd="",
        database="students_attendance"
    )
    mycursor = mydb.cursor()
    string_start = "CREATE TABLE test2 (Date DATE PRIMARY KEY NOT NULL, Day VARCHAR(255)"
    string_beforename = ", "
    string_aftername = " CHAR(1) DEFAULT 'A'"
    string_end = ")"
    
    names = {}
    
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images("dataset"))
    
    finalString = string_start
    
    for (i, imagePath) in enumerate(imagePaths):
#        print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]
        if name not in names:
            print(name + " " + str(i+1))
            finalString += string_beforename + name + string_aftername
            names[name] = "true"
    finalString += string_end
    mycursor.execute(finalString)
    
#    today = date.today()
#    day = today.strftime("%a")
#    
#    sql = "Insert into students_attendance(date, day, dipen_singh) values (%s, %s, %s)"
#    val = (today, day, 'P')
#    mycursor.execute(sql, val)
    
    
#"CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))"
#CREATE TABLE `students_attendance`. ( `Date` DATE NOT NULL , `Day` VARCHAR NOT NULL , `Dipen_Singh` VARCHAR NOT NULL )

def datefunc():
    today = date.today()
    day = today.strftime("%a")

    print(today)


#datefunc()
mysqlfunc()