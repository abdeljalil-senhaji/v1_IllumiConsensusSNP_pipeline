#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess
import os
import sys

def usage():
    print("Usage: run_bowtie2_on_blast.py -1 <R1> -2 <R2> -b <blast_file> -db <ref_dir> -o <output_dir>")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Run Bowtie2 on top 2 BLAST references")
    parser.add_argument("-1", dest="R1", required=True)
    parser.add_argument("-2", dest="R2", required=True)
    parser.add_argument("-b", dest="blast_file", required=True)
    parser.add_argument("-db", dest="ref_dir", required=True)
    parser.add_argument("-o", dest="output_dir", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Get the two first references from BLAST file (column 2)
    refs = []
    try:
        with open(args.blast_file) as f:
            for i, line in enumerate(f):
                if i >= 2:
                    break
                cols = line.strip().split()
                if len(cols) > 1:
                    refs.append(cols[1])
    except Exception as e:
        print("[ERREUR] Impossible de lire le fichier BLAST : {}".format(str(e)))
        sys.exit(1)

    if not refs:
        print("[ERREUR] Aucune référence trouvée dans le fichier BLAST.")
        sys.exit(1)

    # Extraire le nom de base sans _R1...fq
    filename_base = os.path.splitext(os.path.basename(args.R1))[0]
    if "_R1" in filename_base:
        filename_base = filename_base.split("_R1")[0]

    for ref in refs:
        sam_file = os.path.join(args.output_dir, "{}_{}.sam".format(filename_base, ref))
        index_path = os.path.join(args.ref_dir, ref)
        index_file = "{}.1.bt2".format(index_path)

        if not os.path.isfile(index_file):
            print("[ALERTE] Index Bowtie2 introuvable pour : {}".format(ref))
            continue

        print("[INFO] Alignement avec Bowtie2 sur la référence : {}".format(ref))

        cmd = [
            "bowtie2",
            "--very-sensitive-local",
            "-x", index_path,
            "-1", args.R1,
            "-2", args.R2,
            "-S", sam_file,
            "--threads", "8"
        ]

        retcode = subprocess.call(cmd)
        if retcode != 0:
            print("[ERREUR] Échec de l'alignement sur la référence : {}".format(ref))
            sys.exit(1)

        print("[OK] Alignement terminé : {}".format(sam_file))

    print("[INFO] Alignements terminés dans : {}".format(args.output_dir))

if __name__ == "__main__":
    main()