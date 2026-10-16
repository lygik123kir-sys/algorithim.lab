from collections import deque

def build_graph():


    lines = [
        ["Площадь Восстания", "Владимирская", "Пушкинская",
         "Технологический институт"],
        ["Невский проспект", "Сенная площадь", "Технологический институт"],
        ["Гостиный двор", "Маяковская", "Площадь Александра Невского"],
        ["Спасская", "Достоевская", "Лиговский проспект",
         "Площадь Александра Невского", "Новочеркасская",
         "Ладожская", "Проспект Большевиков"],
        ["Адмиралтейская", "Садовая", "Звенигородская", "Обводный канал"],
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

    def add_edge(first, second):

        graph.setdefault(first, [])
        graph.setdefault(second, [])
        if second not in graph[first]:
            graph[first].append(second)
        if first not in graph[second]:
            graph[second].append(first)

    for line in lines:
        for first, second in zip(line, line[1:]):
            add_edge(first, second)
    for first, second in transfers:
        add_edge(first, second)
    return graph


def restore_path(parent, finish):
    path = []
    current = finish
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def bfs(graph, start, finish):
    if start not in graph or finish not in graph:
        raise ValueError("Начальная и конечная станции должны быть в графе.")

    queue = deque([start])


    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == finish:
            return restore_path(parent, finish)
        for neighbor in graph[current]:
            if neighbor not in parent:

                parent[neighbor] = current
                queue.append(neighbor)
    return None


def dfs(graph, start, finish):
    if start not in graph or finish not in graph:
        raise ValueError("Начальная и конечная станции должны быть в графе.")
    parent = {start: None}

    def visit(current):
        if current == finish:
            return True
        for neighbor in graph[current]:
            if neighbor not in parent:
                parent[neighbor] = current

                if visit(neighbor):
                    return True
        return False

    if visit(start):
        return restore_path(parent, finish)
    return None


def read_station(prompt, graph):
    def normalize(text):
        return " ".join(text.strip().casefold().replace("ё", "е").split())

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

    for title, search in [("BFS — поиск в ширину", bfs),
                          ("DFS — поиск в глубину", dfs)]:
        path = search(graph, start, finish)
        print("\n" + title)
        if path is None:
            print("Маршрут не найден.")
        else:
            print(" → ".join(path))
            print("Количество рёбер (перегоны + пересадки):", len(path) - 1)


if __name__ == "__main__":

    main()
