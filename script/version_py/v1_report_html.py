#!/usr/bin/env python3
#coding: utf-8


import csv
import re
import argparse
import os
from jinja2 import Environment, FileSystemLoader
 
     

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
        read1_line = lines[6]
        read1_count = int(read1_line.split(' ')[0])
        read2_line = lines[7]
        read2_count = int(read2_line.split(' ')[0])
    return mapping_percentage, read1_count, read2_count


# fonction crée le csv

def write_to_csv(file, data):
    input_filename1 = os.path.splitext(os.path.basename(args.input_file1))[0]
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Sample Name', 'Mapping Percent', 'Read1 Count', 'Read2 Count', 'Coverege percent'])
        writer.writerow([input_filename1] + list(data))
        
        
        
#fonction pour crée le html : 

def generate_html_report(csv_file, html_file):
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            data.append(dict(zip(headers, row)))

        # Load the template file using jinja2.Environment
        
        template_loader = FileSystemLoader(templatesFolder)
        template_env = Environment(loader=template_loader)
        template = template_env.get_template('template.html')
        
        # Render the template using the data from the CSV file
        rendered_template = template.render(headers=headers, data=data)
        # Write the rendered template to the HTML file
        with open(html_file, 'w') as f:
           f.write(rendered_template)    
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract mapping and coverage information from two files and write it to a csv file.')
    parser.add_argument('-i', '--input_file1', type=str, required=True, help='The flagstats.txt file')
    parser.add_argument('-c', '--input_file2', type=str, required=True, help='The coverage.txt file')
    #parser.add_argument('-t', '--template', type=str, required=True, help='The html template file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='The output report html file')
    parser.add_argument('-t','--templates', type=str, nargs=1, help='Template folder localisation', default="templates")
    args = parser.parse_args()

#-----------------------------------------------------
#inputPath=args.input_file1[0]
#inputPath2=args.input_file2[0]
#outputPath=args.output_file[0]
    templatesFolder=args.templates[0]

#inputFile=re.split('/',inputPath)[-1]
#inputFile2=re.split('/',inputPath2)[-1]
#outputFile=re.split('/',outputPath)[-1]

#sampleID=re.split('\\.txt',inputFile)[0]
#folder=re.split(inputFile,inputPath)[0]

#sampleList=[]
#sampleList.append(sampleID)
#------------------------------------------------------
    mapping_data = extract_mapping_info(args.input_file1)
    covered_percent = extract_covered_percent(args.input_file2, "Covered_percent")
    data = mapping_data + (covered_percent,)
    write_to_csv(args.output_file, data)
    generate_html_report(args.output_file, args.output_file.replace('.csv', '.html'))
    print("done extraction")

