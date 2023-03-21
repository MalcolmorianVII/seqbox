# import pytest

def test_get_data_from_db(ORM_model,get_fxn,data_to_get):
    # Model instance attributes
    valid_table_cols = ORM_model.__table__.columns.keys()[1:] # Exclude the id col & the relations
    # Before adding to db
    before_add = len(ORM_model.query.all())
    # DB changes
    add_result = add_function(test_data)
    # After adding to db
    after_add = len(ORM_model.query.all())
    # test length of input data
    assert len(test_data) == len(inst_attribs)
    assert after_add - before_add == 1


artic_covid_result_valid_keys = ['sample_name','pct_N_bases','pct_covered_bases','num_aligned_reads']
covid_confirmatory_pcr_info_valid_keys = ['sample_identifier','date_extracted',
                                            'extraction_identifier','date_covid_confirmatory_pcred',
                                            'covid_confirmatory_pcr_identifier','group_name','covid_confirmatory_pcr_protocol']

cultures_info_valid_keys = ['culture_identifier','date_cultured','submitter_plate_id','submitter_plate_well']

extraction_info_valid_keys = ['sample_identifier','date_extracted',
                            'extraction_identifier','group_name',
                            'extraction_from','nucleic_acid_concentration','submitter_plate_id']

group_info_valid_keys = ['group_name','institution']
mykrobe_res_info_valid_keys = ['sample', 'drug', 'susceptibility', 'mykrobe_version']
pangolin_result_info_valid_keys = ['taxon','lineage','status'] # status instead of qc_status??
pcr_result_info_valid_keys = ['sample_identifier', 'date_pcred', 'pcr_identifier', 'group_name', 'assay_name']
project_info_valid_keys = ['project_name','group_name','institution']
raw_sequencing_batch_info_valid_keys = ['batch_directory','batch_name','date_run','sequencing_type','instrument_name','flowcell_type']

readset_batch_info_valid_keys = ['raw_sequencing_batch_name','readset_batch_name','readset_batch_dir','basecaller']
readset_info_valid_keys = ['data_storage_device',
                         'sample_identifier', 'group_name', 
                         'readset_batch_name','barcode',
                         'path_fastq','path_fast5','path_r1','path_r2',
                         'date_tiling_pcred','tiling_pcr_identifier',
                         'date_extracted','extraction_identifier'] # some fields depend on whether its illumina/nanopore data

sample_source_info_with_project_valid_keys = ['projects','sample_source_identifier']
sample_source_info_valid_keys = ['projects','sample_source_identifier','sample_source_type','group_name','institution']
sample_info_valid_keys = ['sample_source_identifier','sample_identifier','group_name','institution']
tiling_pcr_info_valid_keys = ['sample_identifier', 'date_extracted', 'extraction_identifier', 'date_tiling_pcred',
                'tiling_pcr_identifier', 'group_name', 'tiling_pcr_protocol']

def test_check_culture_info_decorator(test_check_info):
    def test_check_info_wrapper(*args,**kwargs):
        test_get_data_from_db(check_cultures_test_data, cultures_info_valid_keys)
        assert culture_info['submitter_plate_id'].startswith('CUL')
        assert culture_info['submitter_plate_well'] in {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
                                                       'A11', 'A12', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',
                                                       'B9', 'B10', 'B11', 'B12', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
                                                       'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4',
                                                       'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'E1', 'E2',
                                                       'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
                                                       'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
                                                       'F11', 'F12', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8',
                                                       'G9', 'G10', 'G11', 'G12', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
                                                       'H7', 'H8', 'H9', 'H10', 'H11', 'H12'}
    return test_check_info_wrapper


def extend_test_check_extraction_info(extraction_info):
    allowed_extraction_from = ['cultured_isolate', 'whole_sample']
    allowed_submitter_plate_prefixes = ('EXT', 'CUL')
    assert extraction_info['extraction_from'] not in allowed_extraction_from
    assert extraction_info['submitter_plate_id'].startswith(allowed_submitter_plate_prefixes)
    assert extraction_info['submitter_plate_well'] in {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12'}

def extend_check_pcr_result(pcr_result_info):
    allowable_results = {'Negative', 'Negative - Followup', 'Positive - Followup', 'Positive',
                         'Indeterminate', 'Not Done'}
    assert pcr_result_info['pcr_result'] in allowable_results


test_get_data_from_db(check_artic_covid_result_test_data, artic_covid_result_valid_keys)
test_get_data_from_db(check_covid_confirmatory_pcr_test_data, covid_confirmatory_pcr_valid_keys)
# test_get_data_from_db(check_cultures_test_data, cultures_info_valid_keys)
test_get_data_from_db(check_extraction_fields_test_data, extraction_info_valid_keys)
test_get_data_from_db(check_group_test_data, group_info_valid_keys)

test_get_data_from_db(check_mykrobe_res_test_data, mykrobe_res_info_valid_keys)
test_get_data_from_db(check_pangolin_result_test_data, pangolin_result_info_valid_keys)
test_get_data_from_db(check_pcr_result_test_data, pcr_result_info_valid_keys)
test_get_data_from_db(check_project_test_data, project_info_valid_keys)
test_get_data_from_db(check_raw_sequencing_batch_test_data, raw_sequencing_batch_info_valid_keys)

test_get_data_from_db(check_readset_batches_test_data, readset_batch_info_valid_keys)
test_get_data_from_db(check_readset_fields_test_data, readset_info_valid_keys)
test_get_data_from_db(check_sample_source_associated_with_project_test_data, sample_source_info_with_project_valid_keys)
test_get_data_from_db(check_sample_sources_test_data, sample_source_info_valid_keys)

test_get_data_from_db(check_samples_test_data, sample_info_valid_keys)
test_get_data_from_db(check_tiling_pcr_test_data, tiling_pcr_info_valid_keys)

def test_check_artic_covid_result(artic_covid_result_info):
    valid_keys = ['sample_name','pct_N_bases','pct_covered_bases','num_aligned_reads']
    assert artic_covid_result_info['sample_name']
    assert artic_covid_result_info['pct_N_bases']
    assert artic_covid_result_info['pct_covered_bases']
    assert artic_covid_result_info['num_aligned_reads']
    for key in artic_covid_result_info.keys():
        assert key in valid_keys

