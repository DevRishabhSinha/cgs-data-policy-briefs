import sympy as sp
import scipy.optimize as opt

# Define symbols
theta_1, theta_0 = sp.symbols('theta_1 theta_0')  # theta_1 is the weight, theta_0 is the bias

# Define the sigmoid function
def sigmoid(z):
    return 1 / (1 + sp.exp(-z))

# Define the loss function for a single data point
def loss(y_true, y_pred):
    return -y_true * sp.log(y_pred) - (1 - y_true) * sp.log(1 - y_pred)

# Define the logistic regression model
def model(x, theta_1, theta_0):
    return sigmoid(theta_1 * x + theta_0)

# Training data
x_values = [0, 1, 3, 4]
y_values = [0, 0, 1, 1]

# Total loss for the dataset, divided by the number of data points (average loss)
total_loss = sum(loss(y, model(x, theta_1, theta_0)) for x, y in zip(x_values, y_values)) / len(x_values)

# Define the equations based on total loss < 0.01
equations = [total_loss - 0.01]

# Initial guess for our solver
initial_guess = {theta_1: 1, theta_0: -1.5}

# Convert our equation to a numerical function for optimization
numerical_loss = sp.lambdify((theta_1, theta_0), total_loss, 'numpy')
numerical_equation = sp.lambdify((theta_1, theta_0), equations, 'numpy')

# Objective function for the optimizer: we want it to be as close to 0 as possible
def objective(theta):
    return numerical_loss(theta[0], theta[1])

# Constraint that the total loss must be less than 0.01
constraints = ({'type': 'ineq', 'fun': lambda theta: 0.01 - numerical_loss(theta[0], theta[1])})

# Perform the optimization
result = opt.minimize(objective, x0=list(initial_guess.values()), constraints=constraints)

# Check if the result is successful and the loss is less than 0.01
if result.success and objective(result.x) < 0.01:
    result_vector = result.x
else:
    result_vector = None

result_vector, numerical_loss(result_vector[0], result_vector[1]) if result_vector is not None else "No valid theta found"

print(result_vector)