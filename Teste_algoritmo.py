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


# Função para verificar se há conflito de horários entre dois intervalos
def has_conflict(interval1, interval2):
    return interval1[1] > interval2[0] and interval1[0] < interval2[1]


# Entrada de dados
n = int(input("Digite o número de intervalos: "))
intervals = []
for i in range(n):
    start = int(input(f"Digite o horário de início do intervalo {i+1}: "))
    end = int(input(f"Digite o horário de término do intervalo {i+1}: "))
    value = int(input(f"Digite o valor do intervalo {i+1}: "))
    intervals.append((start, end, value))

# Verifica se há conflito de horários
has_conflict_flag = False
conflicting_intervals = []
for i in range(n - 1):
    for j in range(i + 1, n):
        if has_conflict(intervals[i], intervals[j]):
            has_conflict_flag = True
            conflicting_intervals.append((i, j))

if has_conflict_flag:
    # Filtra os intervalos para incluir apenas o de maior valor entre os intervalos em conflito
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

    # Agendamento dos intervalos utilizando o algoritmo de Weighted Interval Scheduling
    result = weighted_interval_scheduling(filtered_intervals)

    # Combinar os intervalos agendados dos conflitos com os intervalos não conflitantes
    final_result = []
    for i in range(n):
        if i in conflict_set:
            continue  # Ignora os intervalos conflitantes já agendados
        else:
            final_result.append(intervals[i])
    final_result.extend(result)

else:
    # Execução do algoritmo
    final_result = weighted_interval_scheduling(intervals)

# Ordena os intervalos agendados pelo horário de início
final_result.sort(key=lambda x: x[0])

# Remover agendamentos duplicados
final_result = list(set(final_result))

# Saída dos resultados em ordem crescente de horário de início
print("Intervalos agendados:")
for interval in final_result:
    print(f"Início: {interval[0]}, Término: {interval[1]}, Valor: {interval[2]}")
