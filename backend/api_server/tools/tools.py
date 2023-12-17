def merge_and_average_dicts(dict1, dict2, weight1=1, weight2=1):
    # Объединение ключей из обоих словарей
    all_keys = set(dict1.keys()) | set(dict2.keys())
    averaged_dict = {}

    for key in all_keys:
        value1 = dict1.get(key, 0)  # Получаем значение из первого словаря, если ключ отсутствует, то 0
        value2 = dict2.get(key, 0)  # То же самое для второго словаря

        # Вычисление взвешенного среднего значения
        total_weight = weight1 + weight2
        averaged_value = (value1 * weight1 + value2 * weight2) / total_weight
        averaged_dict[key] = averaged_value

    return averaged_dict


def merge_and_average_multiple_dicts(dict_list, weights_list):
    if len(dict_list) != len(weights_list):
        raise ValueError("Длина списка словарей и списка весов должна быть одинаковой")

    # Объединение всех ключей из всех словарей
    all_keys = set(key for d in dict_list for key in d.keys())
    averaged_dict = {}

    for key in all_keys:
        weighted_sum = 0
        total_weight = 0

        for dict_, weight in zip(dict_list, weights_list):
            value = dict_.get(key, 0)
            weighted_sum += value * weight
            total_weight += weight

        averaged_dict[key] = weighted_sum / total_weight if total_weight > 0 else 0

    return averaged_dict


def split_dict_into_labels_and_values(input_dict, threshold=0.05, min_items=3):
    labels = []
    values = []
    additional_items = []

    # Первоначальное добавление элементов, удовлетворяющих порогу
    for label, value in input_dict.items():
        if value >= threshold:
            labels.append(label)
            values.append(value)
        else:
            additional_items.append((label, value))

    # Если не хватает элементов, добавляем дополнительные с наибольшими вероятностями
    additional_items.sort(key=lambda x: x[1], reverse=True)  # Сортировка по убыванию вероятности
    while len(labels) < min_items and additional_items:
        label, value = additional_items.pop(0)
        labels.append(label)
        values.append(value)

    return labels, values
