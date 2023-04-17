import pytest
from datetime import datetime
from scripts.seqbox_utils import check_sample_source_associated_with_project,check_mykrobe_res,check_pangolin_result,check_artic_covid_result,check_raw_sequencing_batch,check_readset_batches,check_cultures,check_extraction_fields,check_group,check_project,check_sample_sources,check_samples,check_covid_confirmatory_pcr,check_tiling_pcr,check_pcr_result,check_readset_fields
from app.models import SampleSource,Project
from app import db

def test_check_sample_source_associated_with_project(sample_source_info):
    # create a mock version of the SampleSource and Project classes
    mock_sample_source_class = mocker.patch('app.models.SampleSource')
    mock_project_class = mocker.patch('app.models.Project')

    # create a mock version of the database session
    mock_session = mocker.Mock()
    mocker.patch('app.db', mock_session)

    # create a mock version of the SampleSource object with a project association
    mock_sample_source = mock_sample_source_class.return_value
    mock_project = mock_project_class.return_value
    mock_project.project_name = 'COVIDseq'
    mock_sample_source.projects = [mock_project]

    # call the function when the projects data doesnt exist yet
    check_sample_source_associated_with_project(mock_sample_source, sample_source_info[0])

    # assert that no new project was added
    assert len(mock_sample_source.projects) == 1
    assert mock_sample_source.projects[0].project_name == "COVIDseq"

    # create a sample source info with a new project association
    sample_source_info = {
        "sample_source_identifier": "CMT17B",
        "group_name": "Immunology",
        "projects": "COCOSU",
        "institution":"MLW"
    }

    mock_project.project_name = sample_source_info["projects"]
    mock_sample_source.projects.append(mock_project)
    # mock_sample_source.projects.append(sample_source_info["projects"])

    # call the function
    check_sample_source_associated_with_project(mock_sample_source, sample_source_info)

    # assert that the new project was added
    assert len(mock_sample_source.projects) == 2
    assert mock_sample_source.projects[1].project_name == "COCOSU"
 


def test_check_mykrobe_res(mykrobe_res_info):
    
    for key in mykrobe_res_info:
        if key != 'all_valid_fields':
            with pytest.raises(SystemExit) as excinfo:
                check_mykrobe_res(mykrobe_res_info[key])
            assert excinfo.value.code == 1

    assert check_mykrobe_res(mykrobe_res_info['all_valid_fields']) is None


def test_check_pangolin_result(pangolin_result_info, capsys):
    check_pangolin_result(pangolin_result_info)
    captured = capsys.readouterr()
    assert captured.out == ''

def test_check_pangolin_result_empty_taxon(pangolin_result_info, capsys):
    pangolin_result_info['taxon'] = ''
    with pytest.raises(SystemExit):
        check_pangolin_result(pangolin_result_info)
    captured = capsys.readouterr()
    assert 'taxon column should not be empty' in captured.out

def test_check_pangolin_result_empty_lineage(pangolin_result_info, capsys):
    pangolin_result_info['lineage'] = ''
    with pytest.raises(SystemExit):
        check_pangolin_result(pangolin_result_info)
    captured = capsys.readouterr()
    assert 'lineage column should not be empty' in captured.out

def test_check_pangolin_result_empty_status(pangolin_result_info, capsys):
    pangolin_result_info['status'] = ''
    with pytest.raises(SystemExit):
        check_pangolin_result(pangolin_result_info)
    captured = capsys.readouterr()
    assert 'status column should not be empty' in captured.out

def test_check_pangolin_result_qc_status(pangolin_result_info, capsys):
    pangolin_result_info['qc_status'] = 'passed'
    pangolin_result_info.pop('status')
    check_pangolin_result(pangolin_result_info)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert pangolin_result_info['status'] == 'passed'


def test_check_artic_covid_result(artic_covid_result_info,capsys):
    check_artic_covid_result(artic_covid_result_info[0])
    captured = capsys.readouterr()
    assert captured.out == ''

    
    with pytest.raises(SystemExit):
        check_artic_covid_result(artic_covid_result_info[1])
    captured = capsys.readouterr()
    assert captured.out == f'sample_name column should not be empty. it is for \n{artic_covid_result_info[1]}\nExiting.\n'


