from expert import Expert
from sales import Sales
from query import Query

class Manager:
    def __init__(self):
        self.products = []
        self.expert = Expert()
        self.query = Query()
        self.sales = Sales()

    def get_response(self, input):
        advice = self.expert.get_advice(input)

        print("advidccee" +advice)

        function_name, result = self.query.process_query(advice) 

        print("The called function is ", function_name)

        if function_name == "retrieve_best_products":
            self.products = result
        # Concatenate the advice and the result and in a dictionary (then string)
        # how to convert list in string
            string_result = ""
            for item in result:
                string_result += str(item) + "\n"
        else:
            string_result = str(result)

        response = {
            "advice": advice,
            "function": function_name,
            #convert result to a string
            "result": string_result
        }
        #convert response to string
        str_response = ""
        for key, value in response.items():
            str_response += f"{key}: {value}\n"
        pitch = self.sales.get_response(str_response)

        return pitch

    def get_init_message(self):
        return "Hello! I am your personnal assistant for today. How can I help you ?"

    def display_employees(self):
        for employee in self._employees:
            print(employee)
    
    def get_products(self):
        return self.products