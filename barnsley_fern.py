import tkinter as tk

import matplotlib

matplotlib.use("TkAgg")
import os
import random
import re
import sys
from bisect import bisect

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

transform_sets = {
    0 : ["0", "0.16*y", 0.01],
    1 : ["0.85*x+0.04*y", "-0.04*x+0.85*y+1.6", 0.85],
    2 : ["0.2*x-0.26*y", "0.23*x+0.22*y+1.6", 0.07],
    3 : ["-0.15*x+0.28*y-0.028", "0.26*x+0.24*y+1.05", 0.07]
}

graph_xlims = (-2, 2)
graph_ylims = (-2, 2)
render_resolution = 50000 # X by X points

def update_graph():
    # Get all transformation sets
    elements = [sublist[1] for sublist in transform_sets.values()]
    probabilities = [sublist[-1] for sublist in transform_sets.values()]

    min_val_x = 100000
    max_val_x = 0
    min_val_y = 100000
    max_val_y = 0

    points = np.zeros((render_resolution, 2), dtype=np.float32)
    current_val = (0,0)
    
    # Generate Points
    for i in range(render_resolution):
        # Get next transformation
        dict_lookup = choose_by_probability(probabilities, elements)
        
        x_s = transform_sets[dict_lookup][0]
        y_s = transform_sets[dict_lookup][1]
        
        # Eval new position
        translation_lambda = lambda x, y: (round(eval(x_s), 2), round(eval(y_s), 2))
        new_val = translation_lambda(current_val[0], current_val[1])
        
        points[i][0] = new_val[0]
        points[i][1] = new_val[1]
        
        # Get bounds
        if new_val[0] > max_val_x: max_val_x = new_val[0]
        elif new_val[0] < min_val_x: min_val_x = new_val[0]
        
        if new_val[1] > max_val_y: max_val_y = new_val[1]
        elif new_val[1] < min_val_y: min_val_y = new_val[1]

        # Iterate
        current_val = new_val

    # Redraw
    a.clear()
    a.set_xlim(min_val_x-1, max_val_x+1)
    a.set_ylim(min_val_y-1, max_val_y+1)
    scatter = a.scatter(points[:, 0], points[:, -1], s=0.01)
    canvas.draw()

def probability_callback(event):
    widget = event.widget
    row = int(widget.grid_info()["row"])
    expression = get_expression_widget(row, 1)
    new_transform = str(expression.get()).split(",")
    transform_sets[row] = [new_transform[0], new_transform[1], float(widget.get())]
    update_graph()

def expression_callback(event):
    widget = event.widget
    new_transform = str(widget.get()).split(",")
    row = int(widget.grid_info()["row"])
    probability = get_expression_widget(row, 3)
    transform_sets[row] = [new_transform[0], new_transform[1], float(probability.get())]
    update_graph()

def get_expression_widget(row, column):
    for widget in expr_frame.grid_slaves():
        if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == column:
            return widget

def choose_by_probability(probabilities, elements):
    population = list(transform_sets.keys())
    weights = [transform_sets[key][-1] for key in transform_sets]
    return random.choices(population,weights)[0]

'''
# Example USAGE:
elements = [sublist[1] for sublist in transform_sets.values()]
probabilities = [sublist[-1] for sublist in transform_sets.values()]
print(choose_by_probability(probabilities, elements))

# lambda translations USAGE
x_x = "x*2+1"
y_x = "y*3-2"
translation_lambda = lambda x, y: (eval(x_x), eval(y_x))
print(translation_lambda(1,2)) # Output: (3, 4)
for i in transform_sets.values():
    this = lambda x, y: (eval(i[0]), eval(i[1]))
    print(this(1, 2))
'''

# GUI
root = tk.Tk()

root.geometry("800x800")  
root.configure(bg='white')
root.resizable(True, True) 
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)

# Creating Frame for graph
graph_frame = tk.Frame(root, bg='white')
graph_frame.grid(row=0, column=0, sticky="nsew")

# Creating Frame for expressions
expr_frame = tk.Frame(root, bg='white')
expr_frame.grid(row=1, column=0, sticky="nsew")

graph_frame.columnconfigure(0, weight=1)
graph_frame.rowconfigure(0, weight=1)

# Graph
f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
a.set_title('Scatter Plot')
a.set_xlim(graph_xlims)
a.set_ylim(graph_ylims)
# # Sine graph in graph_frame


canvas = FigureCanvasTkAgg(f, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Text fields in expr_frame
for i in range(len(transform_sets.values())):
    expr_frame.rowconfigure(i, weight=1)
    expr_frame.columnconfigure(1, weight=1)
    expr_frame.columnconfigure(3, weight=1)

    label = tk.Label(expr_frame, text=str(f"Expression {i+1}"))
    label.grid(row=i, column=0, sticky='nsw')

    txt = tk.Entry(expr_frame)
    txt.insert(tk.END, str(f"{transform_sets[i][0]}, {transform_sets[i][1]}"))
    txt.bind("<Return>", expression_callback)
    txt.grid(row=i, column=1, sticky='nsew')
    
    label = tk.Label(expr_frame, text="Probability (%)")
    label.grid(row=i, column=2, sticky='nsw')
    
    prob_txt = tk.Entry(expr_frame)
    prob_txt.insert(tk.END, str(f"{transform_sets[i][2]}"))
    prob_txt.bind("<Return>", probability_callback)
    prob_txt.grid(row=i, column=3,sticky='nsew')

root.mainloop()