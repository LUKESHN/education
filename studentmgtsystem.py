import time
import re
import mysql.connector as db
import os
from multipledispatch import dispatch
from prettytable import PrettyTable
class Admin:
    def __init__(self):
        #create database
        mydb=db.connect(host="localhost",user="root",passwd="Squ@d123")
        query='''create database if not exists Student;'''
        cur=mydb.cursor()
        cur.execute(query)
        mydb.close()


        self.connection()
        query='''create table if not exists Admin_l(
        a_id int primary key ,
        a_username varchar(100),
        a_password varchar(100));'''
        self.cur.execute(query)
        self.mydb.close()
    #create directory to store files
        try:
            os.mkdir("AllFiles")
        except:
            pass
        self.connection()
        query='''create table if not exists UserDetails_s(sid int primary key auto_increment,
        sname varchar(50) not null,
        contact varchar(50) unique,
        email varchar(100) not null unique,
        address text not null,
        s_course varchar(50) not null,
        course_start_date date not null,
        student_fees bigint not null,
        course_duration varchar(100) not null,
        password varchar(100));'''
        self.cur.execute(query)
        self.mydb.close()


       
        #Admin Default data

        self.a_id=1
        self.a_username="admin"
        self.a_password="admin"
        self.AddAdminValue(self.a_id,self.a_username,self.a_password)



    #This method is used to connect python to mysql Lukesh database
    def connection(self):
        self.mydb=db.connect(host="localhost",user="root",passwd="Squ@d123",database="Student")
        self.cur=self.mydb.cursor()

    #this method is used to add default admin data
    def AddAdminValue(self,a_id,a_username,a_password):
        self.connection()
        try:
            data=(a_id,a_username,a_password)
            query='''insert into Admin_l(a_id,a_username,a_password)
            values(%s,%s,%s);'''
            self.cur.execute(query,data)
            self.cur.execute("commit;")
            self.mydb.close()

        except:
            pass

    def AdminLogin(self,a_username,a_password):
        self.connection()
        data=(a_username,)
        query='''select a_username,a_password from Admin_l where a_username=%s;'''
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()
        return record
    def checkpass(self,passwd):
        self.connection()
        data=(passwd,)
        query='''select a_username,a_password from Admin_l where a_password=%s;'''
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()
        return record

    def ChangeAdminUsername(self,n_username,passwd):
        self.connection()
        data=(n_username,passwd)
        query='''update Admin_l set a_username=%s where a_password=%s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return "UserName Successfully Changed"

    def ChangeAdminPassword(self,n_password,oldpass):
        self.connection()
        data=(n_password,oldpass)
        query='''update Admin_l set a_password=%s where a_password=%s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return "Successfully Password Changed"

    def deletestudent(self,email):
        self.connection()
        data=(email,)
        query='''delete from UserDetails_s where email=%s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
            
        self.mydb.close()
     
        os.remove(f"AllFiles/{email}.txt")
        return True
    def RemoveAccount(self,email,contact):
        self.connection()
        data=(email,contact)
        query='''delete from UserDetails_s where email=%s and contact=%s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
            
        self.mydb.close()
     
        os.remove(f"AllFiles/{email}.txt")
        return True

    def CheckAcc(self,email,contact):
        self.connection()
        query='''select email,contact from UserDetails_s where email=%s and contact=%s;'''
        data=(email,contact)
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()

        if record is None:
            return False

        else:
            return True
    
