# Ciclo Hamiltoniano
def hamiltonian_cicle(data):
    current_block = (
        data["snake_head"][0] // data["block_size"],
        data["snake_head"][1] // data["block_size"],
    )
    if current_block[1] == 0:
        if current_block[0] == 0:
            return "D"  # DOWN
        return "L"  # LEFT
    if current_block[0] % 2 == 0:
        if current_block[1] == data["board_size"][1] // data["block_size"] - 1:
            return "R"  # RIGHT
        return "D"  # DOWN
    elif current_block[0] % 2 != 0:
        if current_block[1] == 1 and current_block[0] < data["board_size"][0] // data["block_size"] - 1:
            return "R"  # RIGHT
        return "U"  # UP
