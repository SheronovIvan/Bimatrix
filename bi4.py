import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

p_s = 0
q_s = 0
def solve_game():
    try:
        A = np.array([[float(entry_A11.get()), float(entry_A12.get())],
                      [float(entry_A21.get()), float(entry_A22.get())]])
        B = np.array([[float(entry_B11.get()), float(entry_B12.get())],
                      [float(entry_B21.get()), float(entry_B22.get())]])
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте ввод! Все поля должны содержать числа.")
        return

    output_text.delete('1.0', tk.END)

    # Поиск чистых равновесий Нэша
    nash_points = []
    for i in range(2):
        for j in range(2):
            a_col = A[:, j]
            if A[i, j] != np.max(a_col):
                continue
            b_row = B[i, :]
            if B[i, j] == np.max(b_row):
                nash_points.append((i, j))
    
    if nash_points:
        output_text.insert(tk.END, "Найдены чистые равновесия Нэша:\n")
        for (i, j) in nash_points:
            output_text.insert(tk.END, 
                f"Стратегия ({i+1}, {j+1}) → Выигрыши: ({A[i,j]}, {B[i,j]})\n")
        a11, a12, a21, a22 = A.flatten()
        b11, b12, b21, b22 = B.flatten()

        C = a11 - a12 - a21 + a22
        alpha = a22 - a12
        D = b11 - b12 - b21 + b22
        beta = b22 - b21
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

               output_text.insert(tk.END, f"• p* = ({p:.3f}; {1-p:.3f})\n")
               output_text.insert(tk.END, f"• q* = ({q:.3f}; {1-q:.3f})\n")
               output_text.insert(tk.END, f"\nОжидаемые выигрыши:\nИгрок 1: {H_a:.3f}\nИгрок 2: {H_b:.3f}\n")      
               #p_s = p
               #q_s = q
    
    else:
    
        output_text.insert(tk.END, "Чистых равновесий не найдено\n")
        
        # Расчет смешанных стратегий
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

        q_star = solutions[0][1]
        p_star = solutions[0][0]
        q_star = np.clip(q_star, 0, 1)
        p_star = np.clip(p_star, 0, 1)
        p_s = p_star
        q_s = q_star

        output_text.insert(tk.END, "\nСмешанные стратегии:\n")
        output_text.insert(tk.END, f"• p* = ({p_star:.3f}; {1-p_star:.3f})\n")
        output_text.insert(tk.END, f"• q* = ({q_star:.3f}; {1-q_star:.3f})\n")

        # Расчет выигрышей
        payoff_A = p_star*(q_star*a11 + (1-q_star)*a12) + (1-p_star)*(q_star*a21 + (1-q_star)*a22)
        payoff_B = p_star*(q_star*b11 + (1-q_star)*b12) + (1-p_star)*(q_star*b21 + (1-q_star)*b22)
        output_text.insert(tk.END, f"\nОжидаемые выигрыши:\nИгрок 1: {payoff_A:.3f}\nИгрок 2: {payoff_B:.3f}\n")

    # Построение графика
    for widget in frame_plot.winfo_children():
        widget.destroy()
        
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(-0.1,1.1)
    ax.set_ylim(-0.1,1.1)
    ax.set_xlabel('p')
    ax.set_ylabel('q')
    ax.set_title('Линии лучших ответов')
    ax.grid(True, linestyle='--', alpha=0.5)

    if nash_points:
        p_s = beta / D if D != 0 else None
        q_s = alpha / C if C != 0 else None

    
    lines_q = []
    if 0 <= q_s <= 1:
        lines_q.append(((0, q_s), (0, 1)))  
    if 0 <= q_s <= 1:
        lines_q.append(((0, q_s), (1, q_s)))            
    if 0 <= q_s <= 1:
        lines_q.append(((1, q_s), (1, 0)))           

    lines_p = []
    if 0 <= p_s <= 1:
        lines_p.append(((p_s, 0), (1, 0)))  
    if 0 <= p_s <= 1:
        lines_p.append(((p_s, 0), (p_s, 1)))  
    if 0 <= p_s <= 1:
        lines_p.append(((p_s, 1), (0, 1)))   

    for start, end in lines_q:
        ax.plot([start[0], end[0]], [start[1], end[1]], 'green', linewidth=2)

    for start, end in lines_p:
        ax.plot([start[0], end[0]], [start[1], end[1]], 'blue', linewidth=2)
    # Линии лучших ответов

    '''
    q = np.linspace(0,1,300)
    p_br1 = np.piecewise(q, 
        [q < q_s, q > q_s], 
        [1, 0, 0.5]) if 'q_s' in locals() else np.zeros(300)
    ax.plot(p_br1, q, 'b-', lw=2)

    p = np.linspace(0,1,300)
    q_br2 = np.piecewise(p, 
        [p < p_s, p > p_s], 
        [1, 0, 0.5]) if 'p_s' in locals() else np.zeros(300)
    ax.plot(p, q_br2, 'r-', lw=2)
    '''
    # Отображение точек равновесия
    for (i,j) in nash_points:
        ax.plot(1-i, 1-j, 'o', markersize=12, markerfacecolor='lime', 
              markeredgecolor='black', label=f'Равновесие ({i+1},{j+1})')
    
    if not nash_points and (0 <= p_star <= 1) and (0 <= q_star <= 1):
        ax.plot(p_star, q_star, 'X', markersize=10, markerfacecolor='gold',
              markeredgecolor='black', label='Смешанное равновесие')

    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI
