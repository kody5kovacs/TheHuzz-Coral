#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 19:55:58 2023

@author: gohil.vasudev
"""
'''
This script is for implementing various MAB algorithms
'''

import numpy as np
import matplotlib.pyplot as plt
import thehuzz_utils as TU

"""
Compute the reward of the arm
"""
class MABalgos: 
    def __init__(self, n_arms, n_picks_reset):
        self.n_arms = n_arms
        self.values = np.zeros(n_arms)
        self.counts = np.zeros(n_arms)
        self.n_picks_reset = n_picks_reset
        self.arm_merged_cov_dict = [None for i in range(self.n_arms)] # each arm has its own merged coverage
        self.arm_tot_cov_incr_hist = [[] for i in range(self.n_arms)] 
        self.arm_arm_cov_incr_hist = [[] for i in range(self.n_arms)] 
        self.arm_seed = [None for i in range(self.n_arms)]
    
    def select_arm(self):
        t = 1
    
    def update(self, arm, reward):
        t = 1

    def compute_reward(self, tot_incr_cov, arm_incr_cov): 
        return (tot_incr_cov*0.75) + (arm_incr_cov*0.25) 

    def update_arm(self, arm, tot_incr_cov, arm_merged_cov_dict, arm_incr_cov, tot_cov_points):#, full_batch_simulated): 
        self.tot_cov_points = tot_cov_points
        # update merged and increase in cov data
        self.arm_merged_cov_dict[arm] = arm_merged_cov_dict # update merged cov
        self.arm_tot_cov_incr_hist[arm].append(tot_incr_cov)
        self.arm_tot_cov_incr_hist[arm] = self.arm_tot_cov_incr_hist[arm][-self.n_picks_reset*self.n_arms:]
        self.arm_arm_cov_incr_hist[arm].append(arm_incr_cov)
        self.arm_arm_cov_incr_hist[arm] = self.arm_arm_cov_incr_hist[arm][-self.n_picks_reset:]
        
        # update arms based on reward
        reward = self.compute_reward(tot_incr_cov, arm_incr_cov)
        self.update(arm, reward)

    def check_reset(self, arm, arm_has_batch_testcases):
        ## reset arms if needed
        #reset_arms = self.check_reset(arm, full_batch_simulated) # check if the arm needs to be reset

        reset_arms = [] 

        # RC1: if arm local cov not incr in last n_picks*n_arms times, reset arm
        if (len(self.arm_arm_cov_incr_hist[arm]) == self.n_picks_reset) \
            and (sum(self.arm_arm_cov_incr_hist[arm]) == 0): 
            reset_arms.append([arm, 'RC1', len(self.arm_arm_cov_incr_hist[arm]), sum(self.arm_arm_cov_incr_hist[arm])])

        ## RC2: if arm global cov not incr in last n_picks times, reset the arm
        #if (len(self.arm_tot_cov_incr_hist[arm]) == self.n_picks_reset*self.n_arms) \
        #    and (sum(self.arm_tot_cov_incr_hist[arm]) == 0): 
        #    reset_arms.append([arm, 'RC2', len(self.arm_tot_cov_incr_hist[arm]), sum(self.arm_tot_cov_incr_hist[arm])])

        # RC3: if we did not have enough tests to simulate in a iteration, reset 
        if not arm_has_batch_testcases: 
            reset_arms.append([arm, 'RC3', arm_has_batch_testcases])

        for arm_info in reset_arms: self.reset_arm(arm_info[0])

        return reset_arms

    def reset_arm(self, arm):
        self.values[arm] = 0
        self.counts[arm] = 0
        self.arm_merged_cov_dict[arm] = None 
        self.arm_tot_cov_incr_hist[arm] = [] 
        self.arm_arm_cov_incr_hist[arm] = [] 

class Greedy(MABalgos):
    def select_arm(self):
        return np.argmax(self.values)
    
    def update(self, arm, reward):
        self.counts[arm] += 1
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]


class EpsilonGreedy(MABalgos):
    def __init__(self, *xargs): 
        super().__init__(*xargs)
        self.epsilon = 0.1
    
    def select_arm(self):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.n_arms)
        else:
            return np.argmax(self.values)
    
    def update(self, arm, reward):
        self.counts[arm] += 1
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]


class UCB(MABalgos):
    def __init__(self, *xargs): 
        super().__init__(*xargs)
        self.time = 0

    def select_arm(self):
        self.time += 1
        ucb_values = self.values + np.sqrt((2 * np.log(self.time)) / (self.counts + 1e-6))
        return np.argmax(ucb_values)
    
    def update(self, arm, reward):
        self.counts[arm] += 1
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]


class ThompsonSampling:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.successes = np.zeros(n_arms)
        self.failures = np.zeros(n_arms)
    
    def select_arm(self):
        sampled_theta = np.random.beta(self.successes + 1, self.failures + 1)
        return np.argmax(sampled_theta)
    
    def update(self, arm, reward):
        if reward == 1:
            self.successes[arm] += 1
        else:
            self.failures[arm] += 1

class ThompsonSampling_non_binary_rewards:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.mu = np.zeros(n_arms)   # Mean estimate for each arm
        self.sigma = np.ones(n_arms) # Standard deviation estimate for each arm
    
    def select_arm(self):
        sampled_rewards = np.random.normal(self.mu, self.sigma)
        return np.argmax(sampled_rewards)
    
    def update(self, arm, reward):
        self.sigma[arm] += 1  # Update standard deviation estimate
        self.mu[arm] = (self.mu[arm] * (self.sigma[arm] - 1) + reward) / self.sigma[arm]




# class EXP3:
#     def __init__(self, n_arms, learning_rate):
#         self.n_arms = n_arms
#         self.learning_rate = learning_rate
#         self.weights = np.ones(n_arms)
    
#     def select_arm(self):
#         probabilities = np.exp(self.learning_rate * self.weights)
#         probabilities /= np.sum(probabilities)
#         return np.random.choice(self.n_arms, p=probabilities)
    
#     def update(self, arm, reward):
#         estimated_reward = reward / (self.weights[arm] + 1e-6)
#         self.weights[arm] *= np.exp(self.learning_rate * estimated_reward / self.n_arms)

class EXP3(MABalgos):
    def __init__(self, *xargs): 
        super().__init__(*xargs)
        self.gamma = 0.1
        self.weights = np.ones(self.n_arms)
    
    def select_arm(self):
        tmp = self.weights / np.sum(self.weights)
        tmp[np.isnan(tmp)] = 0.0
        self.probabilities = ((1 - self.gamma) * tmp) + (self.gamma / self.n_arms)
        # self.probabilities = (1 - self.gamma) * self.weights / np.sum(self.weights) + self.gamma / self.n_arms
        # self.probabilities[np.isnan(self.probabilities)] = 0.0
        arm = np.random.choice(self.n_arms, p=self.probabilities)
        self.counts[arm] += 1
        return arm
    
    def update(self, arm, reward):
        reward = reward / self.tot_cov_points
        estimated_reward = reward / self.probabilities[arm]
        weight_update = np.exp((self.gamma / self.n_arms) * estimated_reward)
        self.weights[arm] *= weight_update
        self.values = self.weights

    def reset_arm(self, arm): 
        super().reset_arm(arm)
        self.weights[arm] = (np.sum(self.weights) - self.weights[arm]) / (self.n_arms - 1)

class my_EXP3:
    def __init__(self, n_arms, learning_rate):
        self.n_arms = n_arms
        self.learning_rate = learning_rate
        self.weights = np.ones(n_arms)
        self.probabilities = np.zeros(n_arms)
    
    def select_arm(self):
        sum_wts = np.sum(self.weights)
        self.probabilities = ((1-self.learning_rate) * (self.weights/sum_wts)) + self.learning_rate/self.n_arms
        #probabilities = np.exp(self.learning_rate * self.weights)
        #probabilities /= np.sum(probabilities)
        return np.random.choice(self.n_arms, p=self.probabilities)
    
    def update(self, arm, reward):
        estimated_reward = reward / (self.probabilities[arm] + 1e-6)
        #estimated_reward = reward / (self.weights[arm] + 1e-6)
        self.weights[arm] *= np.exp(self.learning_rate * estimated_reward / self.n_arms)


def calculate_regret(true_means, chosen_arms, timesteps):
    optimal_mean = np.max(true_means)
    # optimal_arm = np.argmax(true_means)
    
    rewards = np.array([pull_arm(arm, true_means) for arm in chosen_arms])
    # optimal_rewards = np.array([pull_arm(optimal_arm, true_means)] * timesteps)
    # regret = np.cumsum(optimal_rewards - rewards)
    
    expected_rewards = np.array([true_means[arm] for arm in chosen_arms])
    cumulative_rewards = np.cumsum(rewards)
    cumulative_expected_rewards = np.cumsum(expected_rewards)
    regret = cumulative_expected_rewards - cumulative_rewards + optimal_mean * timesteps
    # # Apply rolling mean for smoothing
    # smoothed_regret = np.convolve(regret, np.ones(window_size)/window_size, mode='valid')
    # # print(smoothed_regret)
    # return smoothed_regret
    return regret
    

def pull_arm(arm, reward_probs):
    # Simulate pulling an arm and getting a reward
    # reward =  np.random.normal(reward_probs[arm], 1)
    if np.random.rand() < reward_probs[arm]:
        reward = 1
    else:
        reward = 0
    return reward

def create_mab_object(mab_algo, xargs): 
    if mab_algo == 'Greedy':
        return Greedy(*xargs)
    elif mab_algo == 'UCB':
        return UCB(*xargs)
    elif mab_algo == 'thompson_sampling':
        return ThompsonSampling(*xargs)
    elif mab_algo == 'thompson_sampling_non_binary_rewards':
        return ThompsonSampling_non_binary_rewards(*xargs)
    elif mab_algo == 'EpsilonGreedy':
        #epsilon = 0.1
        return EpsilonGreedy(*xargs)
    elif mab_algo == 'EXP3':
        #learning_rate = 0.1
        return EXP3(*xargs)
    elif mab_algo == 'my_exp3':
        learning_rate = 0.1
        return my_EXP3(*xargs, learning_rate)


def run_algos(algorithms, num_iterations, n_arms, window_size):
    # regret_data = []
    reward_data = []
    for algorithm in algorithms:
        # algo_regret = np.zeros(num_iterations)
        algo_reward = np.zeros(num_iterations)
        if algorithm == 'greedy':
            algo = Greedy(n_arms)
        elif algorithm == 'UCB':
            algo = UCB(n_arms)
        elif algorithm == 'thompson_sampling':
            algo = ThompsonSampling(n_arms)
        elif algorithm == 'thompson_sampling_non_binary_rewards':
            algo = ThompsonSampling_non_binary_rewards(n_arms)
        elif algorithm == 'epsilon_greedy':
            epsilon = 0.1
            algo = EpsilonGreedy(n_arms, epsilon)
        elif algorithm == 'exp3':
            learning_rate = 0.1
            algo = EXP3(n_arms, learning_rate)
        elif algorithm == 'my_exp3':
            learning_rate = 0.1
            algo = my_EXP3(n_arms, learning_rate)
        
        
        chosen_arms = []
        for t in range(num_iterations):
            chosen_arm = algo.select_arm()
            chosen_arms.append(chosen_arm)
            #reward = rewards[chosen_arm]#10 #pull_arm(chosen_arm)
            reward = pull_arm(chosen_arm, reward_probs)
            # golden_reward = pull_arm(np.argmax(reward_probs), reward_probs)
            # regret = calculate_regret(reward_probs, chosen_arms, t+1)
            # algo_regret[t] = regret[t]
            algo_reward[t] = reward
            algo.update(chosen_arm, reward)
        # regret_data.append(algo_regret)
        reward_data.append(algo_reward)
            
        
        
        # ax = plt.hist(chosen_arms,density=True,bins=n_arms,rwidth=0.5)
        fig, ax1 = plt.subplots()
        ax1.hist(chosen_arms,density=True,bins=range(n_arms+1),rwidth=0.5,color='tab:blue',align='left')
        # ax1.hist(chosen_arms,density=True,bins=n_arms,rwidth=0.5,color='tab:blue',align='left')
        ax1.set_ylabel("Prob. of choosing arm",color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.set_ylim(0,1)
        
        ax2 = ax1.twinx()
        ax2.scatter(range(n_arms),reward_probs,color='red')
        ax2.set_ylabel("True reward probs",color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.set_ylim(0,1)
        fig.suptitle(algorithm)
    # return regret_data
    return reward_data
    
def rolling_mean(input_list, window_size):
    if window_size <= 0:
        raise ValueError("Window size must be greater than 0")
    
    rolling_means = []
    current_sum = 0
    
    for i in range(len(input_list)):
        current_sum += input_list[i]
        
        if i >= window_size - 1:
            if i >= window_size:
                current_sum -= input_list[i - window_size]
            rolling_means.append(current_sum / window_size)
    
    return rolling_means

#### Usage
###n_arms = 5
###reward_probs = np.random.rand(n_arms)
###num_iterations = 10000
###window_size = 1000
###algorithms = ['greedy','epsilon_greedy','UCB','thompson_sampling','exp3']
###
###
###reward_data = run_algos(algorithms, num_iterations - window_size + 1, n_arms, window_size)
###plt.figure(figsize=(10, 6))
###for i, algo_reward in enumerate(reward_data):
###    smoothed_reward = rolling_mean(algo_reward, window_size) #np.convolve(algo_reward, np.ones(window_size) / window_size, mode='valid')
###    plt.plot(np.arange(window_size, num_iterations - window_size + 1 + 1), smoothed_reward, label=algorithms[i])
###plt.xlabel('Number of Iterations')
###plt.ylabel('Average Reward')
###plt.title('Reward Comparison for Multi-Armed Bandit Algorithms')
###plt.legend()
###plt.grid(True)
###plt.show()

'''
regret_data = run_algos(algorithms, num_iterations - window_size + 1, n_arms, window_size)

plt.figure(figsize=(10, 6))
for i, algo_regret in enumerate(regret_data):
    smoothed_regret = np.convolve(algo_regret, np.ones(window_size) / window_size, mode='valid')
    plt.plot(np.arange(window_size, num_iterations - window_size + 1 + 1), smoothed_regret, label=algorithms[i])
    # plt.plot(np.arange(1, num_iterations+1), algo_regret, label=algorithms[i])
    

plt.xlabel('Number of Iterations')
plt.ylabel('Regret')
plt.title('Regret Comparison for Multi-Armed Bandit Algorithms')
plt.legend()
plt.grid(True)
plt.show()
'''
    
        #self.arm_test_ids = [-1 for i in range(self.n_arms)] # each arm is associated with a array of testcases
        #                                    # for new arm, instead of array we use -1 to ask fuzzer to generate seed
    #def update_arm_test_ids(self, test_id_arm_id_pairs): 
    #    for test_id, arm_id in test_id_arm_id_pairs: 
    #        if self.arm_test_ids[arm_id] == -1: # new arm
    #            self.arm_test_ids[arm_id] = [test_id]
    #        else: 
    #            self.arm_test_ids[arm_id].append(test_id)


    #    ## if need to check, check and make sure that all arms have seeds assigned
    #    #if do_check == 'check': 
    #    #    orig_arms = set(range(n_arms)) # no of particles is same as batch size
    #    #    seed_arms = set([i[1] for i in seed_id_arm_id_pairs])
    #    #    assert orig_arms == seed_arms, f"each arm is not getting one seed, {n_arms}, {seed_id_arm_id_pairs}"
            