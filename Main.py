from datetime import datetime
import pandas
from abc import ABC , abstractmethod
#import streamlit 


current_time = datetime.now().strftime('%A:%H:%M')

#reading csv files using pandas 
df = pandas.read_csv("hotels.csv", dtype={'id': str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pandas.read_csv("card_security.csv", dtype=str)



class Hotel:
    def __init__(self, hotel_id):
        #creating instance variables for the hotel class
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.city = df.loc[df["id"] == self.hotel_id, "city"].squeeze()
    
    
    def available(self):
        # check if hotel is available 
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False
    
    
    def book(self):
        #book a hotel by changing its availability to no
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)


class Ticket(ABC):
    
    @abstractmethod
    def generate(self):
        pass
    

class ReservationTicket(Ticket):
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object
        
    
    def generate(self):
        #A thank you message to the user after booking a room 
        content = f""" 
        Thank you for your Reservation!
        here is your booking data:
        Booked {current_time}
        Name: {self.the_customer_name}
        Hotel: {self.hotel.name}
        """
        return content
    
    
    @property
    def the_customer_name(self):
        name = self.customer_name.strip()
        name = name.title()
        return name
    
    class DigtialTicket(Ticket):
        def generate(self):
            content = f""" 
        Thank you for your Reservation!
        here is your booking data:
        Booked {current_time}
        Name: {self.the_customer_name}
        Hotel: {self.hotel.name}
        """
            return content
        
        
        def download(self):
            pass
            
    
class CreditCard:
    def __init__(self,number):
        self.number = number
        
    
    def validate(self , expiration, holder, cvc):
        #A way to check if the credit card provided is in our databasse of cards
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
    

class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
    
          
print(df)

hotel_id = input("Enter the id of the hotel:")
hotel = Hotel(hotel_id)


if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
        else:
            print("Card Authentication failed")
    else:
        print("There was a issue with your payment")
else:
    print("Hotel is currently not open")










