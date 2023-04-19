import pytest
from scripts.seqbox_utils import get_sample_source, get_extraction,get_covid_confirmatory_pcr,get_group,get_readset
from app import db
from app.models import Project,Extraction, Sample, SampleSource, Culture, Groups,CovidConfirmatoryPcr,ReadSetIllumina, ReadSetNanopore


def test_get_sample_source(mocker,capsys):
    # create a mock version of the SampleSource,Groups and Project classes
    mock_sample_source_class = mocker.patch('app.models.SampleSource')
    mock_project_class = mocker.patch('app.models.Project')
    mock_group_class = mocker.patch('app.models.Groups')

    # create a mock version of the database session
    mock_session = mocker.Mock()
    mocker.patch('app.db', mock_session)

    # create a mock version of the SampleSource object with a project association
    mock_sample_source = mock_sample_source_class.return_value
    mock_project = mock_project_class.return_value
    mock_groups = mock_group_class.return_value

    mock_groups.group_name = 'group1'
    mock_project.project_name = 'project1'

    mock_sample_source.projects = [mock_project]
    mock_sample_source.groups = [mock_groups]

    # Sample info with existing sample source
    sample_info = {'sample_source_identifier': 'sample1', 'group_name': 'group1'}
# Call the get_sample_source() function
    result = get_sample_source(sample_info)

    # Assert the expected result
    # assert result == False
    assert result.sample_source_identifier == sample_info['sample_source_identifier']

    # Sample info with non-existing sample source
    sample_info = {'sample_source_identifier': 'sample2', 'group_name': 'group1'}
    assert get_sample_source(sample_info) == False

    # More than 1 instance of sample source
    sample_info = {'sample_source_identifier': 'sample1', 'group_name': 'group1'}
    mock_project.project_name = 'project1'
    mock_groups = sample_info['group_name']
    mock_sample_source.projects.append(mock_project)
    mock_sample_source.groups.append(mock_groups)

    result = get_sample_source(sample_info)

    # Assert the expected output
#     # Note: The function should print a message, so you can capture the printed output and assert on it
    captured = capsys.readouterr()
    assert "There is more than one matching sample_source" in captured.out