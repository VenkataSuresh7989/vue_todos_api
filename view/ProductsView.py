from datetime import datetime
from http.client import HTTPException
from config.database import connect_db

#--------------------------------------------- GET PRODUCTs  -----------------------------------------------------------
def getallproducts():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT id, name, created_at, created_by, updated_at, updated_by FROM products WHERE status <> '1'"
        cursor.execute(query)
        rows = cursor.fetchall()

        return {"status": 200, "data": rows}
    except Exception as e:
        print(e)
        return {"status": 403, "data": e}

#--------------------------------------------- CREATE PRODUCT ----------------------------------------------------------
def create_product(name):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # INSERT INTO `products`(`id`, `name`, `created_at`, `created_by`, `updated_at`, `updated_by`, `status`)
        # VALUES(NULL, 'iPhone', '2023-08-26 21:42:15', 'admin', '', '', '1');

        sql = "INSERT INTO `products`(`id`, `name`, `created_at`, `created_by`, `updated_at`, `updated_by`, `status`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        args = ("NULL", name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'admin', '', '', '0')

        cursor.execute(sql, args)
        conn.commit()

        return {"status": 200, "data": "New Product added Successfully."}

    except Exception as e:
        return {"status": 500, "data": e}

#--------------------------------------------- UPDATE PRODUCT BY ID ----------------------------------------------------
def update_product(id, name):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql = "UPDATE products SET `name` = %s, `updated_at` = %s, `updated_by` = %s WHERE `id` = %s"
        args = (name,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'admin',id)

        cursor.execute(sql, args)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"status": 200, "data": {"message": "Product updated successfully."}}

    except Exception as e:
        return {"status": 500, "data": e}

#--------------------------------------------- DELETE PRODUCT BY ID ----------------------------------------------------
def delete_product(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "UPDATE `products` SET `status` = %s WHERE `products`.`id` = %s;"
        args = ["1", id]
        cursor.execute(query, args)
        conn.commit()

        # Check if any rows were affected
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found.")

        return {"status": 200, "data": {"message": "Product deleted successfully." }}

    except Exception as e:
        return {"status": 500, "data": e}