class student(Admin):
    def __init__(self):

        super().__init__()
    #create student table
        self.connection()
        query='''create table if not exists student_table(sid int primary key auto_increment,
        sname varchar(50) not null,
        sage varchar(50) unique,
        email varchar(100) not null unique,
        address text not null,
        student_status_date date not null,
        rollno int not null,
        amount bigint not null,
        password varchar(100));'''
        self.cur.execute(query)
        self.mydb.close()
    #create course table
        self.connection()
        query='''create table if not exists course_table(cid int primary key auto_increment,
        cname varchar(50) not null,
        course_duration varchar(50) not null,
        fees bigint not null);'''
        self.cur.execute(query)
        self.mydb.close()
    # create student fees table
        self.connection()
        query='''create table if not exists payment_table(pid int primary key auto_increment,
        scourse varchar(50) not null,
        spayment varchar(100) not null,
        Date date not null);'''
        self.cur.execute(query)
        self.mydb.close()
    def Addstudent(self,sname,contact,email,address,s_course,course_start_date,student_fees,course_duration):
        self.connection()
        query='''insert into UserDetails_s(sname,contact,email,address,s_course,course_start_date,student_fees,course_duration,password)values(%s,%s,%s,%s,%s,%s,%s,%s,null);'''
        data=(sname,contact,email,address,s_course,course_start_date,student_fees,course_duration)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return True
    def addcourse(self,cname,course_duration,fees):
        self.connection()
        query='''insert into course_table(cname,course_duration,fees)values(%s,%s,%s);'''
        data=(cname,course_duration,fees)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return True
    def Checkemail_account(self,contact=None,email=None):
        self.connection()
        query='''select contact,email from UserDetails_s where contact=%s or email=%s;'''
        data=(contact,email)
        self.cur.execute(query,data)
        record =self.cur.fetchone()
        self.mydb.close()
        if record is None:
            return True
        elif record[0]==contact:
            return "Contact Exists"

        elif record[1]==email:
            return "email Exists"
            
    def CheckUserPass(self,userid,password):
        self.connection()
        query='''select contact,password from UserDetails_s where contact=%s and password=%s;'''
        data=(userid,password)
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()
        
        return record
        # print(record)
    def studentLogin(self , contact , pass1):
        self.connection()
        data = (contact , pass1)
        query = '''select contact from UserDetails_s where contact = %s && password = %s;'''
        self.cur.execute(query , data)
        record = self.cur.fetchone()

        self.mydb.close()

        return record
    def Checkfees(self,u_id):
        self.connection()
        query='''select student_fees from UserDetails_s where contact=%s;'''
        data=(u_id,)
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()
        return record[0]
    def Creditfees(self,contact,amm):
        prev=self.Checkfees(contact)
        curr=prev+amm
        self.connection()
        query='''update UserDetails_s set amount=%s where contact=%s;'''
        data=(curr,contact)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        return "Successfully updated"
    def CheckInfo(self , contact = None, email = None):
        self.connection()

        data = (contact , email)

        query = '''select contact , email from UserDetails_s where contact = %s or email = %s;'''

        self.cur.execute(query , data)
        
        record = self.cur.fetchone()

        # print(record)

        self.mydb.close()

        if record == None:
            return True

        elif record[0] == contact:
            return "Contact Already Exists"

        elif record[1] == email:
            return "\n**********email Already Exists***********\n"
    def studentinfo(self,sname,sage,email,address,student_status_date,rollno,amount):
        self.connection()
        query='''insert into student_table(sname,sage,email,address,student_status_date,rollno,amount,password)values(%s,%s,%s,%s,%s,%s,%s,null);'''
        data=(sname,sage,email,address,student_status_date,rollno,amount)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return True
    def paymentfees(self,scourse,spayment,Date):
        self.connection()
        query='''insert into payment_table(scourse,spayment,Date)values(%s,%s,%s);'''
        data=(scourse,spayment,Date)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return True

    @dispatch(str , str)
    def UpdateUser(self,ra,contact):
        self.connection()
        query='''update UserDetails_s set sname=%s where contact=%s; '''
        data=(ra,contact)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
    @dispatch(str,str,str)
    def UpdateUser(self,ra,address,contact):
        self.connection()
        query='''update UserDetails_s set sname=%s,address=%s  where contact=%s'''
        data=(ra,address,contact)
        self.cur.execute(query,data)
        self.cur.execute("commit;")  

    def ChangePass(self , contact , pass1):
        self.connection()

        query = '''update UserDetails_s set password = %s where contact =%s;'''

        data = (pass1 , contact)
        self.cur.execute(query , data)
        self.cur.execute("commit;")
        self.mydb.close()
    

    def CheckPassExist(self , contact):
        self.connection()

        query = '''select password from UserDetails_s where contact = %s;'''
        data = (contact,)
        self.cur.execute(query , data)
        record = self.cur.fetchone()

        self.mydb.close()
        return record
    
    def fetch_students(self , contact):
        self.connection()
        data = (contact,)
        query = '''select * from userdetails_s where contact = %s;'''

        self.cur.execute(query , data)
        r = self.cur.fetchone()

        self.mydb.close()

        return r

class Regexp(student):
    def __init__(self):

        super().__init__()
    # create table
    #create table UserDetails_s

        # self.connection()
        # query='''create table if not exists UserDetails_s(sid int primary key auto_increment,
        # sname varchar(50) not null,
        # contact varchar(50) unique,
        # email varchar(100) not null unique,
        # address text not null,
        # course_start_date not null,
        # student_fees bigint not null,
        # course_duration varchar(100) not null,
        # password varchar(100));'''
        # self.cur.execute(query)
        # self.mydb.close()
    def Namemailidation(self,s_name):
        ptr=r"^[a-zA-Z\ ]+$"
        if re.match(ptr,s_name):
            return True
        else:
            return False

    def ContactValidation(self,contact):
        ptr=r"^[6789]\d{9}$"
        if re.match(ptr,contact):
            return True
        else:
            return False

    def emailValidation(self,email):
        ptr=r"^\b[a-zA-Z0-9\.\_]+@[a-z]+\.[a-z]+\b"
        if re.findall(ptr,email):
            return True

        else:
            return False
