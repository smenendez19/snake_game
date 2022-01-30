# Ciclo Hamiltoniano
def hamiltonian_cicle(data):
    actual_block = (data["snake_head"][0] // data["block_size"], data["snake_head"][1] // data["block_size"])
    if actual_block[1] == 0:
        if actual_block[0] == 0:
            return "DOWN"
        return "LEFT"
    if actual_block[0] % 2 == 0:
        if actual_block[1] == data["board_size"][1] // data["block_size"] - 1:
            return "RIGHT"
        return "DOWN"
    elif actual_block[0] % 2 != 0:
        if actual_block[1] == 1 and actual_block[0] < data["board_size"][0] // data["block_size"] - 1:
            return "RIGHT"
        return "UP"