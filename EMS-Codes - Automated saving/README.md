# **EMS Application**
###### Entry Management System
It saves the entries in two types `ProfileData` and `DailyData` in the `EMS DATA` folder
whose location is given by the Admin User.
1. `ProfileData` folder stores csv file for each user and there entries, the csv file is named after the unique id
   e.g. 'E2K18408823.csv'.\
   'DEPARTMENT, CLASS/DESIGNATION, ROLL NO., DATE, IN Time, OUT TIME, DURATION'
2. `DailyData`\
   Has Folder name after the year for data if that year
    1. All the entries for a day:- stores the entry's day wise in the folder of that year, in a csv file named after
       that day e.g. '2022-04-12.csv' in the folder of that year '2022'.\
       'REG ID, NAME, DEPARTMENT, CLASS/DESIGNATION, ROLL NO., DATE, IN Time, OUT TIME, DURATION'
    2. Unique entries for a day:- stores the unique entry's day wise in the folder of that year, in a csv file
       named after that day e.g. '2022-04-12-unique.csv' in the folder of that year '2022'.\
       'REG ID, NAME, DEPARTMENT, CLASS/DESIGNATION, ROLL NO.'
   

## **Records Folder**
### **application_data.npy File**
It stores as a dictionary in npy file. Initially all values are `None`. It stores following Keys and value:
1.  `'saving_data_location'` => string variable\
    Stores the location save regular entries' data
2.  `'capacity'` => int variable\
    Stores the capacity of room
3.  `'previous_session_date'` => datetime.date variable\
    Stores the previous date of login into system
4.  `'end_time'` => datetime.datetime variable\
    Stores the time to end day, gives this value to out time if any missed
5.  `'password'` => string variable\
    Stores the password

### **data.npy File**
It stored the data of students and staff in dictionary in npy file (pickle allowed). It is used to access the data while
recording entries. This is added to all the entries in the data entries.\
1. `Key` is a string, that contains reg_id of the user i.e. Enrollment ID or Registration ID.\
   E.g. 'E2K18103382'
2. `value` is a list of strings, storing details of user\
    E.g. ['NAME', 'DEPARTMENT', 'CLASS/DESIGNATION', 'ROLL NO.']

### **reg_if.txt File**
It stored the reg_id of all the user in a string separated by '\n', for fast search. For every of reg_id the id is searched using regex, if exists it will get data from data file

### **reg_stud_id.txt File**
It stored the reg_id of all the students in a string separated by '\n', used while delete old student data option
is ticked. It uses to delete the old student data from data file and then update the new data given to it.

### **reg_id_staff.txt File**
It stored the reg_id of all the staff in a string separated by '\n', used while delete old staff data option
is ticked. It uses to delete the old staff data from data file and then update the new data given to it.

## **Cache Folder**
### **inside_cache.npy File**
Stores the reg_id that inside the room and have not exited yet. It is a dict in a npy file.
1. `key` is a string, contains the reg_id of user
2. `value` is a datetime.datetime object, stores the IN TIME

### **daily_cache.csv File**
Stores detail of the entries after they have exited the room. It contains ['REG ID', 'NAME', 'DEPARTMENT',
'CLASS/DESIGNATION', 'ROLL NO.', 'DATE', 'IN Time', 'OUT TIME', 'DURATION'] in csv file.\
Entries are added to this file only after the user exits. At the end of the day it sorts
the data in ascending order of IN TIME and then stored into `DATA` folder in `EMS DATA`