import pytest
from datetime import datetime
from scripts.seqbox_utils import  get_extraction,get_covid_confirmatory_pcr,get_group,get_readset
from app import db
from app.models import Extraction, Sample, SampleSource, Culture, Groups,CovidConfirmatoryPcr,ReadSetIllumina, ReadSetNanopore


def test_get_sample_source(sample_source_factory, project_factory, group_factory):
    # create sample source, project, and group objects
    sample_source = sample_source_factory.create_sample_source()
    project = project_factory.create_project()
    group = group_factory.create_group()

    # add the sample source to the project and group
    project.sample_sources.append(sample_source)
    group.projects.append(project)

    # create sample info dictionary with the same identifier and group name as the sample source
    sample_info = {
        'sample_source_identifier': sample_source.sample_source_identifier,
        'group_name': group.group_name
    }

    # call the function and assert that it returns the sample source object
    assert get_sample_source(sample_info) == sample_source

    # create a different sample info dictionary with a different identifier and group name
    different_sample_info = {
        'sample_source_identifier': 'different_identifier',
        'group_name': 'different_group'
    }

    # call the function and assert that it returns False
    assert get_sample_source(different_sample_info) == False

def test_get_sample(sample_factory, sample_source_factory, project_factory, group_factory):
    # create sample, sample source, project, and group objects
    sample_source = sample_source_factory.create_sample_source()
    project = project_factory.create_project()
    group = group_factory.create_group()
    sample = sample_factory.create_sample(sample_source=sample_source)

    # add the sample to the project and group
    project.samples.append(sample)
    group.projects.append(project)

    # create readset info dictionary with the same identifier and group name as the sample
    readset_info = {
        'sample_identifier': sample.sample_identifier,
        'group_name': group.group_name
    }

    # call the function and assert that it returns the sample object
    assert get_sample(readset_info) == sample

    # create a different readset info dictionary with a different identifier and group name
    different_readset_info = {
        'sample_identifier': 'different_identifier',
        'group_name': 'different_group'
    }

    # call the function and assert that it returns False
    assert get_sample(different_readset_info) == False


def test_get_mykrobe_result(mykrobe_factory, readset_factory):
    # create mykrobe and readset objects
    mykrobe_result = mykrobe_factory.create_mykrobe()
    readset = readset_factory.create_readset()

    # associate the mykrobe result with the readset
    mykrobe_result.readset = readset

    # create mykrobe info dictionary with the same version, drug, and readset identifier as the mykrobe result
    mykrobe_info = {
        'mykrobe_version': mykrobe_result.mykrobe_version,
        'drug': mykrobe_result.drug,
        'readset_identifier': readset.readset_identifier
    }

    # call the function and assert that it returns the mykrobe result object
    assert get_mykrobe_result(mykrobe_info) == mykrobe_result

    # create a different mykrobe info dictionary with a different version, drug, and readset identifier
    different_mykrobe_info = {
        'mykrobe_version': 'different_version',
        'drug': 'different_drug',
        'readset_identifier': 'different_identifier'
    }

    # call the function and assert that it returns False
    assert get_mykrobe_result(different_mykrobe_info) == False




def test_get_extraction_with_whole_sample(sample_data, extraction_data):
    # Test extraction from whole sample
    readset_info = {"extraction_from": "whole_sample", **extraction_data}
    extraction = get_extraction(readset_info)
    assert extraction == Extraction.query.one()
    
def test_get_extraction_with_cultured_isolate(sample_data, extraction_data):
    # Test extraction from cultured isolate
    readset_info = {"extraction_from": "cultured_isolate", **extraction_data}
    extraction = get_extraction(readset_info)
    assert extraction == Extraction.query.one()
    
def test_get_extraction_with_no_matching_extraction(sample_data):
    # Test no matching extraction
    readset_info = {"extraction_from": "whole_sample",
                    "extraction_identifier": "E002", "date_extracted": "2022-02-02",
                    **sample_data}
    extraction = get_extraction(readset_info)
    assert not extraction
    
def test_get_extraction_with_multiple_matching_extractions(sample_data, extraction_data):
    # Test multiple matching extractions
    Extraction(extraction_identifier="E001", date_extracted="2022-01-01").sample = Sample.query.filter_by(
        sample_identifier=sample_data["sample_identifier"]).one()
    db.session.commit()
    readset_info = {"extraction_from": "whole_sample", **extraction_data}
    with pytest.raises(SystemExit):
        get_extraction(readset_info)



