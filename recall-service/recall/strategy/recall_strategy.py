from recall.context import Context
from typing import List


class RecallStrategy:    ## interface for all strategies
    def name(self):
        pass

    def recall(self, context: Context, n=20) -> List[int]:
        pass
