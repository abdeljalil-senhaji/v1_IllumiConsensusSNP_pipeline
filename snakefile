import re
import glob
import os



rulePath=config["general_path"]["RULE_PATH"]


include: rulePath+"/iget_samples_rule"
include: rulePath+"/trimmomatic_rule"
#include: rulePath+"/fastq_to_fasta_rule"
include: rulePath+"/iget_reference_bowtie2_rule"
include: rulePath+"/bowtie2_rule"
include: rulePath+"/samtools_flagstat_rule"
include: rulePath+"/pileup_sh_rule"
include: rulePath+"/iget_location_rule"
include: rulePath+"/samtools_sam_to_bam_rule"
include: rulePath+"/samtools_sort_rule"
include: rulePath+"/markduplicates_rule"
include: rulePath+"/samtools_mpileup_rule"
#include: rulePath+"/samtools_index_rule"
include: rulePath+"/bcftools_consensus_rule"
include: rulePath+"/spades_rule"
include: rulePath+"/filter_contigs_rule"
include: rulePath+"/blast_rule"
include: rulePath+"/extract_ref_ids_from_blast_rule"
include: rulePath+"/bowtie2_align_from_ref_ids_rule"
include: rulePath+"/report_html_v2_rule"


workdir: config["general_path"]["OUTPUT_PATH"]
input_path = config["general_path"]["INPUT_PATH"]
output_path = config["general_path"]["OUTPUT_PATH"]


sample_ids = []
sampleName=glob.glob("/scratch/recherche/asenhaji/v1_IllumiConsensusSNP_pipeline/data/*.fastq.gz")
for name in sampleName:
    path = input_path + "/"
    name = name.replace(path, '')
    a = re.split('/', name)
    name = a[0]
    name = name.replace('_R1_001.fastq.gz', '')
    name = name.replace('_R2_001.fastq.gz', '')
    sample_ids.append(name)


mate_ids = ["R1","R2"]
ref_ids = ["HAdVrefA",  "HAdVrefB",  "HAdVrefC", "HAdVrefD", "HAdVrefE", "HAdVrefF", "HAdVrefG", "HAdVrefB2"]
with open("/scratch/recherche/asenhaji/v1_IllumiConsensusSNP_pipeline/db/list_ref.txt") as f:
    ref_all_ids = [line.strip() for line in f if line.strip()]

#genome_ids = 


#iget_samples = expand((output_path+"/{sample_id}/{sample_id}_L001_{mate_id}_001.fastq.gz"), sample_id = sample_ids, mate_id = mate_ids),
#iget_reference = expand((output_path+"/{sample_id}/{ref_id}/{ref_id}.fasta", output_path+"/{sample_id}/{ref_id}/{ref_id}.fasta.amb", output_path+"/{sample_id}/{ref_id}/{ref_id}.fasta.ann", output_path+"/{sample_id}/{ref_id}/{ref_id}.fasta.bwt", output_path+"/{sample_id}/{ref_id}/{ref_id}.fasta.fai", output_path+"/{sample_id}/{ref_id}/{ref_id}.fasta.pac", output_path+"/{sample_id}/{ref_id}/{ref_id}.fasta.sa",  sample_id =sample_ids, ref_id = ref_ids),
#trimmomatic = expand((output_path+"/{sample_id}/{sample_id}_R1_paired.fq.gz", output_path+"/{sample_id}/{sample_id}_R2_paired.fq.gz", output_path+"/{sample_id}/{sample_id}_R _unpaired_trim.fq.gz", output_path+"/{sample_id}/{sample_id}_R2_unpaired_trim.fq.gz"), sample_id = sample_ids),

#fastq_to_fasta =  expand(output_path+"/{sample_id}/{sample_id}_reads.fasta",  sample_id = sample_ids),

