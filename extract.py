# Usage: python3 extract.py data < gdc_sample_sheet.tsv > nkx2_1.tsv
import sys
import os

GENE = "NKX2-1"
data_dir = sys.argv[1]                 # folder with the sample folders

# First line of the sample sheet = column names
header = sys.stdin.readline().rstrip("\r\n").split("\t")
id_col   = header.index("File ID")
name_col = header.index("File Name")
type_col = header.index("Sample Type")

for line in sys.stdin:
    cols = line.rstrip("\r\n").split("\t")
    if len(cols) <= type_col:
        continue

    sample_type = cols[type_col]
    if sample_type != "Primary Tumor" and sample_type != "Solid Tissue Normal":
        continue                       # skip other sample types

    file_id = cols[id_col]
    path = os.path.join(data_dir, file_id, cols[name_col])
    if not os.path.exists(path):
        print("missing:", path, file=sys.stderr)
        continue

    with open(path) as f:
        for gene_line in f:
            g = gene_line.rstrip("\r\n").split("\t")
            if len(g) > 6 and g[1] == GENE:          # column 2 = gene name
                print(file_id, g[6], sample_type, sep="\t")   # column 7 = TPM
                break
