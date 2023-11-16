import clingo


class Context:
    def inc(self, x):
        return clingo.symbol.Number(x.number + 1)

    def seq(self, x, y):
        return [x, y]


def on_model(m):
    file = open("output.txt", "w")
    file.write(str(m))
    file.close()


def test():
    ctl = clingo.control.Control()

    inputfile = open("input.txt", "r")
    ctl.add("base", [], str(inputfile.read()))
    inputfile.close()

    ctl.ground([("base", [])], context=Context())

    return ctl.solve(on_model=on_model)


if __name__ == "__main__":
    print(test())
