import pytest
from os import path 
from app import models
import datetime
import glob


def test_read_in_dict(file,read_in_func):
    assert path.exists(file)
    assert file.endswith('.csv')
    assert file.endswith('.xlsx')
    data = read_in_func(file)
    assert data

def decorate_read_in_funcs(read_in_func):
    def read_in_wrapper(dict_info):
        assert isinstance(dict_info,dict)
        read_in_func

    return read_in_wrapper

@decorate_read_in_funcs
def test_read_in_sample_info(sample_info):
    valid_keys = ['sample_identifier','species','sample_type','sample_source_identifier','day_collected',
                   'month_collected','year_collected','day_received','month_received','year_received']
    # sample = models.Sample(sample_identifier=sample_info['sample_identifier'])
    sample = models.Sample()
    valid_table_cols = sample.__table__.columns.keys()[1:] # exclude id & table relations
    
    assert isinstance(sample_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert sample_info[col]
    
    # Tests if every entry in sample info is valid
    for key in sample_info:
        assert key in valid_keys
    assert len(sample_info) > 0

@decorate_read_in_funcs
def test_read_in_sample_source_info(sample_source_info):
    valid_keys = ['sample_source_identifier','sample_source_type','township','city','country','latitude','longitude']
    sample_source = models.SampleSource()
    valid_table_cols = sample_source.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert sample_source_info[col]
    
    # Tests if every entry in sample info is valid
    for key in sample_source_info:
        assert key in valid_keys
    assert len(sample_source_info) > 0

@decorate_read_in_funcs
def test_read_in_culture(culture_info):
    valid_keys = ['date_cultured','culture_identifier','submitter_plate_id','submitter_plate_well']
    culture = models.Culture()
    valid_table_cols = culture.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert culture_info[col]
    
    # Tests if every entry in sample info is valid
    for key in culture_info:
        assert key in valid_keys
    assert len(culture_info) > 0

    assert isinstance(culture_info['date_cultured'],datetime.datetime)
    
@decorate_read_in_funcs
def test_read_in_extraction(extraction_info):
    valid_keys = ['extraction_identifier','extraction_machine','extraction_kit','what_was_extracted',
                    'date_extracted','extraction_processing_institution','extraction_from',
                    'nucleic_acid_concentration','submitter_plate_id']

                
    extraction = models.Extraction()

    assert extraction_info['submitter_plate_id'].startswith('EXT')
    valid_table_cols = extraction.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert extraction_info[col]
    
    # Tests if every entry in sample info is valid
    for key in extraction_info:
        assert key in valid_keys
    assert len(extraction_info) > 0

    assert isinstance(extraction_info['date_extracted'],datetime.datetime)

@decorate_read_in_funcs
def test_read_in_group(group_info):
    valid_keys = ['group_name','institution','pi']
    group = models.Groups()
    valid_table_cols = group.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert group_info[col]
    
    # Tests if every entry in sample info is valid
    for key in group_info:
        assert key in valid_keys
    assert len(group_info) > 0
    
@decorate_read_in_funcs   
def test_read_in_mykrobe(mykrobe_result_info):
    valid_keys = ['mykrobe_version','drug','susceptibility','variants','genes',
                'phylo_group','species','lineage','phylo_group_per_covg''species_per_covg',
                'lineage_per_covg','phylo_group_depth','species_depth','lineage_depth']
    mykrobe = models.Mykrobe()
    
    valid_table_cols = mykrobe.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert mykrobe_result_info[col]
    
    # Tests if every entry in sample info is valid
    for key in mykrobe_result_info:
        assert key in valid_keys
    assert len(mykrobe_result_info) > 0


@decorate_read_in_funcs
def test_read_in_tiling_pcr(tiling_pcr_info):
    valid_keys = ['date_tiling_pcred','tiling_pcr_identifier','tiling_pcr_protocol','number_of_cycles']
    tiling_pcr = models.TilingPcr()

    valid_table_cols = tiling_pcr.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert tiling_pcr_info[col]
    
    # Tests if every entry in sample info is valid
    for key in tiling_pcr_info:
        assert key in valid_keys
    assert len(tiling_pcr_info) > 0

@decorate_read_in_funcs
def test_read_in_artic_covid_result(artic_covid_result_info):
    valid_keys = ['sample_name','pct_N_bases','pct_covered_bases','num_aligned_reads','artic_workflow','artic_profile']
    artic_covid_result = models.ArticCovidResult()
    valid_table_cols = artic_covid_result.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert artic_covid_result_info[col]
    
    # Tests if every entry in sample info is valid
    for key in artic_covid_result_info:
        assert key in valid_keys
    assert len(artic_covid_result_info) > 0 

@decorate_read_in_funcs
def test_read_in_pangolin_result(pangolin_result_info):
    valid_keys = ['lineage','conflict','ambiguity_score','scorpio_call','scorpio_support',
                'scorpio_conflict','version','pangolin_version','pango_version','status','note']
    pangolin_result = models.PangolinResult()
    valid_table_cols = pangolin_result.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert pangolin_result_info[col]
    
    # Tests if every entry in sample info is valid
    for key in pangolin_result_info:
        assert key in valid_keys
    assert len(pangolin_result_info) > 0 

@decorate_read_in_funcs
def test_read_in_covid_confirmatory_pcr(covid_confirmatory_pcr_info):
    valid_keys = ['date_covid_confirmatory_pcred','covid_confirmatory_pcr_identifier',
                'covid_confirmatory_pcr_protocol','covid_confirmatory_pcr_ct']
    covid_confirmatory_pcr = models.CovidConfirmatoryPcr()
    valid_table_cols = covid_confirmatory_pcr.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert covid_confirmatory_pcr_info[col]
    
    # Tests if every entry in sample info is valid
    for key in covid_confirmatory_pcr_info:
        assert key in valid_keys
    assert len(covid_confirmatory_pcr_info) > 0 
    
@decorate_read_in_funcs
def read_in_pcr_result(pcr_result_info):
    valid_keys = ['date_pcred','pcr_identifier','ct','pcr_result']
    pcr_result = models.PcrResult()
    valid_table_cols = pcr_result.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert pcr_result_info[col]
    
    # Tests if every entry in sample info is valid
    for key in pcr_result_info:
        assert key in valid_keys
    assert len(pcr_result_info) > 0 
    assert isinstance(pcr_result_info['date_pcred'],datetime.datetime)

@decorate_read_in_funcs
def test_read_in_raw_sequencing_batch_info(raw_sequencing_batch_info):
    valid_keys = ['batch_name','instrument_model','date_run','instrument_name','sequencing_centre','flowcell_type','sequencing_type','batch_directory']
    raw_sequencing_batch = models.RawSequencingBatch()
    valid_table_cols = raw_sequencing_batch.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert raw_sequencing_batch_info[col]
    
    # Tests if every entry in sample info is valid
    for key in raw_sequencing_batch_info:
        assert key in valid_keys
    assert len(raw_sequencing_batch_info) > 0 

    assert isinstance(raw_sequencing_batch_info['date_run'],datetime.datetime)
    
@decorate_read_in_funcs
def test_read_in_readset_batch(readset_batch_info):
    valid_keys = ['readset_batch_name','readset_batch_dir','basecaller']
    readset_batch = models.ReadSetBatch()
    valid_table_cols = readset_batch.__table__.columns.keys()[1:] # exclude id & table relations
    
    # assert isinstance(sample_source_info,dict)
    # Tests if every Sample col is represented in sample_info i.e 
    # tests whether sample_info has all the data Sample Table needs for a record
    for col in valid_table_cols:
        assert readset_batch_info[col]
    
    # Tests if every entry in sample info is valid
    for key in readset_batch_info:
        assert key in valid_keys
    assert len(readset_batch_info) > 0 


@decorate_read_in_funcs
def test_read_in_raw_sequencing(readset_info, nanopore_default, sequencing_type, batch_directory):
    raw_sequencing = models.RawSequencing()
    if sequencing_type == 'illumina':
        raw_sequencing.raw_sequencing_illumina = models.RawSequencingIllumina()
        valid_keys = ['path_r1','path_r2','library_prep_method']
        
    if sequencing_type == 'nanopore':
        valid_keys = ['path_fast5','library_prep_method','library_prep_method']
        raw_sequencing.raw_sequencing_nanopore = models.RawSequencingNanopore()
        if nanopore_default is True:
            path = path.join(batch_directory, 'fast5_pass', readset_info['barcode'], '*fast5')
            raw_sequencing.raw_sequencing_nanopore.path_fast5 = path
            raw_sequencing.raw_sequencing_nanopore.library_prep_method = readset_info['library_prep_method']
            fast5s = glob.glob(path)
            assert len(fast5s) == 0
        elif nanopore_default is False:
            assert readset_info['path_fast5'].endswith('fast5')
            assert path.isfile(readset_info['path_fast5'])
            raw_sequencing.raw_sequencing_nanopore.path_fast5 = readset_info['path_fast5']


@decorate_read_in_funcs
def read_in_readset(readset_info, nanopore_default, raw_sequencing_batch, readset_batch, covid):
    readset = models.ReadSet()
    if raw_sequencing_batch.sequencing_type == 'nanopore':
        readset.readset_nanopore = models.ReadSetNanopore()
        if nanopore_default is False:
            assert readset_info['path_fastq'].endswith('fastq.gz')
            
        elif nanopore_default is True:
            path = path.join(readset_batch.batch_directory, 'fastq_pass', readset_info['barcode'], '*fastq.gz')
            fastqs = glob.glob(path)
            
            assert len(fastqs) == 1
            assert len(fastqs) == 0 
            assert len(fastqs) > 1
                
    elif raw_sequencing_batch.sequencing_type == 'illumina':
        readset.readset_illumina = models.ReadSetIllumina()
        assert readset_info['path_r1'].endswith('fastq.gz')
        assert readset_info['path_r2'].endswith('fastq.gz')

