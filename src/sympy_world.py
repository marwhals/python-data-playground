from sympy import symbols, Eq, solve

# declare two symbols
x, y = symbols('x y')

'''
The equation is:

$$x + 5y = 10$$
'''

# declare an equation
equation = Eq(x + 5 * y, 10)

# solve the equation
solution = solve(equation)
print(solution)
