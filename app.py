from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
db = SQLAlchemy(app)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String, nullable=False)

class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

def create_rule(rule_string):
    # Parse rule_string into an AST (Abstract Syntax Tree)
    tokens = re.split(r'(\s+AND\s+|\s+OR\s+)', rule_string)  # Split by AND/OR
    root = Node(type="combined")
    current_node = root

    for token in tokens:
        token = token.strip()
        if token in ['AND', 'OR']:
            new_node = Node(type=token)
            current_node.right = new_node
            current_node = new_node
        else:
            current_node.left = Node(type="expression", value=token)

    return root

def evaluate_rule(node, data):
    """Recursively evaluate the AST against the provided data."""
    if node.type == "expression":
        # Assume the expression is in the form "attribute > value" or "attribute = value"
        if ">" in node.value:
            attribute, value = node.value.split(">")
            return data.get(attribute.strip(), 0) > int(value.strip())
        elif "=" in node.value:
            attribute, value = node.value.split("=")
            return data.get(attribute.strip(), None) == value.strip().strip("'")  # Removing quotes
        # Add more conditions as needed for <, >=, <= etc.

    # Recursively evaluate left and right nodes
    left_result = evaluate_rule(node.left, data) if node.left else True
    right_result = evaluate_rule(node.right, data) if node.right else True

    if node.type == 'AND':
        return left_result and right_result
    elif node.type == 'OR':
        return left_result or right_result

    return False  # Default case

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    data = request.get_json()
    rule_string = data.get('rule_string')

    if not rule_string:
        return jsonify({"error": "Missing rule_string"}), 400

    # Create AST
    ast = create_rule(rule_string)
    # Save rule to database
    new_rule = Rule(rule_string=rule_string)
    db.session.add(new_rule)
    db.session.commit()

    return jsonify(ast.to_dict()), 200

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    data = request.get_json()
    rules = data.get('rules', [])

    if not rules or len(rules) < 2:
        return jsonify({"error": "At least two rules required for combination"}), 400

    # Combine rules
    combined_rule_string = ' AND '.join(rules)  # Example: Combine rules with AND
    combined_ast = create_rule(combined_rule_string)
    return jsonify(combined_ast.to_dict()), 200

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.get_json()
    rule_id = data.get('rule_id')
    user_data = data.get('user_data')

    # Fetch the rule from the database
    rule = Rule.query.get(rule_id)
    if not rule:
        return jsonify({"error": "Rule not found"}), 404

    # Create AST from the rule
    ast = create_rule(rule.rule_string)

    # Evaluate the rule against user data
    result = evaluate_rule(ast, user_data)
    return jsonify({"result": result}), 200

# Create database tables within application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
