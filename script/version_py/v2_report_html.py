#!/usr/bin/env python3
#coding: utf-8


import csv
import re
import argparse
import os
import jinja2



def extract_covered_percent(file, column_name):
    with open(file, 'r') as f:
        header = f.readline().strip().split("\t")
        covered_percent_column = header.index(column_name)
        for line in f:
            line_data = line.strip().split("\t")
            covered_percent = float(line_data[covered_percent_column])
            break
    return covered_percent


def extract_mapping_info(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        mapping_line = lines[4]
        mapping_percentage = float(re.search(r'\d+\.\d+', mapping_line).group(0))
        all_reads_line = lines[0].split('\t')[0]
        aligned_reads_line = lines[4].split('\t')[0]
        #unaligned_reads_line = lines[7].split('\t')[0]
        # Extraire le nombre de reads alignés et non alignés
        all_reads_count = int(all_reads_line.split(' ')[0])
        aligned_reads_count = int(aligned_reads_line.split(' ')[0])
        #unaligned_reads_count = int(unaligned_reads_line.split(' ')[0])
        unaligned_reads_count = all_reads_count - aligned_reads_count 
    print(all_reads_count)
    return mapping_percentage, all_reads_count, aligned_reads_count, unaligned_reads_count

def write_to_csv(file, data):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Sample Name', 'Mapping Percent', 'all_reads_count', 'aligned_reads_count', 'unaligned_reads_count', 'Coverage percent'])
        data_sorted = sorted(data, key=lambda x: x[0])  # trier les données par ordre alphabétique sur la colonne "Sample Name"
        for row in data_sorted:
            writer.writerow(row)


def generate_html_report(csv_file, html_file):
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            data.append(dict(zip(headers, row)))
    # Load the template file using jinja2.Environment
    template_loader = jinja2.FileSystemLoader(args.template)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("template.html")
    # Render the template using the data from the CSV file
    rendered_template = template.render(headers=headers, data=data, samplename=samplename)
    # Write the rendered template to the HTML file
    with open(html_file, 'w') as f:
        f.write(rendered_template)


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Extract mapping and coverage information from two directories and write it to a csv file.')
   parser.add_argument('-i1', '--flagstats_directory', type=str, required=True, help='The directory containing the flagstats.txt files')
   parser.add_argument('-i2', '--coverage_directory', type=str, required=True, help='The directory containing the coverage.txt files')
   parser.add_argument('-t', '--template', type=str, required=True, help='The html template file')
   parser.add_argument('-o', '--output-file', type=str, required=True, help='The output report html file')
   args = parser.parse_args()




   # extraire le nom d'echantillon du chemin d'acces du dossier d'entree
   basename = os.path.basename(args.flagstats_directory)
   if "." in basename:
      samplename = basename.split(".")[1]
   else:
      samplename = basename
   print(f"Processing files for {samplename}")


# process all files in input directory 
   data = []
   for filename1 in os.listdir(args.flagstats_directory):
       if filename1.endswith("stats.txt"):
           filename2 = filename1.replace("stats", "cov")
           flagstats_file = os.path.join(args.flagstats_directory, filename1)
           coverage_file = os.path.join(args.coverage_directory, filename2)
           mapping_data = extract_mapping_info(flagstats_file)
           covered_percent = extract_covered_percent(coverage_file, "Covered_percent")
           input_filename = os.path.basename(flagstats_file).split('.')[0]
           data.append([input_filename] + list(mapping_data) + [covered_percent])
           print(f"Processed {flagstats_file} and {coverage_file}")
   write_to_csv(args.output_file, data)
   generate_html_report(args.output_file, args.output_file.replace('.csv', '.html'))
   print(" ***done create report*** ")
