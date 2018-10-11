"""pipeline.py

Util functions for working with pipelines"""

__author__ = 'tinglev@kth.se'

def create_pipeline_from_array(array_of_steps):
    if len(array_of_steps) < 2:
        return array_of_steps
    for i in range(len(array_of_steps) - 1):
        array_of_steps[i].set_next_step(array_of_steps[i+1])
    return array_of_steps
