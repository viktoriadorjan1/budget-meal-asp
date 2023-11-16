import clingo


class Context:
    def inc(self, x):
        return clingo.symbol.Number(x.number + 1)

    def seq(self, x, y):
        return [x, y]


def on_model(m):
    print(m)
    file = open("output.txt", "a")
    file.write(str(m) + "\n")
    file.close()


def solve(to_solve):
    ctl = clingo.control.Control()
    ctl.configuration.solve.models = 0

    ctl.add("base", [], to_solve)
    ctl.ground([("base", [])])

    return ctl.solve(on_model=on_model)


if __name__ == "__main__":
    print(solve(""))
