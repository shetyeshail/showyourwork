import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
x = np.linspace(-1, 1, 1000)
for sgn in [-1, 1]:
    y = 4.0 / 5.0 * (sgn * np.sqrt(1.0 - x ** 2) + np.sqrt(np.abs(x)))
    plt.plot(x, y, "C0-", lw=2)
plt.xlim(-2.5, 2.5)
plt.gca().axis("off")
fig.savefig("heart.pdf", bbox_inches="tight")
