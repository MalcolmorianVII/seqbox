set -e
set -o pipefail

#rm app/pa_seqbox_v2_test.db
python3 test_no_web.py # creates db
python3 ../src/scripts/seqbox_cmd.py add_groups -i 01.test_todo_list_query/groups.csv
python3 ../src/scripts/seqbox_cmd.py add_projects -i 01.test_todo_list_query/projects.csv
python3 ../src/scripts/seqbox_cmd.py add_sample_sources -i 01.test_todo_list_query/sample_sources.csv
python3 ../src/scripts/seqbox_cmd.py add_samples -i 01.test_todo_list_query/samples.csv
python3 ../src/scripts/seqbox_cmd.py add_extractions -i 01.test_todo_list_query/extraction.csv
python3 ../src/scripts/seqbox_cmd.py add_tiling_pcrs -i 01.test_todo_list_query/tiling_pcr.csv
python3 ../src/scripts/seqbox_cmd.py add_covid_confirmatory_pcrs -i 01.test_todo_list_query/confirmatory_pcr.csv
python3 ../src/scripts/seqbox_cmd.py add_raw_sequencing_batches -i 01.test_todo_list_query/raw_sequencing_batch.csv
python3 ../src/scripts/seqbox_cmd.py add_readset_batches -i 01.test_todo_list_query/readset_batches.csv
python3 ../src/scripts/seqbox_cmd.py add_readsets -i 01.test_todo_list_query/nanopore_default_readsets.csv -s -n
python3 ../src/scripts/seqbox_filehandling.py add_readset_to_filestructure -i 01.test_todo_list_query/nanopore_default_readsets.csv -c test_seqbox_config.yaml -s -n


echo "****Test round 2****"
python3 ../src/scripts/seqbox_cmd.py add_groups -i 01.test_todo_list_query/groups.csv
python3 ../src/scripts/seqbox_cmd.py add_projects -i 01.test_todo_list_query/projects.csv
python3 ../src/scripts/seqbox_cmd.py add_sample_sources -i 01.test_todo_list_query/sample_sources.csv
python3 ../src/scripts/seqbox_cmd.py add_samples -i 01.test_todo_list_query/samples.csv
python3 ../src/scripts/seqbox_cmd.py add_extractions -i 01.test_todo_list_query/extraction.csv
python3 ../src/scripts/seqbox_cmd.py add_tiling_pcrs -i 01.test_todo_list_query/tiling_pcr.csv
python3 ../src/scripts/seqbox_cmd.py add_covid_confirmatory_pcrs -i 01.test_todo_list_query/confirmatory_pcr.csv
python3 ../src/scripts/seqbox_cmd.py add_raw_sequencing_batches -i 01.test_todo_list_query/raw_sequencing_batch.csv
python3 ../src/scripts/seqbox_cmd.py add_readset_batches -i 01.test_todo_list_query/readset_batches.csv
python3 ../src/scripts/seqbox_cmd.py add_readsets -i 01.test_todo_list_query/nanopore_default_readsets.csv -s -n
python3 ../src/scripts/seqbox_filehandling.py add_readset_to_filestructure -i 01.test_todo_list_query/nanopore_default_readsets.csv -c test_seqbox_config.yaml -s -n

