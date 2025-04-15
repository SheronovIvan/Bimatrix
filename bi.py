import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def solve_game():
    try:
        A = np.array([[float(entry_A11.get()), float(entry_A12.get())],
                      [float(entry_A21.get()), float(entry_A22.get())]])
        B = np.array([[float(entry_B11.get()), float(entry_B12.get())],
                      [float(entry_B21.get()), float(entry_B22.get())]])
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте ввод! Все поля должны содержать числа.")
        return

    

    # Поиск чистых равновесий Нэша
    nash_pure = []
    for i in range(2):
        for j in range(2):
            # Проверка максимума в столбце для A
            is_max_A = A[i, j] == np.max(A[:, j])
            # Проверка максимума в строке для B
            is_max_B = B[i, j] == np.max(B[i, :])
            if is_max_A and is_max_B:
                nash_pure.append((i, j))

    # Вывод результатов для чистых стратегий
    if nash_pure:
        output_text.insert(tk.END, "Найдены чистые равновесия Нэша:\n")
        for (i, j) in nash_pure:
            output_text.insert(tk.END, 
                f"• Стратегия ({i+1}, {j+1}) → Выигрыши: ({A[i,j]}, {B[i,j]})\n")
    else:
        output_text.insert(tk.END, "Чистых равновесий не найдено.\n")

    # Расчет смешанных равновесий
    try:
        delta_A = A[0,0] - A[0,1] - A[1,0] + A[1,1]
        delta_B = B[0,0] - B[1,0] - B[0,1] + B[1,1]
        
        q = (A[1,1] - A[0,1]) / delta_A if delta_A != 0 else 0.5
        p = (B[1,1] - B[1,0]) / delta_B if delta_B != 0 else 0.5
        
        q = np.clip(q, 0.0, 1.0)
        p = np.clip(p, 0.0, 1.0)
        
        valid_mixed = (0 <= p <= 1) and (0 <= q <= 1)
        
        if valid_mixed and not nash_pure:
            output_text.insert(tk.END, "\nНайдено смешанное равновесие:\n")
            output_text.insert(tk.END, f"• p* = ({p:.3f}; {1-p:.3f})\n")
            output_text.insert(tk.END, f"• q* = ({q:.3f}; {1-q:.3f})\n")
            
            # Расчет ожидаемых выигрышей
            payoff_A = p*q*A[0,0] + p*(1-q)*A[0,1] + (1-p)*q*A[1,0] + (1-p)*(1-q)*A[1,1]
            payoff_B = p*q*B[0,0] + p*(1-q)*B[0,1] + (1-p)*q*B[1,0] + (1-p)*(1-q)*B[1,1]
            
            output_text.insert(tk.END, f"\nОжидаемые выигрыши:\n")
            output_text.insert(tk.END, f"• Игрок 1: {payoff_A:.3f}\n")
            output_text.insert(tk.END, f"• Игрок 2: {payoff_B:.3f}\n")
            
    except Exception as e:
        output_text.insert(tk.END, f"\nОшибка при расчете смешанных стратегий: {str(e)}")

    # Построение графиков
    for widget in frame_plot.winfo_children():
        widget.destroy()
        
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("Вероятность p", fontsize=12)
    ax.set_ylabel("Вероятность q", fontsize=12)
    ax.set_title("Линии лучших ответов", fontsize=14, pad=20)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Линия BR1 для игрока 1 (толщина 3)
    q_values = np.linspace(0, 1, 100)
    p_br1 = []
    for q in q_values:
        payoff_1_1 = q*A[0,0] + (1-q)*A[0,1]  # Ожидаемый выигрыш за строку 1
        payoff_1_2 = q*A[1,0] + (1-q)*A[1,1]  # Ожидаемый выигрыш за строку 2
        
        if payoff_1_1 > payoff_1_2:
            p_br1.append(1.0)
        elif payoff_1_1 < payoff_1_2:
            p_br1.append(0.0)
        else:
            p_br1.append(0.5)
            
    ax.plot(p_br1, q_values, 'b-', linewidth=3, label="BR1 (Игрок 1)")

    # Линия BR2 для игрока 2 (толщина 3)
    p_values = np.linspace(0, 1, 100)
    q_br2 = []
    for p in p_values:
        payoff_2_1 = p*B[0,0] + (1-p)*B[1,0]  # Ожидаемый выигрыш за столбец 1
        payoff_2_2 = p*B[0,1] + (1-p)*B[1,1]  # Ожидаемый выигрыш за столбец 2
        
        if payoff_2_1 > payoff_2_2:
            q_br2.append(1.0)
        elif payoff_2_1 < payoff_2_2:
            q_br2.append(0.0)
        else:
            q_br2.append(0.5)
            
    ax.plot(p_values, q_br2, 'r-', linewidth=3, label="BR2 (Игрок 2)")



    # Отображение равновесий
    legend_added = False
    
    for (i, j) in nash_pure:
        ax.plot(i, j, 's', markersize=12, markerfacecolor='lime', 
                markeredgecolor='black', label=f'Чистое равновесие ({i+1},{j+1})')

        
    if valid_mixed and not nash_pure:
        ax.plot(p, q, 'X', markersize=15, markerfacecolor='lime', 
                markeredgecolor='black', label='Смешанное равновесие')
        legend_added = True

    if legend_added:
        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI
