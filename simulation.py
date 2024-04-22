import matplotlib.pyplot as plt
import random as rnd


def chigurh():
    coin_toss = rnd.randint(1, 100)

    return coin_toss


# "Abstract" class
class Person(object):

    # constructors
    def __init__(self, p_id, p_x=None, p_y=None):
        self.id = p_id
        if p_x is None:
            self.x = 0
        else:
            self.x = p_x

        if p_y is None:
            self.y = 0
        else:
            self.y = p_y

    def get_location(self):
        print("My location is: " + str(self.x) + ", " + str(self.y))
        return self.x, self.y

    def overlaps(self, p_object):
        return self.x == p_object.x and self.y == p_object.y


# "Interface"
class Perishable:
    is_active = True

    def perish(self):
        self.is_active = False

    def has_perished(self):
        return not self.is_active


class Biteable:
    is_bitten = False

    def bite_status(self):
        return self.is_bitten


# Intermediate classes
# Active types can move around and encounter other objects
class Active(Person):

    def encounter(self, p_object):
        pass

    def move(self):
        pass  # move, somehow

    def attack(self, p_object):
        p_object.perish()


# Inactive types cannot move around and remain at the same position
class Inactive(Person):
    is_eaten = False

    @staticmethod
    def was_infected(p_object):
        status = False
        if type(p_object).__name__ == "Infected":
            status = True

        return status


# Active classes
class Susceptible(Active, Perishable, Biteable):
    group_list = []
    is_cooperating = False

    def encounter(self, p_object):
        if type(p_object).__name__ == "Susceptible":

            if not p_object.is_cooperating and not self.is_cooperating:
                self.cooperate(p_object)

        elif type(p_object).__name__ == "Infected":

            result = chigurh()

            if self.is_cooperating:
                if 50 < (result+10) <= 85:
                    self.attack(p_object)
                else:
                    for member in self.group_list:
                        p_object.attack(member)
            else:
                if 50 < result <= 60:
                    self.attack(p_object)
                else:
                    bite(self)

            if self.is_bitten:
                self.perish()

        elif type(p_object).__name__ == "Removed":

            if p_object.was_infected:
                self.burn(p_object)
            else:
                self.bury(p_object)

        elif type(p_object).__name__ == "Mutant":

            p_object.attack(self)

        return self.is_active

    def perish(self):
        super().perish()
        if self.is_cooperating:
            for member in self.group_list:
                member.is_cooperating = False
            self.group_list.clear()

    def burn(self, p_object):
        p_object.burned = True

    def bury(self, p_object):
        p_object.buried = True

    def cooperate(self, p_object):
        self.group_list.append(p_object)
        p_object.group_list.append(self)
        self.is_cooperating = True
        p_object.is_cooperating = True
        p_object.x = self.x
        p_object.y = self.y


def bite(p_object):
    p_object.is_bitten = False


class Infected(Active, Perishable, Biteable):
    is_carrier = False
    bonus = 0

    def encounter(self, p_object):
        if type(p_object).__name__ == "Susceptible":

            p_object.encounter(self)

        elif type(p_object).__name__ == "Infected":

            result = chigurh() + self.bonus
            second_result = chigurh() + self.bonus

            if 50 < result <= 100:
                self.is_carrier = True

            if self.is_carrier:
                if 50 < second_result <= 100:
                    bite(p_object)
                else:
                    p_object.attack(self)
            else:
                if 40 < second_result <= 60:
                    self.attack(p_object)
                else:
                    p_object.attack(self)

            p_object.attack(self)

        elif type(p_object).__name__ == "Removed":
            if p_object.burned:
                self.eat(p_object)

        elif type(p_object).__name__ == "Mutant":
            if not self.is_carrier:
                p_object.attack(self)

        return self.is_active

    def eat(self, p_object):
        p_object.is_eaten = True
        self.bonus += 10


class Mutant(Active):
    def encounter(self, p_object):
        if type(p_object).__name__ == "Susceptible" or type(p_object).__name__ == "Infected":
            p_object.encounter(self)

        return True

    def attack(self, p_object):
        if type(p_object).__name__ == "Susceptible":
            super().attack(p_object)
        elif type(p_object).__name__ == "Infected":
            p_object.is_mutating = True
            super().attack(p_object)


# Inactive classes
class Removed(Inactive):
    def __init__(self, p_id, p_x=None, p_y=None, p_object=None):
        super().__init__(p_id, p_x, p_y)
        self.was_infected = self.was_infected(p_object)
        self.burned = False
        self.buried = False


