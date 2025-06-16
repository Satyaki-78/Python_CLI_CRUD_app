"""
Program Start Display Menu ->

Add Record (1)
Display All Records (2)
Search Record (3)
Modify Record (4)
Delete Record (5)
Exit (e)
"""

#Global list used for dynamically creating user-input prompts and SQL query generation
dict = [
    ['roll = %s',"Enter Roll: ","Roll"],
    ['sname = %s',"Enter Name: ","Name"],
    ['marks = %s',"Enter Marks: ","Marks"],
    ['dob = %s',"Enter DOB: ","DOB"]
    ]

def printChoices():
    #Printing Field Choices dynamically
    for item in range(1,len(dict)):
        print(f"{dict[item][2]} ({item})")

def sqlConnection():
    #Static behaviour function
    import mysql.connector as sqltor
    try:
        mycon = sqltor.connect(host="localhost",user="root",passwd="ABCD1234",database="pythondb",port="3310")
        return mycon
    except sqltor.Error as e:
        print(f"Error Occured --> {e}")
        return

def displayAllRecords():
    con = sqlConnection()
    cursor = con.cursor()
    cursor.execute("SELECT * from student;")
    result = cursor.fetchall()
    if result:
        import pandas as pd
        columns = [item[2] for item in dict]
        #from tabulate import tabulate
        df_result = pd.DataFrame(result, columns=columns).to_string(index=False)
        print(f"\nExisting Records:\n\n{df_result}\n")
        #print(f"\nExisting Records:\n\n{tabulate(df_result, headers=df_result.columns, tablefmt='fancy_grid', showindex=False)}\n")
    else:
        print(f"\nNo existing records !! Table is empty.\n")
    
    return


def searchRecord(returnRoll:bool):
    roll = input("Enter Roll for searching: ")
    con = sqlConnection()
    cursor = con.cursor()
    cursor.execute("SELECT * from student where roll = %s;",(roll,))
    result = cursor.fetchone()
    if result:
        print(f"\nExisting Record:")
        for item in dict:
            column = item[2]
            value = result[dict.index(item)]
            print(f"{column}: {value}")
        print()
    else:
        print(f"\nNo record found for Roll {roll}\n")
        return
    
    if returnRoll == True:
        return roll
    else:
        return

def createRecord():
    con = sqlConnection()
    try:
        params = []
        query_fields = ""
        ctr = 1
        #Dynamically generating sql query and taking field input at the same time
        for field_id in range(len(dict)):
            field_input = input(dict[field_id][1])
            params.append(field_input)
            if ctr > 1:
                query_fields += ", "+ "%s"
            else:
                query_fields += "%s"
            ctr += 1
        params = tuple(params)
        sql_query = f"INSERT INTO student VALUES ({query_fields});"
        
        cursor = con.cursor()
        #Checking for existing record
        cursor.execute("SELECT roll FROM student WHERE roll = %s;",(params[0],))
        result = cursor.fetchone()
        if result:
            print("\nA record with same roll already exists!...CANNOT INSERT ROW !\n")
        else:
            cursor.execute(sql_query,params)
            con.commit()
            print("\nRecord Inserted Successfully !!\n")
    except Exception as e:
        con.rollback()
        print(f"\nError Occured --> {e}\n")
    finally:
        con.close()
        return

def updateRecord():
    roll = searchRecord(returnRoll=True)
    # Exit from the function if no record is found
    if roll == None:
        return
    
    con = sqlConnection()
    
    #Creating a python set which will be used to allow only the entry of editable field's id 
    editable_fields = set(str(field_id) for field_id in range(1,len(dict)))
    params = []
    field_id = []
    query_fields = ""
    print("Choose which field(s) to update [Field (choice)]")
    printChoices()
    
    field_id = list(input("Enter choice(s) with spaces: ").split())
    #Restricting user from entering no of choices more than the no of fields in the table
    if len(field_id) > (len(dict)-1):
        print(f"\nYou gave {len(field_id)} choices.")
        print("No of choices cannot exceed total no of given fields !!\n")
        return
    #Checking if field_id list contains field ids other than allowed field
    if not set(field_id).issubset(editable_fields):
        while not set(field_id).issubset(editable_fields):
            print("\nInvalid Input !!\n")
            print("Choose which field(s) to update [Field (choice)]")
            printChoices()
            field_id = list(input("Enter choice(s) with spaces: ").split())
    #Dynamically creating the SQL command
    ctr = 1
    for item in field_id:
        item = int(item)
        field_input = input(dict[item][1])
        params.append(field_input)
        if ctr > 1:
            query_fields += ", "+dict[item][0]
        else:
            query_fields += dict[item][0]
        ctr += 1
    
    base_sql = "UPDATE student SET " +query_fields+ " WHERE roll = %s;"
    
    params.append(roll)
    params = tuple(params)
    if con.is_connected():
        confirm_update = input("Confirm Update ? (y/n): ")
        if confirm_update not in ['y','n']:
            while confirm_update not in ['y','n']:
                print("\nInvalid Input\n")
                confirm_update = input("Confirm Update ? (y/n): ")
        # Continuing for updating only if valid input is given
        if confirm_update == 'y':
            try:
                cursor = con.cursor()
                cursor.execute(base_sql, params)
                con.commit()
                print("\nRecord Updated Successfully !!\n")
            except Exception as e:
                con.rollback()
                print(f"\nError Occured --> {e}\n")
            finally:
                con.close()
                return
        else:
            print()
            return


def deleteRecord():
    roll = searchRecord(returnRoll=True)
    if roll == None:
        return
    confirm_delete = input("Delete Record ? (y/n): ")
    if confirm_delete not in ['y','n']:
        while confirm_delete not in ['y','n']:
            print("\nInvalid Input\n")
            confirm_delete = input("Delete Record ? (y/n): ")
    if confirm_delete == 'y':
        try:
            con = sqlConnection()
            cursor = con.cursor()
            cursor.execute("DELETE FROM student WHERE roll = %s;",(roll,))
            con.commit()
            print("\nRecord Deleted Successfully !!\n")
        except Exception as e:
            con.rollback()
            print(f"\nError Occured --> {e}\n")
        finally:
            con.close()
            return
    else:
        print()
        return

# main code
while True:
    action = input("""Select Action [(choice) Action]\n(1) Add Record | (2) Display All Records | (3) Search Record | (4) Modify Record | (5) Delete Record | (e) Exit\n--> """)
    if action not in ['1','2','3','4','5','e']:
        while action not in ['1','2','3','4','5','e']:
            print("\nInvalid Input\n")
            action = input("""Select Action [(choice) Action]\n(1) Add Record | (2) Display All Records | (3) Search Record | (4) Modify Record | (5) Delete Record | (e) Exit\n--> """)
    if action == '1':
        createRecord()
    elif action == '2':
        displayAllRecords()
    elif action == '3':
        searchRecord(returnRoll=False)
    elif action == '4':
        updateRecord()
    elif action == '5':
        deleteRecord()
    else:
        break