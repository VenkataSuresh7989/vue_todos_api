from view import ProductsView

#--------------------------------------------- GET PRODUCTs  -----------------------------------------------------------
def getallproducts():
    return ProductsView.getallproducts()

#--------------------------------------------- CREATE PRODUCT ----------------------------------------------------------
def create_product(name):
    return ProductsView.create_product(name)

#--------------------------------------------- UPDATE PRODUCT BY ID ----------------------------------------------------
def update_product(id,name):
    return ProductsView.update_product(id,name)

#--------------------------------------------- DELETE PRODUCT BY ID ----------------------------------------------------
def delete_product(id):
    return ProductsView.delete_product(id)