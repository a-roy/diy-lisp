# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

math_operators = ['+', '-', '/', '*', 'mod', '>']

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_boolean(ast) or is_integer(ast) or is_symbol(ast):
        return ast
    elif ast[0] == 'quote':
        return ast[1]
    elif ast[0] == 'atom':
        return is_atom(evaluate(ast[1], env))
    elif ast[0] == 'eq':
        args = [evaluate(x, env) for x in ast[1:]]
        return is_atom(args[0]) and evaluate(args[0], env) == evaluate(args[1], env)
    elif ast[0] in math_operators:
        args = [evaluate(x, env) for x in ast[1:]]
        if not (is_integer(args[0]) and is_integer(args[1])):
            raise LispError('Arguments must be integers.')

        if ast[0] == '+':
            return args[0] + args[1]
        elif ast[0] == '-':
            return args[0] - args[1]
        elif ast[0] == '/':
            return args[0] // args[1]
        elif ast[0] == '*':
            return args[0] * args[1]
        elif ast[0] == 'mod':
            return args[0] % args[1]
        elif ast[0] == '>':
            return args[0] > args[1]
    else:
        raise LispError('Symbol Unknown: %s' % ast[0])
