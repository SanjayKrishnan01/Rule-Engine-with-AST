import re
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right

def create_rule(rule_string):
    tokens = tokenize(rule_string)
    return parse_expression(tokens)

def tokenize(rule_string):
    return re.findall(r'\'[^\']*\'|\w+|>=|<=|>|<|=|\(|\)|AND|OR', rule_string)

def parse_expression(tokens):
    def parse_or():
        expr = parse_and()
        while tokens and tokens[0] == 'OR':
            tokens.pop(0)  # consume 'OR'
            right = parse_and()
            expr = Node("operator", 'OR', expr, right)
        return expr

    def parse_and():
        expr = parse_comparison()
        while tokens and tokens[0] == 'AND':
            tokens.pop(0)  # consume 'AND'
            right = parse_comparison()
            expr = Node("operator", 'AND', expr, right)
        return expr

    def parse_comparison():
        if tokens[0] == '(':
            tokens.pop(0)  # consume '('
            expr = parse_or()
            tokens.pop(0)  # consume ')'
            return expr
        left = Node("operand", tokens.pop(0))
        if tokens and tokens[0] in ['>', '<', '>=', '<=', '=']:
            op = tokens.pop(0)
            right = Node("operand", tokens.pop(0))
            return Node("operator", op, left, right)
        return left

    return parse_or()

def evaluate_rule(root, data):
    if isinstance(data, str):
        data = json.loads(data)
    
    logger.debug(f"Evaluating node: {root.type} - {root.value}")
    
    if root.type == "operand":
        if root.value in data:
            result = data[root.value]
        elif root.value.replace(".", "").isdigit():
            result = float(root.value)
        else:
            result = root.value.strip("'")
        logger.debug(f"Operand result: {result}")
        return result
    
    if root.type == "operator":
        left_value = evaluate_rule(root.left, data)
        right_value = evaluate_rule(root.right, data)
        
        logger.debug(f"Operator: {root.value}, Left: {left_value}, Right: {right_value}")
        
        if root.value == 'AND':
            result = left_value and right_value
        elif root.value == 'OR':
            result = left_value or right_value
        elif root.value == '>':
            result = float(left_value) > float(right_value)
        elif root.value == '<':
            result = float(left_value) < float(right_value)
        elif root.value == '>=':
            result = float(left_value) >= float(right_value)
        elif root.value == '<=':
            result = float(left_value) <= float(right_value)
        elif root.value == '=':
            result = str(left_value) == str(right_value)
        
        logger.debug(f"Operator result: {result}")
        return result
    
    raise ValueError("Invalid node type")