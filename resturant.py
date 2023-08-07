import json

class Snack:
    def __init__(self, snack_id, name, price, availability):
        self.snack_id = snack_id
        self.name = name
        self.price = price
        self.availability = availability

    def to_dict(self):
        return {
            "snack_id": self.snack_id,
            "name": self.name,
            "price": self.price,
            "availability": self.availability
        }

    @staticmethod
    def from_dict(data):
        return Snack(data["snack_id"], data["name"], data["price"], data["availability"])

    @staticmethod
    def save_to_file(snacks, filename):
        snack_list = [snack.to_dict() for snack in snacks]
        with open(filename, "w") as file:
            json.dump(snack_list, file, indent=4)

    @staticmethod
    def load_from_file(filename):
        snacks = []
        try:
            with open(filename, "r") as file:
                snack_list = json.load(file)
                for data in snack_list:
                    snacks.append(Snack.from_dict(data))
        except FileNotFoundError:
            pass
        return snacks




class SnackManager:
    def __init__(self):
        self.snacks = Snack.load_from_file("snacks.json")
    
    def display_menu(self):
        print("Canteen Snack Management System")
        print("1. Display Snacks")
        print("2. Add Snack")
        print("3. Remove Snack")
        print("4. Update Availability")
        print("5. Record Sale")
        print("6. Exit")
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.display_snacks()
            elif choice == "2":
                self.add_snack()
            elif choice == "3":
                self.remove_snack()
            elif choice == "4":
                self.update_availability()
            elif choice == "5":
                self.record_sale()
            elif choice == "6":
                self.exit_program()
                break
            else:
                print("Invalid choice. Please select a valid option.")
    
    def display_snacks(self):
        for snack in self.snacks:
            print(f"Snack ID: {snack.snack_id}")
            print(f"Name: {snack.name}")
            print(f"Price: {snack.price}")
            print(f"Availability: {'Available' if snack.availability else 'Not Available'}")
            print("--------------------")
    


    #add
    def add_snack(self):
        snack_id = int(input("Enter Snack Id: "))
        name = input("Enter Snack name: ")
        price = int(input("Enter Snack price: "))
        availability_input = input("Is the Snack Available? (yes/no): ").lower()

        if availability_input == "yes":
            availability = True
        else:
            availability = False

        new_snack = Snack(snack_id, name, price, availability)
        self.snacks.append(new_snack)
        Snack.save_to_file(self.snacks, "snacks.json")
        self.snacks = Snack.load_from_file("snacks.json")
        print(f"Snack '{name}' has been added to the inventory.")
    


    #remove
    def remove_snack(self):
        snack_id = int(input("Enter Snack ID to remove: "))
        snack_to_remove= None

        for el in self.snacks:
            if el.snack_id == snack_id:
                snack_to_remove= el
                break
        if snack_to_remove:
            self.snacks.remove(snack_to_remove)
            Snack.save_to_file(self.snacks, "snacks.json")
            self.snacks = Snack.load_from_file("snacks.json")
            print(f"Snack '{snack_to_remove.name}' has been removed from the inventory.")
        else:
            print("Snack not found with the provided ID.")
    
    
    
    #update
    def update_availability(self):
        snack_id = int(input("Enter Snack ID to update: "))
        snack_to_update=None

        for el in self.snacks:
            if el.snack_id == snack_id:
                snack_to_update = el
        
        if snack_to_update:
            new_availability_input = input("Is the Snack Available? (yes/no): ").lower()
            snack_to_update.availability = new_availability_input == "yes"
            print(f"Availability of snack '{snack_to_update.name}' has been updated.")
            Snack.save_to_file(self.snacks, "snacks.json")
            self.snacks = Snack.load_from_file("snacks.json")
        else:
            print("Snack with the given ID not found!")
    


    #record_sale
    def record_sale(self):
        snack_id = int(input("Enter Snack ID to record sale: "))
        snack_to_record = None

        for snack in self.snacks:
            if snack.snack_id == snack_id:
                snack_to_record = snack
                break
        
        if snack_to_record and snack_to_record.availability:
            snack_to_record.availability = not snack_to_record.availability
            print(f"{snack_to_record.snack_id} is sold! Total :- {snack_to_record.price} rs")
            Snack.save_to_file(self.snacks, "snacks.json")
            self.snacks = Snack.load_from_file("snacks.json")
        else:
            print("Snack with the given ID not found or the item is not available!")
    
    def exit_program(self):
        Snack.save_to_file(self.snacks, "snacks.json")
        print("Pleasure doing business. Have a Nice Day!")

manager = SnackManager()
manager.run()