def test_get_culture_returns_matching_culture_object():
    # arrange
    culture_info = {
        'culture_identifier': 'ID123',
        'date_cultured': '01/01/2022',
        'sample_identifier': 'SAMPLE123',
        'group_name': 'GROUP123'
    }

    expected_culture = Culture(
        culture_identifier='ID123',
        date_cultured=datetime.strptime('01/01/2022', '%d/%m/%Y'),
        sample=Sample(sample_identifier='SAMPLE123'),
        group=Groups(group_name='GROUP123')
    )

    # act
    actual_culture = get_culture(culture_info)

    # assert
    assert actual_culture == expected_culture


def test_get_culture_returns_false_if_no_matching_culture_found():
    # arrange
    culture_info = {
        'culture_identifier': 'ID456',
        'date_cultured': '01/01/2022',
        'sample_identifier': 'SAMPLE456',
        'group_name': 'GROUP456'
    }

    # act
    actual_result = get_culture(culture_info)

    # assert
    assert actual_result == False


def test_get_culture_raises_exception_if_multiple_matching_cultures_found():
    # arrange
    culture_info = {
        'culture_identifier': 'ID789',
        'date_cultured': '01/01/2022',
        'sample_identifier': 'SAMPLE789',
        'group_name': 'GROUP789'
    }

    Culture(culture_identifier='ID789',
            date_cultured=datetime.strptime('01/01/2022', '%d/%m/%Y'),
            sample=Sample(sample_identifier='SAMPLE789'),
            group=Groups(group_name='GROUP789')
    ).save()

    Culture(culture_identifier='ID789',
            date_cultured=datetime.strptime('01/01/2022', '%d/%m/%Y'),
            sample=Sample(sample_identifier='SAMPLE789'),
            group=Groups(group_name='GROUP789')
    ).save()

    # act & assert
    with pytest.raises(SystemExit):
        get_culture(culture_info)



def test_get_projects_returns_list_of_projects():
    # arrange
    info = {
        'projects': 'Project A; Project B; Project C',
        'group_name': 'Group 1'
    }

    # act
    actual_result = get_projects(info)

    # assert
    assert isinstance(actual_result, list)
    assert len(actual_result) == 3


def test_get_projects_raises_error_if_project_not_found():
    # arrange
    info = {
        'projects': 'Project A; Non-existent Project; Project C',
        'group_name': 'Group 2'
    }

    # act & assert
    with pytest.raises(SystemExit):
        get_projects(info)


def test_get_projects_raises_error_if_projects_key_not_found():
    # arrange
    info = {
        'group_name': 'Group 3'
    }

    # act & assert
    with pytest.raises(AssertionError):
        get_projects(info)


def test_get_projects_raises_error_if_group_name_key_not_found():
    # arrange
    info = {
        'projects': 'Project A; Project B; Project C'
    }

    # act & assert
    with pytest.raises(AssertionError):
        get_projects(info)


def test_get_artic_covid_result_returns_matching_result():
    # arrange
    artic_covid_result_info = {
        'artic_profile': 'ARTIC_V3',
        'artic_workflow': 'ARTIC_nCoV_v3',
        'readset_batch_name': 'batch_001',
        'barcode': 'NB-1111'
    }

    # act
    actual_result = get_artic_covid_result(artic_covid_result_info)

    # assert
    assert actual_result is not False
    assert isinstance(actual_result, ArticCovidResult)


def test_get_artic_covid_result_returns_false_if_no_matching_result():
    # arrange
    artic_covid_result_info = {
        'artic_profile': 'ARTIC_V4',
        'artic_workflow': 'ARTIC_nCoV_v4',
        'readset_batch_name': 'batch_002',
        'barcode': 'NB-2222'
    }

    # act
    actual_result = get_artic_covid_result(artic_covid_result_info)

    # assert
    assert actual_result is False


