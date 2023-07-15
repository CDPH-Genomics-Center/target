version 1.0

task task_multiqc {
  input {
    Array[File] inputFiles
    String outputPrefix
    String docker = "ewels/multiqc:1.14"
  }
  
  command <<<
    set -ex
    for file in ~{sep=' ' inputFiles}; do
    if [ -e $file ] ; then
    cp $file .
    else
    echo "<W> multiqc: $file does not exist!"
    fi
    done
    multiqc --force --no-data-dir -n ~{outputPrefix}.multiqc .
  >>>

  output {
    File report = "${outputPrefix}.multiqc.html"
  }

  runtime {
    docker: "~{docker}"
  }
}

