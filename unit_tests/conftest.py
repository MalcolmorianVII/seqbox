import pytest
from app import db
import numpy as np

@pytest.fixture
def db():
    # Set up a database for testing
    ...


@pytest.fixture()
def sample_source_info():
    
    neg_control = {
        "sample_source_identifier": "sample_001",
        "group_name": "group1",
        "projects": "project1",
        "institution":"MLW"
    }
    pos_control = {
        "sample_source_identifier": "CMT15I",
        "group_name": "Core",
        "projects": "COVIDseq",
        "institution":"MLW"
    }

    yield pos_control,neg_control

@pytest.fixture
def mykrobe_res_info():
    # Test with a dictionary that has a blank 'sample' field
    blank_sample = {'sample': '', 'drug': 'isoniazid', 
                        'susceptibility': 'resistant', 'mykrobe_version': 'v1.0'}
    
    # Test with a dictionary that has a blank 'drug' field
    blank_drug = {'sample': 'sample_01', 'drug': '', 
                        'susceptibility': 'resistant', 'mykrobe_version': 'v1.0'}
    
    # Test with a dictionary that has a blank 'susceptibility' field
    blank_susc = {'sample': 'sample_01', 'drug': 'isoniazid', 
                        'susceptibility': '', 'mykrobe_version': 'v1.0'}
    
    # Test with a dictionary that has a blank 'mykrobe_version' field
    blank_mykrobe_version = {'sample': 'sample_01', 'drug': 'isoniazid', 
                        'susceptibility': 'resistant', 'mykrobe_version': ''}
    
    # Test with a dictionary that has all fields blank
    all_blank_fields = {'sample': '', 'drug': '', 
                        'susceptibility': '', 'mykrobe_version': ''}
    
    # Test with a blank dictionary  
    blank_dict = {}

    # Unexpected input i.e list with gibberish
    gibberish = [1,2,3]


    # Test with a dictionary that has all fields filled in
    all_valid_fields = {'sample': 'sample_01', 'drug': 'isoniazid', 
                        'susceptibility': 'resistant', 'mykrobe_version': 'v1.0'}
    
    yield {'blank_sample':blank_sample,'blank_drug':blank_drug,
    'blank_susc':blank_susc,'blank_mykrobe_version':blank_mykrobe_version,
    'all_blank_fields':all_blank_fields,'blank_dict':blank_dict,'gibberish':gibberish,
    'all_valid_fields':all_valid_fields}
    # yield blank_sample,blank_drug,blank_susc,blank_mykrobe_version,all_blank_fields,all_fields

@pytest.fixture
def pangolin_result_info():
    return {'taxon': 'SARS-CoV-2', 'lineage': 'B.1.1.7', 'status': 'passed'}

@pytest.fixture
def artic_covid_result_info():
    yield {
        'sample_name': 'sample1',
        'pct_N_bases': '0.5',
        'pct_covered_bases': '99.0',
        'num_aligned_reads': '1000'
    },{
        'sample_name': '',
        'pct_N_bases': '0.5',
        'pct_covered_bases': '99.0',
        'num_aligned_reads': '1000'
    }

@pytest.fixture
def raw_sequencing_batch_info():
    # Create test data with an empty batch_directory column
    empty_batch_directory = {'batch_directory': '', 'batch_name': 'Test Batch', 'date_run': '2022-01-01', 
                 'sequencing_type': 'Whole Genome Sequencing', 'instrument_name': 'NovaSeq',
                 'flowcell_type': 'SP'}
    all_non_empty_cols = {'batch_directory': '/path/to/batch', 'batch_name': 'Test Batch', 'date_run': '2022-01-01', 
                 'sequencing_type': 'Whole Genome Sequencing', 'instrument_name': 'NovaSeq',
                 'flowcell_type': 'SP'}
                
    yield empty_batch_directory,all_non_empty_cols

@pytest.fixture
def readset_batch_info():
    # Create test data with an empty raw_sequencing_batch_name column
    empty_raw_sequencing_batch_name = {'raw_sequencing_batch_name': '', 'readset_batch_name': 'Test Readset Batch', 
                 'readset_batch_dir': '/path/to/readset/batch', 'basecaller': 'Guppy'}
    
    # Create test data with all non-empty columns
    all_non_empty = {'raw_sequencing_batch_name': 'Test Raw Sequencing Batch', 'readset_batch_name': 'Test Readset Batch', 
                 'readset_batch_dir': '/path/to/readset/batch', 'basecaller': 'Guppy'}

    yield empty_raw_sequencing_batch_name,all_non_empty

