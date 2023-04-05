import pytest
# from my_module import check_sample_source_associated_with_project
from scripts.seqbox_utils import check_sample_source_associated_with_project, get_sample_source,query_projects


def test_check_sample_source_associated_with_project_existing_relationship(sample_source, sample_source_info, projects, db, query_projects, mocker):
    # Test the function when there is an existing relationship between the sample source and project(s)
    # Set up the mock for query_projects function
    p = (True, projects[0])
    mocker.patch('scripts.seqbox_utils.query_projects', return_value=p)
    # Associate the sample source with the project(s) in the input file
    sample_source_info['projects'] = projects[0].project_name
    # Call the function
    check_sample_source_associated_with_project(sample_source, sample_source_info)
    # Check that the project(s) in the input file are associated with the sample source in the database
    assert set([x.project_name for x in sample_source.projects]) == set([projects[0].project_name])

def test_check_sample_source_associated_with_project_new_relationship(sample_source, sample_source_info, projects, db, query_projects, mocker):
    # Test the function when there is a new relationship between the sample source and project(s)
    # Set up the mock for query_projects function
    p = (False, None)
    mocker.patch('my_module.query_projects', return_value=p)
    # Associate the sample source with the project(s) in the input file
    sample_source_info['projects'] = projects[0].project_name
    # Call the function
    check_sample_source_associated_with_project(sample_source, sample_source_info)
    # Check that the project(s) in the input file are associated with the sample source in the database
    assert set([x.project_name for x in sample_source.projects]) == set([projects[0].project_name])
    # Check that sys.exit(1) was called when the project did not exist in the database
    with pytest.raises(SystemExit):
        check_sample_source_associated_with_project(sample_source, sample_source_info)


def test_check_sample_source_associated_with_project(sample_source, sample_source_info):
    # Test case where all projects in the file are already associated with the sample source in the DB
    project1 = Project(project_name="project1")
    project2 = Project(project_name="project2")
    sample_source.projects = [project1, project2]

    check_sample_source_associated_with_project(sample_source, sample_source_info)

    assert set([x.project_name for x in sample_source.projects]) == {"project1", "project2"}

    # Test case where there are new projects in the file that need to be associated with the sample source in the DB
    project3 = Project(project_name="project3")
    query_projects = Mock(return_value=(True, project3))
    with patch("your_module.query_projects", query_projects):
        check_sample_source_associated_with_project(sample_source, sample_source_info)

    assert set([x.project_name for x in sample_source.projects]) == {"project1", "project2", "project3"}


def test_get_sample_source(sample_source, sample_source_info):
    # Test case where there is a matching sample source in the DB
    query = Mock(return_value=[sample_source])
    with patch("your_module.SampleSource.query", query):
        result = get_sample_source(sample_source_info)

    assert result == sample_source

    # Test case where there is no matching sample source in the DB
    query = Mock(return_value=[])
    with patch("your_module.SampleSource.query", query):
        result = get_sample_source(sample_source_info)

    assert not result

    # Test case where there is more than one matching sample source in the DB
    query = Mock(return_value=[sample_source, sample_source])
    with patch("your_module.SampleSource.query", query):
        with pytest.raises(SystemExit):
            get_sample_source(sample_source_info)

# Test from get_sample