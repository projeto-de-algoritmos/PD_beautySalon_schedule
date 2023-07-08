import tkinter as tk
from tkinter import messagebox


def weighted_interval_scheduling(intervals):
    intervals.sort(key=lambda x: x[1])  # Ordena os intervalos pelo horário de término
    n = len(intervals)
    memo = [0] * (n + 1)

    for i in range(1, n + 1):
        value = intervals[i - 1][2]
        j = i - 1
        while j >= 1 and intervals[j - 1][1] > intervals[i - 1][0]:
            j -= 1
        value += memo[j]
        memo[i] = max(value, memo[i - 1])

    schedule = []
    i = n
    while i > 0:
        if intervals[i - 1][2] + memo[i - 1] >= memo[i]:
            schedule.append(intervals[i - 1])
            j = i - 1
            while j >= 1 and intervals[j - 1][1] > intervals[i - 1][0]:
                j -= 1
            i = j
        else:
            i -= 1
    schedule.reverse()

    return schedule


def has_conflict(interval1, interval2):
    return interval1[1] > interval2[0] and interval1[0] < interval2[1]


def handle_submit():
    num_intervals = int(entry_num_intervals.get())

    intervals = []
    for i in range(num_intervals):
        name = entry_names[i].get()
        description = entry_descriptions[i].get()
        start = int(entry_starts[i].get())
        end = int(entry_ends[i].get())
        value = int(entry_values[i].get())
        intervals.append((start, end, value, name, description))

    has_conflict_flag = False
    conflicting_intervals = []
    for i in range(num_intervals - 1):
        for j in range(i + 1, num_intervals):
            if has_conflict(intervals[i][:2], intervals[j][:2]):
                has_conflict_flag = True
                conflicting_intervals.append((i, j))

    if has_conflict_flag:
        filtered_intervals = []
        conflict_set = set()
        for interval_pair in conflicting_intervals:
            interval1 = intervals[interval_pair[0]]
            interval2 = intervals[interval_pair[1]]
            if interval1[2] > interval2[2]:
                conflict_set.add(interval_pair[1])
                filtered_intervals.append(interval1)
            else:
                conflict_set.add(interval_pair[0])
                filtered_intervals.append(interval2)

        result = weighted_interval_scheduling(filtered_intervals)

        final_result = []
        for i in range(num_intervals):
            if i not in conflict_set:
                final_result.append(intervals[i])
        final_result.extend(result)

    else:
        final_result = weighted_interval_scheduling(intervals)

    final_result.sort(key=lambda x: x[0])

    # Remover duplicatas de pessoas agendadas
    unique_people = set()
    unique_result = []
    for interval in final_result:
        person = interval[3]
        if person not in unique_people:
            unique_result.append(interval)
            unique_people.add(person)

    messagebox.showinfo("Agendamento", format_result(unique_result))


def format_result(result):
    formatted = "Intervalos agendados:\n"
    for interval in result:
        formatted += f"Nome: {interval[3]}, Descrição: {interval[4]}, Início: {interval[0]}, Término: {interval[1]}, Valor: {interval[2]}\n"
    return formatted


# Interface Gráfica
root = tk.Tk()
root.title("Agendamento de Intervalos")
root.geometry("400x400")

frame = tk.Frame(root)
frame.pack(pady=20)

label_num_intervals = tk.Label(frame, text="Número de Intervalos:")
label_num_intervals.pack()

entry_num_intervals = tk.Entry(frame)
entry_num_intervals.pack(pady=10)

frame_intervals = tk.Frame(root)
frame_intervals.pack()

entry_names = []
entry_descriptions = []
entry_starts = []
entry_ends = []
entry_values = []

def create_interval_fields():
    num_intervals = int(entry_num_intervals.get())

    for i in range(num_intervals):
        label_name = tk.Label(frame_intervals, text=f"Nome Intervalo {i+1}:")
        label_name.pack()

        entry_name = tk.Entry(frame_intervals)
        entry_name.pack()
        entry_names.append(entry_name)

        label_description = tk.Label(frame_intervals, text=f"Descrição Intervalo {i+1}:")
        label_description.pack()

        entry_description = tk.Entry(frame_intervals)
        entry_description.pack()
        entry_descriptions.append(entry_description)

        label_start = tk.Label(frame_intervals, text=f"Início Intervalo {i+1}:")
        label_start.pack()

        entry_start = tk.Entry(frame_intervals)
        entry_start.pack()
        entry_starts.append(entry_start)

        label_end = tk.Label(frame_intervals, text=f"Término Intervalo {i+1}:")
        label_end.pack()

        entry_end = tk.Entry(frame_intervals)
        entry_end.pack()
        entry_ends.append(entry_end)

        label_value = tk.Label(frame_intervals, text=f"Valor Intervalo {i+1}:")
        label_value.pack()

        entry_value = tk.Entry(frame_intervals)
        entry_value.pack()
        entry_values.append(entry_value)

    btn_submit = tk.Button(root, text="Agendar", command=handle_submit)
    btn_submit.pack(pady=10)

btn_create_fields = tk.Button(frame, text="Criar Campos", command=create_interval_fields)
btn_create_fields.pack()

root.mainloop()
