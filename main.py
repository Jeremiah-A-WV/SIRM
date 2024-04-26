import matplotlib.pyplot as plt
import random as rnd
import numpy as np


# Island measurements
WIDTH = 800
HEIGHT = 1100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Other constants
STARTING_HEALTH = 100
DEFAULT_POWER = 10


class Person:
    def __init__(self, size_range=(4, 8)):
        self.x = rnd.randint(0, WIDTH)
        self.y = rnd.randint(0, HEIGHT)
        self.size = rnd.randrange(*size_range)

    def get_location(self):
        return self.x, self.y

    def is_touching(self, obj):
        return (np.linalg.norm(np.array(self.get_location()) - np.array(obj.get_location()))
                < (self.size + obj.size))


class Active(Person):
    def __init__(self):
        super().__init__()
        self.attack_power = DEFAULT_POWER
        self.health = STARTING_HEALTH
        self.speed = 10

    def fight(self, obj):
        keep_fighting = True

        while keep_fighting:
            if flip(50, 75):
                obj.health -= self.attack_power
                self.health -= (obj.attack_power - 10)
            else:
                self.health -= obj.attack_power
                obj.health -= self.attack_power

            if obj.health <= 0 or self.health <= 0:
                keep_fighting = False

        return self.health > 0

    def move(self):
        move_x = rnd.randint(-1, 1) * self.speed
        move_y = rnd.randint(-1, 1) * self.speed

        if self.get_location()[0] < 0:
            self.x += abs(move_x)
        elif self.get_location()[0] > WIDTH:
            self.x += -abs(move_x)
        else:
            self.x += move_x

        if self.get_location()[1] < 0:
            self.y += abs(move_y)
        elif self.get_location()[1] > HEIGHT:
            self.y += -abs(move_y)
        else:
            self.y += move_y


class Susceptible(Active):
    def __init__(self):
        super().__init__()


class Infected(Active):
    def __init__(self):
        super().__init__()


class Removed(Person):
    def __init__(self):
        super().__init__()
        self.is_carrier = False
        self.is_burned = False
        self.is_buried = False


class Mutated(Active):
    def __init__(self):
        super().__init__()


def flip(mini, maxi):
    return rnd.randint(mini, maxi)


