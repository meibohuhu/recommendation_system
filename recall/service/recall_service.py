from recall.context import Context
from typing import List
import recall.strategy as strategy
import concurrent.futures
import time
from recall import util


strategies: List[strategy.RecallStrategy] = [
    strategy.HighRatingStrategy(),
    strategy.MostRatingStrategy(),
]

def anime_recall(context: Context, n=20) -> List[int]:
    """
    returns a list of anime ids
    """
    pass

def similar_animes(context: Context, n=20) -> List[int]:
    pass

def run_strategy(strategy: strategy.RecallStrategy, context: Context, n):
    pass
