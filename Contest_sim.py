import random as rand
import math
import numpy as np
from scipy.stats import binom

# Notation (paper symbol -> identifier)
#   m          num_contests   contests per dominance relationship (odd)
#   sigma_E    error   standard deviation of the environmental deviation
#   dL         Ldiff          L_B - L_A
#   L          L              realised load, lethal equivalents
#   w          fitness        exp(-L)


class Bird:
    def __init__(self, L):
        # Inputs:
        # L = realised load
        self.L = L
        self.fitness = math.exp(-L)

class Population:
    def __init__(self, pop_size, num_contests):
        # Inputs: 
        # pop_size = population size 
        # num_contests = how many contests per dominance relationship (make sure odd)
        self.pop_size = pop_size    
        self.num_contests = num_contests
        self.birds = []
        self.winners = []
        for i in range(pop_size):
            L = rand.expovariate(1)
            self.birds.append(Bird(L))

    def Resolve_dominance(self, req_deltaL, error):
        # Resolves the dominance relationship of a pair with num_contests contests 
        # two modes: deltaL = None | deltaL = value
        # when deltaL = None: two random individuals selected from the population
        # when deltaL = value: two random individuals made (not from pop) with required deltaL
        # Gaussian noise with standard deviation error is added to each load
        # probability of A winning is then calculated from the effective fitness
        # winner is selected based on probA and added to the winners 'bucket'
        # this is then repeated 'num_contests' times (with different error every time)
        # winner is then returned (based on which bucket is bigger)
        # Inputs:
        # req_deltaL = required difference in realised load
        # error = per-trial noise
        # Outputs:
        # winner = '1' if A won | '0' if B won
        # wdiff_rat = ratio of fitnesses (to make it independent of magnitude of fitness and only on the ratio)
        # Ldiff = difference in realised load of A and B
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
        for i in range(self.num_contests):
            errorA = rand.gauss(0, error)
            LAerr = LA + errorA
            errorB = rand.gauss(0, error)
            LBerr = LB + errorB
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


    def Many_contests(self, num_dominance_relationships, req_deltaL, error):
        # Runs contest num_dominance_relationships times
        # Inputs:
        # num_dominance_relationships = number of separate dominance relationships
        # num_contests = number of contests per dominance
        # error = per-trial noise
        # Outputs:
        # list of tuples of winners, wdiff_rat, Ldiff for each different contest
        for i in range(num_dominance_relationships):
            self.winners.append(self.Resolve_dominance(req_deltaL, error))
        return self.winners


    @staticmethod
    def Plot_prob_against_Ldiff(pop_size, num_dominance_relationships, num_contests, error):
        # plotting probability of A winning against the difference in realised load, L
        # Inputs:
        # pop_size = population size
        # num_dominance_relationships = number of separate dominance relationships
        # num_contests = number of fights per contest
        # error = per-trial noise
        # Outputs: x: Ldiff | y: probA
        pop = Population(pop_size=pop_size, num_contests=num_contests)
        winners_wdiff_list = pop.Many_contests(num_dominance_relationships, None, error)
        winnerAB_list = [i[0] for i in winners_wdiff_list]
        diff_list = [i[2] for i in winners_wdiff_list]
        bins = np.linspace(-3, 3, 21)     
        return Population.bin_count(bins, diff_list, winnerAB_list)


    @staticmethod
    def Plot_prob_against_wdiff(pop_size, num_dominance_relationships, num_contests, error):
        # plotting probability of A winning against the difference in fitness, w
        # Inputs:
        # pop_size = population size
        # num_dominance_relationships = number of separate contests
        # num_contests = number of fights per contest
        # error = per-trial noise
        pop = Population(pop_size=pop_size, num_contests=num_contests)
        winners_wdiff_list = pop.Many_contests(num_dominance_relationships, None, error)
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
    def Plot_prob_against_m(pop_size, num_dominance_relationships, req_deltaL, error):
        # plotting probability of A winning against the number of contests, m
        # Inputs:
        # pop_size = population size
        # num_dominance_relationships = number of separate contests
        # req_deltaL = required difference in realised load
        # error = per-trial noise
        num_contests = list(range(1, 100, 2))  # 1,3,5,...,99
        probA_list = []
        for i in range(len(num_contests)):
            pop = Population(pop_size=pop_size, num_contests=num_contests[i])
            winners_wdiff_list = pop.Many_contests(num_dominance_relationships, req_deltaL, error)
            winnerAB_list = [int(i[0]) for i in winners_wdiff_list]
            x = np.mean(winnerAB_list)
            probA_list.append(x)
        return probA_list, num_contests


    @staticmethod
    def Plot_prob_against_error(pop_size, num_dominance_relationships, num_contests, req_deltaL):
        # plotting probability of A winning against the error
        # new pop needs to be created each time so self.winners doesn't accumulate values 
        # we are testing for different populations with different errors 
        # Inputs:
        # pop_size = population size
        # num_dominance_relationships = number of separate contests
        # num_contests = number of fights per contest
        # req_deltaL = required difference in realised load
        error_list = np.linspace(0, 2, 100)
        probA_list = []
        for i in range(len(error_list)):
            pop = Population(pop_size, num_contests)
            winners_wdiff_list = pop.Many_contests(num_dominance_relationships, req_deltaL, error_list[i])
            winnerAB_list = [int(i[0]) for i in winners_wdiff_list]
            x = np.mean(winnerAB_list)
            probA_list.append(x)
        return probA_list, error_list


    @staticmethod
    def Binomial_curve(deltaL, error=0):
        # for plotting the theoretical binomial curve (ProbA against m) (uses the probit approximation)
        # Inputs:
        # deltaL = difference in realised load
        p = 1 / (1 + math.exp(-deltaL / math.sqrt(1 + math.pi * error**2 / 4)))
        odd_nums = list(range(1, 100, 2))
        y = []
        for i in odd_nums:
            y.append(1 - binom.cdf(i//2, i, p))      
        return odd_nums, y