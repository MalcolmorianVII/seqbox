import pytest

@pytest.mark.info_present
def test_is_elution_info_present(supply_dict_info_per_sample):
    message = f"elution_plate_id and elution_plate_well must both be present or both be absent for this line {supply_dict_info_per_sample}. Exiting."
    assert isinstance(supply_dict_info_per_sample, "dict")
    assert supply_dict_info_per_sample['elution_plate_id'] == '' & supply_dict_info_per_sample['elution_plate_well'] == ''
    assert supply_dict_info_per_sample['elution_plate_id'] != '' & supply_dict_info_per_sample['elution_plate_well'] != ''
    assert supply_dict_info_per_sample['elution_plate_id'] == '' & supply_dict_info_per_sample['elution_plate_well'] != '',message
    supply_dict_info_per_sample['elution_plate_id'] != '' & supply_dict_info_per_sample['elution_plate_well'] == '',message


    