def test_get_artic_covid_result_raises_error_if_multiple_matching_results():
    # arrange
    artic_covid_result_info = {
        'artic_profile': 'ARTIC_V3',
        'artic_workflow': 'ARTIC_nCoV_v3',
        'readset_batch_name': 'batch_001',
        'barcode': 'NB-2222'
    }

    # act & assert
    with pytest.raises(SystemExit):
        get_artic_covid_result(artic_covid_result_info)


def test_get_pangolin_result():
    # create a pangolin result in the database
    pangolin_result_info = {
        'version': 'v1.0',
        'artic_profile': 'ncov2019',
        'artic_workflow': '1.2.3',
        'readset_batch_name': 'batch1',
        'barcode': 'bar1'
    }
    pangolin_result = PangolinResult(version=pangolin_result_info['version'])
    artic_covid_result = ArticCovidResult(profile=pangolin_result_info['artic_profile'],
                                          workflow=pangolin_result_info['artic_workflow'])
    readset = ReadSet()
    readset_batch = ReadSetBatch(name=pangolin_result_info['readset_batch_name'])
    readset_nanopore = ReadSetNanopore(barcode=pangolin_result_info['barcode'])
    pangolin_result.artic_covid_result = artic_covid_result
    artic_covid_result.readset = readset
    readset.readset_batch = readset_batch
    readset.readset_nanopore = readset_nanopore
    db.session.add(pangolin_result)
    db.session.commit()

    # test with valid pangolin result info
    result = get_pangolin_result(pangolin_result_info)
    assert isinstance(result, PangolinResult)
    assert result.version == pangolin_result_info['version']

    # test with pangolin result info that doesn't exist in the database
    pangolin_result_info['version'] = 'v2.0'
    result = get_pangolin_result(pangolin_result_info)
    assert result is False

    # test with pangolin result info that matches multiple PangolinResult objects in the database
    pangolin_result_info = {
        'version': 'v1.0',
        'artic_profile': 'ncov2019',
        'artic_workflow': '1.2.3',
        'readset_batch_name': 'batch1',
        'barcode': 'bar1'
    }
    pangolin_result2 = PangolinResult(version=pangolin_result_info['version'])
    pangolin_result2.artic_covid_result = artic_covid_result
    db.session.add(pangolin_result2)
    db.session.commit()
    with pytest.raises(SystemExit):
        get_pangolin_result(pangolin_result_info)


def test_get_tiling_pcr():
    # Create a sample and extraction to use for the test
    sample = Sample(sample_identifier='sample1')
    extraction = Extraction(date_extracted=datetime.datetime.now())
    extraction.sample = sample
    db.session.add_all([sample, extraction])
    db.session.commit()

    # Create a TilingPcr to use for the test
    tiling_pcr = TilingPcr(
        pcr_identifier='pcr1',
        date_pcred=datetime.datetime.now(),
    )
    tiling_pcr.extraction = extraction
    db.session.add(tiling_pcr)
    db.session.commit()

    # Test with a valid tiling_pcr_info
    tiling_pcr_info = {
        'tiling_pcr_identifier': 'pcr1',
        'date_tiling_pcred': datetime.datetime.strftime(tiling_pcr.date_pcred, '%d/%m/%Y'),
        'sample_identifier': 'sample1',
    }
    result = get_tiling_pcr(tiling_pcr_info)
    assert result == tiling_pcr

    # Test with an invalid tiling_pcr_identifier
    tiling_pcr_info = {
        'tiling_pcr_identifier': 'pcr2',
        'date_tiling_pcred': datetime.datetime.strftime(tiling_pcr.date_pcred, '%d/%m/%Y'),
        'sample_identifier': 'sample1',
    }
    result = get_tiling_pcr(tiling_pcr_info)
    assert result == False

    # Test with an invalid date_tiling_pcred
    tiling_pcr_info = {
        'tiling_pcr_identifier': 'pcr1',
        'date_tiling_pcred': datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=1), '%d/%m/%Y'),
        'sample_identifier': 'sample1',
    }
    result = get_tiling_pcr(tiling_pcr_info)
    assert result == False

    # Test with an invalid sample_identifier
    tiling_pcr_info = {
        'tiling_pcr_identifier': 'pcr1',
        'date_tiling_pcred': datetime.datetime.strftime(tiling_pcr.date_pcred, '%d/%m/%Y'),
        'sample_identifier': 'sample2',
    }
    result = get_tiling_pcr(tiling_pcr_info)
    assert result == False


