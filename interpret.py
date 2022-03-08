import parser as ps

def interpret(string: str):
    eval_tree(ps.tree(string))

def eval_tree(node: ps.Node) -> int | None:
    match node:
        case ps.ProgramNode(left, right):
            eval_tree(left)
            if node is not None:
                eval_tree(right)
        case ps.ValueNode(value=value):
            return value
        case ps.OperatorNode(func=func, arguments=args):
            return func(*map(eval_tree, args))
        case ps.IdentNode(name):
            return ps.symbol_table.get(name, None)
