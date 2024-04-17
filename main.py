import numpy as np
import matplotlib.pyplot as plt
import random as rnd


# "Abstract" class
class Person(object):

    # constructor
    def __init__(self, p_id):
        self.id = p_id
        self.x = 0
        self.y = 0

    def get_location(self):
        print("My location is: " + str(self.x) + ", " + str(self.y))
        return self.x, self.y


# "Interfaces"

# Perishable types can perish and become Removed
class Perishable:
    is_alive = True

    def perish(self):
        self.is_alive = False

    def has_perished(self):
        return not self.is_alive


# Attacker types can attack and make others Removed
class Attacker:
    def attack(self, p_object):
        p_object.perish()


# Derived intermediate classes

# Active types can move around and encounter other objects
class Active(Person):

    def encounter(self, p_object):
        pass

    def move(self):
        pass  # move, somehow


# Inactive types cannot move around and remain at the same position
class Inactive(Person):
    was_infected = False

# END derived intermediate classes


# Active classes
class Susceptible(Active, Perishable, Attacker):
    cooperating = False
    bitten = False

    def encounter(self, p_object):
        if type(p_object).__name__ == "Susceptible":
            if not p_object.cooperating and not self.cooperating:
                self.cooperate()
                p_object.cooperate()
        elif type(p_object).__name__ == "Infected":
            if not self.cooperating:
                p_object.bite(self)
            else:
                self.attack(p_object)
        elif type(p_object).__name__ == "Removed":
            if p_object.was_infected:
                self.burn(p_object)
                self.bury(p_object)
            else:
                self.bury(p_object)
        elif type(p_object).__name__ == "Mutated":
            p_object.attack(self)

    def cooperate(self):
        self.cooperating = True

    def burn(self, p_object):
        p_object.burned = True

    def bury(self, p_object):
        p_object.buried = True


class Infected(Active, Perishable):
    def encounter(self, p_object):
        pass

    def mutate(self):
        pass

    def bite(self, p_object):
        p_object.bitten = True


class Mutated(Active, Attacker):
    def encounter(self, p_object):
        pass

    def mutate(self, p_object):
        pass


# Inactive classes
class Removed(Inactive):
    burned = False
    buried = False


def zombiola(p_total, p_initially_infected):
    # Instance variables
    # establish total population
    total = p_total

    # set initial size of each subpopulation
    s_count = total - p_initially_infected
    i_count = p_initially_infected
    r_count = total - (s_count + i_count)
    m_count = total - (s_count + i_count + r_count)

    # create empty lists to hold class objects
    susceptible = []
    infected = []
    removed = []
    mutated = []

    # initialize s_count objects of class Susceptible
    for s in range(s_count):
        sus = Susceptible(s+1)
        susceptible.append(sus)

    # initialize i_count objects of class Infected
    for i in range(i_count):
        inf = Infected(i+1)
        infected.append(inf)

    # initialize r_count objects of class Removed
    for r in range(r_count):
        rem = Removed(r+1)
        removed.append(rem)

    # initialize m_count objects of class Mutated
    for m in range(m_count):
        mut = Mutated(m+1)
        mutated.append(mut)

    # check length of each list
    print(len(susceptible))
    print(len(infected))
    print(len(removed))
    print(len(mutated))

    # keep_surviving = (s_count > 0)
    #
    # while keep_surviving:
    #
    #     if s_count <= 0:
    #         keep_surviving = False
    #
    #     for sus in susceptible:
    #         pass
    #
    #     for inf in infected:
    #         pass
    #
    #     for rem in removed:
    #         pass
    #
    #     for mut in mutated:
    #         pass


zombiola(50, 3)
