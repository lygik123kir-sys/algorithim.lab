import heapq


def build_graph():

    lines = [
        (3, ["Площадь Восстания", "Владимирская", "Пушкинская",
             "Технологический институт"]),
        (6, ["Невский проспект", "Сенная площадь",
             "Технологический институт"]),
        (4, ["Гостиный двор", "Маяковская",
             "Площадь Александра Невского"]),
        (2, ["Спасская", "Достоевская", "Лиговский проспект",
             "Площадь Александра Невского", "Новочеркасская",
             "Ладожская", "Проспект Большевиков"]),
        (5, ["Адмиралтейская", "Садовая", "Звенигородская",
             "Обводный канал"]),
    ]

    transfers = [
        ("Невский проспект", "Гостиный двор"),
        ("Площадь Восстания", "Маяковская"),
        ("Спасская", "Садовая"),
        ("Спасская", "Сенная площадь"),
        ("Садовая", "Сенная площадь"),
        ("Достоевская", "Владимирская"),
        ("Пушкинская", "Звенигородская"),
    ]

    graph = {}

    def add_edge(first, second, weight):
        graph.setdefault(first, [])
        graph.setdefault(second, [])

        if (second, weight) not in graph[first]:
            graph[first].append((second, weight))

        if (first, weight) not in graph[second]:
            graph[second].append((first, weight))

    for weight, line in lines:
        for first, second in zip(line, line[1:]):
            add_edge(first, second, weight)

    for first, second in transfers:
        add_edge(first, second, 1)

    return graph


def restore_path(parent, finish):
    path = []
    current = finish

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def dijkstra(graph, start, finish):
    if start not in graph or finish not in graph:
        raise ValueError(
            "Начальная и конечная станции должны быть в графе."
        )

    # Минимальное известное время до каждой станции.
    distances = {station: float("inf") for station in graph}
    distances[start] = 0


    parent = {start: None}


    queue = [(0, start)]

    while queue:
        current_time, current = heapq.heappop(queue)

        # Пропускаем запись, если уже найден более быстрый путь.
        if current_time > distances[current]:
            continue

        if current == finish:
            return current_time, restore_path(parent, finish)

        for neighbor, weight in graph[current]:
            new_time = current_time + weight

            if new_time < distances[neighbor]:
                distances[neighbor] = new_time
                parent[neighbor] = current
                heapq.heappush(queue, (new_time, neighbor))

    return None


def read_station(prompt, graph):
    def normalize(text):
        return " ".join(
            text.strip().casefold().replace("ё", "е").split()
        )

    names = {normalize(station): station for station in graph}

    while True:
        entered = normalize(input(prompt))

        if entered in names:
            return names[entered]

        print("Станция не найдена. Скопируйте название из списка выше.")


def main():
    graph = build_graph()

    print("Станции фрагмента схемы:")
    for station in sorted(graph):
        print(" •", station)

    start = read_station("Откуда: ", graph)
    finish = read_station("Куда: ", graph)

    result = dijkstra(graph, start, finish)

    print("\nАлгоритм Дейкстры — поиск самого быстрого маршрута")

    if result is None:
        print("Маршрут не найден.")
    else:
        total_time, path = result
        print(" → ".join(path))
        print("Время в пути:", total_time, "мин")
        print("Количество рёбер (перегоны + пересадки):", len(path) - 1)


if __name__ == "__main__":
    main()