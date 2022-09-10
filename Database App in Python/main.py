from NorthwindDB import NorthwindDB


def main():
    db = NorthwindDB()
    while True:
        print()
        print("***********WELCOME********")
        print()
        print("  PRESS 1 to add new Customer")
        print("  PRESS 2 to add an order")
        print("  PRESS 3 to remove an order")
        print("  PRESS 4 to ship an order")
        print("  PRESS 5 to display Pending Order Details")
        print("  PRESS 6 to restock parts")
        print("  PRESS 7 to exit program")
        print()
        try:
            choice = int(input())
            if (choice == 1):
                #Adding a customer - insert Customer details
                CustomerId = input("  Enter Customer id: ")
                CompanyName = input("  Enter Company name :")
                ContactName = input("  Enter Contact name :")
                ContactTitle = input("  Enter Contact title :")
                Address = input("  Enter Address: ")
                City = input("  Enter City: ")
                Region = input("  Enter  Region: ")
                PostalCode = input("  Enter Postal Code: ")
                Country = input("  Enter Country: ")
                Phone = input("  Enter Phone: ")
                Fax = input("  Enter Fax: ")
                db.insert_customer(CustomerId, CompanyName,ContactName,ContactTitle,Address,City,Region,PostalCode,Country,Phone,Fax)
            elif (choice == 2):
                # Adding an order- insert order details
                ProductId = int(input("  Enter Product id: "))
                Quantity = int(input("  Enter Quantity: "))
                Discount = float(input("  Enter percentage of discount to be given (Enter value between 0 to 100) "))
                CustomerId = input("  Enter Customer Id: ")
                EmployeeId = int(input("  Enter Employee Id: "))
                OrderDate= input("  Enter Order Date: ")
                RequiredDate= input("  Enter Required Date: ")
                ShippedDate= input("  Enter Shipping Date: ")
                ShipVia= int(input("  Enter Shipped Via: "))
                Freight = float(input("  Enter Freight Details :"))
                shipName = input("  Enter Ship name :")
                shipAddress = input("  Enter Ship Address :")
                shipCity = input("  Enter Ship City :")
                shipRegion = input("  Enter Ship Region :")
                shipPostalCode = int(input("  Enter Ship Postal Code :"))
                shipCountry = input("  Enter Ship Country :")
                # Checking if the Quantity is a positive integer not equal to 0.
                if Quantity <= 0:
                    print()
                    raise Exception("  Quantity Cannot be negative or 0")
                # Checking if the Discount is a valid number between 0 and 100.
                if Discount< 0 or Discount > 100:
                    print()
                    raise Exception("  Discount has to be between 0 and 100")
                else:
                    Discount = Discount * 0.01
                    db.insert_order(ProductId, Quantity, Discount, CustomerId, EmployeeId, OrderDate,RequiredDate, ShippedDate, ShipVia,Freight,shipName,shipAddress,shipCity,shipRegion,shipPostalCode,shipCountry)
            elif choice == 3:
                #remove an order
                OrderId = int(input("  Enter Order Id which you want to delete: "))
                db.delete_Order(OrderId)
            elif choice == 4:
                # Ship an Order
                OrderId = int(input("  Enter Order Id of the Pending Order which you want shipped:  "))
                db.ship_order(OrderId)
            elif choice == 5:
                #display pending Order details
                db.fetch_order()
            elif choice == 6:
                # Restock Parts
                ProductId = int(input("  Enter Product Id of the part you need to restock: "))
                Quantity = int(input("  Enter Quantity of stocks to be added: "))
                # Checking if the Quantity is a positive integer not equal to 0.
                if Quantity <= 0:
                    print()
                    raise Exception("  Quantity Cannot be negative or 0!")
                else:
                    db.restock_parts(ProductId, Quantity)
            elif choice == 7:
                db.close_connection()
                break
            else:
                print("  Invalid input ! Try again")
        except Exception as e:
            print(e)
            print("  Invalid Details ! Try again")


if __name__ == "__main__":
    main()
