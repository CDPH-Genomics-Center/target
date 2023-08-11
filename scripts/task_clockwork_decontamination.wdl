version 1.0

task map_reads {
  input {
    String sample_name
    File reference
    File input_reads_1
    File input_reads_2
    String output_bam
    String memory = "32GB"			
    String docker = "dbest/clockwork:v1.0.0"
    Int threads = 1
  }

  command {
    clockwork map_reads --threads ${threads} --unsorted_sam ${sample_name} ${reference} ${output_bam} ${input_reads_1} ${input_reads_2}
  }
  
  output {
    File bam_file = output_bam
  }
  
  runtime {
    docker: docker
    memory: memory
    maxRetries: 3
    cpu: threads
  }
}

task remove_contam {
  input {
    File metadata_file
    File input_bam
    String output_file
    String output_reads_1
    String output_reads_2
    String memory = "32GB"
    String docker = "dbest/clockwork:v1.0.0"
  }

  command {
    clockwork remove_contam ${metadata_file} ${input_bam} ${output_file} ${output_reads_1} ${output_reads_2}
  }

  output {
    File removed_contam_file = output_file
    File cleaned_reads_1 = output_reads_1
    File cleaned_reads_2 = output_reads_2
  }

  runtime {
    docker: docker
    memory: memory
    maxRetries: 3
  }
}

