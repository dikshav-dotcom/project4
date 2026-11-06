# Usage: python3 plot.py < nkx2_1.tsv
import sys
import math
from scipy import stats
import matplotlib
matplotlib.use("Agg")                  # save to file, no window
import matplotlib.pyplot as plt

normal = []
tumor = []

for line in sys.stdin:
    cols = line.rstrip("\r\n").split("\t")
    if len(cols) < 3:
        continue
    value = math.log2(float(cols[1]) + 1)      # log2(TPM + 1)
    if cols[2] == "Solid Tissue Normal":
        normal.append(value)
    elif cols[2] == "Primary Tumor":
        tumor.append(value)

# t-tests
welch   = stats.ttest_ind(tumor, normal, equal_var=False)
student = stats.ttest_ind(tumor, normal)

print("Solid Tissue Normal: n =", len(normal), " mean =", round(sum(normal)/len(normal), 3))
print("Primary Tumor:       n =", len(tumor),  " mean =", round(sum(tumor)/len(tumor), 3))
print("Welch t-test   p =", f"{welch.pvalue:.2e}")
print("Student t-test p =", f"{student.pvalue:.2e}")

# Welch is used on the plot: the two groups have very different spread and size
p = welch.pvalue

# Boxplot
plt.figure(figsize=(5, 6))
plt.boxplot([normal, tumor], notch=True)
plt.xticks([1, 2], [f"Solid Tissue Normal\n(n = {len(normal)})",
                    f"Primary Tumor\n(n = {len(tumor)})"])
plt.ylabel("log2(TPM + 1)")
plt.title(f"Lung Adenocarcinoma: NKX2-1\np = {p:.1e} (Welch t-test)")
plt.tight_layout()
plt.savefig("NKX2-1_boxplot.png", dpi=150)
print("Saved NKX2-1_boxplot.png")
