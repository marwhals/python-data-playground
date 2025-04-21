import torch

# Create tensors with requires_grad=True to track computation
x = torch.tensor(3.0, requires_grad=True)
y = torch.tensor(2.0, requires_grad=True)

# Perform tensor operations
z = x ** 2 * y + y ** 3
print(f'result, z: {z}')

# Compute gradients dz/dx and dz/dy
z.backward()

# Print gradients
print(f'dz/dx: {x.grad.item()}')
print(f'dz/dy: {y.grad.item()}')
