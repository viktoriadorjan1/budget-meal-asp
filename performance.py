import time

from test import solve


def main():
    file = open("performance.txt", "a")
    test1(file)
    test2(file)
    test3(file)
    test4(file)
    test5(file)
    test6(file)
    test7(file)
    test8_2(file)
    test8_3(file)
    test8_4(file)
    test9(file)
    file.close()
    return

# no. relevant ingredients
def test1(file):
    AVG = 30
    for r in range(100):
        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test1:{r}:none {time_it_took}"
            #print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test1:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        '''
        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        avg = 0
        for i in range(3):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test1:{r}:frst {time_it_took}"
            print(res)
            avg += time_it_took
        avg = avg / 3
        res = f"test1:{r}:frst {avg}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        avg = 0
        for i in range(3):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test1:{r}:scnd {time_it_took}"
            print(res)
            avg += time_it_took
        avg = avg / 3
        res = f"test1:{r}:scnd {avg}"
        print(res)
        file.write(res + "\n")
        '''

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test1:{r}:both {time_it_took}"
            #print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test1:{r}:both {avg}"
        print(res)
        file.write(res + "\n")


# no. irrelevant recipes
def test2(file):
    AVG = 30
    for r in range(100):
        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=r, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test2:{r}:none {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test2:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=r, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test2:{r}:frst {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test2:{r}:frst {avg}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=r, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test2:{r}:scnd {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test2:{r}:scnd {avg}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=r, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test2:{r}:both {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test2:{r}:both {avg}"
        print(res)
        file.write(res + "\n")


# no. relevant recipes WITH same ingredient each
def test3(file):
    AVG = 30
    r = 1
    while r <= 100:
        to_solve = get_asp(days=2, meals=1, rel_recipes=r, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test3:{r}:none {time_it_took}"
            #print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test3:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        '''
        to_solve = get_asp(days=2, meals=1, rel_recipes=r, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test3:{r}:frst {end - start}"
        print(res)
        file.write(res + "\n")

        
        to_solve = get_asp(days=2, meals=1, rel_recipes=r, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test3:{r}:scnd {end - start}"
        print(res)
        file.write(res + "\n")
        '''

        to_solve = get_asp(days=2, meals=1, rel_recipes=r, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test3:{r}:both {time_it_took}"
            #print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test3:{r}:both {avg}"
        print(res)
        file.write(res + "\n")

        if r == 1:
            r = r + 9
        else:
            r = r + 10


# no. relevant recipes WITH unique ingredients
def test4(file):
    AVG = 30
    r = 1
    while r <= 100:
        to_solve = get_asp(days=2, meals=1, rel_recipes=r, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)

        # file.write(to_solve + "\n")

        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test4:{r}:none {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test4:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        '''
        to_solve = get_asp(days=2, meals=1, rel_recipes=r, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test4:{r}:frst {end - start}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=r, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test4:{r}:scnd {end - start}"
        print(res)
        file.write(res + "\n")
        '''

        to_solve = get_asp(days=2, meals=1, rel_recipes=r, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        # file.write(to_solve + "\n")

        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test4:{r}:both {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test4:{r}:both {avg}"
        print(res)
        file.write(res + "\n")

        if r == 1:
            r = r + 9
        else:
            r = r + 10


# no. days with one meal
def test5(file):
    AVG = 30
    r = 1
    while r <= 100:
        to_solve = get_asp(days=r, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test5:{r}:none {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test5:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        '''
        to_solve = get_asp(days=r, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test5:{r}:frst {end - start}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=r, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test5:{r}:scnd {end - start}"
        print(res)
        file.write(res + "\n")
        '''

        to_solve = get_asp(days=r, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test5:{r}:both {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test5:{r}:both {avg}"
        print(res)
        file.write(res + "\n")

        r = r+1
        #if r == 1:
        #    r = r + 9
        #else:
        #    r = r + 10


# no. relevant ingredients WITH one recipe ???
def test6(file):
    for r in range(100):
        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=False,
                           first_optim=False, second_optim=False)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test6:{r}:none {end - start}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=False,
                           first_optim=True, second_optim=False)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test6:{r}:frst {end - start}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=False,
                           first_optim=False, second_optim=True)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test6:{r}:scnd {end - start}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=r, unused_ingredients=0,
                           empty_pantry=False,
                           first_optim=True, second_optim=True)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test6:{r}:both {end - start}"
        print(res)
        file.write(res + "\n")


# no. unused pantry items ???
def test7(file):
    AVG = 30
    for r in range(100):
        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=r,
                           empty_pantry=False,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test7:{r}:none {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test7:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=r,
                           empty_pantry=False,
                           first_optim=True, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test7:{r}:frst {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test7:{r}:frst {avg}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=r,
                           empty_pantry=False,
                           first_optim=False, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test7:{r}:scnd {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test7:{r}:sncd {avg}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=r,
                           empty_pantry=False,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test7:{r}:both {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test7:{r}:both {avg}"
        print(res)
        file.write(res + "\n")


# no. days with 2 meals
def test8_2(file):
    AVG = 30
    r = 1
    while r <= 100:
        to_solve = get_asp(days=r, meals=2, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test8_2:{r}:none {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test8_2:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        '''
        to_solve = get_asp(days=r, meals=2, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test8_2:{r}:frst {end - start}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=r, meals=2, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test8_2:{r}:scnd {end - start}"
        print(res)
        file.write(res + "\n")
        '''

        to_solve = get_asp(days=r, meals=2, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test8_2:{r}:both {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test8_2:{r}:both {avg}"
        print(res)
        file.write(res + "\n")

        if r == 1:
            r = r + 9
        else:
            r = r + 10


# no. days with 3 meals
def test8_3(file):
    AVG = 30
    r = 1
    while r <= 100:
        to_solve = get_asp(days=r, meals=3, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test8_3:{r}:none {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test8_3:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        '''
        to_solve = get_asp(days=r, meals=3, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test8_3:{r}:frst {end - start}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=r, meals=3, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test8_3:{r}:scnd {end - start}"
        print(res)
        file.write(res + "\n")
        '''

        to_solve = get_asp(days=r, meals=3, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test8_3:{r}:both {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test8_3:{r}:both {avg}"
        print(res)
        file.write(res + "\n")

        if r == 1:
            r = r + 9
        else:
            r = r + 10


# no. days with 4 meals
def test8_4(file):
    AVG = 30
    r = 1
    while r <= 100:
        to_solve = get_asp(days=r, meals=4, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test8_4:{r}:none {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test8_4:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        '''
        to_solve = get_asp(days=r, meals=4, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test8_4:{r}:frst {end - start}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=r, meals=4, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        start = time.time()
        solve(to_solve)
        end = time.time()
        res = f"test8_4:{r}:scnd {end - start}"
        print(res)
        file.write(res + "\n")
        '''

        to_solve = get_asp(days=r, meals=4, rel_recipes=1, irrel_recipes=0, rel_ingredients=1, unused_ingredients=0,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test8_4:{r}:both {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test8_4:{r}:both {avg}"
        print(res)
        file.write(res + "\n")

        if r == 1:
            r = r + 9
        else:
            r = r + 10


# no. irrelevant recipes with same no. irrelevant ingredients
# no. irrelevant recipes with a unique irrelevant ingredient
# no. irrelevant pantry items (needs irrelevant recipe so it is NOT unused)
def test9(file):
    AVG = 30
    r = 1
    while r <= 100:
        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=r, rel_ingredients=1, unused_ingredients=r,
                           empty_pantry=True,
                           first_optim=False, second_optim=False)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test9:{r}:none {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test9:{r}:none {avg}"
        print(res)
        file.write(res + "\n")

        '''
        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=r, rel_ingredients=1, unused_ingredients=r,
                           empty_pantry=True,
                           first_optim=True, second_optim=False)
        avg = 0
        for i in range(3):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test9:{r}:frst {time_it_took}"
            print(res)
            avg += time_it_took
        avg = avg / 3
        res = f"test9:{r}:frst {avg}"
        print(res)
        file.write(res + "\n")

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=r, rel_ingredients=1, unused_ingredients=r,
                           empty_pantry=True,
                           first_optim=False, second_optim=True)
        avg = 0
        for i in range(3):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test9:{r}:scnd {time_it_took}"
            print(res)
            avg += time_it_took
        avg = avg / 3
        res = f"test9:{r}:scnd {avg}"
        print(res)
        file.write(res + "\n")
        '''

        to_solve = get_asp(days=2, meals=1, rel_recipes=1, irrel_recipes=r, rel_ingredients=1, unused_ingredients=r,
                           empty_pantry=True,
                           first_optim=True, second_optim=True)
        avg = 0
        for i in range(AVG):
            start = time.time()
            solve(to_solve)
            end = time.time()
            time_it_took = end - start
            res = f"test9:{r}:both {time_it_took}"
            # print(res)
            avg += time_it_took
        avg = avg / AVG
        res = f"test9:{r}:both {avg}"
        print(res)
        file.write(res + "\n")

        if r == 1:
            r = r + 9
        else:
            r = r + 10


def get_asp(days: int, meals: int, rel_recipes: int, irrel_recipes: int, rel_ingredients: int, unused_ingredients: int,
            empty_pantry: bool,
            first_optim: bool, second_optim: bool):
    instance = ""

    instance += "nutrient(energy).\n"
    instance += "nutrient(protein).\n"
    instance += "nutrient(fat).\n"
    instance += "nutrient(saturates).\n"
    instance += "nutrient(carbs).\n"
    instance += "nutrient(sugar).\n"
    instance += "nutrient(salt).\n"

    instance += "\n"

    for i in range(days):
        instance += f"day(d{i}).\n"

    for m in range(meals):
        instance += f"meal(m{m}).\n"

    for r in range(rel_recipes):
        instance += f"recipe(r{r}).\n"
        if rel_ingredients == rel_recipes:
            instance += f"needs(r{r}, i{r}, 30000).\n"
        else:
            instance += f"needs(r{r}, i0, 30000).\n"
        for m in range(meals):
            instance += f"meal_type(r{r}, m{m}).\n"

    if not second_optim:
        if irrel_recipes == unused_ingredients:
            for r in range(irrel_recipes):
                instance += f"needs(r{r}, iirrel{r}, 30000).\n"

    if not second_optim:
        for r in range(irrel_recipes):
            instance += f"recipe(r{r}).\n"
            instance += f"meal_type(r{r}, irrelevant).\n"

    for i in range(rel_ingredients):
        if first_optim:
            instance += f"i_costs(aldi, in{i}_0, i{i}, 30000, 300).\n"
            instance += f"ing_has_nutrient(in{i}_0, i{i}, 10000, energy, 4900).\n"
            instance += f"ing_has_nutrient(in{i}_0, i{i}, 10000, fat, 4900).\n"
            instance += f"ing_has_nutrient(in{i}_0, i{i}, 10000, saturates, 4900).\n"
            instance += f"ing_has_nutrient(in{i}_0, i{i}, 10000, carbs, 4900).\n"
            instance += f"ing_has_nutrient(in{i}_0, i{i}, 10000, sugar, 4900).\n"
            instance += f"ing_has_nutrient(in{i}_0, i{i}, 10000, protein, 4900).\n"
            instance += f"ing_has_nutrient(in{i}_0, i{i}, 10000, salt, 4900).\n"
        else:
            for ina in range(36):
                instance += f"i_costs(aldi, in{i}_{ina}, i{i}, 30000, 300).\n"
                instance += f"ing_has_nutrient(in{i}_{ina}, i{i}, 10000, energy, 4900).\n"
                instance += f"ing_has_nutrient(in{i}_{ina}, i{i}, 10000, fat, 4900).\n"
                instance += f"ing_has_nutrient(in{i}_{ina}, i{i}, 10000, saturates, 4900).\n"
                instance += f"ing_has_nutrient(in{i}_{ina}, i{i}, 10000, carbs, 4900).\n"
                instance += f"ing_has_nutrient(in{i}_{ina}, i{i}, 10000, sugar, 4900).\n"
                instance += f"ing_has_nutrient(in{i}_{ina}, i{i}, 10000, protein, 4900).\n"
                instance += f"ing_has_nutrient(in{i}_{ina}, i{i}, 10000, salt, 4900).\n"

    # in case of irrelevant ingredients, NOT unused ingredients
    if irrel_recipes == unused_ingredients:
        # if not optimised for i_costs
        if not first_optim:
            # for all irrelevant ingredients
            for i in range(unused_ingredients):
                # have one page (36) long list of unique ingredient names for that ingredient
                for ina in range(36):
                    instance += f"i_costs(aldi, inirrel{i}_{ina}, iirrel{i}, 30000, 300).\n"
                    instance += f"ing_has_nutrient(inirrel{i}_{ina}, iirrel{i}, 10000, energy, 4900).\n"
                    instance += f"ing_has_nutrient(inirrel{i}_{ina}, iirrel{i}, 10000, fat, 4900).\n"
                    instance += f"ing_has_nutrient(inirrel{i}_{ina}, iirrel{i}, 10000, saturates, 4900).\n"
                    instance += f"ing_has_nutrient(inirrel{i}_{ina}, iirrel{i}, 10000, carbs, 4900).\n"
                    instance += f"ing_has_nutrient(inirrel{i}_{ina}, iirrel{i}, 10000, sugar, 4900).\n"
                    instance += f"ing_has_nutrient(inirrel{i}_{ina}, iirrel{i}, 10000, protein, 4900).\n"
                    instance += f"ing_has_nutrient(inirrel{i}_{ina}, iirrel{i}, 10000, salt, 4900).\n"

    if empty_pantry:
        for i in range(rel_ingredients):
            instance += f"pantry_item(i{i}, 0).\n"
        if not second_optim:
            for i in range(unused_ingredients):
                instance += f"pantry_item(i{i}, 0).\n"
    else:
        for i in range(rel_ingredients):
            instance += f"pantry_item(i{i}, 300).\n"
        if not second_optim:
            for i in range(unused_ingredients):
                instance += f"pantry_item(i{i}, 300).\n"

    instance += '''
    nutrient_needed(energy, 129400, 129400).
nutrient_needed(protein, 3200, 11300).
nutrient_needed(fat, 2900, 5000).
nutrient_needed(saturates, 0, 1400).
nutrient_needed(carbs, 14600, 21000).
nutrient_needed(sugar, 0, 2500).
nutrient_needed(salt, 0, 600).

% the amount of times the recipe has been scheduled for the week
schedule_count(R, C) :- C = #count {D,M : schedule(R, D, M)}, recipe(R).

% calculates the amount of nutrient a recipe has
recipe_has_nutrient(R,N,T) :- T = #sum{FA: FA=IA*NA/Q, ing_has_nutrient(_, I, Q, N, NA), needs(R,I,IA)}, recipe(R), nutrient(N).

% decides whether the amount we need to buy of an ingredient is integer or not.
int(R, I, (((A2 * C)-A3) / A1)) :- (((A2 * C)-A3)) \ A1 == 0, recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(_, _, I, A1, P), schedule_count(R,C).
% buy amount A of ingredient I for a certain recipe R with total cost of T.
% two cases when it is an integer and when it is not in which case we need to buy 1 more (ceil function)
buy(R, I, A, S, IN, T) :- T = P*A, T > 0, int(R, I, A), recipe(R), i_costs(S, IN, I, A1, P).
buy(R, I, A, S, IN, T) :- T = P*A, T > 0, C > 0, A = (((A2 * C)-A3) / A1)+1, not int(R, I, _), recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(S, IN, I, A1, P), schedule_count(R,C).

% total price is the sum of costs of ingredients we need to buy.
total_cost(S) :- S = #sum {T,R,I,A : buy(R, I, A, _, IN, T)}.

% schedule exactly one recipe with correct meal type, for every day for every meal
1 {schedule(R, D, M) : recipe(R), meal_type(R,M)} 1 :- day(D), meal(M).

% do not schedule recipe if it needs an ingredient NOT in pantry or webstore
:- schedule(R, _, _), recipe(R), needs(R, I, AN), not i_costs(_, _, I, _, _), A < AN, pantry_item(I, A).

% ensure that 50-80g of protein is consumed within a day.
%:- #sum {A,R,M : schedule(R,D,M), recipe_has_nutrient(R, N, A)} < A2, nutrient_needed(N,A2, _), day(D), nutrient(N).
%:- #sum {A,R,M: schedule(R,D,M), recipe_has_nutrient(R, N, A)} > A3, nutrient_needed(N,_,A3), day(D), nutrient(N).

daily_nutrient_sum(D, N, S) :- S = #sum {A,R,M : schedule(R,D,M), recipe_has_nutrient(R, N, A)}, day(D), nutrient(N).
%full_nutrient_sum(N, T) :- T = #sum {S,D: daily_nutrient_sum(_, N, S), day(D)}, nutrient(N).

% nutritional difference for the entire week
daily_nutrient_diff(D, N, T) :- T = A2-S, S < A2, nutrient_needed(N,A2, _), day(D), nutrient(N), daily_nutrient_sum(D,N,S).
daily_nutrient_diff(D, N, T) :- T = S-A3, S > A3, nutrient_needed(N,_, A3), day(D), nutrient(N), daily_nutrient_sum(D,N,S).
daily_nutrient_diff(D, N, 0) :- S >= A2, S <= A3, nutrient_needed(N,A2, A3), day(D), nutrient(N), daily_nutrient_sum(D,N,S).

% minimize the difference of being out of range for nutrients (most important: @2).
#minimize {T @2: T = S, daily_nutrient_diff(_, _, S)}.
% minimize total cost (less important important: @1)
#minimize {T @1 : total_cost(T)}.
    '''

    return instance


if __name__ == "__main__":
    main()
