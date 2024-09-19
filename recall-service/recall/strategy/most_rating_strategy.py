from recall.strategy.recall_strategy import RecallStrategy
import recall.dataset.anime as dataset
from random import sample
from recall.config import config


class MostRatingStrategy(RecallStrategy):
    def __init__(self):
        super().__init__()
        self.build_pool()

    def name(self):
        return 'MostRating'
    
    def build_pool(self):    ## create 500 pool for animes
        (anime_df, _) = dataset.load_dataset()
        sorted_df = anime_df.sort_values(by=['members'], ascending=False)
        self.pool = sorted_df.iloc[:500].index.to_list()   ## self.pool private variable 
        print(f'{self.name()} pool loaded.')


    def recall(self, context, n):   ## pick up n elements from pool
        if config['most_rating']['shuffle_sample']:    ## true/false
            return sample(self.pool, n)

        return self.pool[:n]    ## otherwise return first n elements
