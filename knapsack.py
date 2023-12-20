import numpy as np


class GA_knapsack():
    def __init__(self, names, costs, importances, budget, n=10, N=100):
        self.n = n  # 親個体数、子個体数
        self.N = N # 世代数

        self.budget = budget  # 予算
        self.number_of_items = len(names)  # 商品の総数
        self.names = names  # 商品名
        self.costs = costs  # 値段
        self.importances = importances  # 重要度

    def crossover(self, ind1, ind2):
        id = np.sort(np.random.randint(low=0, high=self.number_of_items, size=2))
        ind1_tmp = ind1[id[0]:id[1]]
        ind2_tmp = ind2[id[0]:id[1]]
        ind1[id[0]:id[1]] = ind2_tmp
        ind2[id[0]:id[1]] = ind1_tmp
        return ind1, ind2

    def mutation(self, ind):
        id = np.random.randint(low=0, high=self.number_of_items)
        p = np.random.uniform(0, 1)
        if p<0.10:
            if ind[id]==0:
                ind[id] = 1
            else:
                ind[id] = 0
        return ind

    def evaluate(self, pop):
        reputations = []
        for ind in pop:
            cost = sum(self.costs[ind==1])
            if cost > self.budget:
                reputations.append(0)
            else:
                reputations.append(sum(self.importances[ind==1]))
        return reputations
    

def main(names, costs, importances, budget):
    names = np.array(names)
    costs = np.array(costs, dtype=int)
    importances = np.array(importances, dtype=int)
    n = 20  # 親個体数、子個体数
    N = 500 # 世代数
    budget = int(budget)  # 予算
    number_of_items = len(names)   # 商品の総数

    ga = GA_knapsack(names, costs, importances, budget, n, N)
    while True:
        # ランダムにn個体を生成
        pop = np.array([np.random.randint(low=0, high=2, size=number_of_items) for _ in range(n) ])
        # 個体を評価、ソート
        reputations = ga.evaluate(pop)
        pop = pop[np.argsort(reputations)[::-1]]
        if np.max(reputations)>0:
            break
    replist = []
    for g in range(ga.N):
        # 子個体を生成
        offspring = pop.copy()
        for i, ind1, ind2 in zip(range(len(offspring[::2])), offspring[::2], offspring[1::2]):
            ind1, ind2 = ga.crossover(ind1, ind2)
            ind1, ind2 = ga.mutation(ind1), ga.mutation(ind2)
            offspring[::2][i], offspring[1::2][i] = ind1, ind2
        offspring[-1] = np.random.randint(low=0, high=2, size=number_of_items)
        offspring[-2] = np.random.randint(low=0, high=2, size=number_of_items)
        # 集団を評価し、ソート
        pop = np.vstack([pop, offspring])
        reputations = ga.evaluate(pop)
        pop = pop[np.argsort(reputations)[::-1]]
        # 次世代の親個体を選出
        pop = pop[:ga.n]
        replist.append(np.sort(reputations)[::-1][0])

    best_solution = names[pop[0]==1]
    total = sum(costs[pop[0]==1])
    satisfy = sum(importances[pop[0]==1])

    return best_solution, total, satisfy