@pytest.fixture
def sample_covid_confirmatory_pcr():
    # A sample CovidConfirmatoryPcr object to use in the tests
    return CovidConfirmatoryPcr(
        pcr_identifier='pcr123',
        date_pcred=datetime.strptime('01/01/2022', '%d/%m/%Y'),
        extraction_identifier='ext123',
        date_extracted=datetime.strptime('02/01/2022', '%d/%m/%Y'),
        sample_identifier='sample123'
    )

def test_get_covid_confirmatory_pcr_returns_false_if_no_match():
    covid_confirmatory_pcr_info = {
        'covid_confirmatory_pcr_identifier': 'pcr123',
        'date_covid_confirmatory_pcred': '01/01/2022',
        'extraction_identifier': 'ext456',
        'date_extracted': '02/01/2022',
        'sample_identifier': 'sample123'
    }
    assert get_covid_confirmatory_pcr(covid_confirmatory_pcr_info) == False

def test_get_covid_confirmatory_pcr_returns_single_match(sample_covid_confirmatory_pcr):
    covid_confirmatory_pcr_info = {
        'covid_confirmatory_pcr_identifier': 'pcr123',
        'date_covid_confirmatory_pcred': '01/01/2022',
        'extraction_identifier': 'ext123',
        'date_extracted': '02/01/2022',
        'sample_identifier': 'sample123'
    }
    result = get_covid_confirmatory_pcr(covid_confirmatory_pcr_info)
    assert result == sample_covid_confirmatory_pcr

def test_get_covid_confirmatory_pcr_raises_error_if_multiple_matches():
    CovidConfirmatoryPcr(
        pcr_identifier='pcr123',
        date_pcred=datetime.strptime('01/01/2022', '%d/%m/%Y'),
        extraction_identifier='ext123',
        date_extracted=datetime.strptime('02/01/2022', '%d/%m/%Y'),
        sample_identifier='sample123'
    )
    CovidConfirmatoryPcr(
        pcr_identifier='pcr123',
        date_pcred=datetime.strptime('01/01/2022', '%d/%m/%Y'),
        extraction_identifier='ext123',
        date_extracted=datetime.strptime('02/01/2022', '%d/%m/%Y'),
        sample_identifier='sample123'
    )
    covid_confirmatory_pcr_info = {
        'covid_confirmatory_pcr_identifier': 'pcr123',
        'date_covid_confirmatory_pcred': '01/01/2022',
        'extraction_identifier': 'ext123',
        'date_extracted': '02/01/2022',
        'sample_identifier': 'sample123'
    }
    with pytest.raises(SystemExit):
        get_covid_confirmatory_pcr(covid_confirmatory_pcr_info)


def test_get_pcr_assay(database):
    # Create a PcrAssay object to be added to the database
    pcr_assay = PcrAssay(assay_name='Assay 1')
    database.session.add(pcr_assay)
    database.session.commit()

    # Test that get_pcr_assay returns the expected object when given a matching assay name
    pcr_assay_info = {'assay_name': 'Assay 1'}
    matching_pcr_assay = get_pcr_assay(pcr_assay_info)
    assert matching_pcr_assay == pcr_assay

    # Test that get_pcr_assay returns False when no matching assay is found in the database
    pcr_assay_info = {'assay_name': 'Nonexistent Assay'}
    matching_pcr_assay = get_pcr_assay(pcr_assay_info)
    assert matching_pcr_assay is False

    # Add another PcrAssay object with the same assay name to the database
    pcr_assay_2 = PcrAssay(assay_name='Assay 1')
    database.session.add(pcr_assay_2)
    database.session.commit()

    # Test that get_pcr_assay raises a SystemExit when multiple matching assays are found in the database
    pcr_assay_info = {'assay_name': 'Assay 1'}
    with pytest.raises(SystemExit):
        get_pcr_assay(pcr_assay_info)

