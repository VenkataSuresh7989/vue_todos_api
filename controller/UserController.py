from view import UsersView

#--------------------------------------------- GET ALL USERS -----------------------------------------------------------
def getalluser():
    return UsersView.getallusers()

#--------------------------------------------- GET USER BY ID ----------------------------------------------------------
def getuserbyid(id):
    return UsersView.getuserbyid(id)

#--------------------------------------------- CREATE USERS ------------------------------------------------------------
def createuser(username,full_name,email,password):
    return UsersView.createuser(username,full_name,email,password)

#--------------------------------------------- LOGIN USER --------------------------------------------------------------
def is_login(form_data):
    return UsersView.is_login(form_data)

#--------------------------------------------- UPDATE USER BY ID -------------------------------------------------------
def update_user(id,data):
    return UsersView.update_user(id,data)

#--------------------------------------------- DELETE USER BY ID -------------------------------------------------------
def delete_user(id):
    return UsersView.delete_user(id)
