from recall.strategy.recall_strategy import RecallStrategy
import recall.dataset.anime as dataset


class SimpleRecallStrategy(RecallStrategy):

    def __init__(self) -> None:
        super().__init__()
    
    def name(self):
        return 'Simple'
    
    def recall(self, context, n):  
        (anime_df, _) = dataset.load_dataset()
        print(f'Fetched {len(anime_df)} recall results')

        return anime_df.iloc[:n].index.to_list()   ## locate index of n rows in excel, return list of indexes

