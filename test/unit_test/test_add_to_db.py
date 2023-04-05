# import pytest
from app import models
from scripts import seqbox_utils

def test_add_info(ORM_model,add_function,test_data):
    # Model instance attributes
    valid_table_cols = ORM_model.__table__.columns.keys()[1:] # Exclude the id col & the relations
    # Before adding to db
    before_add = len(ORM_model.query.all())
    # DB changes
    add_result = add_function(test_data)
    # After adding to db
    after_add = len(ORM_model.query.all())
    # test length of input data
    assert len(test_data) == len(valid_table_cols)
    assert after_add - before_add == 1


artic_covid_result_info = {"sample_name":"CHJ18AX","pct_N_bases":2,
                            "pct_covered_bases":98,"num_aligned_reads":20000,
                            "workflow":"nanopore","profile":"medaka","readset_id":20,"barcode":"2",
                            "readset_batch_name":"acer12345xrt",
                            "notes":""}

test_add_info(models.ArticCovidResult,seqbox_utils.add_artic_covid_result,artic_covid_result_info)

# artic_covid_result_info = {"sample_name":"CHJ18AX","pct_N_bases":2,
#                             "pct_covered_bases":98,"num_aligned_reads":20000,
#                             "workflow":"nanopore","profile":"medaka","readset_id":20,
#                             "notes":""}

# def add_artic_covid_result(supply_db_conn,data):
#     db = supply_db_conn



# test_add_info(models.ArticCovidResult,seqbox_utils.add_artic_covid_result,artic_covid_result_info)
test_add_info(models.ArticCovidResult,seqbox_utils.add_artic_covid_result,artic_covid_result_info)
# test_add_info(models.CovidConfirmatoryPcr,add_covid_confirmatory_pcr,covid_confirmatory_pcr_info)
# test_add_info(models.ArticCovidResult,add_artic_covid_result,artic_covid_result_info) # Redundancy with test1 above??
# test_add_info(models.Culture,add_culture,culture_info)
# test_add_info(models.Extraction,add_elution_info_to_extraction,elution_info)

# test_add_info(models.Extraction,add_extraction,extraction_info)
# test_add_info(models.Groups,add_group,group_info)
# test_add_info(models.Mykrobe,add_mykrobe_result,mykrobe_result_info)
# test_add_info(models.PangolinResult,add_pangolin_result,pangolin_result_info)
# test_add_info(models.PcrAssay,add_pcr_assay,pcr_assay_info)

# test_add_info(models.PcrResult,add_pcr_result,pcr_result_info)
# test_add_info(models.Project,add_project,project_info)
# test_add_info(models.RawSequencingBatch,add_raw_sequencing_batch,raw_sequencing_batch_info)
# test_add_info(models.ReadSet,add_readset(readset_info, covid, nanopore_default))
# test_add_info(models.ReadSetBatch,add_readset_batch,readset_batch_info)

# test_add_info(models.Sample,add_sample,sample_info)
# test_add_info(models.SampleSource,add_sample_source,sample_source_info)
# test_add_info(models.TilingPcr,add_tiling_pcr,tiling_pcr_info)

# def add_elution_info_to_extraction(elution_info,conn):
#     extraction = test_get_extraction(elution_info)
#     extraction.elution_plate_id = elution_info['elution_plate_id']
#     extraction.elution_plate_well = elution_info['elution_plate_well']
#     conn.session.commit()
#     print(f"Adding elution info for {elution_info['sample_identifier']} extraction on "
#           f"{elution_info['date_extracted']} to the DB")
#     return True
    


# @pytest.mark.add_info_to_db
# def test_add_elution_info_to_extractions(supply_elution_info,supply_db_conn):
#     all_elution_info = read_in_as_dict(supply_elution_info)
#     not_added_message = f"Elution information is not present for {elution_info['sample_identifier']} from {elution_info['group_name']}. Not adding to DB."
#     no_extraction_info_message = f"""No Extraction match for {elution_info['sample_identifier']}, extracted on
#               {elution_info['date_extracted']} for extraction id
#               {elution_info['extraction_identifier']}
#               need to add that extract and re-run. Exiting."""
#     for elution_info in all_elution_info:
#         assert elution_info['elution_plate_well'] in {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
#                                                     'A11', 'A12', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',
#                                                     'B9', 'B10', 'B11', 'B12', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
#                                                     'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4',
#                                                     'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'E1', 'E2',
#                                                     'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
#                                                     'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
#                                                     'F11', 'F12', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8',
#                                                     'G9', 'G10', 'G11', 'G12', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
#                                                     'H7', 'H8', 'H9', 'H10', 'H11', 'H12'}
#         assert test_is_elution_info_present(elution_info) is True
#         assert test_get_extraction(elution_info) is False
#         assert add_elution_info_to_extraction(elution_info,supply_db_conn),not_added_message
        