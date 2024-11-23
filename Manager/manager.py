import Expert
import Querry
import Sales

class Manager:
    def __init__(self):
        self.products = []
        self.expert = Expert()
        self.querry = Querry()
        self.sales = Sales()

    def get_response(self, input):
        advice = self.expert.get_advice(input)   
        products, response = self.querry.get_response(advice) 
        if products != None:
            self.products = products  
        pitch = self.sales.get_pitch(response , self.products)
    
        return pitch, products

    def get_init_message(self):
        return "Hello! I am your personnal assistant for today. How can I help you ?"

    def display_employees(self):
        for employee in self._employees:
            print(employee)
    
    def get_products(self):
        return self.products