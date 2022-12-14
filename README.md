# Binomial Pricing Model
## Video Demo: https://youtu.be/JbPrwPxZu8I
## Description:
This program uses the binomial model to price European or American Call/Put options. The theory behind the model is based on chapter 13 in the book "Options, Futures and Other Derivatives" by John C. Hull. The price the option a binomial tree is used where the price is deducted recursively by going backwards through the tree.

## How to use
The program takes the following input parameters
* S: Stock price
* K: Strike price
* v: volatility
* r: risk-free rate (continously compounded)
* time: time to expiration
* steps: steps in the tree
* Type: Call or Put
* Class: E for European, A for American
* Plot: Yes, Y or No

## Example
Using the following parameters should return an option price of 18.0274.

optionPrice(50, 45, 0.3, 0.05, 4, 4, "Call", "E", "Y")

## Plotting the binomial tree
In addition the program can save a plot of the binomial tree. Like illustraded below. The graph is saved to the current folder. Make sure that you set the obtion Plot = "Y" like -> optionPrice(x, x, x, x, x, x, x, x, "Y")


![Binomial Tree](BinomialTree.png?raw=true "Binomial Tree")

## Development considerations
I thought about letting the program call the user for input but thought it would be annoying in the long run to have to answer each of the scripts input queries. Instead the user manually chooses the parameters in the main function. But future improvement could definitely be implementing validation of user inputs.

In addition the program does not consider and visualize where American options would be exercized early at each step in the tree. This could be implemented in the future.
