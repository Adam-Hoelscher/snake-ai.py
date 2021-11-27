def rle(iterable):
    answer = []
    count = 1
    iterator = iter(iterable)

    try:
        run_value = next(iterator)
        count = 1
    except StopIteration:
        return answer

    while True:
        try:
            value = next(iterator)
            if value == run_value:
                count += 1
            else:
                answer.append((count, run_value))
                count = 1
                run_value = value
        except StopIteration:
            if run_value:
                answer.append((count, run_value))
            break

    return answer