# aplication start from here
app=Regexp()
while True:
    print("\n **************** student management system**************\n")
    print("\n1--Admin Login \n2--student Login  \n3--Generate User Password \n4--Exit\n")

    ch=input("Enter Your Choice:")

    #This section is used for Admin Task
    if ch=="1":
        print("\n**************Admin LoginSection *************\n")
        a_username=input("Enter student Username:")
        a_password=input("Enter student Password:")
        admin=app.AdminLogin(a_username,a_password)
        if admin==None:
            print("\n************ Invalid Username**********")
        else:
            if a_password!=admin[1]:
                print("\n***********Invalid Password**************\n")
            else:
                print("\n***************Successfully Logged In**************\n")
                #admin page section
                while True:
                    print("\n *********** Welcome To admin Section ************\n")
                    print("1--Add User\n2--Remove User\n3--Change Admin Username/password\n4-admin log out\n")
                    
                    ach=input("Enter Your Choice:")
                    #add user section
                    if ach=="1":
                        print("\n********* Create student section **********\n")
                        
                        #Name Validation
                        while True:
                            sname=input("Enter student Name:")
                            x=app.Namemailidation(sname)
                            if x==True:
                                break
                            else:
                                print("\n****** Invalid Name Input ***********\n")


                        #Contact Validation
                        while True:

                            contact=input("Enter student Contact:")
                            x1=app.ContactValidation(contact)
                            if x1==True:
                                break
                            else:
                                print("\n******** Contact Invalid *********\n")

                        #email Validation
                        while True:

                            email=input("Enter student email:")
                            x2=app.emailValidation(email)
                            if x2==True:
                                break
                            else:
                                print("\n******** Wrong email **********\n")


                        
                        #Address Input
                        address=input("Enter student Address:")
                        #student course
                        s_course=input("enter student course:")
                        #student fees
                        student_fees=input("enter amount of student fees:")
                        #course duration
                        course_duration=input("enter student course duration:")
                        # course start date
                        course_start_date=time.strftime("%Y-%m-%d")
                        #studentstatus date
                        student_status_date=time.strftime("%Y-%m-%d")
                        #age
                        sage=input("enter student age:")
                        #defailt amount
                        amount=0
                        #rollno
                        rollno=input("enter student rollno:")
                        # password--null
                        xa=app.Checkemail_account(contact,email)
                        if xa is True:
                        
                            addstudent=app.Addstudent(sname,contact,email,address,s_course,course_start_date,student_fees,course_duration)
                            if addstudent==True:

                            #create file to store info
                                with open(f"AllFiles/{email}.txt","a") as file:
                                    file.write(f"User Name: {sname}\n")
                                    file.write(f"User Contact: {contact}\n")
                                    file.write(f"User email-Id: {email}\n")
                                    file.write(f"User Address: {address}\n")
                                    file.write(f"course On: {s_course}\n")
                                    file.write(f"course start date:{course_start_date}\n")
                                    file.write(f"student fees:{student_fees}\n")
                                    file.write(f"course duration: {course_duration}\n")
                                print("\n********student successfully added")
                            else:
                                print("\n**********not added**********\n")
                        else:
                            print(f"\n*************{xa}************\n") 
                            
        

                        #remove user section
                    elif ach=="2":
                        print("\n************* Close  student Account *************\n")
                        while True:
                            email=input("Enter email Id to remove student Account:")
                            x=app.emailValidation(email)
                            if x==True:
                                break
                            else:
                                print("\n************ Invalid email Id *************\n")

                        checkuser=app.Checkemail_account(email=email)
                        if checkuser==True:
                            print("/n\n************* User Does Not Exists *************\n ")
                        else:
                            contact=input("Enter contact Number:")
                            checkaccc=app.CheckAcc(email,contact)
                            if checkaccc==False:
                                print("\n************** Incorrect contact Number ************\n")

                            else:

                                r_acc=app.RemoveAccount(email,contact)
                                if r_acc==True:
                                    print("\n************* Account Successfully Closed ************\n")

                                else:
                                    print(f"\n*************{r_acc}**************\n")
                     #change admin password
                    elif ach=="3":
                        print("\n****************Change Admin Username and password ************\n")
                        print("1-Change Admin Username\n2-change admin password")
                        cch=input("Enter your Choice:")
                        if cch=="1":
                            passwd=input("Enter Admin Password:")
                            x=app.checkpass(passwd)
                            if x==None:
                                print("\n*********Invalid Admin Password**********]n")
                            else:
                                n_username=input("Enter New UserName:")
                                x1=app.ChangeAdminUsername(n_username,passwd)
                                print(f"\n***************{x1}*************\n")
                        
                                

                        elif cch=="2":
                            oldpass=input("Enter Your old password:")
                            y=app.checkpass(oldpass)
                            if y==None:
                                print("\n*********** Invalid Old password ***********\n")
                            else:
                                n_password=input("Enter your New Password:")
                                y1=app.ChangeAdminPassword(n_password,oldpass)
                                print(f"\n**********{y1}*******\n")

                        else:
                            print("\n***********Invalid Option ************\n")
                    #admin log out
                    elif ach=="4":
                        print("\n***************Admin Logged Out **************\n")
                        break
                    else:
                        print("\n************** Admin Invalid Option ***********\n")
    # student login
    elif ch=="2":

        print("\n*************** WELCOME To student student account section***************\n")
        while True:
            contact=input("Enter student Contact:")
            x1=app.ContactValidation(contact)
            if x1==True:
                break
            else:
                print("\n******** Contact Invalid *********\n")
        pass1 = input("Enter Password :")
        y = app.studentLogin(contact , pass1)
        if y == None:
            print("\n********** incorrect Details ************\n")
        else:
            print("\n********* Successfully Login ********\n")
            while True:
                print("\n 1-student information \n2-courses \n3update student account  \n4-check fees balance\n5-fees payment\n6 exit")
                uch=input("enter your choice:")
                if uch=="1":
                    r = app.fetch_students(contact)
                    x = PrettyTable()
                    x.field_names = ["sid","sname" ,"contact" , "email","address" ,"s_course" ,"course_start_date" ,"student_fees","course_duration" ,"password"]
                    x.add_row(r)
                    print(x)
                    print()


                  
                            
                elif uch=="2":
                    print("\n*********courses*********\n")
                    print("\n1-Apply for courses\n2-exit\n")
                    
                    ach=input("enter  choice:")
                    if ach=="1":

                        print("\n******course user***********\n")
                        cname=input("enter course name")
                        course_duration=input("enter your course duration")
                        fees=input ("enter amount of  course fees")
                        x=app.addcourse(cname,course_duration,fees)
                        if x==True:
                            print("\n************successfully added courses********\n")
                        else:
                            print("\n*********not added******\n")
                        
                        
                elif uch=="3":
                    
                    print("\n************UserDetails**************\n")
                    ud=input("enter your choice:")
                    if ud=="1":

                        ra=input("enter your name:")
                        app.UpdateUser(ra,contact)
                        print("\n***********successfully updated**********\n")
                    elif ud=="2":
                        ra=input("enter new name:")
                        ad=input("enter new address:")
                        app.UpdateUser(ra,ad,contact)
                        print("\n************successfully updated********\n")
                    elif ud=="3":
                        print("\n*********thank you*******\n")
                        break
                    else:
                        print("\n*************invalid choice************\n")

                
                
                elif uch=="4":
                    print("\n************ Check  fees Balance ****************\n")
                    balance=app.Checkfees(contact)
                    print(f"\n********** Balance is :{balance} ****************\n")

                elif uch=="5":
                    print("/n**************payments fees amount ***********\n")
                    Date=time.strftime("%Y-%m-%d")
                    scourse=input("enter course:")
                    spayment=input("enter payment:")
                    
                    a=app.paymentfees(scourse,spayment,Date)
                    if a==True:
                        print("\n**********successfully payment added*********\n")
                    else:
                        print("\n***********not added************\n")
                   
                elif uch=="6":
                    print("\n**********exit********\n")
                    break
                else:
                    print("\n***********invalid choice***********\n")


   
                    
                    
        
                   
        
    #generate  password
    elif ch=="3":
        
        print("\n ************* Generate User Password ************\n")
        while True:
            data = input("Enter Contact or email :")
            
            contact = False
            email = False
            if data.isdigit():
                v_contact = app.ContactValidation(data)
                if v_contact is True:
                    contact = app.CheckInfo(contact = data)
                    break
                else:
                    print("\n****************** Invalid Contact Number ***********\n")

            else:
                v_email = app.emailValidation(data)
                if v_email is True:
                    email = app.CheckInfo(email = data)
                    break

                else:
                    print("\n************** Invalid email-ID ****************\n")

        if (contact is True) or (email is True):
                print("\n**************** Account Does Not Exists ***********\n")

        else:
            contact = input("Enter Your contact Number :")
            checkexit = app.CheckPassExist(contact)
            if checkexit[0] is None:
                pass1 = input("Enter Password :")
                pass2 = input("Enter Confirm Password :")

                if pass1 == pass2:
                    app.ChangePass(contact , pass1)
                    print("\n************ Pasword Succesfully Updated *************\n")
                else:
                    print("\n*********** Password MisMatched **********\n")
            else:
                print("\n*************** Password Already Updated **********\n")

    elif ch=="4":
        print("\n*************Thank you***********\n")
        break
    else:
        print("\n************invalid option*************\n")


                        




                               