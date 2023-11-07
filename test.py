import clingo


class Context:
    def inc(self, x):
        return clingo.symbol.Number(x.number + 1)

    def seq(self, x, y):
        return [x, y]


def on_model(m):
    file = open("tmp.txt", "w")
    file.write(str(m))
    file.close()


def test(to_solve):
    ctl = clingo.control.Control()
    ctl.add("base", [], str(to_solve))
    ctl.ground([("base", [])], context=Context())
    return ctl.solve(on_model=on_model)


if __name__ == "__main__":
    print(test())
