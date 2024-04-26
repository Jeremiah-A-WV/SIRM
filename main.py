import matplotlib.pyplot as plt
import random as rnd
import numpy as np

# Island measurements
WIDTH = 800
HEIGHT = 1100

# Colors for the pygame simulation
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Object constants
STARTING_HEALTH = 100
DEFAULT_POWER = 10


# Base classes
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
            if flip(50, 75) >= 60:
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


# Derived classes
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


# Generates a number between mini and maxi, inclusively
def flip(mini, maxi):
    return rnd.randint(mini, maxi)


# Lists to store the variables after every run of the loop
sus_line = []
inf_line = []
rem_line = []
mut_line = []


def simulation(p_total, p_initially_infected):
    result = 0
    total = p_total
    sus_count = total - p_initially_infected
    inf_count = p_initially_infected
    rem_count = total - (sus_count + inf_count)
    mut_count = total - (sus_count + inf_count + rem_count)

    sus_list = []
    inf_list = []
    rem_list = []
    mut_list = []

    sus_line.append(sus_count)
    inf_line.append(inf_count)
    rem_line.append(rem_count)
    mut_line.append(mut_count)

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

    print(sus_count, inf_count, rem_count, mut_count, iter_days)

    while keep_surviving:
        if sus_count == 0:
            keep_surviving = False

        for sus in sus_list[:]:

            for inf in inf_list[:]:
                sus.move()
                inf.move()
                if sus.is_touching(inf):
                    if 55 < flip(50, 75) <= 60:
                        if sus.fight(inf):
                            result += 1
                        else:
                            result += 2
                    else:
                        result += 3

                    if result == 1:
                        rem_list.append(perish(inf))
                        rem_count += 1
                        del inf_list[inf_list.index(inf)]
                        inf_count -= 1
                        print(f"SUS KILLED INF "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                    elif result == 2:
                        rem_list.append(perish(inf))
                        rem_count += 1
                        del sus_list[sus_list.index(sus)]
                        sus_count -= 1
                        print(f"SUS WAS KILLED BY INF "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                    elif result == 3:
                        inf_list.append(bite(sus))
                        inf_count += 1
                        del sus_list[sus_list.index(sus)]
                        sus_count -= 1
                        print(f"SUS BECAME INF "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")

                    result = 0

            for rem in rem_list[:]:
                sus.move()
                if sus.is_touching(rem):
                    if rem.is_carrier:
                        if not rem.is_burned:
                            print("SUS BURNED REM")
                            burn(rem)
                    elif not rem.is_buried:
                        print("SUS BURIED REM")
                        bury(rem)

            for mut in mut_list[:]:
                sus.move()
                mut.move()
                if sus.is_touching(mut):
                    if 60 < flip(50, 75) <= 65:
                        print(f"MUT WAS TOO SLOW "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                        result += 1
                    else:
                        result += 2

                    if result == 1:
                        sus.move()
                        result = 0
                    elif result == 2:
                        rem_list.append(perish(sus))
                        rem_count += 1
                        del sus_list[sus_list.index(sus)]
                        sus_count -= 1
                        print(f"SUS WAS KILLED BY MUT "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                        result = 0

        for inf in inf_list[:]:
            for sus in sus_list[:]:
                inf.move()
                sus.move()
                if inf.is_touching(sus):
                    if inf.fight(sus):
                        result += 1
                    else:
                        result += 2

                    if result == 1:
                        rem_list.append(perish(sus))
                        rem_count += 1
                        del sus_list[sus_list.index(sus)]
                        sus_count -= 1
                        print(f"INF KILLED SUS "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                    if result == 2:
                        rem_list.append(perish(inf))
                        rem_count += 1
                        del inf_list[inf_list.index(inf)]
                        inf_count -= 1
                        print(f"INF WAS KILLED BY SUS "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                    result = 0

            for rem in rem_list[:]:
                inf.move()
                if inf.is_touching(rem):
                    if not rem.is_buried:
                        result += 1

                    if result == 1:
                        mut_list.append(mutate(inf))
                        mut_count += 1
                        del inf_list[inf_list.index(inf)]
                        inf_count -= 1
                        print(f"INF ATE REM "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")

                    result = 0

            for mut in mut_list[:]:
                inf.move()
                mut.move()
                if inf.is_touching(mut):
                    if flip(50, 75) <= 55:
                        result += 1
                    else:
                        result += 2

                    if result == 1:
                        mut_list.append(mutate(inf))
                        mut_count += 1
                        del inf_list[inf_list.index(inf)]
                        inf_count -= 1
                        print(f"MUT MUTATED INF "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                    elif result == 2:
                        rem_list.append(perish(inf))
                        rem_count += 1
                        del inf_list[inf_list.index(inf)]
                        inf_count -= 1
                        print(f"MUT KILLED "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")

                    result = 0

        for mut in mut_list[:]:
            for sus in sus_list[:]:
                mut.move()
                sus.move()
                if mut.is_touching(sus):
                    if flip(50, 75) >= 55:
                        print(f"MUT WAS TOO SLOW "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                        sus.move()
                    else:
                        print(f"MUT KILLED SUS "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                        rem_list.append(perish(sus))
                        rem_count += 1
                        del sus_list[sus_list.index(sus)]
                        sus_count -= 1

            for inf in inf_list[:]:
                mut.move()
                inf.move()
                if mut.is_touching(inf):
                    if flip(50, 75) <= 60:
                        result += 1
                    else:
                        result += 2

                    if result == 1:
                        mut_list.append(mutate(inf))
                        mut_count += 1
                        del inf_list[inf_list.index(inf)]
                        inf_count -= 1
                        print(f"MUT MUTATED INF "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")
                    elif result == 2:
                        rem_list.append(perish(inf))
                        rem_count += 1
                        del inf_list[inf_list.index(inf)]
                        inf_count -= 1
                        print(f"MUT KILLED INF "
                              f"S:{sus_count} I:{inf_count} R:{rem_count} M:{mut_count}")

                    result = 0

        iter_days += 1

        if (sus_count + inf_count + rem_count + mut_count) > total:
            raise Exception("ERROR -- TOTAL IS TOO HIGH")
        elif (sus_count + inf_count + rem_count + mut_count) < total:
            raise Exception("ERROR -- TOTAL IS TOO LOW")
        elif iter_days == 130:
            print("END OF ROUND")
            break
        sus_line.append(sus_count)
        inf_line.append(inf_count)
        rem_line.append(rem_count)
        mut_line.append(mut_count)
    print(sus_count, inf_count, rem_count, mut_count, iter_days)
    return sus_count, inf_count, rem_count, mut_count, iter_days, total


# Make obj an instance of Infected, intended for Susceptible types
def was_infected(obj):
    return isinstance(obj, Infected)


# Make obj an instance of Removed
# Intended for Susceptible and Infected types
def perish(obj):
    rem = Removed()
    rem.is_carrier = was_infected(obj)
    rem.x = obj.x
    rem.y = obj.y

    return rem


# Make obj an instance of Mutated, intended for Infected types
def mutate(obj):
    mut = Mutated()
    mut.x = obj.x
    mut.y = obj.y

    return mut


# Make obj an instance of Infected, intended for Susceptible types
def bite(obj):
    inf = Infected()
    inf.x = obj.x
    inf.y = obj.y

    return inf


# Makes obj is_burned true
def burn(obj):
    obj.is_burned = True


# Makes obj is_buried true
def bury(obj):
    obj.is_buried = True


# The output of the simulation is added to each respective variable
s, i, r, m, days, population = simulation(50, 3)

# Labels the axis' of the plot and creates the title
plt.xlabel('Time')
plt.ylabel('Number of individuals')
plt.title('SIR Model Simulation')

# Plot the changes in each line list
plt.plot(days, population, s, label='Susceptible', color='green')
plt.plot(days, population, i, label='Infected', color='red')
plt.plot(days, population, r, label='Recovered', color='black')
plt.plot(days, population, m, label='Mutated', color='blue')
plt.plot(sus_line)
plt.plot(inf_line)
plt.plot(rem_line)
plt.plot(mut_line)

#
# plt.plot(s)
# plt.plot(i)
# plt.plot(r)
# plt.plot(m)

plt.grid(True)
plt.show()
