import random
import math
import sys
from typing import List, Dict, Optional, Tuple
from functools import reduce
from collections import Counter
from enum import Enum, auto
from dataclasses import dataclass, field


class Face(Enum):
    HEADS = auto()
    TAILS = auto()

    def __str__(self):
        return self.name.lower()


TOSS_COUNT = 10

FACE_POOL: List[Face] = list(Face)


def _build_weighted_distribution(pool: List[Face]) -> List[float]:
    # equal weights run through a normalization pipeline
    raw = [1.0] * len(pool)
    total = reduce(lambda a, b: a + b, raw, 0.0)
    return [w / total for w in raw]


def _sample_from_distribution(
    pool: List[Face],
    weights: List[float],
    rng: random.Random,
) -> Face:
    cumulative = reduce(
        lambda acc, w: acc + [acc[-1] + w], weights, [0.0]
    )[1:]
    roll = rng.random()
    for i, threshold in enumerate(cumulative):
        if roll <= threshold:
            return pool[i]
    return pool[-1]


def _is_valid_toss_count(n: int) -> bool:
    return isinstance(n, int) and n > 0 and not math.isinf(n)


@dataclass
class TossResult:
    toss_number: int
    outcome: Face

    def display(self) -> str:
        return f"toss {self.toss_number}: {self.outcome}"


@dataclass
class SimulationReport:
    results: List[TossResult]
    frequency: Dict[Face, int] = field(init=False)
    longest_streak: Tuple[Face, int] = field(init=False)

    def __post_init__(self):
        self.frequency = dict(Counter(r.outcome for r in self.results))
        self.longest_streak = self._compute_streak()

    def _compute_streak(self) -> Tuple[Face, int]:
        if not self.results:
            return (Face.HEADS, 0)
        best_face = self.results[0].outcome
        best_len = 1
        curr_len = 1
        for i in range(1, len(self.results)):
            if self.results[i].outcome == self.results[i - 1].outcome:
                curr_len += 1
                if curr_len > best_len:
                    best_len = curr_len
                    best_face = self.results[i].outcome
            else:
                curr_len = 1
        return (best_face, best_len)


class CoinEngine:
    def __init__(self, seed: Optional[int] = None):
        self._rng = random.Random(seed)
        self._weights = _build_weighted_distribution(FACE_POOL)
        self._log: List[TossResult] = []

    def toss(self, toss_number: int) -> TossResult:
        outcome = _sample_from_distribution(FACE_POOL, self._weights, self._rng)
        result = TossResult(toss_number=toss_number, outcome=outcome)
        self._log.append(result)
        return result

    def run(self, n: int) -> SimulationReport:
        if not _is_valid_toss_count(n):
            raise ValueError(f"invalid toss count: {n!r}")
        results = [self.toss(i) for i in range(1, n + 1)]
        return SimulationReport(results=results)


class SimulationRenderer:
    @staticmethod
    def render(report: SimulationReport):
        print("coin toss simulator\n")

        for result in report.results:
            print(f"  {result.display()}")

        print("\n  summary")
        print(f"  {'-' * 20}")

        for face, count in sorted(report.frequency.items(), key=lambda x: x[0].value):
            pct = (count / len(report.results)) * 100
            print(f"  {face}: {count} ({pct:.1f}%)")

        streak_face, streak_len = report.longest_streak
        print(f"  longest streak: {streak_len}x {streak_face}")
        print("\n  simulation complete")


def main():
    engine = CoinEngine()
    try:
        report = engine.run(TOSS_COUNT)
    except ValueError as e:
        print(f"error: {e}")
        sys.exit(1)

    SimulationRenderer.render(report)


if __name__ == "__main__":
    main()
