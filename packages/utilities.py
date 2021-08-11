funciones = {"sin": "np.sin", "cos": "np.cos", "tan": "np.tan", "log": "np.log",
             "pi": "np.pi", "sqrt": "np.sqrt", "exp": "np.exp","^":"**"}

def reemplazo(s):
    for i in funciones:
        if i in s:
            s = s.replace(i, funciones[i])
    return s