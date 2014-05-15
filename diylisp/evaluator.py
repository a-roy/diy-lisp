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

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_boolean(ast) or is_integer(ast) or is_symbol(ast):
        return ast
    elif ast[0] == 'quote':
        return ast[1]
    elif ast[0] == 'atom':
        return is_atom(evaluate(ast[1], env))
    elif ast[0] == 'eq':
        exprs = [evaluate(x, env) for x in ast[1:]]
        return is_atom(exprs[0]) and evaluate(exprs[0], env) == evaluate(exprs[1], env)
    else:
        if ast[0] == '+':
            return evaluate(ast[1], env) + evaluate(ast[2], env)
        elif ast[0] == '-':
            return evaluate(ast[1], env) - evaluate(ast[2], env)
        elif ast[0] == '/':
            return evaluate(ast[1], env) / evaluate(ast[2], env)
        elif ast[0] == '*':
            return evaluate(ast[1], env) * evaluate(ast[2], env)
        elif ast[0] == 'mod':
            return evaluate(ast[1], env) % evaluate(ast[2], env)
        elif ast[0] == '>':
            return evaluate(ast[1], env) > evaluate(ast[2], env)
        else:
            raise LispError('Symbol Unknown: %s' % ast[0])
