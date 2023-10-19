import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def Delete_Order(tid):

    url = f"https://localhost:3000/delete-order"

    data3 = {
        "tid":tid
    }

    response3 = requests.post(url,json=data3)
    if(response3.status_code==200):
          print("Transaction deleted successfully")
    else:
        print("error occured during deletion")


def Place_Order(tid,amount):

    while True:
        print("enter 1 to continue to the payment and any other number to cancel the payment")

        status = int(input())
        if(status!=1):
            Delete_Order(tid)
            break


        print("scan the card")
        reader = SimpleMFRC522()

        try:
            print("Hold a card near the reader")
            uid= str(reader.read())
            print("ID: {}".format(uid))

            while True:
               pid = input("enter your pin")
               if(len(pid)==4):
                   break
               else:
                   print("enter the full password")
               
            url2 = f"https://localhost:3000/place-order"

            data2 = {
            "tid":tid,
            "uid" : uid,
            "pid" :pid,
            "amount":amount
            }

            response2 = requests.post(url2,json=data2)

            if response2.status_code == 200:
                print("payment done successfully")
                print(response2.json())
                break

            else:
                print("retry or cancel the payment")
            
        finally:
            GPIO.cleanup()



def Create_Order():
        
        while True:
            storeId = int(input("Enter Store ID: "))
            amount = float(input("Enter Amount: "))
        

            url = f"https://localhost:3000/create-order"  

            data1= {
                "store-id": storeId,  
                "order":[],
                "amount": amount
                }

            response1= requests.post(url,json=data1)

            if response1.status_code == 200:
                print("Data sent successfully to the API.")
                t_id = response1.json()
                break
    
            else:
                print(f"Failed to send data. Status Code: {response1.status_code}")
                print("retry")
        Place_Order(t_id['tid'],amount)


Create_Order()

