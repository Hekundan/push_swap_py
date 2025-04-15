def check_input(stack):
    for i in stack:
        assert isinstance(i, int), "Only integers!"
    assert len(stack) == len(set(stack)), "Stack contains duplicate values"