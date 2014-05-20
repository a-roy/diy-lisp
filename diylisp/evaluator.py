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

def check_args(ast, num):
    if len(ast) != num + 1:
        raise LispError('Wrong number of arguments')

def eval_math(ast, env):
    args = [evaluate(x, env) for x in ast[1:]]
    if not (is_integer(args[0]) and is_integer(args[1])):
        raise LispError('Arguments must be integers.')
    return math_operators[ast[0]](args[0], args[1])

def eval_quote(ast, env):
    check_args(ast, 1)
    return ast[1]

def eval_atom(ast, env):
    check_args(ast, 1)
    return is_atom(evaluate(ast[1], env))

def eval_eq(ast, env):
    check_args(ast, 2)
    args = [evaluate(x, env) for x in ast[1:]]
    return is_atom(args[0]) and args[0] == args[1]

def eval_if(ast, env):
    check_args(ast, 3)
    return evaluate(ast[2] if evaluate(ast[1], env) else ast[3], env)

def eval_define(ast, env):
    check_args(ast, 2)
    if not is_symbol(ast[1]):
        raise LispError('non-symbol: %s' % unparse(ast[1]))
    env.set(ast[1], evaluate(ast[2], env))
    return ""

def eval_lambda(ast, env):
    check_args(ast, 2)
    if not is_list(ast[1]):
        raise LispError('non-list: %s' % unparse(ast[1]))
    return Closure(env, ast[1], ast[2])

keywords = {
        'quote' : eval_quote,
        'atom' : eval_atom,
        'eq' : eval_eq,
        'if' : eval_if,
        'define' : eval_define,
        'lambda' : eval_lambda
        }

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_boolean(ast) or is_integer(ast):
        return ast
    elif is_symbol(ast):
        return env.lookup(ast)

    if not is_atom(ast[0]):
        ast[0] = evaluate(ast[0], env)
    elif is_symbol(ast[0]):
        if ast[0] in keywords:
            return keywords[ast[0]](ast, env)
        elif ast[0] in math_operators:
            return eval_math(ast, env)
        else:
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