root = tk.Tk()
root.title("Анализ игры 2x2")
root.geometry("900x750")  # Размер главного окна
root.minsize(800, 500)    # Минимальный размер

# Настройки шрифтов
entry_font = ('Arial', 12)
button_font = ('Arial', 12, 'bold')
output_font = ('Consolas', 11)

frame_input = tk.Frame(root)
frame_input.pack(pady=20)

# Матрица A
frame_A = tk.LabelFrame(frame_input, text="Матрица A", font=('Arial', 12), labelanchor='n')
frame_A.grid(row=0, column=0, padx=15, pady=1)

entry_A11 = tk.Entry(frame_A, width=8, font=entry_font)
entry_A11.grid(row=0, column=0, padx=5, pady=3)  
entry_A12 = tk.Entry(frame_A, width=8, font=entry_font)
entry_A12.grid(row=0, column=1, padx=5, pady=3)
entry_A21 = tk.Entry(frame_A, width=8, font=entry_font)
entry_A21.grid(row=1, column=0, padx=5, pady=3)
entry_A22 = tk.Entry(frame_A, width=8, font=entry_font)
entry_A22.grid(row=1, column=1, padx=5, pady=3)

# Матрица B
frame_B = tk.LabelFrame(frame_input, text="Матрица B", font=('Arial', 12), labelanchor='n')
frame_B.grid(row=0, column=1, padx=15, pady=1)

entry_B11 = tk.Entry(frame_B, width=8, font=entry_font)
entry_B11.grid(row=0, column=0, padx=5, pady=3)
entry_B12 = tk.Entry(frame_B, width=8, font=entry_font)
entry_B12.grid(row=0, column=1, padx=5, pady=3)
entry_B21 = tk.Entry(frame_B, width=8, font=entry_font)
entry_B21.grid(row=1, column=0, padx=5, pady=3)
entry_B22 = tk.Entry(frame_B, width=8, font=entry_font)
entry_B22.grid(row=1, column=1, padx=5, pady=3)


# Кнопка решения
button_solve = tk.Button(
    root, 
    text="Решить", 
    command=solve_game,
    font=button_font,
    bg='#4CAF50',
    fg='white',
    padx=10,
    pady=5
)
button_solve.pack(pady=(5, 5)) 

# Вывод результатов
output_text = tk.Text(
    root, 
    height=10,          # 15 строк высотой
    width=80,           # 80 символов в ширину
    font=output_font,
    wrap=tk.WORD        # Перенос по словам
)
output_text.pack(pady=(5, 10))

# Область для графика
frame_plot = tk.Frame(root)
frame_plot.pack(fill=tk.BOTH, expand=True, padx=200, pady=10)

root.mainloop()