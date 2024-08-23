import re
def mixed_to_spoken(input_string):  
    # Define a mapping of digits to words  
    digit_to_word = {  
        '0': 'zero',  
        '1': 'one',  
        '2': 'two',  
        '3': 'three',  
        '4': 'four',  
        '5': 'five',  
        '6': 'six',  
        '7': 'seven',  
        '8': 'eight',  
        '9': 'nine'  
    }  
  
    # Function to convert a numeric string into its spoken equivalent  
    def number_to_spoken(number_string):  
        if number_string == '1000':  
            return 'thousand'  
        # Patterns for "thousand", "hundred", etc.  
        number_patterns = {  
            '000': 'thousand',  
        }  
        # Check for patterns  
        for pattern, word in number_patterns.items():  
            if number_string.endswith(pattern):  
                num_len = len(number_string)  
                if num_len > len(pattern):  
                    prefix = number_string[:-len(pattern)]  
                    prefix_spoken = ' '.join(digit_to_word[digit] for digit in prefix)  
                    return f"{prefix_spoken} {word}"  
                else:  
                    return word  
        # If no pattern, spell out each digit  
        return ' '.join(digit_to_word[digit] for digit in number_string)  
  
    # Process each part of the input string  
    parts = input_string.split()  
    spoken_parts = []  
    for part in parts:  
        if part.isdigit():  
            spoken_parts.append(number_to_spoken(part))  
        elif part.isalpha():  
            spoken_parts.append(part)  # Alphabetic parts remain unchanged  
        else:  
            # Handle parts that are a mix of digits and letters  
            # This can be more complex if you need to handle cases like "A10" or "B52"  
            spoken_parts.append(part)  
      
    # Join the processed parts into a single string  
    spoken_form = ' '.join(spoken_parts)  
    return spoken_form

def separate_alphanumeric(text):  
    # Regular expression pattern to match alphanumeric strings  
    pattern = re.compile(r'([a-zA-Z]+)(\d+)')  
      
    # Substitute the matched patterns with separated text  
    separated_text = pattern.sub(r'\1 \2', text)  
      
    return separated_text  
  
  
# Example usage:  
# print(mixed_to_spoken("gamma 5 heading 8000"))  
# print(mixed_to_spoken("gamma 515 heading 8000"))  

# Outputs: gamma five heading eight thousand  
