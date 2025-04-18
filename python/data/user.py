class UserPreview:
    def __init__(self, name, age, address, zip, city, birthday, lived_here, gender, id):
        self.name = name
        self.age = age
        self.address = address
        self.zip = zip
        self.city = city
        self.birthday = birthday
        self.lived_here = lived_here
        self.gender = gender
        self.id = id

class User:
    def __init__(self, user: UserPreview, pid, phone_numbers, vehicles, companies):
        self.name = user.name
        self.age = user.age
        self.address = user.address
        self.zip = user.zip
        self.city = user.city
        self.birthday = user.birthday
        self.lived_here = user.lived_here
        self.id = user.id

        self.pid = pid
        self.phone_numbers = phone_numbers
        self.vehicles  = vehicles
        self.companies = companies