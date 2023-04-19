import pytest
from scripts.seqbox_utils import get_sample_source, get_extraction,get_covid_confirmatory_pcr,get_group,get_readset
from app import db
from app.models import Project,Extraction, Sample, SampleSource, Culture, Groups,CovidConfirmatoryPcr,ReadSetIllumina, ReadSetNanopore
# Import the necessary classes/models
from app.models import SampleSource, Groups, Project

def test_matching_sample_source(mocker):
    # Create mock objects for the required classes
    SampleSource = mocker.Mock()
    Projects = mocker.Mock()
    Groups = mocker.Mock()

    # Mock the return value of SampleSource.query
    sample_source_query_mock = mocker.Mock()
    SampleSource.query = mocker.Mock(return_value=sample_source_query_mock)

    # Mock the return value of filter_by method
    filter_by_mock = mocker.Mock()
    sample_source_query_mock.filter_by.return_value = filter_by_mock

    # Mock the return value of join method for SampleSource.projects
    join_projects_mock = mocker.Mock()
    filter_by_mock.join.return_value = join_projects_mock

    # Mock the return value of join method for Groups
    join_groups_mock = mocker.Mock()
    join_projects_mock.join.return_value = join_groups_mock

    # Mock the return value of filter_by method for group_name
    filter_by_group_name_mock = mocker.Mock()
    join_groups_mock.filter_by.return_value = filter_by_group_name_mock

    # Mock the return value of all method
    all_mock = mocker.Mock()
    filter_by_group_name_mock.all.return_value = all_mock

    # Create mock objects for sample_info dictionary
    sample_info = {
        'sample_source_identifier': 'sample1',
        'group_name': 'group1'
    }

    # Call the function under test
    result = get_sample_source(sample_info)

    # Assert the expected output
    assert result == all_mock 

