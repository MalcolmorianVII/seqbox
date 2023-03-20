import pytest

def add_elution_info_to_extraction(elution_info,conn):
    extraction = test_get_extraction(elution_info)
    extraction.elution_plate_id = elution_info['elution_plate_id']
    extraction.elution_plate_well = elution_info['elution_plate_well']
    conn.session.commit()
    print(f"Adding elution info for {elution_info['sample_identifier']} extraction on "
          f"{elution_info['date_extracted']} to the DB")
    return True
    


@pytest.mark.add_info_to_db
def test_add_elution_info_to_extractions(supply_elution_info,supply_db_conn):
    all_elution_info = read_in_as_dict(supply_elution_info)
    not_added_message = f"Elution information is not present for {elution_info['sample_identifier']} from {elution_info['group_name']}. Not adding to DB."
    no_extraction_info_message = f"""No Extraction match for {elution_info['sample_identifier']}, extracted on
              {elution_info['date_extracted']} for extraction id
              {elution_info['extraction_identifier']}
              need to add that extract and re-run. Exiting."""
    for elution_info in all_elution_info:
        assert elution_info['elution_plate_well'] in {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
                                                    'A11', 'A12', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',
                                                    'B9', 'B10', 'B11', 'B12', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
                                                    'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4',
                                                    'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'E1', 'E2',
                                                    'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
                                                    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
                                                    'F11', 'F12', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8',
                                                    'G9', 'G10', 'G11', 'G12', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
                                                    'H7', 'H8', 'H9', 'H10', 'H11', 'H12'}
        assert test_is_elution_info_present(elution_info) is True
        assert test_get_extraction(elution_info) is False
        assert add_elution_info_to_extraction(elution_info,supply_db_conn),not_added_message
        