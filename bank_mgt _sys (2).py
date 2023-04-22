import mysql.connector as db
import re
import time
import os
from prettytable import PrettyTable
from multipledispatch import dispatch
class Admin:
    def __init__(self):
        #create database
        mydb=db.connect(host="localhost",user="root",passwd="Squ@d123")
        query='''create database if not exists BasicDB;'''
        cur=mydb.cursor()
        cur.execute(query)
        mydb.close()
        # #create history table
        # self.connection()
        # query='''create table if not exists History_table(hid int primary key auto_increment,
        # Date_time datetime,
        # Action varchar(50),
        # Amount bigint not null,
        # Uid varchar(50) not null);'''
        # self.cur.execute(query)
        # self.mydb.close()
        #Create Table for Admin
        self.connection()
        query='''create table if not exists Admin_Raviraj(
        a_id int primary key ,
        a_username varchar(100),
        a_password varchar(100));'''
        self.cur.execute(query)
        self.mydb.close()


        #Admin Default data
        self.a_id=1
        self.a_username="admin"
        self.a_password="admin"
        self.AddAdminValue(self.a_id,self.a_username,self.a_password)


        #create directory to store files
        try:
            os.mkdir("AllFiles")

            
        except:
            pass


    #This method is used to connect python to mysql BasicDB database
    def connection(self):
        self.mydb=db.connect(host="localhost",user="root",passwd="Squ@d123",database="BasicDB")
        self.cur=self.mydb.cursor()

    #this method is used to add default admin data
    def AddAdminValue(self,a_id,a_username,a_password):
        self.connection()
        try:
            data=(a_id,a_username,a_password)
            query='''insert into Admin_Raviraj(a_id,a_username,a_password)
            values(%s,%s,%s);'''
            self.cur.execute(query,data)
            self.cur.execute("commit;")
            self.mydb.close()

        except:
            pass

    def AdminLogin(self,a_username,a_password):
        self.connection()
        data=(a_username,)
        query='''select a_username,a_password from Admin_Raviraj where a_username=%s;'''
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()
        return record

    def checkpass(self,passwd):
        self.connection()
        data=(passwd,)
        query='''select a_username,a_password from Admin_Raviraj where a_password=%s;'''
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()
        return record

    def ChangeAdminUsername(self,n_username,passwd):
        self.connection()
        data=(n_username,passwd)
        query='''update Admin_Raviraj set a_username=%s where a_password=%s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return "UserName Successfully Changed"

    def ChangeAdminPassword(self,n_password,oldpass):
        self.connection()
        data=(n_password,oldpass)
        query='''update Admin_Raviraj set a_password=%s where a_password=%s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return "Successfully Password Changed"

    def RemoveAccount(self,email,acc_no):
        self.connection()
        data=(email,acc_no)
        query='''delete from UserDetails_j where email=%s and account_no=%s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
            
        self.mydb.close()
     
        os.remove(f"AllFiles/{email}.txt")
        return True

    def CheckAcc(self,email,acc):
        self.connection()
        query='''select email,account_no from UserDetails_j where email=%s and account_no=%s;'''
        data=(email,acc)
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()

        if record is None:
            return False

        else:
            return True

 
    def LoanUser(self,loanType):
        self.connection()
        query='''select UserDetails_j.cname,
        UserDetails_j.contact,
        UserDetails_j.email,
        UserDetails_j.address,
        UserDetails_j.account_no,
        loan_table.amount,
        loan_table.month,
        loan_table.emi,
        loan_table.loan_status_date from UserDetails_j inner join loan_table on UserDetails_j .cid=loan_table.cid where loan_table.loan_type=%s;'''
        data=(loanType,)
        self.cur.execute(query,data)
        data=self.cur.fetchall()
        self.mydb.close()
        return data
        


    
class Bank(Admin):
    def __init__(self):
        super().__init__()

        #create table userdetails_j

        self.connection()
        query='''create table if not exists UserDetails_j(cid int primary key auto_increment,
        cname varchar(50) not null,
        contact varchar(50) unique,
        email varchar(100) not null unique,
        address text not null,
        created_at date not null,
        account_no bigint not null unique,
        amount bigint not null,
        password varchar(100));'''

        self.cur.execute(query)
        self.mydb.close()
        #create history table 
        self.connection()
        query='''create table if not exists History_table(hid int primary key auto_increment ,
        date_time datetime,
        action varchar(150),
        amount bigint,
        uid bigint);'''
        self.cur.execute(query)
        self.mydb.close()
        #create table for loan section 
        self.connection()
        query='''create table if not exists loan_table(lid int primary key auto_increment,
        amount bigint not null,
        month int not null,
        emi double not null,
        loan_status_date date not null,
        loan_type varchar(150) not null,
        cid int not null,
        foreign key(cid) references UserDetails_j(cid));'''
        self.cur.execute(query)
        self.mydb.close()

    def AddHistory(self,action,u_id):
        
        amount=self.CheckBalance(u_id)
        self.connection()
        data=(action,amount,u_id)


        query='''insert into History_table(date_time,action,amount,uid)values(now(),%s,%s,%s);'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()

    def ShowHistory(self,u_id):
        self.connection()
        data=(u_id,)
        query='''select * from History_table where uid=%s order by hid desc;'''
        self.cur.execute(query,data)
        record=self.cur.fetchall()                             
        self.mydb.close()
        return record

    def CreateAccountNumber(self):
        account_no=10000000

        self.connection()
        query='''select account_no from UserDetails_j order by cid desc limit 1;'''
        self.cur.execute(query)
        record=self.cur.fetchone()

        self.mydb.close()

        if record is not None:
            account_no=record[0]+1
            return account_no

        else:
            return account_no

    def CheckEmail_account(self,c_contact=None,c_email=None):
        self.connection()
        query='''select contact,email from UserDetails_j where contact=%s or email=%s;'''
        data=(c_contact,c_email)
        self.cur.execute(query,data)
        record =self.cur.fetchone()
        self.mydb.close()
        if record is None:
            return True
        elif record[0]==c_contact:
            return "Contact Exists"

        elif record[1]==c_email:
            return "Email Exists"
        


    def CreateAccount(self,c_name,c_contact,c_email,c_address,c_account,account,amount):

        self.connection()
        query='''insert into UserDetails_j(cname,contact,email,address,created_at, account_no,amount,password) values(%s,%s,%s,%s,%s,%s,%s,Null);'''

        data=(c_name,c_contact,c_email,c_address,c_account,account,amount)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return True

    def SetPassword(self,pass1,account_no):
        self.connection()
        query='''update UserDetails_j set password=%s where account_no =%s;'''
        data=(pass1,account_no)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()

    def CheckPassExists(self,account_no):
        self.connection()
        query='''select password from UserDetails_j where account_no=%s;'''
        data=(account_no,)
        self.cur.execute(query,data)
        record=self.cur.fetchone()

        self.mydb.close()
        return record

    def CheckUserPass(self,userid,password):
        self.connection()
        query='''select contact,password from UserDetails_j where contact=%s and password=%s;'''
        data=(userid,password)
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()
        
        return record
        # print(record)

    def CheckBalance(self,u_id):
        self.connection()
        query='''select amount from UserDetails_j where contact=%s;'''
        data=(u_id,)
        self.cur.execute(query,data)
        record=self.cur.fetchone()
        self.mydb.close()
        return record[0]
    
    def CreditAmount(self,u_id,amm):
        prev=self.CheckBalance(u_id)
        curr=prev+amm
        self.connection()
        query='''update UserDetails_j set amount=%s where contact=%s;'''
        data=(curr,u_id)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        return "Successfully updated"

    def WithdrawAmount(self,u_id,amm):
        previous_amm=self.CheckBalance(u_id)
        if amm>previous_amm:
            return "insufficient balance"
        else:
            withdamount=previous_amm-amm
            self.connection()
            data=(withdamount,u_id)
            query='''update UserDetails_j set amount=%s where contact=%s;'''        
            self.cur.execute(query,data)
            self.cur.execute("commit;")
            self.mydb.close()
            return "Successfully Withdrawn"
        
    @dispatch(str,str)
    def UpdateUserName(self,ra,u_id):
        self.connection()
        query='''update UserDetails_j set cname=%s where contact=%s; '''
        data=(ra,u_id)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
    @dispatch(str,str,str)
    def UpdateUserName(self,ra,address,u_id):
        self.connection()
        query='''update UserDetails_j set cname=%s,address=%s where contact=%s'''
        data=(ra,address,u_id)
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        
    def CheckLoan(self,ri,p,month):
        year=month/12
        intrest=p*year*ri/100
        total=p+intrest
        emi=total/(year*12)
        
        # print(emi)
        return emi
    def ApplyLoan(self,p,month,emi,loanType,u_id):
        #get cid using u_id from UserDetails_j table
        self.connection()
        data=(u_id,)
        query='''select cid from UserDetails_j where contact=%s;'''
        self.cur.execute(query,data)
        cid=self.cur.fetchone()
        self.mydb.close()
        #insert loan details into loan table
        self.connection()
        loan_date=time.strftime("%y-%m-%d")
        data=(p,month,emi,loan_date ,loanType,cid[0])
        query='''insert into loan_table(amount,month ,emi,loan_status_date,loan_type,cid)values(%s,%s,%s,%s,%s,%s);'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        print("\n************Loan Applied Successfully*************")


class RegExp(Bank):
    def __init__(self):

        super().__init__()

    def NameValidation(self,c_name):
        ptr=r"^[a-zA-Z\ ]+$"
        if re.match(ptr,c_name):
            return True
        else:
            return False

    def ContactValidation(self,c_contact):
        ptr=r"^[6789]\d{9}$"
        if re.match(ptr,c_contact):
            return True
        else:
            return False

    def EmailValidation(self,c_email):
        ptr=r"^\b[a-zA-Z0-9\.\_]+@[a-z]+\.[a-z]+\b"
        if re.findall(ptr,c_email):
            return True

        else:
            return False


#application starts from here
app=RegExp()
while True:
    print("\n **************** Bank Management System **************\n")
    print("\n1--Admin Login \n2--User Login \n3--loan Section \n4--Generate User Password \n5--Exit\n")

    ch=input("Enter Your Choice:")

    #This section is used for Admin Task
    if ch=="1":
        print("\n**************Admin LoginSection *************\n")
        a_username=input("Enter Admin Username:")
        a_password=input("Enter Admin Password:")
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
                    print("\n *********** Welcome To Admin Section ************\n")
                    print("1--Add User\n2--Remove User\n3--Change Admin Username/ Password\n4--Check User Loan\n5--Admin Log out\n")
                    
                    ach=input("Enter Your Choice:")
                    #add user section
                    if ach=="1":
                        print("\n********* Create Account Section **********\n")
                        LoanStatus=False
                        #Name Validation
                        while True:
                            c_name=input("Enter Customer Name:")
                            x=app.NameValidation(c_name)
                            if x==True:
                                break
                            else:
                                print("\n****** Invalid Name Input ***********\n")


                        #Contact Validation
                        while True:

                            c_contact=input("Enter Customer Contact:")
                            x1=app.ContactValidation(c_contact)
                            if x1==True:
                                break
                            else:
                                print("\n******** Contact Invalid *********\n")

                        #Email Validation
                        while True:

                            c_email=input("Enter Customer Email:")
                            x2=app.EmailValidation(c_email)
                            if x2==True:
                                break
                            else:
                                print("\n******** Wrong Email **********\n")



                        #Address Input
                        c_address=input("Enter Customer Address:")

                        #Account Creation Date
                        c_account=time.strftime("%Y-%m-%d")

                        #account Number generation
                        account=app.CreateAccountNumber()
                        print(account)

                        #amount
                        amount=0

                        #password--Null
                        xa=app.CheckEmail_account(c_contact,c_email)
                        if xa is True:

                            bank_account=app.CreateAccount(c_name,c_contact,c_email,c_address,c_account,account,amount)
                            if bank_account==True:

                                #create file to store info
                                with open(f"AllFiles/{c_email}.txt","a") as file:
                                    file.write(f"User Name: {c_name}\n")
                                    file.write(f"User Contact: {c_contact}\n")
                                    file.write(f"User Email-Id: {c_email}\n")
                                    file.write(f"User Address: {c_address}\n")
                                    file.write(f"Account Created On: {c_account}\n")
                                    file.write(f"Account Number: {account}\n")




                                print("\n************** Account Successfully Created ***********\n")
                           

                        else:
                            print(f"\n***********{xa}************\n")
                            
                        
                    #remove user section
                    elif ach=="2":
                        print("\n************* Close Account *************\n")
                        while True:
                            email=input("Enter Email Id to remove Account:")
                            x=app.EmailValidation(email)
                            if x==True:
                                break
                            else:
                                print("\n************ Invalid Email Id *************\n")

                        checkuser=app.CheckEmail_account(c_email=email)
                        if checkuser==True:
                            print("/n\n************* User Does Not Exists *************\n ")
                        else:
                            acc_no=input("Enter Account Number:")
                            checkaccc=app.CheckAcc(email,acc_no)
                            if checkaccc==False:
                                print("\n************** Incorrect Account Number ************\n")

                            else:

                                r_acc=app.RemoveAccount(email,acc_no)
                                if r_acc==True:
                                    print("\n************* Account Successfully Closed ************\n")

                                else:
                                    print(f"\n*************{r_acc}**************\n")


                    #change admin password
                    elif ach=="3":
                        print("\n****************Change Admin Username and password ************\n")
                        print("1--Change Admin Username\n2--Change Admin password")
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

                    #check user loan
                    elif ach=="4":
                        print("\n***********check user loan**********\n")
                        print("\n1-Apply Home Loan\n2-Apply Education Loan\n3-Personal loan\n")
                        ach=input("enter Loan  choice:")
                        if ach=="1":
                            print("\n******Home Loan User***********\n")
                            loanType="Home Loan"
                            data=app.LoanUser(loanType)
                            x=PrettyTable()
                            x.field_names=["cname","contact","email","address","account_no","Loan_amount","loan_month","emi","loan_status_date"]
                            x.add_rows(data)
                            print(x)
                        elif ach=="2":
                            print("\n**********education loan user*******\n")
                            loanType="education loan"
                            data=app.LoanUser(loanType)
                            x=PrettyTable()
                            x.field_names=["cname","contact","email","address","account_no","Loan_amount","loan_month","emi","loan_status_date"]
                            x.add_rows(data)
                            print(x)

                        elif ach=="3":
                            print("\n********personal loan********\n")
                            loanType="personal loan"
                            data=app.LoanUser(loanType)
                            x=PrettyTable()
                            x.field_names=["cname","contact","email","address","account_no","Loan_amount","loan_month","emi","loan_status_date"]
                            x.add_rows(data)
                            print(x)
                        else:
                            print("\n*********invalid choice*******\n")
                    #admin log out
                    elif ach=="5":
                        print("\n***************Admin Logged Out **************\n")
                        break
                    else:
                        print("\n************** Admin Invalid Option ***********\n")


    #This Section is used for User Task
    elif ch=="2":
        print("\n*************** WELCOME TO SBI BANK ***************\n")
        u_id=input("Enter Contact:")
        x=app.ContactValidation(u_id)
        if x is True:

            chuser=app.CheckEmail_account(c_contact=u_id)
            # print(chuser)
            if chuser != None:
            

                ls=chuser.split()
            
            
                
            if ls[1] == "Exists":
                p_id=input("Enter Password:")
                chpass=app.CheckUserPass(u_id,p_id)
                
                if chpass[1]==p_id:
                    print("\n************ Successsfully logged In ***********\n")
                    while True:
                        print("1--Check Balance\n2--Credit Amount\n3--Withdraw Amount\n4--Transaction History\n5--Update User Details\n6-Apply For Loan\n7--Log Out User")
                        uch=input("Enter Your Choice:")
                        if uch=="1":
                            print("\n************ Check Balance ****************\n")
                            balance=app.CheckBalance(u_id)
                            print(f"\n********** Balance is :{balance} ****************\n")

                        elif uch=="2":
                            print("/n************** Credit Amount ***********\n")
                            amm=int(input("Enter Amount To be Credited:"))
                            x=app.CreditAmount(u_id,amm)
                            print(f"\n****************{x}**************\n")
                            action=f"credit Amount{amm}"
                            app.AddHistory(action ,u_id)

                        elif uch=="3":
                            print("\n************* WithDraw Amount *************\n")
                            amm=int(input("enter amount:"))
                            x1=app.WithdrawAmount(u_id,amm)
                            if x1==True:
                                print("\n**********successfully amount widraw**********\n")
                                action=f"widraw Amount{amm}"
                                app.AddHistory(action,u_id)

                            else:
                                print(x1)

                            # witdra=int(input("Enter Amount to be WithDraw:"))
                            # xcheck=app.CheckBalance(u_id)
                            # if xcheck<witdra:
                            #     print("\n********** Withdraw Amount is greater than Balance**********\n")

                            # else:
                            #     ycheck=app.WithdrawAmount(witdra,u_id)
                            #     print(f"\n************ {ycheck} ***********\n")
                            
                            
                        elif uch=="4":
                            print("\n***********all data from history table*********\n")
                            history=app.ShowHistory(u_id)
                        
                            x=PrettyTable()
                            x.field_names=["hid","date_time","action","amount","u_id"]
                            x.add_rows(history)
                            print(x)
                            
                            

                        elif uch=="5":
                            print("\n************UserDetails**************\n")
                            ud=input("enter your choice:")
                            if ud=="1":
                                ra=input("enter your name:")
                                app.UpdateUserName(ra,u_id)
                                print("\n***********successfully updated**********\n")
                            elif ud=="2":
                                ra=input("enter new name:")
                                ad=input("enter new address:")
                                app.UpdateUserName(ra,ad,u_id)
                                print("\n************successfully updated********\n")
                            elif ud=="3":
                                print("\n*********thank you*******\n")
                                break
                            else:
                                print("\n*************invalid choice************\n")

                            
                        elif uch=="6":
                            print("\n******apply Loan******")
                            print("\n1-Apply Home Loan\n2-Apply edu loan\n3-Apply personal loan")
                            lch=input("enter Loan choice:")
                            if lch=="1":
                                ri=8.75
                                p=int(input("Enter Principle amount:"))
                                month=int(input("enter number of months:"))
                                emi=app.CheckLoan(ri,p,month)
                                print(f"Per Month Emi Is{emi}for {month}months")
                                loanType="Home Loan"
                                app.ApplyLoan(p,month,emi,loanType,u_id)
                            elif lch=="2":
                                ri=8.90
                                p=int(input("enter principle amount:"))
                                month=int(input("enter number of months:"))
                                emi=app.CheckLoan(ri,p,month)
                                print(f"Per Month Emi Is{emi}for {month}months")
                                loanType="education loan"
                                app.ApplyLoan(p,month,emi,loanType,u_id)
                            
                            elif lch=="3":
                                ri=10.50
                                p=int(input("enter principle amount:"))
                                month=int(input("enter number of months:"))
                                emi=app.CheckLoan(ri,p,month)
                                print(f"Per Month Emi Is{emi}for {month}months")
                                loanType="personal loan"
                                app.ApplyLoan(p,month,emi,loanType,u_id)
                            else:
                                print("\n*************invalid loan Choice**************\n")

                                
                        
                        elif uch=="7":
                            print("\n************** Thank You **************\n")
                            break
                        else:
                            print("\n************* Invalid Choice **********\n")

                else:
                    print("\n*************** Wrong Password ****************\n")

        else:
            print("\n************ Contact Not Exists *************\n")

    
    #This section is used for Loan Section
    elif ch=="3":
        print("\n**************Loan Section*************\n")
        # home loan-8.75 personal loan -10.50 education loan-8.90
        print("1-Home Loan\n2-personal loan\n3-Education Loan \n4-Exit")
        while True:
            lch=input("enter loan choice:")
            if lch=="1":
                print("\n********home loan section*********\n")
                ri=8.75
                p=int(input("enter principal amount:"))
                month =int(input("enter number  of  months  in numbers:"))
                emi=app.CheckLoan(ri,p,month)
                print(f"\n***********{emi}**********\n")

            elif lch=="2":
                print("\n************personal loan section**********\n")
                ri=10.50
                p=int(input("enter principal amount:"))
                month =int(input("enter number  of  months  in numbers:"))
                emi=app.CheckLoan(ri,p,month)
                print(f"\n*********{emi}**********\n")
            elif lch=="3":
                print("\n*************Education Loan Section*************\n")
                ri=8.90
                p=int(input("enter principal amount:"))
                month =int(input("enter number  of  months  in numbers:"))
                emi=app.CheckLoan(ri,p,month)
                print(f"\n***********{emi}************\n")
            elif lch=="4":
                print("\n**********exit from loan section**********\n")
                break
            else:
                print("\n***********invalid option ************\n")
    #This Section is used for Generating User Password
    elif ch=="4":
        print("\n**************** Generate user Password *************\n")
        while True:
            data=input("Enter Contact or Email:")
            contact=False
            email=False
            if data.isdigit():

                v_contact=app.ContactValidation(data)
                if v_contact is True:
                    x=app.CheckEmail_account(c_contact=data)
                    break

                else:
                    print("\n************ Invalid Contact Number **************\n")

            else:

                v_email=app.EmailValidation(data)
                if v_email is True:
                    y=app.CheckEmail_account(c_email=data)
                    break

                else:
                    print("\n************ Invalid Email Id **************\n")

        if (contact is True) or (email is True):
            print("\n************* Account Does Not Exists**************\n")

        else:
            account_no=input("Enter account Number:")
            checkexist=app.CheckPassExists(account_no)
            if checkexist[0] is None:
                pass1=input("Password:")
                pass2=input("Confirm Password:")
                if pass1==pass2:
                    app.SetPassword(pass1,account_no)
                    print("\n************ Successfully Password Updated **********\n")

                else:
                    print("\n ************** Password Mismatch *************\n")


            else:
                print("\n********** Password Already Updated ****************\n")

    elif ch=="5":
        print("\n************ Thank You ****************\n")
        break

    else:
        print("\n********* Invalid Option ************\n")

