import re 
  
# Function to match the string 
def match(text): 
          
        # regex 
        pattern = '^[a-zA-Z]'
          
        # searching pattern 
        if re.match(pattern, text): 
                return('Yes') 
        else: 
                return('No') 
  
# Driver Function 
print(match("Geeks")) 
print(match("geeksforGeeks")) 
print(match("geeks")) 