def test_check_raw_sequencing_batch(raw_sequencing_batch_info):

    # Test that the function raises a SystemExit with status code 1
    with pytest.raises(SystemExit) as e:
        check_raw_sequencing_batch(raw_sequencing_batch_info[0])
    assert e.type == SystemExit
    assert e.value.code == 1

    # Test that the function does not raise an exception
    assert check_raw_sequencing_batch(raw_sequencing_batch_info[1]) is None

def test_check_readset_batches(readset_batch_info):
    # Test that the function raises a SystemExit with status code 1
    with pytest.raises(SystemExit) as e:
        check_readset_batches(readset_batch_info[0])
    assert e.type == SystemExit
    assert e.value.code == 1

    # Test that the function does not raise an exception
    assert check_readset_batches(readset_batch_info[1]) is None

def test_empty_culture_info(empty_culture_info):
    with pytest.raises(SystemExit):
        check_cultures(empty_culture_info)

def test_invalid_culture_info(invalid_culture_info):
    with pytest.raises(AssertionError):
        check_cultures(invalid_culture_info)

def test_valid_culture_info(valid_culture_info):
    check_cultures(valid_culture_info)
 

def test_check_extraction_fields(extraction_info):
    check_extraction_fields(extraction_info[0])  # No exception expected

    with pytest.raises(SystemExit) as exc_info:
        check_extraction_fields(extraction_info[1])
    assert exc_info.value.code == 1
    assert f'sample_identifier column should not be empty' in str(exc_info.value)

    
    with pytest.raises(SystemExit) as exc_info:
        check_extraction_fields(extraction_info[2])
    assert exc_info.value.code == 1
    assert f'date_extracted column should not be empty' in str(exc_info.value)

    
    with pytest.raises(SystemExit) as exc_info:
        check_extraction_fields(extraction_info[3])
    assert exc_info.value.code == 1
    assert f'extraction_identifier column should not be empty' in str(exc_info.value)

    with pytest.raises(SystemExit) as exc_info:
        check_extraction_fields(extraction_info[4])
    assert exc_info.value.code == 1

def test_check_group():
    valid_group_info = {'group_name': 'GroupA', 'institution': 'University A'}
    check_group(valid_group_info)

    invalid_group_info1 = {'group_name': 'Group A', 'institution': 'University A'}
    with pytest.raises(SystemExit):
        check_group(invalid_group_info1)

    invalid_group_info2 = {'group_name': 'GroupA/', 'institution': 'University A'}
    with pytest.raises(SystemExit):
        check_group(invalid_group_info2)

    invalid_group_info3 = {'group_name': '', 'institution': 'University A'}
    with pytest.raises(SystemExit):
        check_group(invalid_group_info3)

    invalid_group_info4 = {'group_name': 'GroupA', 'institution': ''}
    with pytest.raises(SystemExit):
        check_group(invalid_group_info4)

def test_check_project():
    # Test case where project name is empty
    project_info = {'project_name': '', 'group_name': 'group1', 'institution': 'institution1'}
    with pytest.raises(SystemExit) as exc_info:
        check_project(project_info)
    assert exc_info.value.code == 1
    
    # Test case where group name is empty
    project_info = {'project_name': 'project1', 'group_name': '', 'institution': 'institution1'}
    with pytest.raises(SystemExit) as exc_info:
        check_project(project_info)
    assert exc_info.value.code == 1
    
    # Test case where institution is empty
    project_info = {'project_name': 'project1', 'group_name': 'group1', 'institution': ''}
    with pytest.raises(SystemExit) as exc_info:
        check_project(project_info)
    assert exc_info.value.code == 1

