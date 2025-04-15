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
    max_in_columns_A = (A == np.max(A, axis=0))
    max_in_rows_B = (B == np.max(B, axis=1)[:, None])

    for i in range(2):
        for j in range(2):
            if max_in_columns_A[i, j] and max_in_rows_B[i, j]:
                nash_points.append((i, j))

    if nash_points:
        output_text.insert(tk.END, "Найдено равновесие(я) в чистых стратегиях:\n")
        for (i, j) in nash_points:
            output_text.insert(tk.END, f"Стратегия игрока 1: {i+1}, игрока 2: {j+1} -> Выигрыши: ({A[i,j]}, {B[i,j]})\n")
    else:
        output_text.insert(tk.END, "\nРавновесий в чистых стратегиях нет. Ищем в смешанных стратегиях:\n")

        a11, a12, a21, a22 = A.flatten()
        b11, b12, b21, b22 = B.flatten()

        C = a11 - a12 - a21 + a22
        alpha = a22 - a12
        D = b11 - b12 - b21 + b22
        beta = b22 - b21

        output_text.insert(tk.END, f"C = {C}, α = {alpha}\n")
        output_text.insert(tk.END, f"D = {D}, β = {beta}\n\n")

        # Решение неравенств
        if C != 0:
            q_star = -alpha / C
        else:
            q_star = 0.5  # любое значение если C=0 (особый случай)

        if D != 0:
            p_star = beta / D
        else:
            p_star = 0.5

        q_star = np.clip(q_star, 0, 1)
        p_star = np.clip(p_star, 0, 1)

        output_text.insert(tk.END, f"Оптимальная смешанная стратегия игрока 1 (p): {round(p_star, 3)}\n")
        output_text.insert(tk.END, f"Оптимальная смешанная стратегия игрока 2 (q): {round(q_star, 3)}\n\n")

        win1 = p_star * (q_star * a11 + (1 - q_star) * a12) + (1 - p_star) * (q_star * a21 + (1 - q_star) * a22)
        win2 = p_star * (q_star * b11 + (1 - q_star) * b12) + (1 - p_star) * (q_star * b21 + (1 - q_star) * b22)

        output_text.insert(tk.END, f"Выигрыш игрока 1: {round(win1, 3)}\n")
        output_text.insert(tk.END, f"Выигрыш игрока 2: {round(win2, 3)}\n")

        # Построение графика
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel('p (Игрок 1)')
        ax.set_ylabel('q (Игрок 2)')
        ax.set_title('График смешанных стратегий')

        # Равновесная точка
        ax.plot(p_star, q_star, 'ro', label=f'Равновесие (p={round(p_star,2)}, q={round(q_star,2)})')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack()

# --- GUI ---

root = tk.Tk()
root.title("Биматричная игра 2x2")

frame_input = tk.Frame(root)
frame_input.pack()

frame_A = tk.LabelFrame(frame_input, text="Матрица A")
frame_A.grid(row=0, column=0, padx=10, pady=10)

frame_B = tk.LabelFrame(frame_input, text="Матрица B")
frame_B.grid(row=0, column=1, padx=10, pady=10)

entries = []
entry_A11 = tk.Entry(frame_A, width=5)
entry_A11.grid(row=0, column=0)
entry_A12 = tk.Entry(frame_A, width=5)
entry_A12.grid(row=0, column=1)
entry_A21 = tk.Entry(frame_A, width=5)
entry_A21.grid(row=1, column=0)
entry_A22 = tk.Entry(frame_A, width=5)
entry_A22.grid(row=1, column=1)

entry_B11 = tk.Entry(frame_B, width=5)
entry_B11.grid(row=0, column=0)
entry_B12 = tk.Entry(frame_B, width=5)
entry_B12.grid(row=0, column=1)
entry_B21 = tk.Entry(frame_B, width=5)
entry_B21.grid(row=1, column=0)
entry_B22 = tk.Entry(frame_B, width=5)
entry_B22.grid(row=1, column=1)

button_solve = tk.Button(root, text="Решить", command=solve_game)
button_solve.pack(pady=10)

output_text = tk.Text(root, height=20, width=60)
output_text.pack()

frame_plot = tk.Frame(root)
frame_plot.pack()

root.mainloop()

