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
        messagebox.showerror("Ошибка", "Некорректный ввод данных!")
        return

    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, "Матрица A:\n" + str(A) + "\n")
    output_text.insert(tk.END, "Матрица B:\n" + str(B) + "\n\n")

    # Поиск чистых стратегий
    nash_points = []
    for i in range(2):
        for j in range(2):
            # Проверка, является ли (i,j) равновесием Нэша
            a_col = A[:, j]
            if A[i, j] != np.max(a_col):
                continue
            b_row = B[i, :]
            if B[i, j] == np.max(b_row):
                nash_points.append((i, j))

    if nash_points:
        output_text.insert(tk.END, "Найдено равновесие(я) в чистых стратегиях:\n")
        for (i, j) in nash_points:
            output_text.insert(tk.END, f"Стратегия игрока 1: {i+1}, игрока 2: {j+1} -> Выигрыши: ({A[i,j]}, {B[i,j]})\n")
    else:
        output_text.insert(tk.END, "Равновесий в чистых стратегиях нет. Ищем в смешанных...\n")
        a11, a12, a21, a22 = A.flatten()
        b11, b12, b21, b22 = B.flatten()

        C = a11 - a12 - a21 + a22
        alpha = a22 - a12
        D = b11 - b12 - b21 + b22
        beta = b22 - b21

        q_star = alpha / C if C != 0 else 0.5
        p_star = beta / D if D != 0 else 0.5

        q_star = np.clip(q_star, 0, 1)
        p_star = np.clip(p_star, 0, 1)

        output_text.insert(tk.END, f"Оптимальные смешанные стратегии:\n")
        output_text.insert(tk.END, f"Игрок 1: p = {round(p_star, 3)}\n")
        output_text.insert(tk.END, f"Игрок 2: q = {round(q_star, 3)}\n")

        win1 = p_star * (q_star * a11 + (1 - q_star) * a12) + (1 - p_star) * (q_star * a21 + (1 - q_star) * a22)
        win2 = p_star * (q_star * b11 + (1 - q_star) * b12) + (1 - p_star) * (q_star * b21 + (1 - q_star) * b22)
        output_text.insert(tk.END, f"Выигрыши: Игрок 1 = {round(win1, 3)}, Игрок 2 = {round(win2, 3)}\n")

# ... (предыдущий код без изменений)

    # Построение графика
    for widget in frame_plot.winfo_children():
        widget.destroy()
    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Расширенные пределы для визуализации продолжений
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlabel('p (Игрок 1)')
    ax.set_ylabel('q (Игрок 2)')
    ax.set_title('Лучшие ответы и равновесия')
    ax.grid(True, linestyle='--', alpha=0.7)
    


    # Линии лучших ответов с продолжениями
    if not nash_points:
        # Для игрока 1 (p зависит от q)
        q_extended = np.linspace(-0.5, 1.5, 500)
        p_br1 = np.clip((alpha + C * q_extended) / C if C != 0 else np.full_like(q_extended, 0.5), 0, 1)
        mask_inside = (q_extended >= 0) & (q_extended <= 1)
        ax.plot(p_br1[mask_inside], q_extended[mask_inside], 'b-', lw=2, label='BR1 (внутри)')
        ax.plot(p_br1[~mask_inside], q_extended[~mask_inside], 'b--', lw=1, alpha=0.5, label='BR1 (вне)')

        # Для игрока 2 (q зависит от p)
        p_extended = np.linspace(-0.5, 1.5, 500)
        q_br2 = np.clip((beta + D * p_extended) / D if D != 0 else np.full_like(p_extended, 0.5), 0, 1)
        mask_inside = (p_extended >= 0) & (p_extended <= 1)
        ax.plot(p_extended[mask_inside], q_br2[mask_inside], 'r-', lw=2, label='BR2 (внутри)')
        ax.plot(p_extended[~mask_inside], q_br2[~mask_inside], 'r--', lw=1, alpha=0.5, label='BR2 (вне)')

        # Точка смешанного равновесия
        if (0 <= p_star <= 1) and (0 <= q_star <= 1):
            ax.plot(p_star, q_star, 'o', markersize=10, markerfacecolor='gold', 
                    markeredgecolor='black', label='Смешанное равновесие')

    # Чистые равновесия
    pure_nash = [(i, j) for (i, j) in nash_points]
    for (i, j) in pure_nash:
        ax.plot(i, j, 's', markersize=12, markerfacecolor='lime', 
                markeredgecolor='black', label=f'Чистое равновесие ({i+1},{j+1})')

    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1))
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()

# ... (остальной код GUI без изменений)

# GUI
root = tk.Tk()
root.title("Биматричная игра 2x2")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

# Матрица A
frame_A = tk.LabelFrame(frame_input, text="Матрица A")
frame_A.grid(row=0, column=0, padx=5)
tk.Label(frame_A, text="Столбец 1").grid(row=0, column=0)
tk.Label(frame_A, text="Столбец 2").grid(row=0, column=1)
entry_A11 = tk.Entry(frame_A, width=5)
entry_A11.grid(row=1, column=0, padx=5)
entry_A12 = tk.Entry(frame_A, width=5)
entry_A12.grid(row=1, column=1, padx=5)
entry_A21 = tk.Entry(frame_A, width=5)
entry_A21.grid(row=2, column=0, padx=5)
entry_A22 = tk.Entry(frame_A, width=5)
entry_A22.grid(row=2, column=1, padx=5)
tk.Label(frame_A, text="Строка 1").grid(row=1, column=2, padx=5)
tk.Label(frame_A, text="Строка 2").grid(row=2, column=2, padx=5)

# Матрица B
frame_B = tk.LabelFrame(frame_input, text="Матрица B")
frame_B.grid(row=0, column=1, padx=5)
tk.Label(frame_B, text="Столбец 1").grid(row=0, column=0)
tk.Label(frame_B, text="Столбец 2").grid(row=0, column=1)
entry_B11 = tk.Entry(frame_B, width=5)
entry_B11.grid(row=1, column=0, padx=5)
entry_B12 = tk.Entry(frame_B, width=5)
entry_B12.grid(row=1, column=1, padx=5)
entry_B21 = tk.Entry(frame_B, width=5)
entry_B21.grid(row=2, column=0, padx=5)
entry_B22 = tk.Entry(frame_B, width=5)
entry_B22.grid(row=2, column=1, padx=5)
tk.Label(frame_B, text="Строка 1").grid(row=1, column=2, padx=5)
tk.Label(frame_B, text="Строка 2").grid(row=2, column=2, padx=5)

button_solve = tk.Button(root, text="Решить игру", command=solve_game)
button_solve.pack(pady=5)

output_text = tk.Text(root, height=15, width=60)
output_text.pack(padx=10, pady=5)

frame_plot = tk.Frame(root)
frame_plot.pack(padx=10, pady=10)

root.mainloop()