import sqlite3 
import csv
try:
    db=sqlite3.connect("app2.db")
    print("Connected to Database Successfully!")
    db.execute("CREATE TABLE IF NOT EXISTS 'Skills'(user_id integer,name text,progress integer)")
    cr=db.cursor()
    user=input("please enter your user id :")
    while not user.isdigit():
         print("User ID must be a number.")
         user=input("please enter your user id :")
         if user.isdigit():
              break
             
    #input Big message
    input_message='''
    WHAT DO YOU WANT TO DO?
    "s"=>Show All Skills
    "a"=>Add New Skill
    "d"=>Delete A skill
    "u"=>Update Skill Progress
    "e" => Export Skills to CSV
    "q"=>Quit the App
    Choose Option:
    '''
   

    #command list
    commands_list=["s","a","d","u","e","q"]
    #define the method 
    def show_skills():  
        print ("Show skills")
        cr.execute("select * from skills where user_id=?",(user))
        results=cr.fetchall()
        print(f"\nYou have{len(results)} skills.")
        if len(results)>=1:
            print("\nShowing skills with progress: ")
            for row in results:
                print("-"*50)
                print(f"Skill => {row[1]}")
                print(f"Progress => {row[2]}%")
                print("-"*50)

    def add_skills():
        while True:
           sk=input("Write Skill Name ").strip().capitalize()
           prog=input("Write Skill progress ").strip()
           user_add=input("do you want add more![Y,N]").strip().capitalize()
           if user_add=='Y':
                add_skills()
                break
           elif user_add=='N':
               print("OK!") 
               break
           else:
                print("something wrong!")  
                break
        while not prog.isdigit() or not (0 <= int(prog) <= 100):
            prog = input("Please enter a valid progress (0-100): ").strip()
            prog=input("Write Skill progress ").strip()
            break

        cr.execute("SELECT name from 'Skills' where name=? and user_id=?",(sk,user))
        result=cr.fetchone()
        if result!=None:
            print("Skill is Exists,You Cannot Add it!")
            user_update=input("Do You Want Update?[Y|N]").strip().capitalize()
            if user_update=='Y':
                update_skills()
            elif user_update=='N':
               print("OK!") 
            else:
                print("something wrong!")      
        else:
            cr.execute("INSERT INTO 'Skills'(user_id,name ,progress) values (?,?,?)",(user,sk,prog))
            print("Successfully added!")
      
    def delete_skills():
        sk=input("Write Skill Name ").strip().capitalize()
        cr.execute("SELECT name from 'Skills' where name=? and user_id=?",(sk,user))
        result=cr.fetchone()
        if result!=None:
           cr.execute("Delete from 'Skills'where name =? and user_id=?",(sk,user))
           
           print("Skill deleted successfully!")
           
        else:
             user_update=input("Do You Want add skill?[Y|N]").strip().capitalize()
             if user_update=='Y':
                 add_skills()
             elif user_update=='N':
               print("OK!") 
             else:
                print("something wrong!")
           
    def update_skills():
        print ("Update skills")
        sk=input("Write Skill Name ").strip().capitalize()
        prog=input("Write New Skill progress ").strip()
        cr.execute("Update 'Skills' set Progress =? where name=? and user_id=?",(prog,sk,user))
        print("Skill updated successfully!")

    def export_skills_to_csv():
        cr.execute("SELECT name, progress FROM Skills WHERE user_id=?", (user))
        results = cr.fetchall()
        
        if not results:
            print("No skills to export.")
        else:
            skills_csv_file = f"C:\\Users\\leens\\Desktop\\Python\\user_{user}_skills.csv"
            with open(skills_csv_file, "w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Skill Name", "Progress"])
                for row in results:
                    writer.writerow(row)
            print(f"Skills exported successfully to {skills_csv_file}")

    #chick if command is exists
    while True:
        user_input=input(input_message).strip().lower()
        if user_input in commands_list:
            if user_input =="s":
                show_skills()
            elif user_input=="a":
                add_skills()
            elif user_input=="d":
                delete_skills()
            elif  user_input=="u":
                update_skills()
            elif  user_input=="e":
                export_skills_to_csv()
            else:
                print("App is closed. Goodbye!")
                exit()      
        else:
            print(f"sorry this command \"{user_input}\" is Not Found")
            break
  
except sqlite3.Error as er:
    print(f"Error Reading Data {er}")


finally:
    db.commit()
    db.close()
    print("Connction To Database Is Closed")