def zombiola(p_total, p_initially_infected):
    # establish total population
    total = p_total

    # number of times the loop is completed
    time = 0

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

    rnd_x = rnd.randint(0, 0)
    rnd_y = rnd.randint(0, 0)

    print(s_count, i_count, r_count, m_count)

    # initialize s_count objects of class Susceptible
    for s in range(s_count):
        sus = Susceptible(s + 1, rnd_x, rnd_y)
        susceptible.append(sus)

    # initialize i_count objects of class Infected
    for i in range(i_count):
        inf = Infected(i + 1, rnd_x, rnd_y)
        infected.append(inf)

    # initialize r_count objects of class Removed
    for r in range(r_count):
        rem = Removed(r + 1, rnd_x, rnd_y)
        removed.append(rem)

    # initialize m_count objects of class Mutant
    for m in range(m_count):
        mut = Mutant(m + 1, rnd_x, rnd_y)
        mutated.append(mut)

    keep_surviving = (s_count > 0)

    while keep_surviving:
        if s_count <= 0 or (s_count + r_count) == total:
            keep_surviving = False

        for sus in susceptible:
            for inf in infected:
                if sus.encounter(inf):
                    i_count -= 1
                    r_count += 1
                    removed.append(Removed(inf.id, inf.x, inf.y, inf))
                    infected.remove(inf)
                    print(1)
                else:
                    if sus.is_bitten:
                        s_count -= 1
                        i_count += 1
                        infected.append(Infected(sus.id, sus.x, sus.y))
                        susceptible.remove(sus)
                        print(2)
                    else:
                        s_count -= 1
                        r_count += 1
                        removed.append(Removed(sus.id, sus.x, sus.y, sus))
                        susceptible.remove(sus)
                        print(3)

            for rem in removed:
                if sus.encounter(rem):
                    pass

            for mut in mutated:
                if not sus.encounter(mut):
                    s_count -= 1
                    r_count += 1
                    removed.append(Removed(sus.id, sus.x, sus.y, sus))
                    susceptible.remove(sus)
                    print(4)

        for inf in infected:
            for sus in susceptible:
                if inf.encounter(sus):
                    if sus.is_bitten:
                        s_count -= 1
                        i_count += 1
                        infected.append(Infected(sus.id, sus.x, sus.y))
                        susceptible.remove(sus)
                        print(5)
                    else:
                        s_count -= 1
                        r_count += 1
                        removed.append(Removed(sus.id, sus.x, sus.y, sus))
                        susceptible.remove(sus)
                        print(6)
                else:
                    i_count -= 1
                    r_count += 1
                    removed.append(Removed(inf.id, inf.x, inf.y, inf))
                    infected.remove(inf)
                    print(7)

            # for each inf

            for mut in mutated:
                if not inf.encounter(mut):
                    i_count -= 1
                    m_count += 1
                    mutated.append(Mutant(inf.id, inf.x, inf.y))
                    infected.remove(inf)
                    print(8)

        for mut in mutated:
            for sus in susceptible:
                if mut.encounter(sus):
                    s_count -= 1
                    r_count += 1
                    removed.append(Removed(sus.id, sus.x, sus.y, sus))
                    susceptible.remove(sus)
                    print(9)

            for inf in infected:
                if mut.encounter(inf):
                    i_count -= 1
                    m_count += 1
                    mutated.append(Mutant(inf.id, inf.x, inf.y))
                    infected.remove(inf)
                    print(10)

        time += 1

    return s_count, i_count, r_count, m_count, time


def plot_sir(S, I, R, M, time):
    """
    Plot the results of the SIR model simulation.

    Parameters:
        S (array): Array of susceptible individuals over time.
        I (array): Array of infected individuals over time.
        R (array): Array of recovered individuals over time.
        days (int): Number of days to simulate.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(time), S, label='Susceptible')
    plt.plot(range(time), I, label='Infected')
    plt.plot(range(time), R, label='Recovered')
    plt.plot(range(time), M, label='Mutated')

    plt.xlabel('Time')
    plt.ylabel('Number of individuals')
    plt.title('SIR Model Simulation')
    plt.legend()
    plt.grid(True)
    plt.show()


total = 50
initial_infected = 3

zombiola(total, initial_infected)


#
# plot_sir(S, I, R, M, time)

# susceptible = [Susceptible(1), Susceptible(2)]
# print(susceptible[0])
# print(susceptible[1])
# print(susceptible[0].is_cooperating)
# print(susceptible[1].is_cooperating)
# print(susceptible[0].group_list)
# print(susceptible[1].group_list)
# susceptible[0].encounter(susceptible[1])
# print(susceptible[0].is_cooperating)
# print(susceptible[1].is_cooperating)
# print(susceptible[0].group_list)
# print(susceptible[1].group_list)
# susceptible[0].perish()
# print(susceptible[0].is_cooperating)
# print(susceptible[1].is_cooperating)
# print(susceptible[0].group_list)
# print(susceptible[1].group_list)
