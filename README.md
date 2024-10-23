#  Rule Engine with AST

A simple 3-tier rule engine application with UI, API, and Backend that determines user eligibility based on attributes like age, department, salary, experience, etc. This system uses an Abstract Syntax Tree (AST) to dynamically create, combine, and modify conditional rules and evaluate them against user data.

### CONTENTS
-Overview
-System Architecture
-Features
-Project Setup
-How to Run
-API Endpoints
-Schema Design
-Testing
-Screenshots
-Artifacts to Submit
-Dependencies
-Design Decisions

# Overview
This project implements a rule engine that allows dynamic creation, combination, and evaluation of rules using an Abstract Syntax Tree (AST). The system can be used for tasks such as determining user eligibility based on predefined conditions such as age, department, income, experience, etc.

# System Architecture

The project follows a 3-tier architecture:
   1.UI Layer: Simple HTML/CSS for user interaction.
   2.API Layer: Flask-based API to create, combine, and evaluate rules.
   3.Data Layer: SQLite Database to store rules.

# Features
    1.Dynamic Rule Creation: Users can create rules dynamically via the UI or API.
    2.Rule Combination: Multiple rules can be combined using logical operators (AND, OR).
    3.Rule Evaluation: Evaluate if user data satisfies the defined rules.
    4.Error Handling: Handles invalid inputs and formats gracefully.
    5.AST Representation: Convert rule strings to an AST for better manipulation.

# Project Setup

#### Clone the Repository:

git clone https://github.com/atchukolanarendra/rule_engine.git
cd rule-engine-with-ast

##### Install Dependencies: 
Create a virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate  

#### Install required packages:
pip install -r requirements.txt

#### Database Initialization: Initialize the SQLite database:
python app.py

# How to Run
#### Run the Flask App:
   python app.py
This will start the server on http://127.0.0.1:5000/.

#### Access the Application: 
Open a browser and visit http://127.0.0.1:5000/ to interact with the UI for rule creation and evaluation.


#  API Endpoints
1. Create Rule:

-Endpoint: /create_rule
-Method: POST
-Payload:
json
{
  "rule_string": "age > 30 AND department = 'Sales'"
}

2. Combine Rules:

Endpoint: /combine_rules
Method: POST
Payload:
json
{
  "rules": ["age > 30 AND department = 'Sales'", "experience > 5"]
}
3. Evaluate Rule:

Endpoint: /evaluate_rule
Method: POST
Payload:
json

{
  "rule_id": 1,
  "user_data": {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
}

# Schema Design
-The system stores rules in an SQLite database. Below is the schema used:

## Rules Table:
  1.id: Integer (Primary Key)
  2.rule_string: String (The string representation of the rule)
  

| **id** | **rule_string**                              |
|--------|----------------------------------------------|
| 1      | age > 30 AND department = 'Sales'            |
| 2      | salary > 50000 AND experience > 5            |

# Testing
### Test case 1:
    Rule Creation: Ensure that a rule string is correctly converted into an AST.
###   Input String: (age>30 AND department = 'Sales')

![image1](https://github.com/user-attachments/assets/9f266421-6c2e-44e9-a9f5-420d7dfcecc3)

### Output for the testcase 1:

![image2](https://github.com/user-attachments/assets/81c9ed25-5bfc-42c5-88db-bbf8194bf0e9)
        The Output shows that, the rule is created, And represenations of string is presented at AST 

### Test case2:
     Rule Combination: Test combining two or more rules and ensure the AST is valid
####   Input String: (age >30 AND department = 'Sales') OR (salary > 20000 OR experience > 5) 
    
