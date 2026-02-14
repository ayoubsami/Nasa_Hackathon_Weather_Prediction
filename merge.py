import glob
import os
import pandas as pd

# CSV files
folder_path = "./files"

csv_files = sorted(
    glob.glob(os.path.join(folder_path, "*.csv")) +
    glob.glob(os.path.join(folder_path, "*.CSV"))
)

csv_files.sort()

for i in range(0, len(csv_files), 5):
    group = csv_files[i:i+5]
    
    output_file = os.path.join(folder_path, "merged_data.csv")

    with open(output_file, "w") as outfile:
        for j, fname in enumerate(group):
            with open(fname) as infile:
                lines = infile.readlines()
                # Write header only from the first file
                if j == 0:
                    outfile.writelines(lines)
                else:
                    outfile.writelines(lines[1:])  # skip header
    year = 2000 + i // 5

    data = pd.read_csv(output_file)
    os.remove(output_file)
    data = data[["lon", "lat", "time","T2M_C","wind_speed","PRECTOT"]]
    data.to_csv(f"output/merged_data_{year}.csv", index=False, float_format="%.2f")


    print(f"Done, Combined {len(group)} files into merged_data.csv")
