import multiprocessing as mp
import tqdm


class MonteCarloEngine:
    def __init__(self):
        self.npools = mp.cpu_count()
        self.pool = mp.Pool(self.npools)

    def compute(self, obj, n_simulations, parallel=False):
        if parallel:
            print(f"Monte-Carlo computing with {self.npools} processors.")
            x = self.pool.imap_unordered(
                obj.simulate, range(n_simulations), chunksize=100
            )
        else:
            print(f"Monte-Carlo computing with 1 processor.")
            x = map(obj.simulate, range(n_simulations))
        return list(tqdm.tqdm(x, total=n_simulations, ncols=75))
