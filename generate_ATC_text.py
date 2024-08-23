import os
import itertools

# Create a folder to store the generated txt files
folder_name = "ATC_text_dataset"
os.makedirs(folder_name, exist_ok=True)

one_term_path = os.path.join(folder_name, "one_term_action")
os.makedirs(one_term_path, exist_ok=True)

two_term_path = os.path.join(folder_name, "two_term_action")
os.makedirs(two_term_path, exist_ok=True)

three_term_path = os.path.join(folder_name, "three_term_action")
os.makedirs(three_term_path, exist_ok=True)


# Simulate different AI machine call signs, formatted as "Group Name + Number"
numbers = ['one', 'two', 'tree', 'four', 'five', 'six', 'seven', 'eight', 'niner']
ai_machines = [f"{group} {number}" for group in ['Alpha', 'Bravo', 'Delta', 'Gamma'] for number in numbers]


# Single-term actions that will not combine with numbers or AI machines
one_term_actions = [
    "Scramble", "Holding Hands", "Flow Four", "Engaged", 
    "Mission Complete", "Initial Five", "Gear Check, Full Stop"
]

# Actions that will combine with AI machine names, but not with numbers
two_term_actions = ["Go Cover", "IN", "OFF", "Cleared to Land"]

# Actions that will combine with both AI machine names and numbers
three_term_actions = ["Angle", "Heading"]

# Angle number range: 3000 ~ 9000 & 100 ~ 360
angle_numbers = ["3000", "4000", "5000", "6000", "7000", "8000", "9000"] + \
                [str(i).zfill(3) for i in range(100, 361, 10)]

# Heading number range: 010 ~ 360
heading_numbers = [str(i).zfill(3) for i in range(10, 361, 10)]

# Function to create and write to a txt file
def save_to_txt(folder_name, filename, content):
    txt_filename = os.path.join(folder_name, filename + '.txt')
    with open(txt_filename, 'w') as file:
        file.write(content)

# 1. Generate one-term actions and save to txt files
for action in one_term_actions:
    filename = f"{action.replace(' ', '_')}".lower()
    text_content = f"{action}".lower()
    save_to_txt(one_term_path, filename, text_content)

# 2. Generate two-term actions combined with AI machines and save to txt files
for action, ai_machine in itertools.product(two_term_actions, ai_machines):
    filename = f"{ai_machine.replace(' ', '_')}_{action.replace(' ', '_')}".lower()
    text_content = f"{ai_machine} {action}".lower()
    save_to_txt(two_term_path, filename, text_content)

# 3. Generate three-term actions combined with AI machines and number ranges and save to txt files
for action in three_term_actions:
    for ai_machine in ai_machines:
        if action == "Heading":
            # Generate Heading combinations
            for heading in heading_numbers:
                filename = f"{ai_machine.replace(' ', '_')}_{action}_{heading}".lower()
                text_content = f"{ai_machine} - {action} - {heading}".lower()
                save_to_txt(three_term_path, filename, text_content)
        elif action == "Angle":
            # Generate Angle combinations
            for angle in angle_numbers:
                filename = f"{ai_machine.replace(' ', '_')}_{action}_{angle}".lower()
                text_content = f"{ai_machine} {action} {angle}".lower()
                save_to_txt(three_term_path, filename, text_content)