def simulation(p_total, p_initially_infected):
    total = p_total
    sus_count = total - p_initially_infected
    inf_count = p_initially_infected
    rem_count = total - (sus_count + inf_count)
    mut_count = total - (sus_count + inf_count + rem_count)

    sus_list = []
    inf_list = []
    rem_list = []
    mut_list = []

    for sc in range(sus_count):
        sus_list.append(Susceptible())

    for ic in range(inf_count):
        inf_list.append(Infected())

    for rc in range(rem_count):
        rem_list.append(Removed())

    for mc in range(mut_count):
        mut_list.append(Mutated())

    keep_surviving = (sus_count > 0)

    iter_days = 0

    while keep_surviving:
        if sus_count == 0 or (sus_count + rem_count == total):
            keep_surviving = False

        for sus in sus_list:
            for inf in inf_list:
                sus.move()
                inf.move()
                if sus.is_touching(inf):
                    if 55 < flip(50, 75) <= 60:
                        if sus.fight(inf):
                            print("SUS KILLED INF")
                            rem_list.append(perish(inf))
                            rem_count += 1
                            inf_list.remove(inf)
                            inf_count -= 1
                    else:
                        print("SUS BECAME INF")
                        inf_list.append(bite(sus))
                        inf_count += 1
                        sus_list.remove(sus)
                        sus_count -= 1

            for rem in rem_list:
                sus.move()
                if sus.is_touching(rem):
                    if rem.is_carrier:
                        if not rem.is_burned:
                            print("SUS BURNED REM")
                            burn(rem)
                    elif not rem.is_buried:
                        print("SUS BURIED REM")
                        bury(rem)

            for mut in mut_list:
                sus.move()
                mut.move()
                if sus.is_touching(mut):
                    if 60 < flip(50, 75) <= 65:
                        print("MUT WAS TOO SLOW")
                        sus.move()
                    else:
                        print("SUS WAS KILLED BY MUT")
                        rem_list.append(perish(sus))
                        rem_count += 1
                        sus_list.remove(sus)
                        sus_count -= 1

        for inf in inf_list:
            for sus in sus_list:
                inf.move()
                sus.move()
                if inf.is_touching(sus):
                    if inf.fight(sus):
                        print("INF KILLED SUS")
                        rem_list.append(perish(sus))
                        rem_count += 1
                        sus_list.remove(sus)
                        sus_count -= 1
                    else:
                        print("INF WAS KILLED BY SUS")
                        rem_list.append(perish(inf))
                        rem_count += 1
                        inf_list.remove(inf)
                        inf_count -= 1

            for rem in rem_list:
                inf.move()
                if inf.is_touching(rem):
                    if not rem.is_buried:
                        print("INF ATE REM")
                        mut_list.append(mutate(inf))
                        mut_count += 1
                        inf_list.remove(inf)
                        inf_count -= 1

            for mut in mut_list:
                inf.move()
                mut.move()
                if inf.is_touching(mut):
                    if flip(50, 75) <= 55:
                        print("MUT MUTATED INF")
                        mut_list.append(mutate(inf))
                        mut_count += 1
                        inf_list.remove(inf)
                        inf_count -= 1
                    else:
                        print("MUT KILLED INF")
                        rem_list.append(perish(inf))
                        rem_count += 1
                        inf_list.remove(inf)
                        inf_count -= 1

        for mut in mut_list:
            for sus in sus_list:
                mut.move()
                sus.move()
                if mut.is_touching(sus):
                    if flip(50, 75):
                        print("MUT WAS TOO SLOW")
                        sus.move()
                    else:
                        print("MUT KILLED SUS")
                        rem_list.append(perish(sus))
                        rem_count += 1
                        sus_list.remove(sus)
                        sus_count -= 1

            for inf in inf_list:
                mut.move()
                inf.move()
                if mut.is_touching(inf):
                    if flip(50, 75):
                        print("INF BECAME MUT")
                        mut_list.append(mutate(inf))
                        mut_count += 1
                        inf_list.remove(inf)
                        inf_count -= 1
                    else:
                        print("INF KILLED BY MUT")
                        rem_list.append(perish(inf))
                        rem_count += 1
                        inf_list.remove(inf)
                        inf_count -= 1

        iter_days += 1

    return sus_count, inf_count, rem_count, mut_count, iter_days


def plot_sir(susceptible, infected, removed, mutated, p_days):
    plt.figure(figsize=(10, 6))
    plt.plot(range(p_days), susceptible, label='Susceptible', color='green')
    plt.plot(range(p_days), infected, label='Infected', color='red')
    plt.plot(range(p_days), removed, label='Recovered', color='black')
    plt.plot(range(p_days), mutated, label='Mutated', color='blue')

    plt.xlabel('Time')
    plt.ylabel('Number of individuals')
    plt.title('SIR Model Simulation')
    plt.legend()
    plt.grid(True)
    plt.show()


def was_infected(obj):
    return isinstance(obj, Infected)


def is_valid_location(p_x, p_y):
    return 0 < p_x < WIDTH and 0 < p_y < HEIGHT


def perish(obj):
    rem = Removed()
    rem.is_carrier = was_infected(obj)
    rem.x = obj.x
    rem.y = obj.y

    return rem


def mutate(obj):
    mut = Mutated()
    mut.x = obj.x
    mut.y = obj.y

    return mut


def bite(obj):
    inf = Infected()
    inf.x = obj.x
    inf.y = obj.y

    return inf


def burn(obj):
    obj.is_burned = True


def bury(obj):
    obj.is_buried = True


s, i, r, m, days = simulation(50, 3)

plot_sir(s, i, r, m, days)