def test_check_sample_sources(sample_source_info):
    check_sample_sources(sample_source_info)
    # If no exception is raised, the function passed the test

    # Test case where sample_source_identifier is empty
    sample_source_info['sample_source_identifier'] = ''
    with pytest.raises(SystemExit):
        check_sample_sources(sample_source_info)

    # Test case where sample_source_type is empty
    sample_source_info['sample_source_identifier'] = 'sample1'
    sample_source_info['sample_source_type'] = ''
    with pytest.raises(SystemExit):
        check_sample_sources(sample_source_info)

    # Test case where projects is empty
    sample_source_info['sample_source_type'] = 'type1'
    sample_source_info['projects'] = ''
    with pytest.raises(SystemExit):
        check_sample_sources(sample_source_info)

    # Test case where group_name is empty
    sample_source_info['projects'] = 'project1'
    sample_source_info['group_name'] = ''
    with pytest.raises(SystemExit):
        check_sample_sources(sample_source_info)

    # Test case where institution is empty
    sample_source_info['group_name'] = 'group1'
    sample_source_info['institution'] = ''
    with pytest.raises(SystemExit):
        check_sample_sources(sample_source_info)


def test_check_sample_sources():
    # test empty sample_source_identifier
    with pytest.raises(SystemExit):
        check_sample_sources({'sample_source_identifier': '', 'sample_source_type': 'type', 'projects': 'proj1', 'group_name': 'group', 'institution': 'inst'})
    # test empty sample_source_type
    with pytest.raises(SystemExit):
        check_sample_sources({'sample_source_identifier': 'id', 'sample_source_type': '', 'projects': 'proj1', 'group_name': 'group', 'institution': 'inst'})
    # test empty projects
    with pytest.raises(SystemExit):
        check_sample_sources({'sample_source_identifier': 'id', 'sample_source_type': 'type', 'projects': '', 'group_name': 'group', 'institution': 'inst'})
    # test empty group_name
    with pytest.raises(SystemExit):
        check_sample_sources({'sample_source_identifier': 'id', 'sample_source_type': 'type', 'projects': 'proj1', 'group_name': '', 'institution': 'inst'})
    # test empty institution
    with pytest.raises(SystemExit):
        check_sample_sources({'sample_source_identifier': 'id', 'sample_source_type': 'type', 'projects': 'proj1', 'group_name': 'group', 'institution': ''})


def test_check_samples_empty_sample_source_identifier(capsys):
    sample_info = {
        'sample_source_identifier': '',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'institution': 'institution1'
    }
    check_samples(sample_info)
    captured = capsys.readouterr()
    assert 'sample_source_identifier column should not be empty' in captured.out
    assert 'Exiting.' in captured.out
    assert sys.exit.called

def test_check_samples_empty_sample_identifier(capsys):
    sample_info = {
        'sample_source_identifier': 'source1',
        'sample_identifier': '',
        'group_name': 'group1',
        'institution': 'institution1'
    }
    check_samples(sample_info)
    captured = capsys.readouterr()
    assert 'sample_identifier column should not be empty' in captured.out
    assert 'Exiting.' in captured.out
    assert sys.exit.called

def test_check_samples_empty_group_name(capsys):
    sample_info = {
        'sample_source_identifier': 'source1',
        'sample_identifier': 'sample1',
        'group_name': '',
        'institution': 'institution1'
    }
    check_samples(sample_info)
    captured = capsys.readouterr()
    assert 'group_name column should not be empty' in captured.out
    assert 'Exiting.' in captured.out
    assert sys.exit.called

def test_check_samples_empty_institution(capsys):
    sample_info = {
        'sample_source_identifier': 'source1',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'institution': ''
    }
    check_samples(sample_info)
    captured = capsys.readouterr()
    assert 'institution column should not be empty' in captured.out
    assert 'Exiting.' in captured.out
    assert sys.exit.called

def test_check_samples_valid_input(capsys):
    sample_info = {
        'sample_source_identifier': 'source1',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'institution': 'institution1'
    }
    check_samples(sample_info)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert not sys.exit.called


