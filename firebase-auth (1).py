import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred =credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app( cred )
# sig up account

''' 
email =input('Please enter your email address:')
password =input('Please enter your password:')

user= auth.create_user(email = email, password = password, phone_number = '+84944991349')
print("User createrd successfully : {0}".format(user.uid))

get the user

email ='zz@gmail.com'
phone = "+84944991349"
by_phone =auth.get_user_by_phone_number(phone)
user= auth.get_user_by_email(email)
print("User id is :{0}".format(user.uid))
print("User id is : {0}".format(by_phone.uid))'
'''



#list all the users
''' 
page = auth.list_users()

while page:
    for user in page.users:
        print("User : "+ user.uid)

        #get next page
    page=page.get_next_page()
'''

#create user by id


'''email = input("Please enter your email address :")
password = input("Please enter your password :")
id=input("Please enter your id :")
user=auth.create_user(uid = id, email=email, password= password)
print("Successfully created  new user : {0}".format(user.uid))
'''
#change password

'''email = input("Please enter your email : ")
link = auth.generate_password_reset_link(email,action_code_settings=None )
print(link) '''
#change password by veri link email
email = input("Please enter your email address: ")
link = auth.generate_email_verification_link(email,action_code_settings=None )
print(link)