def test_get_pcr_result():
    pcr_result_info = {
        'date_pcred': '01/01/2022',
        'pcr_identifier': 'pcr123',
        'assay_name': 'COVID-19 PCR Test',
        'sample_identifier': 'sample123'
    }

    # add pcr assay to database
    assay = PcrAssay(assay_name='COVID-19 PCR Test')
    db.session.add(assay)
    db.session.commit()

    # add sample to database
    sample = Sample(sample_identifier='sample123')
    db.session.add(sample)
    db.session.commit()

    # add matching pcr result to database
    pcr_result = PcrResult(date_pcred=datetime.datetime.strptime('01/01/2022', '%d/%m/%Y'),
                           pcr_identifier='pcr123',
                           pcr_assay_id=assay.id,
                           sample_id=sample.id)
    db.session.add(pcr_result)
    db.session.commit()

    # test with matching pcr result
    assert get_pcr_result(pcr_result_info) == pcr_result

    # test with non-existent assay
    pcr_result_info['assay_name'] = 'Non-existent PCR Test'
    with pytest.raises(SystemExit):
        get_pcr_result(pcr_result_info)

    # test with non-existent sample
    pcr_result_info['sample_identifier'] = 'non-existent sample'
    assert get_pcr_result(pcr_result_info) == False

    # clean up database
    db.session.delete(pcr_result)
    db.session.delete(sample)
    db.session.delete(assay)
    db.session.commit()

def test_get_readset_batch(db_session):
    # create a readset batch
    readset_batch_name = "test_readset_batch"
    readset_batch = ReadSetBatch(name=readset_batch_name)
    db_session.add(readset_batch)
    db_session.commit()

    # call the get_readset_batch function with the created readset batch's name
    readset_batch_info = {"readset_batch_name": readset_batch_name}
    result = get_readset_batch(readset_batch_info)

    # assert that the function returns the correct readset batch object
    assert result == readset_batch

    # clean up
    db_session.delete(readset_batch)
    db_session.commit()



def test_get_group():
    # Test case 1: Group exists
    group_info = {'group_name': 'Group A', 'institution': 'University X'}
    group = get_group(group_info)
    assert group != False
    assert group.group_name == 'Group A'
    assert group.institution == 'University X'
    
    # Test case 2: Group doesn't exist
    group_info = {'group_name': 'Group B', 'institution': 'University Y'}
    group = get_group(group_info)
    assert group == False
    
    # Add more test cases as needed

def test_get_readset_from_readset_identifier():
    # Test case where no matching readset is found
    readset_info = {'readset_identifier': 'nonexistent_readset'}
    assert get_readset_from_readset_identifier(readset_info) == False
    
    # Test case where one matching readset is found
    readset = ReadSet(readset_identifier='readset_1')
    db.session.add(readset)
    db.session.commit()
    readset_info = {'readset_identifier': 'readset_1'}
    assert get_readset_from_readset_identifier(readset_info) == readset
    
    # Test case where multiple matching readsets are found
    readset2 = ReadSet(readset_identifier='readset_1')
    db.session.add(readset2)
    db.session.commit()
    readset_info = {'readset_identifier': 'readset_1'}
    with pytest.raises(SystemExit):
        get_readset_from_readset_identifier(readset_info)


def test_get_readset_covid_true():
    readset_info = {
        'readset_batch_name': 'batch1',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'date_tiling_pcred': '05/04/2022',
        'tiling_pcr_identifier': 'pcr1'
    }
    covid = True
    assert get_readset(readset_info, covid) == []

def test_get_readset_covid_false():
    readset_info = {
        'readset_batch_name': 'batch1',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'date_extracted': '05/04/2022',
        'extraction_identifier': 'extraction1'
    }
    covid = False
    # Assuming no matching readsets exist in the database
    assert get_readset(readset_info, covid) == False

def test_get_readset_illumina():
    readset_info = {
        'readset_batch_name': 'batch1',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'date_extracted': '05/04/2022',
        'extraction_identifier': 'extraction1'
    }
    covid = False
    readset_batch = {
        'raw_sequencing_batch': {
            'name': 'raw_batch1',
            'sequencing_type': 'illumina'
        }
    }
    # Assuming a matching readset exists in the database
    matching_readset = ReadSetIllumina()
    assert get_readset(readset_info, covid) == [matching_readset]

def test_get_readset_nanopore():
    readset_info = {
        'readset_batch_name': 'batch1',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'date_extracted': '05/04/2022',
        'extraction_identifier': 'extraction1'
    }
    covid = False
    readset_batch = {
        'raw_sequencing_batch': {
            'name': 'raw_batch1',
            'sequencing_type': 'nanopore'
        }
    }
    # Assuming a matching readset exists in the database
    matching_readset = ReadSetNanopore()
    assert get_readset(readset_info, covid) == [matching_readset]

