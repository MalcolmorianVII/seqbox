import pytest
from scripts.seqbox_utils import get_sample_source, get_extraction,get_covid_confirmatory_pcr,get_group,get_readset
from app import db
from app.models import Project,Extraction, Sample, SampleSource, Culture, Groups,CovidConfirmatoryPcr,ReadSetIllumina, ReadSetNanopore


# Define the pytest function
def test_get_sample_source(mocker):
    # Create sample info
    sample_info = {'sample_source_identifier': 'sample1', 'group_name': 'group1'}

    # Create mock objects
    sample_source = mocker.MagicMock()
    group = mocker.MagicMock()
    project = mocker.MagicMock()

    # Mock the SampleSource.query object
    mocker.patch('app.models.SampleSource.query', return_value=sample_source)

    # Mock the filter_by method
    sample_source_filter_by_mock = sample_source.filter_by.return_value
    sample_source_filter_by_mock.join.return_value = sample_source_filter_by_mock
    sample_source_filter_by_mock.filter_by.return_value = sample_source_filter_by_mock
    sample_source_filter_by_mock.all.return_value = [sample_source]

    # Call the get_sample_source() function
    result = get_sample_source(sample_info)

    # Assert the expected result
    assert result == False
    # assert result.sample_source_identifier == sample_source.sample_source_identifier

    # Reset the mock objects
    sample_source.reset_mock()

    # Mock the case where no matching sample source is found
    sample_source_filter_by_mock.all.return_value = []
    
    # Call the get_sample_source() function again
    result = get_sample_source(sample_info)

    # Assert the expected result
    assert result == False


def test_check_sample_source_associated_with_project(mocker,sample_source_info):
    # create a mock version of the SampleSource and Project classes
    mock_sample_source_class = mocker.patch('app.models.SampleSource')
    mock_project_class = mocker.patch('app.models.Project')

    # create a mock version of the database session
    mock_session = mocker.Mock()
    mocker.patch('app.db', mock_session)

    # create a mock version of the SampleSource object with a project association
    mock_sample_source = mock_sample_source_class.return_value
    mock_project = mock_project_class.return_value
    mock_project.project_name = 'project1'
    mock_sample_source.projects = [mock_project]

    # Sample info with existing sample source
    sample_info = {'sample_source_identifier': 'sample1', 'group_name': 'group1'}
# Call the get_sample_source() function
    result = get_sample_source(sample_info)

    # Assert the expected result
    # assert result == False
    assert result.sample_source_identifier == sample_source.sample_source_identifier

    # Sample info with non-existing sample source
    sample_info = {'sample_source_identifier': 'sample2', 'group_name': 'group1'}
    assert get_sample_source(sample_info) == False