#fastqc = expand(output_path+"/{sample_id}/fastqc/{sample_id}_fastqc.html", "/{sample_id}/fastqc/{sample_id}_fastqc.zip",  sample_id = sample_ids),
#multiqc = expand((output_path+"/multiqc/results/{sample_id}/multiqc_report.html"), sample_id =sample_ids),
#multiqc = (output_path+"/multiqc/results/multiqc_report.html"),
#iget_location = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_R1_paired.fq.gz", "/{sample_id}/{ref_id}/{sample_id}_R2_paired.fq.gz", sample_id =sample_ids, ref_id = ref_ids),
#bwa_mem = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_{ref_id}.sam"), sample_id =sample_ids, ref_id = ref_ids)
#bowtie2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}.sam"), sample_id =sample_ids, ref_id = ref_ids),
#sam2bam = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}.bam"), sample_id =sample_ids, ref_id = ref_ids),
#samtools_sort = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_sorted.bam"), sample_id =sample_ids, ref_id = ref_ids),
#markduplicates = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_dedup_reads.bam", output_path+"/{sample_id}/{sample_id}_metrics.txt"), sample_id = sample_ids, ref_id = ref_ids),
#createsequencedictionnary1 = expand((output_path+"/{sample_id}/{ref_id}/{ref_id}.fasta.dict"), sample_id =sample_ids, ref_id = ref_ids),
#realignertargetcreator = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}.intervals"), sample_id =sample_ids, ref_id = ref_ids),
#indelrealigner = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_realigned_reads.bam"), sample_id =sample_ids, ref_id = ref_ids),
#baserecalibrator = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_recal_data.grp"), sample_id =sample_ids, ref_id = ref_ids),
#printreads = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_recal_reads.bam"), sample_id =sample_ids, ref_id = ref_ids),
#mpileup = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}.pileup"), sample_id =sample_ids, ref_id = ref_ids),
#varscan = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_VS.vcf"), sample_id =sample_ids, ref_id = ref_ids),
#bgzip = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_5_AF_maj.vcf.gz"), sample_id =sample_ids, ref_id = ref_ids),
#tabix = expand((output_path+"/{sample}/{ref_id}/{sample}_VS.vcf.gz.tbi"), sample_id =sample_ids, ref_id = ref_ids),
#genomecov = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_genomecov.bed"), sample_id =sample_ids,ref_id = ref_ids),
#extractline = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_extractline.bprefixed"), sample_id =sample_ids, ref_id = ref_ids),
#bwa_index = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_consensus.fasta.amb", output_path+"/{sample_id}/{ref_id}/{sample_id}_consensus.fasta.ann", output_path+"/{sample_id}/{ref_id}/{sample_id}_consensus.fasta.bwt", output_path+"/{sample_id}/{ref_id}/{sample_id}_consensus.fasta.fai", output_path+"/{sample_id}/{ref_id}/{sample_id}_consensus.fasta.pac", output_path+"/{sample_id}/{ref_id}/{sample_id}_consensus.fasta.sa""), sample_id = sample_ids, ref_id = ref_ids),
#createsequencedictionnary = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_consensus.dict"), sample_id =sample_ids, ref_id = ref_ids),
#samtools_faidx = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_consensus.fasta.fai"), sample_id = sample_ids, ref_id = ref_ids),
#bwa_mem2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2.sam"), sample_id =sample_ids, ref_id = ref_ids),
#sam2bam2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2.bam"), sample_id =sample_ids, ref_id = ref_ids),
#samtools_sort2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2_sorted.bam"), sample_id =sample_ids, ref_id = ref_ids),
#markduplicates2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2_dedup_reads.bam", output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2_metrics.txt"), sample_id = sample_ids, ref_id = ref_ids),
#realignertargetcreator2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2.intervals"), sample_id =sample_ids, ref_id = ref_ids),
#indelrealigner2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2_realigned_reads.bam"), sample_id =sample_ids, ref_id = ref_ids),
#mpileup2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2.pileup"), sample_id =sample_ids, ref_id = ref_ids),
#varscan2 = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}_alg2_VS.vcf"), sample_id = sample_ids, ref_id = ref_ids),
#spades = expand((output_path+"/{sample_id}/{sample_id}_contigs.fasta"),sample_id=sample_ids),
#filter_contigs = expand((output_path+"/{sample_id}/{sample_id}_contigs_200.fasta"),sample_id=sample_ids),
#blast = expand((output_path+"/{sample_id}/{sample_id}_blast.txt"),sample_id=sample_ids),
#extract_ref_ids_from_blast = expand((output_path+"/{sample_id}/{sample_id}_extractBlast.txt"), sample_id = sample_ids)


bowtie2_align_from_ref_ids = expand((output_path+"/{sample_id}/{sample_id}_{ref_all_id}.sam"), sample_id = sample_ids, ref_all_id = ref_all_ids)

#pileup_sh = expand(output_path+"/rapport_html/{sample_id}/{ref_id}.{sample_id}.cov.txt", sample_id = sample_ids, ref_id = ref_ids),
#samtools_flagstat = expand(output_path+"/rapport_html/{sample_id}/{ref_id}.{sample_id}.stats.txt", sample_id = sample_ids, ref_id = ref_ids),
#samtools_index = expand(output_path+"/{sample_id}/{ref_id}/{sample_id}_GroupReads_dedup_reads.bam.bai", sample_id = sample_ids, ref_id = ref_ids),
#bcftools_consensus = expand(output_path+"/{sample_id}/{ref_id}/{sample_id}_{ref_id}_consensus.fasta", sample_id = sample_ids, ref_id = ref_ids),
#report_html_v2 = expand(output_path + "/rapport_html/{sample_id}/report.html", sample_id = sample_ids),
#samtools_mpileup = expand((output_path+"/{sample_id}/{ref_id}/{sample_id}.pileup"), sample_id =sample_ids, ref_id = ref_ids)


		
rule all:
        input:
#               iget_reference_bowtie2,
#               iget_samples,
#               trimmomatic,
#                fastq_to_fasta,
#               iget_location,
#               sam2bam,
#               fastqc,
#               multiqc,
#               samtools_sort,
#               markduplicates,
#               createsequencedictionnary1,
#               realignertargetcreator,
#               indelrealigner,
#               mpileup,
#               varscan,
#               bgzip,
#               tabix,
#               genomecov,
#               extractline,
#               bwa_index,
#               bowtie2,
#               addorreplacereadgroups,
#               samtools_faidx,
#               spades,
#               filter_contigs,
#               blast,
#                extract_ref_ids_from_blast
                bowtie2_align_from_ref_ids
#                pileup_sh,
#                samtools_flagstat,
#               samtools_index,
#                samtools_mpileup,
#                report_html_v2
#               bcftools_consensus
        shell:
                "touch "+output_path+"/done"
