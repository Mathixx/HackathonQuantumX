from expert import Expert
from sales import Sales
from query import Query

class Manager:
    def __init__(self):
        self.products = []
        self.expert = Expert()
        self.query = Query()
        self.sales = Sales()
        self.last_pitch = ""
        self.last_advice = ""


    def get_response(self, input):
        advice = self.expert.get_advice(self.last_pitch, input)
        self.last_advice = advice
        print("advice : " +  advice) 
        function_name, result = self.query.process_query(advice) 


        if function_name == "retrieve_best_products":
            self.products = result

            string_result = ""
            for item in result:
                string_result += str(item) + "\n"
        else:
            string_result = str(result)


        response = {
            "input": input,
            "advice": advice,
            "function": function_name,
            #convert result to a string
            "result": string_result
        }
        #convert response to string
        str_response = ""
        for key, value in response.items():
            str_response += f"{key}: {value}\n"

        pitch = self.sales.get_response(self.last_advice, str_response)
        print("pitch : " + pitch)
        self.last_pitch = pitch

        return pitch

    def get_init_message(self):
        return "Hello! I am your personnal assistant for today. How can I help you ?"
    
    def get_products(self):
        return self.products