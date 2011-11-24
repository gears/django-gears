def first(function, iterable):
    if function is None:
        function = bool
    for item in iterable:
        if function(item):
            return item
    raise ValueError('No suitable value found.')


def first_or_none(function, iterable):
    try:
        return first(function, iterable)
    except ValueError:
        pass
