import requests


def battlesnake_api(data):
    url = "http://127.0.0.1:8080"

    body = [
        {
            "x": b[0] // 50,
            "y": ((b[1] // 50) - 10) * -1 - 1,
        }
        for b in data["snake_body"]
    ]
    body.reverse()

    # Adapt data for Battlesnake API
    request_data = {
        "you": {
            "head": {
                "x": data["snake_head"][0] // 50,
                "y": ((data["snake_head"][1] // 50) - 10) * -1 - 1,
            },
            "body": body,
        },
        "board": {
            "height": data["board_size"][0] // 50,
            "width": data["board_size"][1] // 50,
            "snakes": [],
            "food": [
                {
                    "x": f[0] // 50,
                    "y": ((f[1] // 50) - 10) * -1 - 1,
                }
                for f in data["food_position"]
            ],
        },
    }

    print("Request:", request_data)
    response = requests.post(url=url + "/move", json=request_data)
    print("Response:", response.json())
    response_data = response.json()
    if response.status_code == 200:
        return response_data["move"][0].upper()
    else:
        print(response.text)
        raise Exception("Battlesnake API request failed")