def test_get_raw_sequencing_batch():
    # Test case 1: Batch name matches exactly one RawSequencingBatch object
    batch_name = "Batch1"
    expected_batch = RawSequencingBatch(name=batch_name)
    db.session.add(expected_batch)
    db.session.commit()

    result = get_raw_sequencing_batch(batch_name)
    assert result == expected_batch

    # Test case 2: Batch name does not match any RawSequencingBatch object
    batch_name = "NonexistentBatch"
    result = get_raw_sequencing_batch(batch_name)
    assert result == False

    # Test case 3: Batch name matches multiple RawSequencingBatch objects
    batch_name = "DuplicateBatch"
    batch1 = RawSequencingBatch(name=batch_name)
    batch2 = RawSequencingBatch(name=batch_name)
    db.session.add_all([batch1, batch2])
    db.session.commit()

    with pytest.raises(SystemExit):
        get_raw_sequencing_batch(batch_name)


def test_get_raw_sequencing(db_session):
    # Create a test RawSequencingBatch
    batch = RawSequencingBatch(name='test_batch')
    db_session.add(batch)
    db_session.commit()

    # Create test objects for query parameters
    readset_info = {
        'tiling_pcr_identifier': 'test_tiling_pcr_identifier',
        'date_tiling_pcred': '01/01/2022',
        'extraction_identifier': 'test_extraction_identifier',
        'date_extracted': '01/01/2022',
        'sample_identifier': 'test_sample_identifier',
        'group_name': 'test_group_name'
    }
    covid = True

    # Create test objects for query joins
    tiling_pcr = TilingPcr(pcr_identifier='test_tiling_pcr_identifier', date_pcred=datetime.datetime(2022, 1, 1))
    db_session.add(tiling_pcr)
    culture = Culture(submitter_plate_id='test_plate_id')
    db_session.add(culture)
    project = Project(name='test_project')
    db_session.add(project)
    group = Groups(group_name='test_group_name')
    db_session.add(group)
    sample = Sample(sample_identifier='test_sample_identifier', projects=[project])
    db_session.add(sample)
    sample_source = SampleSource(name='test_sample_source')
    db_session.add(sample_source)
    extraction = Extraction(
        extraction_identifier='test_extraction_identifier',
        date_extracted=datetime.datetime(2022, 1, 1),
        sample=sample
    )
    db_session.add(extraction)
    raw_sequencing = RawSequencing(
        raw_sequencing_batch=batch,
        tiling_pcr=tiling_pcr,
        extraction=extraction,
        sample=sample,
        sample_source=sample_source
    )
    db_session.add(raw_sequencing)
    db_session.commit()

    # Test when covid is True
    result = get_raw_sequencing(readset_info, batch, covid)
    assert result == raw_sequencing

    # Test when covid is False
    covid = False
    result = get_raw_sequencing(readset_info, batch, covid)
    assert result == raw_sequencing

def test_get_nanopore_readset_from_batch_and_barcode(db_session):
    # Create a test ReadSetBatch and ReadSetNanopore with barcode 'test_barcode'
    test_batch = ReadSetBatch(name='test_batch')
    db_session.add(test_batch)
    db_session.flush()

    test_readset_nanopore = ReadSetNanopore(barcode='test_barcode', readset=test_batch.readset)
    db_session.add(test_readset_nanopore)
    db_session.flush()

    # Test with a barcode that doesn't exist in the database
    result = get_nanopore_readset_from_batch_and_barcode({'barcode': 'nonexistent_barcode', 'readset_batch_name': 'test_batch'})
    assert result == False

    # Test with a barcode that exists in the database
    result = get_nanopore_readset_from_batch_and_barcode({'barcode': 'test_barcode', 'readset_batch_name': 'test_batch'})
    assert result == test_readset_nanopore

    # Test with a readset batch name that doesn't exist in the database
    result = get_nanopore_readset_from_batch_and_barcode({'barcode': 'test_barcode', 'readset_batch_name': 'nonexistent_batch'})
    assert result == False
