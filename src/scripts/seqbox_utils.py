import csv
import sys
from app import db
from app.models import Sample, Project, SampleSource, ReadSet, IlluminaReadSet, ReadSetBatch


def read_in_as_dict(inhandle):
    # since csv.DictReader returns a generator rather than an iterator, need to do this fancy business to
    # pull in everything from a generator into an honest to goodness iterable.
    info = csv.DictReader(open(inhandle, encoding='utf-8-sig'))
    # info is a list of ordered dicts, so convert each one to
    l = []
    for each_dict in info:
        new_info = {x: each_dict[x] for x in each_dict}
        l.append(new_info)
    return l


def check_sample_source_associated_with_project(sample_source, sample_source_info):
    # sample_source_info is a line from the input csv
    # sample_source is the corresponding entry from the DB
    # get the projects from the input file as set
    projects_from_input_file = sample_source_info['projects'].split(';')
    projects_from_input_file = set([x.strip() for x in projects_from_input_file])
    # get the projects from the db for this sample_source
    projects_from_db = set([x.project_name for x in sample_source.projects])
    # are there any sample_source to project relationships in the file which aren't represented in the db?
    new_projects_from_file = projects_from_input_file - projects_from_db
    # if there are any
    if len(new_projects_from_file) > 0:
        # then, for each one
        for project_name in new_projects_from_file:
            print(f"Adding existing sample_source {sample_source_info['sample_source_identifier']} to project "
                  f"{project_name}")
            # query projects, this will only return p[0] is True if the project name already exists for this group
            # otherwise, they need to add the project and re-run.
            p = query_projects(sample_source_info, project_name)
            if p[0] is True:
                # add it to the projects assocaited with this sample source
                sample_source.projects.append(p[1])
            else:
                print(f"Project {project_name} from group {sample_source_info['group_name']} "
                      f" doesnt exist in the db, you need to add it using the seqbox_cmd.py "
                      f"add_projects function.\nExiting now.")
                sys.exit()
    # and update the database.
    db.session.commit()


def does_sample_source_already_exist(sample_source_info):
    # this function checks is a sample source with the specified identifier already exists for this group
    # sample_source is joined to projects by automagic (via sample_source_project)
    # SampleSource.query.with_entities(SampleSource.sample_source_identifier).join(SampleSource.projects)\
    all_sample_sources_for_this_group = \
        SampleSource.query.join(SampleSource.projects)\
        .filter_by(group_name=sample_source_info['group_name']) \
        .distinct()
    # can't help but feel this block could be replaced by sql, but dont know the sql/sqlalchemy for it.
    # make a dictionary of {sample_source_identifier : sample_source db record}
    all_sample_sources_for_this_group = {x.sample_source_identifier: x for x in all_sample_sources_for_this_group}
    # if our sample_source is in the db for this group already
    if sample_source_info['sample_source_identifier'] in all_sample_sources_for_this_group:
        # we need to check if the project we're entering it with here is associated with it in the database
        check_sample_source_associated_with_project(all_sample_sources_for_this_group[sample_source_info['sample_source_identifier']], sample_source_info)
        print(f"This sample source ({sample_source_info['sample_source_identifier']}) already exists in the database "
              f"for the group {sample_source_info['group_name']}")
        return True
    else:
        return False


def does_sample_already_exist(sample_info):
    # this function checks if this sample identifier has already been used by this group, and if so,
    # returns True, if not it returns false
    # the aim of this query is to get a list of all the sample identifiers belonging to a specific group
    # this does a join of sample and projects (via magic), and the filters by the group_name
    # https://stackoverflow.com/questions/40699642/how-to-query-many-to-many-sqlalchemy
    matching_sample = Sample.query.with_entities(Sample.sample_identifier).\
        filter_by(sample_identifier=sample_info['sample_identifier']).join(SampleSource).join(SampleSource.projects)\
        .filter_by(group_name=sample_info['group_name'])\
        .distinct().all()
    if len(matching_sample) == 0:
        return False
    elif len(matching_sample) == 1:
        print(f"This sample ({sample_info['sample_identifier']}) already exists in the database for the group "
              f"{sample_info['group_name']}")
        return True


def add_project(project_info):
    project = Project(project_name=project_info['project_name'], group_name=project_info['group_name'],
                      institution=project_info['institution'], project_details=project_info['project_details'])
    db.session.add(project)
    db.session.commit()


def query_projects(info, project_name):
    # query_projects differs from does_project_already_exist because query_projects returns an error if it can't
    # find match, while does_project_already_exist returns false
    # combine with does_project_already_exist
    matching_projects = Project.query.filter_by(project_name=project_name,
                                                group_name=info['group_name']).all()
    if len(matching_projects) == 0:
        # need this to have the `,` so that can evaluate the return correctly for the elif section
        return False,
    elif len(matching_projects) == 1:
        s = matching_projects[0]
        return True, s
    else:
        print(f"There is already more than one project called {project_name} from {info['group_name']} at "
              f"{info['institution']} in the database, this shouldn't happen.\nExiting.")
        sys.exit()


def get_projects(info):
    assert 'projects' in info
    assert 'group_name' in info
    project_names = [x.strip() for x in info['projects'].split(';')]
    projects = []
    for project_name in project_names:
        # todo - this is new, added for different function, so check it works
        p = query_projects(info, project_name)
        if p[0] is True:
            projects.append(p[1])
        elif p[0] is False:
            print(f"Project {project_name} from group {info['group_name']} "
                  f" doesnt exist in the db, you need to add it using the seqbox_cmd.py "
                  f"add_projects function.\nExiting now.")
            sys.exit()
    return projects


