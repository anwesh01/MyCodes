from getpass import getpass
from sqlite3 import Cursor
from mysql.connector import connect, Error
import random
class NorthwindDB:
    def __init__(self):
        try:
            self.connection = connect(host = 'localhost',
                                  user = 'root',
                                  password = '270191',
                                  database = 'northwind')
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)
    
    #Close connection to MySQL when exiting the program.
    def close_connection(self):
         if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
    
    # Insert new Customer
    def insert_customer(self, CustomerId,CompanyName,ContactName,ContactTitle,Address,City,Region,PostalCode,Country,Phone,Fax):
        
        CustomerId=CustomerId.upper()
        query = "insert into customers \
                 values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format( CustomerId,CompanyName,ContactName,
                                                                                        ContactTitle,Address,City,Region,
                                                                                        PostalCode,Country,Phone,Fax)
        self.cursor.execute(query)
        self.connection.commit()
        print("Customer saved to db")
    
    # Insert new Order
    def insert_order(self, ProductId, Quantity, Discount, CustomerId, EmployeeId, OrderDate,RequiredDate, ShippedDate, 
                    ShipVia,Freight,shipName,shipAddress,shipCity,shipRegion,shipPostalCode,shipCountry):
        
        CustomerId = CustomerId.upper()
        query = "SELECT CustomerID FROM customers"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        custId = False
        for r in records:
            if CustomerId == r[0]:
                custId = True
                break
        if custId == False:
            raise Exception("  Invalid Customer Id !")
        
        query = "SELECT EmployeeID FROM employees"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        emp = False
        for r in records:
            if EmployeeId == int(r[0]):
                emp =True
                break
        if emp == False:
            raise Exception("  Invalid Employee Id !")
        
        query = "SELECT ShipperID FROM shippers"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        shipper = False
        for r in records:
            if ShipVia == int(r[0]):
                shipper =True
                break
        if shipper == False:
            raise Exception("  Invalid Shipper Id in field shipVia !")
        
        query = "SELECT ProductId FROM products"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        prodId = False
        for r in records:
            if ProductId == int(r[0]):
                prodId =True
                break
        
        if prodId == False:
            raise Exception("  Invalid Product Id !")
        
        if emp == True and shipper == True and prodId == True and custId == True:
            query = "select UnitsInStock from  products where ProductId = {}".format(ProductId)
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            UnitsInStock = int(val[0])
            query = "select unitsonorder from products where productid = {}".format(ProductId)
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            UnitsonOrder = int(val[0])
            query="select max(orderid) from orders"
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            OrderId = int(val[0])
            OrderId += 1
        
            query = "select discontinued from products where productId = {}".format(ProductId)
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            discontinued = val[0]
  
            query = "select UnitPrice from products where productId = {}".format(ProductId)
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            UnitPrice = int(val[0])
            query = "select max(id) from order_details" 
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            id1 = int(val[0])
            id1 += 1

            if UnitsInStock > 0 and Quantity <= UnitsInStock and discontinued == 'n':
                
                if ShippedDate != '':
                    query = "insert into orders \
                values({},'{}',{},'{}','{}','{}',{},{},'{}','{}','{}','{}',{},'{}')".format( OrderId, CustomerId, EmployeeId,
                                                                                        OrderDate,RequiredDate, ShippedDate,
                                                                                        ShipVia,Freight,shipName,shipAddress,
                                                                                        shipCity,shipRegion,shipPostalCode,shipCountry)
                    self.cursor.execute(query)
                    self.connection.commit()
                
                else:
                    ShippedDate= "NULL"
                    query = "insert into orders values('%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s')"%( OrderId, 
                                                                                                                            CustomerId, EmployeeId,
                                                                                                                            OrderDate,RequiredDate, 
                                                                                                                            ShippedDate,ShipVia,Freight,
                                                                                                                            shipName,shipAddress, 
                                                                                                                            shipCity,shipRegion,
                                                                                                                            shipPostalCode,
                                                                                                                            shipCountry)
                    self.cursor.execute(query)
                    self.connection.commit()
                
            
                query = "insert into order_details values({},{},{},{},{},{})".format(id1,OrderId,
                                                                                ProductId,UnitPrice,Quantity,Discount)
                self.cursor.execute(query)
                self.connection.commit()
            
                query = "UPDATE products SET unitsinstock = {} WHERE productid = {}".format(UnitsInStock - Quantity, ProductId)
                self.cursor.execute(query)
                self.connection.commit()
                query = "UPDATE products SET unitsonorder = {} WHERE productid = {}".format(UnitsonOrder + Quantity, ProductId)
                self.cursor.execute(query)
                self.connection.commit()
                print()
                print("  Order  with Order Id = ", OrderId,"saved to db !")
                print()
            else:
                raise Exception("  Cannot place the Order, try again !")

    #Fech Pending Order Details
    def fetch_order(self):
        query = "SELECT CustomerId, CompanyName, ContactName, ContactTitle, address, city, country, OrderId, OrderDate, ShippedDate, \
        ShipName,ShipAddress,ShipCity,ShipCountry FROM customers NATURAL JOIN orders WHERE ShippedDate IS NULL ORDER BY OrderDate ASC"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        for row in records:
            print("Customer Id : ", row[0])
            print("Company Name :", row[1])
            print("Contact Name : ", row[2])
            print("Contact Title : ", row[3])
            print("Address : ", row[4])
            print("City : ", row[5])
            print("Country : ", row[6])
            print("Order Id : ", row[7])
            print("Order Date :", row[8])
            print("Shipping Date :", row[9])
            print("Ship Name : ", row[10])
            print("Ship Address : ", row[11])
            print("Ship City : ", row[12])
            print("Ship Country : ", row[13])
            print()
            print()

    #delete Order
    def delete_Order(self, OrderId):
        query = "SELECT OrderId FROM orders"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        val = False
        for r in records:
            if OrderId == int(r[0]):
                val =True
                break
        if val == False:
            raise Exception("  Invalid Order Id !")
        else:
            query = "select Id from order_details where OrderId = {}".format(OrderId)
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            Id = int(val[0])
            query = "select ProductId from order_details where OrderId = {}".format(OrderId)
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            ProductId = int(val[0])
            query = "select Quantity from order_details where OrderId = {}".format(OrderId)
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            Quantity = int(val[0])
            try:
                query = "delete from order_details where Id = {}".format(Id)
                self.cursor.execute(query)
                self.connection.commit()
                query = "delete from orders where OrderId = {}".format(OrderId)
                self.cursor.execute(query)
                self.connection.commit()
                query = "select UnitsInStock from products where ProductId = {}".format(ProductId)
                self.cursor.execute(query)
                val = self.cursor.fetchone()
                UnitsInStock = int(val[0])
                query = "select UnitsOnOrder from products where ProductId = {}".format(ProductId)
                self.cursor.execute(query)
                val = self.cursor.fetchone()
                UnitsOnOrder  = int(val[0])
                query = "update products set UnitsInStock = {}, UnitsOnOrder = {} where ProductId = {}".format(UnitsInStock + Quantity,
                                                                                                        UnitsOnOrder - Quantity, ProductId)
                self.cursor.execute(query)
                self.connection.commit()
                print()
                print("  Order deleted !")
                print()
            except:
                raise Exception("  Cannot delete the order !")

    def restock_parts(self, ProductId, Quantity):
        query = "SELECT ProductId FROM products"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        val = False
        for r in records:
            if ProductId == int(r[0]):
                val = True
                break
        if val == False:
            raise Exception("  Invalid Product Id !")
        else:
            query = "select UnitsInStock from products where ProductId = {}".format(ProductId)
            self.cursor.execute(query)
            val = self.cursor.fetchone()
            UnitsInStock = int(val[0])
            query = "update products set UnitsInStock = {} where ProductId= {}".format(UnitsInStock + Quantity, ProductId)
            self.cursor.execute(query)
            self.connection.commit()
            print()
            print("  Stock Updated")
            print()
    
    def ship_order(self, OrderId):
        query = "SELECT OrderId FROM orders"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        val = False
        for r in records:
            if OrderId == int(r[0]):
                val =True
                break
        if val == False:
            raise Exception("  Invalid Order Id !")
        else:
            query = "UPDATE Orders SET ShippedDate = NOW() WHERE OrderID = {}".format(OrderId)
            self.cursor.execute(query)
            self.connection.commit()
            print()
            print("  Order Shipped !")
            print()
   

        


  


