import matplotlib.pyplot as plt

# Введи свои значения матриц A и B
a11, a12 = -10, 2
a21, a22 = 1, -1

b11, b12 = 5, -2
b21, b22 = -1, 1

# Введи свои значения матриц A и B
a11, a12 = -10, 0
a21, a22 = 0, -100

b11, b12 = -10, 50
b21, b22 = 0, -100


# Вычисление вспомогательных коэффициентов
C = a11 - a12 - a21 + a22
alpha = a22 - a12
D = b11 - b12 - b21 + b22
beta = b22 - b21



# Внутренняя точка, если существует
p_star = beta / D if D != 0 else None
q_star = alpha / C if C != 0 else None

# Построение границ области (4 условия)
lines_q = []
if 0 <= q_star <= 1:
    lines_q.append(((0, q_star), (0, 1)))  
if 0 <= q_star <= 1:
    lines_q.append(((0, q_star), (1, q_star)))            
if 0 <= q_star <= 1:
    lines_q.append(((1, q_star), (1, 0)))           

lines_p = []
if 0 <= p_star <= 1:
    lines_p.append(((p_star, 0), (1, 0)))  
if 0 <= p_star <= 1:
    lines_p.append(((p_star, 0), (p_star, 1)))  
if 0 <= p_star <= 1:
    lines_p.append(((p_star, 1), (0, 1)))          

# График
plt.figure(figsize=(6, 6))
for start, end in lines_q:
    plt.plot([start[0], end[0]], [start[1], end[1]], 'r', linewidth=2)

for start, end in lines_p:
    plt.plot([start[0], end[0]], [start[1], end[1]], 'b', linewidth=2)



# Отметка точки равновесия
plt.plot(p_star, q_star, 'ko')
plt.text(p_star + 0.02, q_star + 0.02, f"({round(p_star, 2)}, {round(q_star, 2)})")

# Оформление
plt.xlim(-0.1, 1.05)
plt.ylim(-0.1, 1.05)
plt.xlabel('p')
plt.ylabel('q')
plt.title('Область допустимых смешанных стратегий')
plt.grid(True)
plt.gca().set_aspect('equal')
plt.show()


