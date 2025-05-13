import random

def generate_sequence(length, user_name):
    nucleotides = ['A', 'C', 'G', 'T']
    sequence_list = [random.choice(nucleotides) for _ in range(length)]
    insert_pos = random.randint(0, length)
    sequence_list.insert(insert_pos, user_name)
    return ''.join(sequence_list)

# ORIGINAL:
# length_input = input("Enter the sequence length: ")
# length = int(length_input)
# MODIFIED (added input validation loop to ensure positive integer input):
while True:
    try:
        length_input = input("Enter the sequence length: ")
        length = int(length_input)
        if length <= 0:
            raise ValueError("Length must be a positive integer.")
        break
    except ValueError as e:
        print(f"Invalid input ({e}). Please enter a positive integer.")

# ORIGINAL:
# seq_id = input("Enter the sequence ID: ")
# description = input("Provide a description of the sequence: ")
# user_name = input("Enter your name: ")
# MODIFIED (strip whitespace to avoid invalid filenames and header formatting):
seq_id = input("Enter the sequence ID: ").strip()
description = input("Provide a description of the sequence: ").strip()
user_name = input("Enter your name: ").strip()

# Generate the full sequence with name inserted
sequence = generate_sequence(length, user_name)

# ORIGINAL:
# file_name = f"{seq_id}.fasta"
# with open(file_name, 'w') as fasta_file:
#     fasta_file.write(f">{seq_id} {description}\n")
#     for i in range(0, len(sequence), 70):
#         fasta_file.write(sequence[i:i+70] + '\n')
# MODIFIED (added exception handling for file operations):
file_name = f"{seq_id}.fasta"
try:
    with open(file_name, 'w') as fasta_file:
        fasta_file.write(f">{seq_id} {description}\n")
        for i in range(0, len(sequence), 70):
            fasta_file.write(sequence[i:i+70] + '\n')
    print(f"The sequence was saved to the file {file_name}")
except IOError as e:
    print(f"Error writing to file {file_name}: {e}")

# ORIGINAL:
# pure_sequence = sequence.replace(user_name, '')
# counts = {nuc: pure_sequence.count(nuc) for nuc in nucleotides}
# MODIFIED (reuse function-local nucleotides list and calculate counts robustly):
from collections import Counter

# Remove the user name from sequence before counting
pure_sequence = sequence.replace(user_name, '')
counts = Counter(pure_sequence)

# Calculate percentages and CG/AT ratio
# ORIGINAL:
# total_bases = sum(counts.values())
# percentages = {nuc: (counts[nuc] / total_bases) * 100 for nuc in nucleotides}
# cg_ratio = ((counts['C'] + counts['G']) / (counts['A'] + counts['T'])) if (counts['A'] + counts['T']) > 0 else float('inf')
# MODIFIED (added zero-division guard and formatted output alignment):
total_bases = sum(counts[nuc] for nuc in ['A', 'C', 'G', 'T'])
if total_bases == 0:
    print("No nucleotide bases to calculate statistics.")
else:
    percentages = {nuc: (counts.get(nuc, 0) / total_bases) * 100 for nuc in ['A', 'C', 'G', 'T']}
    cg = counts.get('C', 0) + counts.get('G', 0)
    at = counts.get('A', 0) + counts.get('T', 0)
    cg_ratio = (cg / at) if at > 0 else float('inf')

    print("Sequence statistics:")
    for nuc in ['A', 'C', 'G', 'T']:
        print(f"{nuc}: {percentages[nuc]:6.2f}%")
    print(f"%CG: {(percentages['C'] + percentages['G']):6.2f}%")
    print(f"C/G to A/T ratio: {cg_ratio:.2f}")

# Improvement 3: Added a __main__ guard and seed option for reproducibility
# MODIFIED (to allow import without running and optional seed input):

if __name__ == "__main__":
    seed_input = input("Enter a random seed (or leave blank): ")
    if seed_input.strip():
        try:
            seed = int(seed_input)
            random.seed(seed)
        except ValueError:
            print("Invalid seed; using system default.")
