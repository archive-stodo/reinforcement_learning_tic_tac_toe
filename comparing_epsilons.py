import numpy as np
import matplotlib.pyplot as plt

class Bandit:

    def __init__(self, m):
        self.m = m
        self.mean = 0
        self.mean_history = []
        self.N = 0

    def pull(self):
        return np.random.randn() + self.m

    def update(self, x):
        self.N += 1
        self.mean = ((1 - 1.0 / self.N) * self.mean) + (1.0 / self.N * x)
        self.mean_history.append(self.mean)

    def reset_stats(self):
        self.mean = 0
        self.mean_history = []
        self.N = 0

class BanditCluster:

    def __init__(self, bandits):
        self.bandits = bandits
        self.actual_results = []
        self.actual_results_over_runs = []
        self.epsilons_over_runs = []

    def reset_bandits_stats(self):
        [bandit.reset_stats() for bandit in self.bandits]

    def run(self, N, eps):
        self.reset_bandits_stats()
        for i in range(N):
            p = np.random.random()
            if p < eps:
                j = np.random.choice(3)
            else:
                j = np.argmax([b.mean for b in self.bandits])

            x = self.bandits[j].pull()
            self.bandits[j].update(x)

            # update other bandits mean_history with their last mean value
            [self.bandits[i].mean_history.append(self.bandits[i].mean) for i in range(len(self.bandits)) if i != j]

            self.actual_results.append(x)

        self.actual_results_over_runs.append(self.actual_results)
        self.actual_results = []
        self.epsilons_over_runs.append(eps)

    def plot_last_run(self):
        cumulative_average = np.cumsum(self.actual_results_over_runs[-1]) / (np.arange(N) + 1)
        plt.plot(cumulative_average, label="results")
        plt.plot(self.bandits[0].mean_history, label="bandit 1")
        plt.plot(self.bandits[1].mean_history, label="bandit 2")
        plt.plot(self.bandits[2].mean_history, label="bandit 3")
        plt.title('Epsilon: ' + str(self.epsilons_over_runs[-1]))
        plt.legend()
        plt.show()

    def plot_actual_results_over_runs(self):
        for i in range(len(self.actual_results_over_runs)):
            cumulative_average = np.cumsum(self.actual_results_over_runs[i]) / (np.arange(N) + 1)
            plt.plot(cumulative_average, label='epsilon: ' + str(self.epsilons_over_runs[i]))

        plt.plot(self.bandits[0].m * np.ones(N), label="bandit 1 mean return")
        plt.plot(self.bandits[1].m * np.ones(N), label="bandit 2 mean return")
        plt.plot(self.bandits[2].m * np.ones(N), label="bandit 3 mean return")

        plt.legend()
        plt.show()

N = 5000
epsilons = [0.1, 0.05, 0.025, 0.01, 0.005]

bandit_cluster = BanditCluster([Bandit(1.0), Bandit(2.0), Bandit(3.0)])
[bandit_cluster.run(N, epsilons[i]) for i in range(len(epsilons))]

bandit_cluster.plot_actual_results_over_runs()