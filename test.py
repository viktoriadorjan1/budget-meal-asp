import clingo


class Context:
    def inc(self, x):
        return clingo.symbol.Number(x.number + 1)

    def seq(self, x, y):
        return [x, y]


def on_model(m):
    print(m)


ctl = clingo.control.Control()
ctl.add("base", [], """
p(@inc(10)).
q(@seq(1,2)).
""")
ctl.ground([("base", [])], context=Context())
print(ctl.solve(on_model=on_model))
