from dbuilder import Engine


def compile(contract, print_=True):
    t = Engine.patched(contract)
    compiled = Engine.compile(t)
    code = compiled.to_func()
    if print_:
        print(code)
    return code
