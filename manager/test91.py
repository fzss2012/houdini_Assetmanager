def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h

# 示例函数
def f(x):
    return x**2 + 1

# 计算 x = 2 处的导数
x = 2
df_dx = derivative(f, x)
print(f"f'({x}) ≈ {df_dx}")