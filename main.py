if __name__ == "__main__":
    count = [0] * 7

    while True:
        read = input().split(":")
        tag, data = read

        match tag:

            case "PLAY":
                print("finding move...")

                for i, value in enumerate(count):
                    if value < 6:
                        print(f"MOVE:{i}")
                        count[i] += 1
                        break
                else:
                    print("MOVE: -1")
                    print("Error: No moves left!")

            case "MOVE":
                op_move = data
                count[int(op_move)] += 1

            case "BOARD":
                count = [0] * 7
                if len(data) > 0:
                    for i in data.split(","):
                        count[int(i)] += 1
                print(f"Board set to: {count}")

            case _:
                print("MOVE: -1")
                print("Unrecognized tag!")