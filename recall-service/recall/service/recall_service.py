from recall.context import Context
from typing import List
import recall.strategy as strategy
import concurrent.futures
import time

strategies: List[strategy.RecallStrategy] = [
    # strategy.SimpleRecallStrategy(),    ## from strategy class, RecallStrategy interface
    strategy.HighRatingStrategy(),
    strategy.MostRatingStrategy(),
    strategy.LargestStrategy()
]

## 猜你喜欢 => recall
def anime_recall(context: Context, n=20) -> List[int]:    ## 返回数据的规模
    """
    returns a list of anime ids
    return outputs: [[1,2,3], [3,4,5]] 不同的策略下，是二维数组
    二维 => 一维新数组 => 用dict去重
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        outputs = executor.map(lambda s: run_strategy(s, context, n), strategies)
        outputs = [aid for l in outputs for aid in l]   ## [[1,2,3], [3,4,5]]
        outputs = list(dict.fromkeys(outputs))   ## 去重
        print(f'Got {len(outputs)} uniq recall results')
        return outputs

## 找相似 => similar
def similar_animes(context: Context, n=20) -> List[int]:
    stra = strategy.SimilarAnimeStrategy()
    return stra.recall(context, n)

def run_strategy(strategy: strategy.RecallStrategy, context: Context, n):
    res = strategy.recall(context, n=n)  ## based on recall strategies, return n 
    print(f'res {res} ')
    return res
