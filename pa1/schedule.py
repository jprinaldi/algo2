#!/usr/bin/env python3

"""
Implementation of two different greedy algorithms for scheduling
jobs in order to minimize the weighted sum of completion times.
"""

import argparse

class Job:
    def __init__(self, weight, length):
        self.weight = weight
        self.length = length
    def __repr__(self):
        return str(self.weight)+" "+str(self.length)
        
class JobDiff(Job):
    def __init__(self, weight, length):
        super().__init__(weight, length)
        self.diff = weight - length
    def __lt__(self, that):
        if self.diff == that.diff:
            return self.weight < that.weight
        else:
            return self.diff < that.diff

class JobRatio(Job):
    def __init__(self, weight, length):
        super().__init__(weight, length)
        self.ratio = weight/length
    def __lt__(self, that):
        return self.ratio < that.ratio

def parse_file(filename):
    job_diffs = []
    job_ratios = []
    with open(filename) as f:
        num_jobs = int(next(f))
        for line in f:
            weight, length = [int(x) for x in line.split()]
            job_diff = JobDiff(weight, length)
            job_ratio = JobRatio(weight, length)
            job_diffs.append(job_diff)
            job_ratios.append(job_ratio)
    return job_diffs, job_ratios

def schedule(jobs):
    jobs.sort(reverse=True)
    completion_time = 0
    sum_ = 0
    for job in jobs:
        completion_time += job.length
        sum_ += job.weight * completion_time
    return sum_

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule jobs greedily")
    parser.add_argument('filename', type=str, help="file containing jobs")

    args = parser.parse_args()

    job_diffs, job_ratios = parse_file(args.filename)
    diffs_sum = schedule(job_diffs)
    ratios_sum = schedule(job_ratios)

    print("Weighted sum of completion times using diffs (possibly suboptimal):", diffs_sum)
    print("Weighted sum of completion times using ratios (optimal):", ratios_sum)
