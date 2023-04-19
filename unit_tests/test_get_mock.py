import pytest
from unittest.mock import patch
from scripts.seqbox_utils import get_sample_source

# Import the necessary classes/models
from app.models import SampleSource, Groups, Project

def test_get_sample_source_with_mocker(mocker,capsys):
    # Create sample_info for testing
    sample_info = {'sample_source_identifier': 'sample1', 'group_name': 'group1'}

    # Mock the query method of SampleSource to return the expected results
    matching_sample_source = SampleSource(sample_source_identifier='sample1')
    # group = Groups(group_name='group1')
    
    mocked_query = mocker.patch.object(SampleSource, 'query')
    mocked_filter_by = mocked_query.return_value.filter_by.return_value
    mocked_join = mocked_filter_by.join.return_value
    mocked_all = mocked_join.join.return_value.filter_by.return_value.all.return_value
    mocked_all.append(matching_sample_source)

    # Call the function under test
    result = get_sample_source(sample_info)

    # Assert the expected output
    assert result == matching_sample_source

    # Mock the query method of SampleSource to return an empty list
    mocked_all = []
    mocked_query.reset_mock()

    # Call the function under test with non-existing sample source
    result = get_sample_source(sample_info)

    # Assert the expected output
    assert result == False

    # Mock the query method of SampleSource to return multiple matching sample sources
    matching_sample_sources = [SampleSource(sample_source_identifier='sample1'), 
                                SampleSource(sample_source_identifier='sample1')]
    mocked_all = matching_sample_sources
    mocked_query.reset_mock()

    # Call the function under test with multiple matching sample sources
    result = get_sample_source(sample_info)

    # Assert the expected output
    # Note: The function should print a message, so you can capture the printed output and assert on it
    captured = capsys.readouterr()
    assert "There is more than one matching sample_source" in captured.out
