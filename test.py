import numpy as np
import matplotlib.pyplot as plt

# Матрицы выигрышей
A = np.array([[-10, 2],
              [1, -1]])

B = np.array([[5, -2],
              [-1, 1]])
'''
# Матрицы выигрышей
A = np.array([[-1, -9],
              [0, -6]])

B = np.array([[-1, 9],
              [-9, -6]])
'''

# Вычисление параметров
a11, a12, a21, a22 = A[0,0], A[0,1], A[1,0], A[1,1]
b11, b12, b21, b22 = B[0,0], B[0,1], B[1,0], B[1,1]

C = a11 - a12 - a21 + a22
alpha = a22 - a12

D = b11 - b12 - b21 + b22
beta = b22 - b21
print(f"C = {C}, α = {alpha}")
print(f"D = {D}, β = {beta}")   
step = 0.01
for p in np.arange(0, 1+step, step):
    for q in np.arange(0, 1+step, step):
        cond1 = (p - 1)*(C*q - alpha) >= 0
        cond2 = p*(C*q - alpha) >= 0
        cond3 = (q - 1)*(D*p - beta) >= 0
        cond4 = q*(D*p - beta) >= 0
        if cond1 and cond2 and cond3 and cond4:
            # Вычисление выигрышей
            H_a = a11*p*q + a12*p*(1 - q) + a21*(1 - p)*q + a22*(1 - p)*(1 - q)
            H_b = b11*p*q + b12*p*(1 - q) + b21*(1 - p)*q + b22*(1 - p)*(1 - q)
            print(f"p = {p:.2f}, q = {q:.2f} => H_a = {H_a:.2f}, H_b = {H_b:.2f}")

def find_mixed_equilibrium(A, B):
    a11, a12, a21, a22 = A.flatten()
    b11, b12, b21, b22 = B.flatten()
    
    C = a11 - a12 - a21 + a22
    alpha = a22 - a12
    D = b11 - b12 - b21 + b22
    beta = b22 - b21
    
    solutions = []
    
    # Проверка граничных случаев
    for p in [0, 1]:
        for q in [0, 1]:
            if (p == 0 or p == 1) and (q == 0 or q == 1):
                continue  # Уже проверено в чистых стратегиях
            # Проверка условий оптимальности
            cond1 = (p - 1)*(C*q - alpha) >= 0
            cond2 = p*(C*q - alpha) >= 0
            cond3 = (q - 1)*(D*p - beta) >= 0
            cond4 = q*(D*p - beta) >= 0
            if cond1 and cond2 and cond3 and cond4:
                solutions.append((p, q))
    
    # Проверка внутренних точек (если C и D не нули)
    if C != 0 and D != 0:
        p_star = beta / D
        q_star = alpha / C
        if 0 <= p_star <= 1 and 0 <= q_star <= 1:
            cond1 = (p_star - 1)*(C*q_star - alpha) >= 0
            cond2 = p_star*(C*q_star - alpha) >= 0
            cond3 = (q_star - 1)*(D*p_star - beta) >= 0
            cond4 = q_star*(D*p_star - beta) >= 0
            if cond1 and cond2 and cond3 and cond4:
                solutions.append((p_star, q_star))
    
    return solutions

res = find_mixed_equilibrium(A, B)
print(res[0][0], res[0][1])
