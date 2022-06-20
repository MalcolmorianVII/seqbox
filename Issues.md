# Issue Tracker

## Issue 1:No matching distribution found for python-graphviz

**Description:**
* ERROR: Could not find a version that satisfies the requirement python-graphviz (from versions: none)

**Solution**
* python-graphviz not found in pyPI.Therefore removed it from the requirements.txt

# Issue 2:flask installations
**Description:**
* It seems all the packages installed through pip are here:
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages

*Problems:*
Conda env issue i.e the seqbox env not being activated when running the script.

*Solution*
Changed the python interpreter on VSCode

# Issue 3: Changing paths
Relative paths issue for test bash scripts
Made the following changes:
	1. test/test_no_web.py to  test_no_web.py
	2. /src/scripts/seqbox_cmd.py to  ../src/scripts/seqbox_cmd.py
	3.  /src/scripts/seqbox_filehandling.py to  /src/scripts/seqbox_filehandling.py
	
Changed from /Users/flashton/Dropbox/non-project/test_input_data/20201201_1355_MN33881_FAO20804_109641e0/fast5_pass  TO /Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/data

Other changes 
Replace test/06.test to 06.test
Replace test/test_seqbox_config.yaml to test_seqbox_config.yaml

*Data to download*
20201201_1355_MN33881_FAO20804_109641e0
20210601_1134_DK-111231_0_FAO09894_ba56ad3
Illumina_batch_1

# Issue 4:  test2 quagmire
Command ./run_test_02.sh

*Error:*
File "/Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/seqbox/test/../src/scripts/seqbox_filehandling.py", line 72, in run_add_readset_to_filestructure
    add_readset_to_filestructure(readset_nanopre.readset, config)
AttributeError: 'NoneType' object has no attribute 'readset'

Suggestion: None == False equals False hence giving error

Solution: Changed to  if not readset_nanopre :

Now it reads like this:

There is no readset for
{'sample_identifier': 'CMT15I', 'date_tiling_pcred': '01/06/2021', 'tiling_pcr_identifier': '1', 'date_extracted': '', 'extraction_identifier': '', 'group_name': 'Core', 'barcode': 'barcode01', 'data_storage_device': 'local', 'readset_batch_name': '20201201_1355_MN33881_FAO20804_109641e0'}
Exiting.

# Issue 5: Test 3

 File "/Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/seqbox/src/scripts/seqbox_utils.py", line 286, in read_in_extraction
    if extraction_info['extraction_processing_institution'] != '':
KeyError: 'extraction_processing_institution'

Printing extraction_info gives the following:

---------Extraction info------------
{'sample_identifier': 'PTS15G_sample1', 'extraction_identifier': '1', 'extraction_machine': 'QiaSymphony', 'extraction_kit': 'MiniKit', 'what_was_extracted': 'DNA', 'date_extracted': '01/06/2021', 'processing_institution': 'MLW', 'group_name': 'Core', 'extraction_from': 'isolate'}
---------Extraction info------------

Solution: There is no extraction_processing_institution BUT processing institution therefore change lines 289 & 290 of seqbox_utils.py to reflect the correct key in the dict
STATUS:Run successfully!!!


# Issue 6 : TEST 4

 File "/Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/seqbox/src/scripts/seqbox_utils.py", line 993, in basic_check_readset_fields
    if readset_info[r].strip() == '':
KeyError: 'barcode'

Solution:

------Printing readset info-------
{'sample_identifier': 'ABS15I_sample1', 'date_pcred': '', 'pcr_identifier': '', 'date_extracted': '01/06/2021', 'extraction_identifier': '1', 'group_name': 'Core', 'path_r1': '/Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/data/illumina_batch_1/ABS15I_sample1_1.fastq.gz', 'path_r2': '/Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/data/illumina_batch_1/ABS15I_sample1_2.fastq.gz', 'readset_batch_name': 'illumina_batch_1', 'data_storage_device': 'local'}
------Printing readset info-------

Suggestion: Readset info dict does not have a barcode Key. BUT these two functions :

basic_check_readset_fields(readset_info) & 

check_readset_fields(readset_info, nanopore_default, raw_sequencing_batch, covid)

Suggest that the barcode key should exist

Therefore find where the readset_info dict is made


More digging

 File "/Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/seqbox/test/../src/scripts/seqbox_cmd.py", line 63, in add_readsets
    if basic_check_readset_fields(readset_info) is False:

Discovery:
The code is not taking into account the illumina_batch_1 which should not have barcode.

Therefore added this line in seqbox_utils.py line 997 to 999:


if not has_barcode:
            print("Illumina batch no need for a barcode")
            return

Now it is giving the following:
There is no readset for
{'sample_identifier': 'ABS15I_sample1', 'date_pcred': '', 'pcr_identifier': '', 'date_extracted': '01/06/2021', 'extraction_identifier': '1', 'group_name': 'Core', 'path_r1': '/Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/data/illumina_batch_1/ABS15I_sample1_1.fastq.gz', 'path_r2': '/Users/malcolmorian/Documents/Bioinformatics/Projects2022/seq_service/data/illumina_batch_1/ABS15I_sample1_2.fastq.gz', 'readset_batch_name': 'illumina_batch_1', 'data_storage_device': 'local'}
Exiting.

Refer to test2 solution i.e seqbox_file handling.py 

TEST 5: Just like test 4

TEST 6
Runs okay & exists upon finding repeats

TEST 7: Issues no repeat for …. See 


