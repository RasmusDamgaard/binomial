import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib import pyplot as plt


def main():
    # Calculate option price and optionally save tree graph
    price = optionPrice(40, 50, 0.3, 0.05, 4, 4, "Put", "E", "Y")
    print("Option price:", price)


def optionPrice(S, K, v, r, time, steps, Type="Call", Class="E", Plot="N"):
    """
    Usage: Price European or American put/call option
    Based on Chapter 13 in Options, Futures and Other Derivatives
    by John C. Hull.

    S: Stock price
    K: Strike price
    v: volatility
    r: risk-free rate (continously compounded)
    time: time to expiration
    steps: steps in the tree
    Type: Call or Put
    Class: E for European, A for American
    Plot: Yes, Y or No

    """
    # Initial Stock price tree
    M = np.zeros((steps + 1, steps + 1))

    # Initial Option price tree
    O = np.zeros((steps + 1, steps + 1))

    # Timesteps
    t = time / steps

    # Discount factor
    df = np.exp(-r * t)

    # Binomial tree formulas
    u = np.exp(v * np.sqrt(t))
    d = 1 / u
    a = np.exp(r * t)
    q = (a - d) / (u - d)

    # Initial stock price
    M[0, 0] = S

    # Build stock price tree
    for i in range(len(M) - 1):
        M[0, i + 1] = d * M[0, i]

    for i in range(len(M) - 1):
        for j in range(len(M) - 1):
            M[i + 1, j + 1] = u * M[i, j]

    # Recursively build option price tree starting from the end
    for i in range(len(M) - 1, -1, -1):
        O[i, len(M) - 1] = payoff(M[i, len(M) - 1], K, Type)

    for i in range(len(M) - 1, 0, -1):
        for j in range(len(M) - 1, 0, -1):
            if Class == "E":
                O[j - 1, i - 1] = (q * O[j, i] + (1 - q) * O[j - 1, i]) * df
            elif Class == "A":
                O[j - 1, i - 1] = max(
                    (q * O[j, i] + (1 - q) * O[j - 1, i]) * df,
                    payoff(M[j - 1, i - 1], K, Type),
                )

    if Plot in ("Y", "Yes"):
        plotTree(M, O, steps)

    return f"{O[0, 0]:.4f}"


def payoff(S, K, Type="Call"):
    """
    Gives payoff of option
    S: Stock price
    K: Strike price
    Type: "Call" or "Put" option

    """
    if Type == "Call":
        return max(S - K, 0)
    elif Type == "Put":
        return max(K - S, 0)


def plotTree(S, O, n):
    """
    Visualizes binomial tree
    Takes a NxN matrix of option prices and NxN matrix of stock prices as inputs.
    Returns None but saves a png of the visualization to the current folder.
    """
    # Convert S, O matrices to array
    Sa = S[np.triu_indices(n + 1)]
    Oa = O[np.triu_indices(n + 1)]

    # figure
    fig = plt.figure(figsize=[5, 5])
    ax = plt.subplot()

    # offset text from tree points
    trans_offset1 = mtransforms.offset_copy(
        ax.transData, fig=fig, x=-0.10, y=0.25, units="inches"
    )

    trans_offset2 = mtransforms.offset_copy(
        ax.transData, fig=fig, x=-0.10, y=0.15, units="inches"
    )

    # Initialize location list for txt
    xm = np.zeros((2 * n + 1, 1))
    ym = np.zeros((2 * n + 1, 1))

    # build tree
    # First part of the loop is inspired by the reply in this thread by Anton Menshov
    # https://stackoverflow.com/questions/33712179/plot-lattice-tree-in-python
    for i in range(n):
        x = [1, 0, 1]
        for j in range(i):
            x.append(0)
            x.append(1)
        x = np.array(x) + i
        y = np.arange(-(i + 1), i + 2)[::-1]
        ax.plot(x, y, "ro-")

        # Create grid for text
        xg = x[::2]
        yg = y[::2]

        # reverse zip list try
        xg = np.flip(xg)
        xg = np.append(xg, np.zeros((2 * n + 1) - len(xg)))

        yg = np.flip(yg)
        yg = np.append(yg, np.zeros((2 * n + 1) - len(yg)))

        # create matrix
        xm = np.column_stack((xm, xg))
        ym = np.column_stack((ym, yg))

    # text coordinates list creation
    Xl = xm[np.triu_indices(n + 1)]
    Yl = ym[np.triu_indices(n + 1)]

    for _, (x, y) in enumerate(zip(Xl, Yl)):
        ax.text(x, y, f"{Oa[_]:.2f}", size="small", transform=trans_offset1)
        ax.text(x, y, f"{Sa[_]:.2f}", size="x-small", transform=trans_offset2)

    # remove borders and axes
    ax.axis("off")

    # print fig
    plt.savefig("BinomialTree")


if __name__ == "__main__":
    main()