def test_check_covid_confirmatory_pcr_empty_sample_identifier(capsys):
    covid_confirmatory_pcr_info = {
        'sample_identifier': '',
        'date_extracted': '2022-01-01',
        'extraction_identifier': 'extraction1',
        'date_covid_confirmatory_pcred': '2022-01-02',
        'covid_confirmatory_pcr_identifier': 'pcr1',
        'group_name': 'group1',
        'covid_confirmatory_pcr_protocol': 'protocol1'
    }
    check_covid_confirmatory_pcr(covid_confirmatory_pcr_info)
    captured = capsys.readouterr()
    assert 'sample_identifier column should not be empty' in captured.out
    assert 'Exiting.' in captured.out
    assert sys.exit.called

def test_check_covid_confirmatory_pcr_empty_date_extracted(capsys):
    covid_confirmatory_pcr_info = {
        'sample_identifier': 'sample1',
        'date_extracted': '',
        'extraction_identifier': 'extraction1',
        'date_covid_confirmatory_pcred': '2022-01-02',
        'covid_confirmatory_pcr_identifier': 'pcr1',
        'group_name': 'group1',
        'covid_confirmatory_pcr_protocol': 'protocol1'
    }
    check_covid_confirmatory_pcr(covid_confirmatory_pcr_info)
    captured = capsys.readouterr()
    assert 'date_extracted column should not be empty' in captured.out
    assert 'Exiting.' in captured.out
    assert sys.exit.called

def test_check_covid_confirmatory_pcr_empty_extraction_identifier(capsys):
    covid_confirmatory_pcr_info = {
        'sample_identifier': 'sample1',
        'date_extracted': '2022-01-01',
        'extraction_identifier': '',
        'date_covid_confirmatory_pcred': '2022-01-02',
        'covid_confirmatory_pcr_identifier': 'pcr1',
        'group_name': 'group1',
        'covid_confirmatory_pcr_protocol': 'protocol1'
    }
    check_covid_confirmatory_pcr(covid_confirmatory_pcr_info)
    captured = capsys.readouterr()
    assert 'extraction_identifier column should not be empty' in captured.out
    assert 'Exiting.' in captured.out
    assert sys.exit.called

def test_check_covid_confirmatory_pcr_empty_date_covid_confirmatory_pcred(capsys):
    covid_confirmatory_pcr_info = {
        'sample_identifier': 'sample1',
        'date_extracted': '2022-01-01',
        'extraction_identifier': 'extraction1',
        'date_covid_confirmatory_pcred': '',
        'covid_confirmatory_pcr_identifier': 'pcr1',
        'group_name': 'group1',
        'covid_confirmatory_pcr_protocol': 'protocol1'
    }
    check_covid_confirmatory_pcr(covid_confirmatory_pcr_info)
    captured = capsys.readouterr()
    assert 'date_covid_confirmatory_pcred column should not be empty' in captured.out
    assert 'Exiting.' in captured.out
    assert sys.exit.called

def test_check_covid_confirmatory_pcr_empty_covid_confirmatory_pcr_identifier(capsys):
    covid_confirmatory_pcr_info = {
        'sample_identifier': 'sample1',
        'date_extracted': '2022-01-01',
        'extraction_identifier': 'extraction1',
        }

def test_check_tiling_pcr():
    # Valid input
    tiling_pcr_info = {
        'sample_identifier': '12345',
        'date_extracted': '2022-03-01',
        'extraction_identifier': 'EX-12345',
        'date_tiling_pcred': '2022-03-15',
        'tiling_pcr_identifier': 'TPCR-12345',
        'group_name': 'Group A',
        'tiling_pcr_protocol': 'Protocol A'
    }
    assert check_tiling_pcr(tiling_pcr_info) == True

    # Invalid input: missing sample_identifier
    tiling_pcr_info = {
        'date_extracted': '2022-03-01',
        'extraction_identifier': 'EX-12345',
        'date_tiling_pcred': '2022-03-15',
        'tiling_pcr_identifier': 'TPCR-12345',
        'group_name': 'Group A',
        'tiling_pcr_protocol': 'Protocol A'
    }
    assert check_tiling_pcr(tiling_pcr_info) == False

    # Invalid input: empty tiling_pcr_protocol
    tiling_pcr_info = {
        'sample_identifier': '12345',
        'date_extracted': '2022-03-01',
        'extraction_identifier': 'EX-12345',
        'date_tiling_pcred': '2022-03-15',
        'tiling_pcr_identifier': 'TPCR-12345',
        'group_name': 'Group A',
        'tiling_pcr_protocol': ''
    }
    assert check_tiling_pcr(tiling_pcr_info) == False



