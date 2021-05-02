import subprocess
import os

ai_variants = [1, 2]

# size_map = {}
# for ai in ai_variants:
#     size_map[ai] = {}

# # first do the various size of boards
# size_dir = os.path.join("varied_size_boards")

# for size_board in os.listdir(size_dir):
#     print(size_board)
#     name_split = size_board.split("_")
#     rows = int(name_split[0].split("rows")[0])
#     cols = int(name_split[1].split("cols")[0])
#     size = rows * cols
#     fp = os.path.join(size_dir, size_board)

#     for ai in ai_variants:
#         size_cmd = f"python3 minesweeperPerformanceTest.py -f {fp} {ai}"
#         raw_output = subprocess.check_output(size_cmd.split())
#         info = str(raw_output).split(r"\n")[-2]
#         total_digs = int(info.split(",")[0].split("=")[1])
#         total_time = float(info.split(",")[1].split("=")[1])
#         data = (total_digs, total_time)
#         if size in size_map[ai]:
#             size_map[ai][size].append(data)
#         else:
#             size_map[ai][size] = [data]

# for ai in ai_variants:
#     with open(f"varied_size_ai{ai}.txt", "w+") as f:
#         f.write("Size\t# Tiles Flipped\tTime (sec)\n")
#         size_data = size_map[ai]
#         for size in size_data:
#             values = size_data[size]
#             avg_tiles, avg_time = sum([i[0] for i in values]) / len(values), sum([i[1] for i in values]) / len(values)
#             f.write(f"{size}\t{avg_tiles}\t{avg_time}\n")

# log_size_ai1 = open("size_data_ai1.txt", "w+")
# log_size_ai2 = open("size_data_ai2.txt", "w+")

# then do the various density of bombs

density_map = {}
for ai in ai_variants:
    density_map[ai] = {}

density_dir = os.path.join("varied_density_boards")

i = 0
for board in os.listdir(density_dir):
    print(board, i)
    i+=1
    name_split = board.split("_")
    density = int(name_split[2].split("d")[0])
    fp = os.path.join(density_dir, board)

    for ai in ai_variants:
        cmd = f"python3 minesweeperPerformanceTest.py -f {fp} {ai}"
        raw_output = subprocess.check_output(cmd.split())
        info = str(raw_output).split(r"\n")[-2]
        total_digs = int(info.split(",")[0].split("=")[1])
        total_time = float(info.split(",")[1].split("=")[1])
        data = (total_digs, total_time)
        if density in density_map[ai]:
            density_map[ai][density].append(data)
        else:
            density_map[ai][density] = [data]

for ai in ai_variants:
    with open(f"varied_density_ai{ai}.txt", "w+") as f:
        f.write("Density\t# Tiles Flipped\tTime (sec)\n")
        density_data = density_map[ai]
        for density in density_data:
            values = density_data[density]
            avg_tiles, avg_time = sum([i[0] for i in values]) / len(values), sum([i[1] for i in values]) / len(values)
            f.write(f"{density}\t{avg_tiles}\t{avg_time}\n")