root = tk.Tk()
root.title("Анализ биматричной игры 2x2")
root.geometry("1000x800")

# Фрейм для матриц
frame_matrices = tk.Frame(root)
frame_matrices.pack(pady=10)

# Матрица A
frame_A = tk.LabelFrame(frame_matrices, text=" Матрица A (Игрок 1) ", font=('Arial', 10))
frame_A.grid(row=0, column=0, padx=10)

labels_A = [
    [tk.Label(frame_A, text="Столбец 1", width=8), tk.Label(frame_A, text="Столбец 2", width=8)],
    [tk.Label(frame_A, text="Строка 1"), tk.Label(frame_A, text="Строка 2")]
]

entry_A11 = tk.Entry(frame_A, width=8)
entry_A12 = tk.Entry(frame_A, width=8)
entry_A21 = tk.Entry(frame_A, width=8)
entry_A22 = tk.Entry(frame_A, width=8)

# Расположение элементов
labels_A[0][0].grid(row=0, column=1, padx=5)
labels_A[0][1].grid(row=0, column=2, padx=5)
labels_A[1][0].grid(row=1, column=0, padx=5)
labels_A[1][1].grid(row=2, column=0, padx=5)

entry_A11.grid(row=1, column=1)
entry_A12.grid(row=1, column=2)
entry_A21.grid(row=2, column=1)
entry_A22.grid(row=2, column=2)

# Матрица B
frame_B = tk.LabelFrame(frame_matrices, text=" Матрица B (Игрок 2) ", font=('Arial', 10))
frame_B.grid(row=0, column=1, padx=10)

labels_B = [
    [tk.Label(frame_B, text="Столбец 1", width=8), tk.Label(frame_B, text="Столбец 2", width=8)],
    [tk.Label(frame_B, text="Строка 1"), tk.Label(frame_B, text="Строка 2")]
]

entry_B11 = tk.Entry(frame_B, width=8)
entry_B12 = tk.Entry(frame_B, width=8)
entry_B21 = tk.Entry(frame_B, width=8)
entry_B22 = tk.Entry(frame_B, width=8)

# Расположение элементов
labels_B[0][0].grid(row=0, column=1, padx=5)
labels_B[0][1].grid(row=0, column=2, padx=5)
labels_B[1][0].grid(row=1, column=0, padx=5)
labels_B[1][1].grid(row=2, column=0, padx=5)

entry_B11.grid(row=1, column=1)
entry_B12.grid(row=1, column=2)
entry_B21.grid(row=2, column=1)
entry_B22.grid(row=2, column=2)

# Кнопка решения
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
solve_button = tk.Button(button_frame, text="Анализировать игру", command=solve_game, 
                        font=('Arial', 12), bg='#4CAF50', fg='white')
solve_button.pack()

# Вывод результатов
output_text = tk.Text(root, height=15, width=80, font=('Courier New', 10))
output_text.pack(pady=10, padx=10)

# Область для графиков
frame_plot = tk.Frame(root)
frame_plot.pack(fill=tk.BOTH, expand=True)

root.mainloop()
