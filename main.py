import random


if __name__ == "__main__":
    count = [0] * 7
    available = list(range(0,7))


    while True: # The game platform loop
        read = input().split(":") # Read the unput from the program
        tag, data = read # KOMENTO:DATA

        match tag:

            case "PLAY": # PLAY: AI TURN
                if sum(count) == 42:
                    print(f"MOVE: -1")

                else:
                    print("finding move...")
                    choice = random.choice(available)
                    while count[choice] == 6:
                        available.remove(choice)
                        choice = random.choice(available)

                    count[choice] += 1
                    print(f"MOVE:{choice}")

            case "MOVE": # MOVE:{int} THe play command
                op_move = data  
                count[int(op_move)] += 1   
                print(data)

            case "BOARD": # BOARD. Tämä tarkoittaa, että tekoälysi sovelluslogiikan pitäisi asettaa lauta johonkin tiettyyn konfiguraatioon. 
                count = [0] * 7
                if len(data) > 0:
                    for i in data.split(","):
                        count[int(i)] += 1
                print(f"Board set to: {count}")

            case "CURRENT":
                print(f"Board set to: {count}")

            case _:
                print("MOVE: -1")
                print("Unrecognized tag!")