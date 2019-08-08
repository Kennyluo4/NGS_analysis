
# Scripts collection for analysis

* this is the collection of all the analysis scripts majorly used for sequencing study.

    

| script | function*|
| ---| --- |
| DNAprocess.py | a module used for DNA sequence processing.functions include: get reverse complementary sequence translate DNA sequence to Amio Acid |                   
| get_fastqc.py | used for get the fastqc report summary of all files (FAIL, WARN and PASS for each module). figures are excluded
| fastq_length_filter.py| from trimmomatic result fastq files. classify reads with different length range based on the cutoff. output 2 types (long and short) fastq files |
| mstrg_prep.py| For merged transcript GFF file by stringtie, appending refgene ID to stringtie assigned gene ID (MSTRG.*) if the gene region includes a ref gene |
| get_trim_report.py| extract the trimming statistics from Trimmomatic log file |
| get_align_stat.py| extract alignment statistics from Hisat2 |
| extract_assembled_id_from_stringtie.py| extract ref gene ID, transcript ID and assembled stringtie gene ID. (recommend to use mstrg_prep.py to avoid this step) |
| class_transform.py| transform result from OrthoMCL, classify by species within a category  |
| reciprocol_blast_selection.py| Get the top hit pairs for reciprocal blast |
| get_MATS_result.py| handling rMATS result. Summarizing all the significant alternative splicing even from different output files from rMATS |
| counting_transcripts.py| counting the number of transcripts in GFF/GTF file. |
| extractGOfromGFF.py| extract GO ids from gff3 file |
| ---| --- |
 
 \* for specific requirement or usage, please look into the script file.
