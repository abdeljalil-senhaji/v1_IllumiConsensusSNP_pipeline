# functions.py

def get_bowtie_outputs(wildcards):
    import os
    extract_file = os.path.join(wildcards.prefix, wildcards.sample, wildcards.sample + "_extractBlast.txt")
    with open(extract_file) as f:
        refs = [line.strip() for line in f if line.strip()]
    return [os.path.join(wildcards.prefix, wildcards.sample, "{}.sam".format(ref)) for ref in refs]