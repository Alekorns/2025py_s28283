from Bio import Entrez, SeqIO
import pandas as pd, matplotlib.pyplot as plt
from io import StringIO
import ssl; ssl._create_default_https_context = ssl._create_unverified_context

class N:
    def __init__(s, e, k):
        Entrez.email = e
        Entrez.api_key = k
        Entrez.tool = "BioScriptEx10"

    def s(s, t):
        try:
            h = Entrez.efetch(db="taxonomy", id=t, retmode="xml")
            s.o = Entrez.read(h)[0]["ScientificName"]
            h = Entrez.esearch(db="nucleotide", term=f"txid{t}[Organism]", usehistory="y")
            r = Entrez.read(h)
            s.w, s.q, s.c = r["WebEnv"], r["QueryKey"], int(r["Count"])
            return s.o
        except Exception as e:
            print("Search error:", e)
            return

    def f(s, n=200):
        try:
            h = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text",
                              webenv=s.w, query_key=s.q, retmax=n)
            return h.read()
        except Exception as e:
            print("Fetch error:", e)
            return ""

def main():
    r = N(input("Email: "), input("API key: "))
    t = input("TaxID: ")
    if not r.s(t): return
    mn, mx = int(input("Min length: ")), int(input("Max length: "))
    d = [(x.id, len(x.seq), x.description) for x in SeqIO.parse(StringIO(r.f(250)), "genbank")
         if mn <= len(x.seq) <= mx]
    if not d:
        print("No records")
        return
    df = pd.DataFrame(d, columns=["Accession", "Length", "Description"])
    csv_file = f"taxid_{t}.csv"
    img_file = f"taxid_{t}.png"
    df.to_csv(csv_file, index=False)
    df_sorted = df.sort_values("Length", ascending=False)
    plt.figure(figsize=(12, 6))
    plt.plot(df_sorted["Accession"], df_sorted["Length"], marker='o')
    plt.xticks(rotation=90)
    plt.xlabel("Accession")
    plt.ylabel("Sequence Length")
    plt.title(" Sequence Lengths")
    plt.tight_layout()
    plt.savefig(img_file)
    print(f"\n CSV saved as {csv_file}")
    print(f" Plot saved as {img_file}")

if __name__ == "__main__":
    main()
