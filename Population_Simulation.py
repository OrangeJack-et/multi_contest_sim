import random as rand
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

class Bird:
    def __init__(self, L):
        # Inputs:
        # L = realised load
        self.L = L
        self.fitness = math.exp(-L)



class Population:
    def __init__(self, pop_size, rep_contests):
        # Inputs: 
        # pop_size = population size 
        # rep_contests = how many contests per claim (make sure odd)
        self.pop_size = pop_size
        self.rep_contests = rep_contests
        self.birds = []
        self.winners = []
        for i in range(pop_size):
            L = rand.expovariate(1)
            self.birds.append(Bird(L))


    def Contest(self, req_deltaL, error):
        # fight function that returns 1 for A winning and -1 for B winning (commetns needs changing sicne not accuarate any more )
        # A whole contest with rep_contests number of fights
        # Inputs:
        # req_deltaL = required difference in realised load
        # error = per-trial noise
        if req_deltaL is None:
            A = B = rand.randint(0, self.pop_size - 1)
            while A == B:
                B = rand.randint(0, self.pop_size - 1)
            LA = self.birds[A].L
            LB = self.birds[B].L

            Ldiff = self.birds[B].L - self.birds[A].L
        else:
            LA = rand.expovariate(1)
            LB = LA + req_deltaL
            Ldiff = req_deltaL
        bucketA = 0
        bucketB = 0
        for i in range(self.rep_contests):
            errorA = rand.uniform(-error, error)
            LAerr = LA + errorA
            if LAerr < 0:
                LAerr = 0
            errorB = rand.uniform(-error, error)
            LBerr = LB + errorB
            if LBerr < 0:
                LBerr = 0
            wA = math.exp(-LAerr)
            wB = math.exp(-LBerr)
            probA = wA / (wA + wB)

            x = rand.random()
            if x < probA:
                bucketA += 1
            else:
                bucketB += 1
        if bucketA > bucketB:
            # A winning = 1
            winner = '1'
        else:
            # B winning = 0
            winner = '0'
        wdiff_rat = (math.exp(-LA) - math.exp(-LB)) / math.exp(-LA)

        return [winner, wdiff_rat, Ldiff]


    def Many_contests(self, num_contests, req_deltaL, error):
        # Runs contest num_contest times
        # Inputs:
        # num_contests = number of separate contests
        # rep_contests = number of fights per contest
        # error = per-trial noise
        for i in range(num_contests):
            self.winners.append(self.Contest(req_deltaL, error))
        return self.winners


    @staticmethod
    def Plot_prob_against_Ldiff(pop_size, num_contests, rep_contests, error):
        # plotting probability of A winning against the different in realsied load, L
        # Inputs:
        # pop_size = population size
        # num_contests = number of separate contests
        # rep_contests = number of fights per contest
        # error = per-trial noise
        pop = Population(pop_size=pop_size, rep_contests=rep_contests)
        winners_wdiff_list =pop.Many_contests(num_contests, None, error)
        winnerAB_list = [i[0] for i in winners_wdiff_list]
        diff_list = [i[2] for i in winners_wdiff_list]
        bins = np.linspace(-3, 3, 21)     
        return Population.bin_count(bins, diff_list, winnerAB_list)


    @staticmethod
    def Plot_prob_against_wdiff(pop_size, num_contests, rep_contests, error):
        # plottign probability of A winning against the difference in fitness, w
        # Inputs:
        # pop_size = population size
        # num_contests = number of separate contests
        # rep_contests = number of fights per contest
        # error = per-trial noise
        pop = Population(pop_size=pop_size, rep_contests=rep_contests)
        winners_wdiff_list =pop.Many_contests(num_contests, None, error)
        winnerAB_list = [i[0] for i in winners_wdiff_list]
        diff_list = [i[1] for i in winners_wdiff_list]
        bins = np.linspace(0, 1, 21)  
        return Population.bin_count(bins, diff_list, winnerAB_list)


    @staticmethod
    def bin_count(bins, diff_list, winnerAB_list):
        # counts the number in each bin for plotting
        # Inputs:
        # bins = the linspace for plotting the x-axis
        # diff_list = the list of the difference (the x value)
        # winnerAB_list
        num_in_bin = []
        num_A_in_bin = []
        prop_bin_list = []
        bin_indices = np.digitize(diff_list, bins)
        for i in range(1, len(bins)):
            tot_counter = 0
            counter = 0
            for j in range(len(diff_list)):
                if bin_indices[j] == i:
                    tot_counter += 1
                    if winnerAB_list[j] == '1':
                        counter += 1
            if tot_counter != 0:
                prop_bin_list.append(counter / tot_counter)
            else:
                prop_bin_list.append(None)
            num_in_bin.append(tot_counter)
            num_A_in_bin.append(counter)

        centre_bin = []
        for i in range(len(bins) - 1):
            centre = (bins[i] + bins[i + 1]) / 2
            centre_bin.append(centre)
        return centre_bin, prop_bin_list        


    @staticmethod
    def Plot_prob_against_m(pop_size, num_contests, req_deltaL, error):
        # plotting probability of A winning against the number of contests, m
        # Inputs:
        # pop_size = population size
        # num_contests = number of separate contests
        # req_deltaL = required difference in realisedl load
        # error = per-trial noise
        rep_contests = []
        rep_contests = list(range(1, 100, 2)) #1,3,5,...,99
        probA_list = []
        for i in range(len(rep_contests)):
            pop = Population(pop_size=pop_size, rep_contests=rep_contests[i])
            winners_wdiff_list = pop.Many_contests(num_contests, req_deltaL, error)
            winnerAB_list = [int(i[0]) for i in winners_wdiff_list]
            x = np.mean(winnerAB_list)
            probA_list.append(x)
        return probA_list, rep_contests

    @staticmethod
    def Plot_prob_against_error(pop_size, num_contests, rep_contests, req_deltaL):
        # plotting probability of A winning against the number of contests, m
        # new pop needs to be created each time so self.winners doesnt accumulate values 
        # we are testing for different populations with different errors 
        # Inputs:
        # pop_size = population size
        # num_contests = number of separate contests
        # rep_contests = number of fights per contest
        # req_deltaL = required difference in realised load
        error_list = np.linspace(0, 3,  100)
        probA_list = []
        for i in range(len(error_list)):
            pop = Population(pop_size, rep_contests)
            winners_wdiff_list = pop.Many_contests(num_contests, req_deltaL, error_list[i])
            winnerAB_list = [int(i[0]) for i in winners_wdiff_list]
            x = np.mean(winnerAB_list)
            probA_list.append(x)
        return probA_list, error_list

    @staticmethod
    def Binomial_curve(deltaL):
        # for plotting the theorietical binomial curve (ProbA against m)
        # Inputs:
        # deltaL = difference in realised load
        p = 1 / (1 + math.exp(-deltaL))
        odd_nums = list(range(1, 100, 2))
        y = []
        for i in odd_nums:
            y.append(1 - binom.cdf(i//2, i, p))      
        return odd_nums, y

print('9')