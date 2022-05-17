import matplotlib.pyplot as plt
import numpy as np
import roots as r

poly = r.POLY([1,2,3,4,5], n=50)

x = [np.real(i) for i in poly.roots]
y = [np.imag(i) for i in poly.roots]

fig, ax = plt.subplots()
plotted_roots = ax.scatter(x, y)

ax.set_title('drag vertices to update path')
ax.set_xlim(np.amin(x)-3, np.amax(x)+3)
ax.set_ylim(np.amin(y)-3, np.amax(y)+3)
ax.grid(True)

plt.show()