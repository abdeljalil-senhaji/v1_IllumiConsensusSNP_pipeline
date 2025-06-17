#!/usr/bin/env python3
#coding: utf-8


#Create by Abdeljalil Senhaji Rachik
#01/02/2022
#Aphp Hopital saint louis - service virologie
#Script adapter for the Adeno 7rf pipeline



import sys
import csv
import re
import argparse
import os
import jinja2
import glob




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
        # Extraire le nombre de reads alignés et non alignés
        all_reads_count = int(all_reads_line.split(' ')[0])
        aligned_reads_count = int(aligned_reads_line.split(' ')[0])
        unaligned_reads_count = all_reads_count - aligned_reads_count 
    print(all_reads_count)
    return mapping_percentage, all_reads_count, aligned_reads_count, unaligned_reads_count


def write_to_csv(file, data):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Sample Name', 'Mapping Percent', 'All_reads_count', 'Aligned_reads_count', 'Unaligned_reads_count', 'Coverage percent'])
        data_sorted = sorted(data, key=lambda x: x[0])  # trier les données par ordre alphabétique sur la colonne "Sample Name"
        for row in data_sorted:
            writer.writerow(row)


def generate_html_report(csv_file, html_file, samplename):
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            data.append(dict(zip(headers, row)))
    # Load the template file using jinja2.Environment
    template_loader = jinja2.FileSystemLoader(searchpath=args.template)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("template.html")
    # Render the template using the data from the CSV file
    rendered_template = template.render(headers=headers, data=data, samplename=samplename)
    # Write the rendered template to the HTML file
    with open(html_file, 'w') as f:
        f.write(rendered_template)



if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Extract mapping and coverage information from two directories and write it to a csv file.')
   parser.add_argument('-i1', '--flagstats_directory', type=str, nargs=1, required=True, help='The directory containing the flagstats.txt files')
   parser.add_argument('-i2', '--coverage_directory', type=str, nargs=1, required=True, help='The directory containing the coverage.txt files')
   parser.add_argument('-t', '--template', type=str, nargs=1, required=True, help='The html template file')
   parser.add_argument('-o', '--output_file', type=str, required=True, help='The output report html file')
   args = parser.parse_args()

# Rediriger les path afin de l'adapter avec la logique snakemake:

   inputPath1=args.flagstats_directory
   inputPath2=args.coverage_directory


   flagstats_directory1=os.path.dirname(inputPath1)
   coverage_directory1=os.path.dirname(inputPath2)

# Extraire le nom d'echantillon du premier fichier

   flagstat_files = glob.glob(f"{flagstats_directory1}/*.stats.txt")
   if not flagstat_files:
      print(f"No flagstat files found in {flagstats_directory1}")
      sys.exit(1)

   samplename = os.path.basename(flagstat_files[0]).split(".")[1]
   print(f"Processing files for {samplename}")

# Process all files in input directory 
   data = []
   for filename1 in os.listdir(flagstats_directory1):
       if filename1.endswith("stats.txt"):
           filename2 = filename1.replace("stats", "cov")
           flagstats_file = os.path.join(flagstats_directory1, filename1)
           coverage_file = os.path.join(coverage_directory1, filename2)
           mapping_data = extract_mapping_info(flagstats_file)
           print(" ***done extract mapping information*** ")
           covered_percent = extract_covered_percent(coverage_file, "Covered_percent")
           print(" ***done extract covered_percent*** ")
           #extract ref name
           input_filename = os.path.splitext(os.path.basename(flagstats_file))[0].split(".")[0]
           data.append([input_filename] + list(mapping_data) + [covered_percent])
           print(f"Processed {flagstats_file} and {coverage_file}")
   write_to_csv(args.output_file, data)
   print(" ***done create csv file*** ")
   generate_html_report(args.output_file, args.output_file.replace('.csv', '.html'), samplename=samplename)
   print(" ***done create report HTML*** ")


