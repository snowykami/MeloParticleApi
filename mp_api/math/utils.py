from ..typing import T_Num

import numpy as np


def arithmetic_sequence(start: T_Num, end: T_Num, num: int) -> list[T_Num]:
    """返回一个等差数列，支持浮点数。

    Args:
        start (T_Num): 数列的起始值。
        end (T_Num): 数列的终止值。
        num (int): 样本数量。

    Returns:
        list[T_Num]: 一个包含等差数列的列表。
    """
    return np.linspace(start, end, num).tolist()