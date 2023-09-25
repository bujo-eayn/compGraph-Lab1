import re
import os
import pandas as pd
import logging

# Initialize the logging configuration
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "log_output.txt")

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Define a function to generate email addresses
def generate_email(name):
    # Remove special characters from the name
    clean_name = re.sub(r'[^A-Za-z\s]', '', name)

    # Split the name into parts
    name_parts = clean_name.split()

    # Generate the email address
    if len(name_parts) >= 2:
        first_name = name_parts[0]
        last_name = name_parts[-1]
        email = f"{first_name[0].lower()}{last_name.lower()}@gmail.com"
    else:
        email = f"{clean_name.lower()}@gmail.com"

    return email

# Define the path to the original Excel file
original_file_path = "test_file_3b.xlsx"

# Load the original Excel file
data = pd.read_excel(original_file_path)

# Populate the "Email Address" column with generated email addresses
data["Email Address"] = data["Student Name"].apply(generate_email)

# Define the output directory
output_dir = "output"

# Ensure the output directory exists, create it if it doesn't
os.makedirs(output_dir, exist_ok=True)

# Extract the original file name without extension
file_name_without_extension = os.path.splitext(os.path.basename(original_file_path))[0]

# Initialize a counter for appending numbers to the filename
file_counter = 1

# Generate the initial output file path
output_file_path = os.path.join(output_dir, f"output_{file_name_without_extension}.xlsx")

# Check if the file already exists, and if so, append a number to the filename until it's unique
while os.path.exists(output_file_path):
    output_file_path = os.path.join(
        output_dir, f"output_{file_name_without_extension}_{file_counter}.xlsx"
    )
    file_counter += 1

# Save the modified data frame to the unique output file
data.to_excel(output_file_path, index=False)

# Separate Male and Female students
male_students = data[data['Gender'] == 'M']
female_students = data[data['Gender'] == 'F']

# Define the output file paths for male and female students
output_male_path = os.path.join(output_dir, f"output_{file_name_without_extension}_male.xlsx")
output_female_path = os.path.join(output_dir, f"output_{file_name_without_extension}_female.xlsx")

# Save male and female students to separate output files
male_students.to_excel(output_male_path, index=False)
female_students.to_excel(output_female_path, index=False)

# Shuffle the DataFrame Victor
shuffled_data = data.sample(frac=1).reset_index(drop=True)

# Define the output JSON file path
output_json_file = "shuffled_student_data.json"

# Save the shuffled data to a JSON file
shuffled_data.to_json(output_json_file, orient="records", lines=True)

# Log the number of male and female students
num_male_students = len(male_students)
num_female_students = len(female_students)

# List the names of students with special characters
def has_special_characters(name):
    pattern = r"[!@#$%^&*().?\":{}|<>']"
    return bool(re.search(pattern, name))

names_with_special_characters = data[data['Student Name'].apply(has_special_characters)]['Student Name'].tolist()

# Log the information to the log file
logging.info(f"Number of Male Students: {num_male_students}")
logging.info(f"Number of Female Students: {num_female_students}")
logging.info("Names with Special Characters:")
for name in names_with_special_characters:
    logging.info(name)

print(f"Modified data saved to {output_file_path}")
print(f"Male students saved to {output_male_path}")
print(f"Female students saved to {output_female_path}")
print(f"Log file saved to {log_file_path}")

