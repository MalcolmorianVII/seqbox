import pytest

@test_check_culture_info_decorator
def test_check_info(test_data,valid_keys):
    assert isinstance(test,dict)
    assert len(test_data) > 1
    for valid_key in valid_keys:
        assert test_data[valid_key]

    # Feels like redudancy
    # for key in test_data.keys():
    #     assert key in valid_keys

artic_covid_result_valid_keys = ['sample_name','pct_N_bases','pct_covered_bases','num_aligned_reads']
covid_confirmatory_pcr_info_valid_keys = ['sample_identifier','date_extracted',
                                            'extraction_identifier','date_covid_confirmatory_pcred',
                                            'covid_confirmatory_pcr_identifier','group_name','covid_confirmatory_pcr_protocol']

cultures_info_valid_keys = ['culture_identifier','date_cultured','submitter_plate_id','submitter_plate_well']

def test_check_culture_info_decorator(test_check_info):
    def test_check_info_wrapper(*args,**kwargs):
        test_check_info(check_cultures_test_data, cultures_info_valid_keys)
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


test_check_info(check_artic_covid_result_test_data, artic_covid_result_valid_keys)
test_check_info(check_covid_confirmatory_pcr_test_data, covid_confirmatory_pcr_valid_keys)
# test_check_info(check_cultures_test_data, cultures_info_valid_keys)
test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)

test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)

test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)

test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)
test_check_info(check_function, test_data, valid_keys)

def test_check_artic_covid_result(artic_covid_result_info):
    valid_keys = ['sample_name','pct_N_bases','pct_covered_bases','num_aligned_reads']
    assert artic_covid_result_info['sample_name']
    assert artic_covid_result_info['pct_N_bases']
    assert artic_covid_result_info['pct_covered_bases']
    assert artic_covid_result_info['num_aligned_reads']
    for key in artic_covid_result_info.keys():
        assert key in valid_keys