def get_sample_source(sample_info):
    # want to find whether this sample_source is already part of this project
    matching_sample_source = SampleSource.query.\
        filter_by(sample_source_identifier=sample_info['sample_source_identifier'])\
        .join(SampleSource.projects)\
        .filter_by(group_name=sample_info['group_name']).all()
    # matching_sample_source = SampleSource.query.all()
    # print(matching_sample_source)
    # print(sample_info['sample_source_identifier'], sample_info['group_name'])
    if len(matching_sample_source) == 0:
        print(f"There is no matching sample_source with the sample_source_identifier "
              f"{sample_info['sample_source_identifier']} for group {sample_info['group_name']}, please add using "
              f"python seqbox_cmd.py add_sample_source and then re-run this command. Exiting.")
        sys.exit()
    elif len(matching_sample_source) == 1:
        return matching_sample_source[0]
    else:
        print(f"There is more than one matching sample_source with the sample_source_identifier "
              f"{sample_info['sample_source_identifier']} for group {sample_info['group_name']}, This shouldn't happen. Exiting.")
    # for x in matching_sample_source:
    #     print(x.sample_source_identifier, [y.group_name for y in x.projects])


def read_in_sample_info(sample_info):
    sample = Sample(sample_identifier=sample_info['sample_identifier'])
    if sample_info['species'] != '':
        sample.species = sample_info['species']
    if sample_info['sample_type'] != '':
        sample.sample_type = sample_info['sample_type']
    if sample_info['sample_source_identifier'] != '':
        sample.sample_source_id = sample_info['sample_source_identifier']
    if sample_info['day_collected'] != '':
        sample.day_collected = sample_info['day_collected']
    if sample_info['month_collected'] != '':
        sample.month_collected = sample_info['month_collected']
    if sample_info['year_collected'] != '':
        sample.year_collected = sample_info['year_collected']
    return sample


def read_in_sample_source_info(sample_source_info):
    # todo - sample_source_identifier shouldnt be allowed to be null
    sample_source = SampleSource(sample_source_identifier=sample_source_info['sample_source_identifier'])
    if sample_source_info['sample_source_type'] != '':
        sample_source.sample_source_type = sample_source_info['sample_source_type']
    if sample_source_info['township'] != '':
        sample_source.location_third_level = sample_source_info['township']
    if sample_source_info['city'] != '':
        sample_source.location_second_level = sample_source_info['city']
    if sample_source_info['country'] != '':
        sample_source.country = sample_source_info['country']
    if sample_source_info['latitude'] != '':
        sample_source.latitude = sample_source_info['latitude']
    if sample_source_info['longitude'] != '':
        sample_source.longitude = sample_source_info['longitude']
    return sample_source


def add_sample(sample_info):
    # sample_info is a dict of one line of the input csv (keys from col header)
    # for the projects listed in the csv, check if they already exist for that group
    # if it does, return it, if it doesnt, instantiate a new Project and return it
    # print(sample_info)
    sample_source = get_sample_source(sample_info)
    # instantiate a new Sample
    sample = read_in_sample_info(sample_info)
    sample_source.samples.append(sample)
    print(f"Adding sample {sample_info['sample_identifier']}")
    db.session.add(sample)
    db.session.commit()


def add_sample_source(sample_source_info):
    # sample_info is a dict of one line of the input csv (keys from col header)
    # for the projects listed in the csv, check if they already exist for that group
    # if it does, return it, if it doesnt, instantiate a new Project and return it
    projects = get_projects(sample_source_info)
    # print(projects)
    # instantiate a new SampleSource
    sample_source = read_in_sample_source_info(sample_source_info)
    sample_source.projects = projects
    print(f'adding {sample_source_info["sample_source_identifier"]} to project(s) {projects}')
    db.session.add(sample_source)
    db.session.commit()

# def get_read_sets(read_set_info, sample_identifier, group):
#     read_sets = []
#     # read_set_info is a list of dioctionaries generated from the read set input csv
#     # rs is a dictoinary where the keys are the header of the read set input csv, and the values are from one line
#     # of the CSV
#     for rs in read_set_info:
#         if rs['sample_identifier'] == sample_identifier:
#             if rs['group'] == group:
#                 read_set = return_read_set(rs)
#                 read_sets.append(read_set)
#     return read_sets


# def return_read_set(rs):
#     ## TODO - add nanopore
#     ## todo - isn't handling existing readset yet
#     batch = get_batch(rs['batch'], rs['group'])
#     read_set = ReadSet(type=rs['type'], read_set_filename=rs['read_set_filename'], batch=batch)
#     if rs['type'] == 'Illumina':
#         irs = IlluminaReadSet(path_r1=rs['path_r1'], path_r2=rs['path_r2'])
#         read_set.illumina_read_sets = irs
#     return read_set


# def get_batch(batch_name, group):
#     matching_batch = ReadSetBatch.query.filter_by(name=batch_name).all()
#     if len(matching_batch) == 0:
#         rsb = ReadSetBatch(name=batch_name)
#         return rsb
#     elif len(matching_batch) == 1:
#         return matching_batch[0]
#     else:
#         print(f"There is already more than one batch called {batch_name} from {group} in the database, "
#               "this shouldn't happen.\nExiting.")
#         sys.exit()