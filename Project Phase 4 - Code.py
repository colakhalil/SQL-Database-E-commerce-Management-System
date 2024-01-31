from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
import json

PR = "Product Reviews"
SR = "Supplier Reviews"


def get_supplier_feedback_data_from_user(ID):
    feedback = {}
    feedback["user_id"] = ID
    feedback["supplier_rating"] = (input("Rate the supplier overall (1-5): "))
    feedback["supplier_comments"] = input("Any comments about the supplier: ")
    return feedback

def get_product_feedback_data_from_user(ID):
    feedback = {}
    feedback["user_id"] =ID
    feedback["product_rating"] = (input("Rate the product (1-5): "))
    feedback["product_comments"] = input("Any comments about the product: ")
    return feedback

def connectDB():
    # Replace the connection string with your MongoDB connection string
    # You can obtain the connection string from your MongoDB Atlas dashboard or configure it locally
    # For example, if your database is running on localhost, the connection string might look like this:
    # "mongodb://localhost:27017/"

    connection_string = "mongodb+srv://idilguler:ardaakkan2002@cluster0.lywxfhi.mongodb.net/"
    client = MongoClient(connection_string)

    # Access a specific database (replace "your_database_name" with your actual database name)
    db = client.cluster0
    print("Connection established to your db")
    return db
    # Close the connection when you're done
    # client.close()


def option1(db):
    print("1- " + PR)
    print("2- " + SR)
    choice = input("Enter the option you want to create: ")
    collection_name = PR
    if (choice == "2"):
        collection_name = SR
    createCollection(db, collection_name)


def createCollection(db, collection_name):
    try:
        # If the collection doesn't exist, create it
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        elif collection_name in db.list_collection_names():
            print("Collection already exists")
    except Exception as e:
        print("An error occured: ", e)

def option2(db):
    print("1- " + PR)
    print("2- " + SR)
    choice = input("Enter the option you want read: ")
    collection_name = PR
    if (choice == "2"):
        collection_name = SR
    read_all_data(db, collection_name)


def read_all_data(db, collection_name):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Use the find method to retrieve all documents
        result = collection.find()

        # Iterate through the documents and print them
        for document in result:
            print(document)

    except Exception as e:
        print(f"An error occurred: {e}")

def option3(db):
    print("1- " + PR)
    print("2- " + SR)
    choice = input("Enter the option you want read: ")
    collection_name = PR
    if (choice == "2"):
        collection_name = SR
    filter_id = input("Please enter the id of the user that you want to see his/her reviews on " + collection_name + ": ")
    print_records_by_id(db,collection_name , filter_id)

def print_records_by_id(db, collection_name, id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Find all documents with matching customer_id
        result = collection.find({"user_id": id})

        # Print matching documents
        for document in result:
            print(document)

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")

def option4(db,id):
    print("1- " + PR)
    print("2- " + SR)
    choice = input("Enter the option you want to insert into: ")
    if (choice == "1"):
        collection_name = PR
        feedback = get_product_feedback_data_from_user(id)
        insert_into_collection(db,collection_name, feedback)
    elif(choice =="2"):
        collection_name = SR
        feedback = get_supplier_feedback_data_from_user(id)
        insert_into_collection(db,collection_name, feedback)


def insert_into_collection(db, collection_name, data):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Insert the data into the collection
        result = collection.insert_one(data)

        # Print the inserted document ID
        print("Insertion successfully completed")
        print(f"Inserted document ID: {result.inserted_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

def option5(db):
    print("1- " + PR)
    print("2- " + SR)
    choice = input("Enter the option you want delete from: ")
    collection_name = PR
    if (choice == "2"):
        collection_name = SR
    deleted_id = input("PLease enter the id of the user that you want to delete his/her review from "+collection_name +": ")
    delete_record_by_customer_id(db, collection_name, deleted_id)

def delete_record_by_customer_id(db, collection_name, user_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Find the first document where 'customer_id' matches the given ID
        record_to_delete = collection.find_one({"user_id": user_id})

        # If a document is found, delete it
        if record_to_delete:
            result = collection.delete_one({"_id": record_to_delete["_id"]})
            if result.deleted_count == 1:
                print(f"Successfully deleted record with user ID {user_id}")
            else:
                print(f"No record found with user ID {user_id}")
        else:
            print(f"No record found with user ID {user_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")

def option6(db):
    print("1- " + PR)
    print("2- " + SR)
    choice = input("Enter the option you want to update : ")
    collection_name = PR
    if (choice == "1"):
        collection_name = PR
        choice2= input("Enter 1 to update product rating or enter 2 to update product comment: ")
        updated_id = input("PLease enter the id of the user that you want to update his/her review "+collection_name +": ")
        updated_column = "product_rating"
        if(choice2 =="2"):
            updated_column = "product_comments"
        update_record(db,collection_name , updated_column ,updated_id )
    elif(choice=="2"):
        collection_name = SR
        choice2= input("Enter 1 to update supplier rating or enter 2 to update supplier comment: ")
        updated_id = input("Please enter the id of the user that you want to update his/her review "+collection_name +": ")
        updated_column = "supplier_rating"
        if(choice2 =="2"):
            updated_column = "supplier_comments"
        update_record(db,collection_name , updated_column ,updated_id )

def update_record(db, collection_name, what_to_update, id ):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Ask the user to enter the new updated version
        updated_value = input(f"Enter the new updated {what_to_update}: ")

        # Get the specific element to update
        record_to_update = collection.find_one({"user_id": id, what_to_update: {"$exists": True}})

        # If the element exists, update it
        if record_to_update:
            result = collection.update_one(
                {"_id": record_to_update["_id"]},
                {"$set": {what_to_update: updated_value}}
            )
            if result.modified_count == 1:
                print(f"Successfully updated {what_to_update} to {updated_value}")
            else:
                print(f"No record found to update {what_to_update}")
        else:
            print(f"No record found to update {what_to_update} for customer ID {id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")
    
def main_menu(db):
    user_id = input("Welcome to Review Portal!\nPlease enter your user id: ")
    print("Please pick the option that you want to proceed.")
    while True:

        print("1- Create a collection.")
        print("2- Read all data in a collection.")
        print("3- Read some part of the data while filtering.")
        print("4- Insert data.")
        print("5- Delete data.")
        print("6- Update data.")
        print("0- Exit.")
        choice = input("Selected option: ")

        if choice == "1":
            option1(db)
        elif choice == "2":
            option2(db)
        elif choice == "3":
            option3(db)
        elif choice == "4":       
            option4(db,user_id)
        elif choice == "5":      
            option5(db)
        elif choice == "6":       
            option6(db)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")
        # This prompt ensures the user decides to continue or exit
        print("\nWhat would you like to do next?")


if __name__ == "__main__":
    db = connectDB()
    if db is not None:
        main_menu(db)