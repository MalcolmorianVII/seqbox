set -e
set -o pipefail

#rm app/pa_seqbox_v2_test.db
python3 test_no_web.py # creates db
python3 ../src/scripts/seqbox_cmd.py add_groups -i 06.test/groups.csv
python3 ../src/scripts/seqbox_cmd.py add_projects -i 06.test/projects.csv
python3 ../src/scripts/seqbox_cmd.py add_sample_sources -i 06.test/sample_sources.csv
python3 ../src/scripts/seqbox_cmd.py add_samples -i 06.test/samples.csv
python3 ../src/scripts/seqbox_cmd.py add_extractions -i 06.test/extraction.csv
python3 ../src/scripts/seqbox_cmd.py add_raw_sequencing_batches -i 06.test/raw_sequencing_batch.csv
python3 ../src/scripts/seqbox_cmd.py add_readset_batches -i 06.test/readset_batches.csv
python3 ../src/scripts/seqbox_cmd.py add_readsets -i 06.test/nanopore_readsets.csv
python3 ../src/scripts/seqbox_filehandling.py add_readset_to_filestructure -i 06.test/nanopore_readsets.csv -c test_seqbox_config.yaml

