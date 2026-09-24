N = 4

def is_safe(state, col):
    row = len(state)

    for r, c in enumerate(state):
        if c == col:
            return False

        if abs(c - col) == abs(r - row):
            return False

    return True


def solve(state):
    if len(state) == N:
        print(state)

        for row in state:
            print(" ".join("Q" if col == row else "." for col in range(N)))

        print()
        return

    for col in range(N):
        if is_safe(state, col):
            solve(state + (col,))


solve(())