def test_check_pcr_result():
    # Valid input
    pcr_result_info = {
        'sample_identifier': '12345',
        'date_pcred': '2022-03-15',
        'pcr_identifier': 'PCR-12345',
        'group_name': 'Group A',
        'assay_name': 'Assay A',
        'pcr_result': 'Negative'
    }
    assert check_pcr_result(pcr_result_info) == True

    # Invalid input: missing sample_identifier
    pcr_result_info = {
        'date_pcred': '2022-03-15',
        'pcr_identifier': 'PCR-12345',
        'group_name': 'Group A',
        'assay_name': 'Assay A',
        'pcr_result': 'Negative'
    }
    assert check_pcr_result(pcr_result_info) == False

    # Invalid input: empty pcr_result
    pcr_result_info = {
        'sample_identifier': '12345',
        'date_pcred': '2022-03-15',
        'pcr_identifier': 'PCR-12345',
        'group_name': 'Group A',
        'assay_name': 'Assay A',
        'pcr_result': ''
    }
    assert check_pcr_result(pcr_result_info) == False

    # Invalid input: invalid pcr_result
    pcr_result_info = {
        'sample_identifier': '12345',
        'date_pcred': '2022-03-15',
        'pcr_identifier': 'PCR-12345',
        'group_name': 'Group A',
        'assay_name': 'Assay A',
        'pcr_result': 'Invalid'
    }
    # This test case should exit with error code 1, so we need to use pytest's `raises` function to capture the exception.
    with pytest.raises(SystemExit):
        check_pcr_result(pcr_result_info)



def test_check_readset_fields(raw_sequencing_batch, covid):
    readset_info = {
        'data_storage_device': 'external',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'readset_batch_name': 'batch1',
        'barcode': 'ATCG',
        'path_fastq': '/path/to/fastq',
        'path_fast5': '/path/to/fast5',
        'path_r1': '/path/to/r1',
        'path_r2': '/path/to/r2',
        'date_tiling_pcred': '2022-01-01',
        'tiling_pcr_identifier': 'pcr123',
        'date_extracted': datetime.now(),
        'extraction_identifier': 'ext123',
    }
    
    # Check that all fields are present
    assert check_readset_fields(readset_info, True, raw_sequencing_batch, covid) == None
    
    # Check that missing fields raise an error
    readset_info['path_r1'] = ''
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, False, raw_sequencing_batch, covid)
    
    readset_info['path_r1'] = '/path/to/r1'
    readset_info['path_r2'] = ''
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, False, raw_sequencing_batch, covid)
    
    readset_info['path_r2'] = '/path/to/r2'
    readset_info['date_extracted'] = 'NaT'
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, False, raw_sequencing_batch, covid)
    
    readset_info['date_extracted'] = datetime.now()
    readset_info['extraction_identifier'] = ''
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, False, raw_sequencing_batch, covid)
    
    readset_info['extraction_identifier'] = 'ext123'
    readset_info['date_tiling_pcred'] = ''
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, False, raw_sequencing_batch, True)
    
    readset_info['date_tiling_pcred'] = '2022-01-01'
    readset_info['tiling_pcr_identifier'] = ''
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, False, raw_sequencing_batch, True)
    
    readset_info['tiling_pcr_identifier'] = 'pcr123'
    readset_info['barcode'] = ''
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, True, raw_sequencing_batch, covid)
    
    readset_info['barcode'] = 'ATCG'
    readset_info['path_fastq'] = ''
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, False, raw_sequencing_batch, False)
    
    readset_info['path_fastq'] = '/path/to/fastq'
    readset_info['path_fast5'] = ''
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, False,raw_sequencing_batch, False)
