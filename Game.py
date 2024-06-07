# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import os
import random

instances = "./instances"
# List to store the full paths of files

files = []
    
# Traverse files in the directory
for filename in os.listdir(instances):
    full_path = os.path.join(instances, filename)
    if os.path.isfile(full_path):
        files.append(full_path)

# +
def read_random_file(filepath = None):
    # Choose a random file from the list
    if not filepath == None:
        random_file = filepath
    else:    
        random_file = random.choice(files)
    grid = {}
    number_of_groups = 0

    with open(random_file, 'r', encoding='utf-8') as file:
        for line in file:
            numbers = line.split()
            row = int(numbers[0])
            col = int(numbers[1])
            group = int(numbers[2])
            number_of_groups = max(group, number_of_groups)
            if len(numbers) == 4:
                value = int(numbers[3])
            else:
                value = 0
            
            grid[(row, col)] = (value, group)
    h, w = (max(grid))
    grid = [[grid[(i, j)] for j in range(w + 1)] for i in range(h + 1)]
    
    return random_file,grid, number_of_groups + 1

def convert(grid):
    """convert a grid from the format in the solver to the format in the interface"""
    Ncells = max([grid[i,j,1] for i in range(len(grid)) for j in range(len(grid[1]))])
    Newgrid = [[None for i in range(len(grid[1]))]for j in range(len(grid))]
    for j in range(len(grid[1])):
        for i in range(len(grid)):
            if grid[i,j,0] == -1:
                Newgrid[i][j] = (0,grid[i,j,1])
            else:Newgrid[i][j] = (grid[i,j,0],grid[i,j,1]-1)
    return (Newgrid,Ncells)


