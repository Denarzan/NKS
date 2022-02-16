def integrity(time, fp, h) -> float:
    """
    Функція для обрахунку інтегралу.
    :param time: Час правої границі інтервалу.
    :param fp: Значення статистичної щільності розподілу ймовірності відмови.
    :param h: Довжина інтервалу.
    :return: Результат інтегралу.
    """
    return sum(fp[0: int(time // h)]) * h + safe_list_get(fp, int(time // h), 0) * (time % h)


def p(time, fp, h) -> float:
    """
    Функція для обрахунку значення ймовірності безвідмовної роботи пристрою на час правої границі інтервалу.
    :param time: Час правої границі інтервалу.
    :param fp: Значення статистичної щільності розподілу ймовірності відмови.
    :param h: Довжина інтервалу.
    :return: Значення ймовірності безвідмовної роботи пристрою на час правої границі інтервалу.
    """
    return 1 - integrity(time, fp, h)


def safe_list_get(given_list, idx, default):
    """
    Функція, яка є повторення методу get() для словника. Бере зі списку елемент за індексом, а якщо його немає
    повертає значення за замовчуванням.
    :param given_list: Заданий список.
    :param idx: Індекс, за яким потрібно взяти значення.
    :param default: Значення, що повертається, якщо заданого індекса не знайдено.
    :return: Елемент списку.
    """
    return given_list[idx] if idx < len(given_list) else default


if __name__ == '__main__':
    # Безвідмовна робота, години.
    t = 1102

    # Інтенсивність відмов, години.
    lambda_t = 5420

    # γ
    gama = 0.86

    # Вхідна вибірка наробітків до відмови.
    input_time_list = [
        912, 2981, 2048, 1268, 1879, 381, 1855, 460, 4, 376, 364, 1961, 707, 673, 193, 1617, 679, 319, 1155, 29, 2208,
        107, 663, 769, 187, 222, 38, 628, 2310, 375, 414, 2598, 509, 275, 468, 918, 60, 646, 618, 560, 1484, 446, 1755,
        1140, 192, 1101, 103, 2853, 5771, 104, 1163, 55, 72, 491, 253, 898, 1280, 85, 318, 121, 692, 948, 515, 622,
        1420, 252, 1487, 1885, 765, 966, 241, 79, 722, 378, 444, 661, 1532, 2505, 455, 394, 960, 1288, 1074, 109, 88,
        430, 1672, 2224, 427, 277, 1175, 863, 672, 1426, 199, 603, 1337, 258, 818, 138
    ]

    # Сортуємо дану вибірку
    input_time_list.sort()

    # Середній час наробіток до відмови, години.
    average_time = sum(input_time_list) / len(input_time_list)

    # Максимальне значенням наробітку до відмови, години.
    max_time = max(input_time_list)

    # Довжина одного інтервалу (h).
    length = max_time / 10

    # Границі інтервалів.
    interval_limits = [i / 10 for i in range(0, max_time * 10 + 1, max_time)]
    # (множення і потім ділення на 10, щоб можна було записати в один рядок)

    # Статистична щільность розподілу ймовірності відмови.
    failure_probability = [
        len([time for time in input_time_list if interval_limits[i] < time <= interval_limits[i + 1]]) / (
                    len(input_time_list) * length) for i in range(len(interval_limits) - 1)]

    # Ймовірності безвідмовної роботи пристрою на час правої границі інтервалу.
    probabilities = [p(t, failure_probability, length) for t in interval_limits]

    # Знаходимо індекс першого елемента, що менше за задану γ.
    t_y_index = probabilities.index(list(filter(lambda y: y <= gama, probabilities))[0])

    # Так як t_y знаходиться в інтервалі між ti та ti-1, знайдемо дані значення.
    t_i = t_y_index * length
    t_i_minus_1 = (t_y_index - 1) * length

    # Статистичний γ-відсотковий наробіток на відмову.
    t_y = t_i - length * (p(t_i, failure_probability, length) - gama) / (
                p(t_i, failure_probability, length) - p(t_i_minus_1, failure_probability, length))

    # Ймовірність безвідмовної роботи.
    probability_of_trouble_free_operation = p(t, failure_probability, length)

    # Інтенсивність відмов.
    failure_intensity = failure_probability[int(lambda_t // length)] / p(lambda_t, failure_probability, length)
    print("Задля доказу того, що робота виконана самостійно, всі значення було обраховано в один рядок.")
    print("Відсортована вхідна вибірка наробітків до відмови:", input_time_list)
    print("Середній час наробіток до відмови:", average_time)
    print("Максимальне значенням наробітку до відмови:", max_time)
    print("Довжина одного інтервалу:", length)
    print("Границі інтервалів:", interval_limits)
    print("Статистична щільность розподілу ймовірності відмови:", failure_probability)
    print("Ймовірності безвідмовної роботи пристрою на час правої границі інтервалу:", probabilities)
    print("Статистичний γ-відсотковий наробіток на відмову:", t_y)
    print("Ймовірність безвідмовної роботи", probability_of_trouble_free_operation)
    print("Інтенсивність відмов:", failure_intensity)