@pytest.fixture
def empty_culture_info():
    return {
        'culture_identifier': '',
        'date_cultured': '',
        'submitter_plate_id': '',
        'submitter_plate_well': ''
    }

@pytest.fixture
def invalid_culture_info():
    return {
        'culture_identifier': '1',
        'date_cultured': '2022-01-01',
        'submitter_plate_id': 'invalid',
        'submitter_plate_well': 'Z1'
    }

@pytest.fixture
def valid_culture_info():
    return {
        'culture_identifier': 'CUL001',
        'date_cultured': '2022-01-01',
        'submitter_plate_id': 'CUL-2022-01-01',
        'submitter_plate_well': 'A1'
    }

@pytest.fixture
def extraction_info():
    # Valid input
    valid_extraction_info = {
        'sample_identifier': 'SAMPLE1',
        'date_extracted': '2022-01-01',
        'extraction_identifier': 1,
        'group_name': 'GROUP1',
        'extraction_from': 'cultured_isolate',
        'nucleic_acid_concentration': 1.0,
        'submitter_plate_id': 'EXT-1',
        'submitter_plate_well': 'A1'
    }

    # Invalid input: empty sample_identifier
    empty_sample_id = {
        'sample_identifier': '',
        'date_extracted': '2022-01-01',
        'extraction_identifier': 1,
        'group_name': 'GROUP1',
        'extraction_from': 'cultured_isolate',
        'nucleic_acid_concentration': 1.0,
        'submitter_plate_id': 'EXT-1',
        'submitter_plate_well': 'A1'
    }

    # Invalid input: empty date_extracted
    empty_date = {
        'sample_identifier': 'SAMPLE1',
        'date_extracted': np.datetime64('NaT'),
        'extraction_identifier': 1,
        'group_name': 'GROUP1',
        'extraction_from': 'cultured_isolate',
        'nucleic_acid_concentration': 1.0,
        'submitter_plate_id': 'EXT-1',
        'submitter_plate_well': 'A1'
    }

    # Invalid input: 
    empty_extraction_id = {
        'sample_identifier': 'SAMPLE1',
        'date_extracted': '2022-01-01',
        'extraction_identifier': np.nan,
        'group_name': 'GROUP1',
        'extraction_from': 'cultured_isolate',
        'nucleic_acid_concentration': 1.0,
        'submitter_plate_id': 'EXT-1',
        'submitter_plate_well': 'A1'
    }

    # Invalid input: 
    empty_group_name= {
        'sample_identifier': 'SAMPLE1',
        'date_extracted': '2022-01-01',
        'extraction_identifier': 1,
        'group_name': '',
        'extraction_from': 'cultured_isolate',
        'nucleic_acid_concentration': 1.0,
        'submitter_plate_id': 'EXT-1',
        'submitter_plate_well': 'A1'
    }
    yield valid_extraction_info,empty_sample_id,empty_date,empty_extraction_id,empty_group_name

# @pytest.fixture
# def sample_source_info():
#     return {
#         'sample_source_identifier': 'sample1',
#         'sample_source_type': 'type1',
#         'projects': 'project1',
#         'group_name': 'group1',
#         'institution': 'institution1'
#     }

@pytest.fixture
def nanopore_default():
    return True

@pytest.fixture
def raw_sequencing_batch():
    class MockRawSequencingBatch:
        sequencing_type = 'nanopore'
    return MockRawSequencingBatch()

@pytest.fixture
def covid():
    return False

# GET FIXTURES 

@pytest.fixture
def sample_data():
    sample = Sample(sample_identifier="S001")
    sample_source = SampleSource(sample_source_identifier="SS001")
    group = Groups(group_name="Group A")
    sample_source.projects.append(group)
    sample.sample_source = sample_source
    db.session.add_all([sample, sample_source, group])
    db.session.commit()
    return {"sample_identifier": "S001", "group_name": "Group A"}

@pytest.fixture
def extraction_data(sample_data):
    extraction = Extraction(extraction_identifier="E001", date_extracted="2022-01-01")
    sample = Sample.query.filter_by(sample_identifier=sample_data["sample_identifier"]).one()
    culture = Culture(culture_identifier="C001")
    extraction.sample = sample
    culture.sample = sample
    db.session.add_all([extraction, culture])
    db.session.commit()
    return {"extraction_identifier": "E001", "date_extracted": "2022-01-01",
            "sample_identifier": sample_data["sample_identifier"], "group_name": sample_data["group_name"]}

