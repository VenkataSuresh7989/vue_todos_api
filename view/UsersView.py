import json

from datetime import datetime, timedelta
from http.client import HTTPException
from starlette import status
from config.authentication import cipher_suite, pwd_context, authenticate_user, fake_users_db, \
    ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, getall_users
from config.common import is_valid_email
from config.database import connect_db

#--------------------------------------------- GET ALL USERS ---------------------------------------------------------


def getallusers():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT id, username, full_name, email, hashed_password, disabled FROM users WHERE status <> '1'"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            row["hashed_password"] = cipher_suite.decrypt(row["hashed_password"]).decode()
        return {"status": 200, "data": rows}
    except Exception as e:
        print(e)
        return {"status": 403, "data": str(e)}


#--------------------------------------------- GET USER BY ID ---------------------------------------------------------
def getuserbyid(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (id))
        rows = cursor.fetchall()
        return {"status": 200, "data": rows}
    except Exception as e:
        print(e)
        return {"status": 403, "data": e}

#--------------------------------------------- CREATE USERS ---------------------------------------------------------
def createuser(username,full_name,email,password):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        if is_valid_email(email):
            # Verification for Email Alredy Exist or not.
            query_string = "SELECT * FROM users WHERE email LIKE %s"
            cursor.execute(query_string, email)
            isEmail = cursor.fetchall()
            user_pwd = cipher_suite.encrypt(password.encode())
            print("user_pwd : ",user_pwd)

            if (isEmail.__len__() == 1):
                return {"status": 422, "data": "User already exists with " + email }
            else:

                sql = "INSERT INTO `users` (`id`, `username`, `full_name`, `email`, `hashed_password`, `disabled`, `created_at`, `created_by`, `updated_at`, `updated_by`, `status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                args = ("NULL", username, full_name, email, user_pwd,  'False', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "admin", '', '', '0')

                cursor.execute(sql, args)
                conn.commit()

                return {"status": 200, "data": "New User added Successfully."}
        else:
            return {"status": 422, "data": "Invalid email."}
    except Exception as e:
        return {"status": 500, "data": e}

#--------------------------------------------- LOGIN USER ---------------------------------------------------------
def is_login(form_data):
    fake_users_db = getall_users()
    print("fake_users_db : ",fake_users_db)
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "user_info" : get_user_id(form_data.username,form_data.password, fake_users_db)}

def get_user_id(username,password , getInfo):
    for info in getInfo:
        if is_valid_email(username):
            if username == info["email"] and password == cipher_suite.decrypt(info["hashed_password"]).decode():
                return getResp(info)
        else:
            if username == info["username"] and password == cipher_suite.decrypt(info["hashed_password"]).decode():
                return getResp(info)

def getResp(info):
    resp = {}
    for subinfo in info:
        if subinfo == "hashed_password":
            resp[subinfo] = cipher_suite.decrypt(info[subinfo]).decode()
        else:
            resp[subinfo] = info[subinfo]
    return resp

def getusername(id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT username FROM users WHERE id = %s"
    args = (id)
    cursor.execute(query, args)
    username = cursor.fetchall()
    return username

#--------------------------------------------- UPDATE USER BY ID ---------------------------------------------------------
def update_user(id, data):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        request_data = json.loads(data)
        request_data = request_data[0]

        update_query = "UPDATE users SET"

        update_params = []

        # Check each field in the request data and add it to the SQL query if it's provided
        if 'username' in request_data and request_data['username'] is not None:
            update_query += " username = %s,"
            update_params.append(request_data['username'])
        if 'full_name' in request_data and request_data['full_name'] is not None:
            update_query += " full_name = %s,"
            update_params.append(request_data['full_name'])
        if 'email' in request_data and request_data['email'] is not None:
            update_query += " email = %s,"
            update_params.append(request_data['email'])
        if 'hashed_password' in request_data and request_data['hashed_password'] is not None:
            update_query += " hashed_password = %s,"
            update_params.append(cipher_suite.encrypt(request_data['hashed_password'].encode()))

        if 'username' in request_data:
            updated_user = request_data['username']
        else:
            updated_user = getusername(id)[0]['username']

        update_query += " updated_at = %s, updated_by = %s"
        update_params.extend([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), updated_user])

        update_query = update_query.rstrip(",") + " WHERE id = %s;"
        update_params.append(id)

        cursor.execute(update_query, update_params)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"status": 200, "data" : { "message": "User updated successfully", "user_id": id } }

    except Exception as e:
        return {"status": 500, "data": e}


#--------------------------------------------- DELETE USER BY ID ---------------------------------------------------------
def delete_user(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "UPDATE `users` SET `status` = %s WHERE `users`.`id` = %s;"
        args = ["1",id]
        cursor.execute(query, args)
        conn.commit()

        # Check if any rows were affected
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"status": 200, "data": {"message": "User deleted successfully", "user_id": id}}

    except Exception as e:
        return {"status": 500, "data" : e}

