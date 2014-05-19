# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse
import operator

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

math_operators = {
        '+' : operator.add,
        '-' : operator.sub,
        '/' : operator.floordiv,
        '*' : operator.mul,
        'mod' : operator.mod,
        '>' : operator.gt}

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_boolean(ast) or is_integer(ast):
        return ast
    elif is_symbol(ast):
        return env.lookup(ast)

    if not is_atom(ast[0]):
        ast[0] = evaluate(ast[0], env)
    elif ast[0] == 'quote':
        return ast[1]
    elif ast[0] == 'atom':
        return is_atom(evaluate(ast[1], env))
    elif ast[0] == 'eq':
        args = [evaluate(x, env) for x in ast[1:]]
        return is_atom(args[0]) and args[0] == args[1]
    elif is_symbol(ast[0]) and ast[0] in math_operators:
        args = [evaluate(x, env) for x in ast[1:]]
        if not (is_integer(args[0]) and is_integer(args[1])):
            raise LispError('Arguments must be integers.')
        return math_operators[ast[0]](args[0], args[1])
    elif ast[0] == 'if':
        if (evaluate(ast[1], env)):
            return evaluate(ast[2], env)
        else:
            return evaluate(ast[3], env)
    elif ast[0] == 'define':
        if len(ast) != 3:
            raise LispError('Wrong number of arguments')
        if not is_symbol(ast[1]):
            raise LispError('non-symbol: %s' % unparse(ast[1]))
        env.set(ast[1], evaluate(ast[2], env))
        return ""
    elif ast[0] == 'lambda':
        if len(ast) != 3:
            raise LispError('Wrong number of arguments')
        if not is_list(ast[1]):
            raise LispError('Expected list: %s' % ast[1])
        return Closure(env, ast[1], ast[2])

    if is_symbol(ast[0]):
        ast[0] = env.lookup(ast[0])
    if is_closure(ast[0]):
        args = [evaluate(x, env) for x in ast[1:]]
        num_args = len(args)
        num_params = len(ast[0].params)
        if num_args != num_params:
            raise LispError('wrong number of arguments, expected %d got %d'
                    % (num_params, num_args))
        bindings = dict(zip(ast[0].params, args))
        return evaluate(ast[0].body, ast[0].env.extend(bindings))

    raise LispError('not a function: %s' % unparse(ast[0]))
