-- in addition to the below, need to check the filestructure

-- # should be at least two projects (pseudo seq and acineto seq) belonging to Core
select * from groups
join project p on groups.id = p.groups_id;



-- # PTS15G should be in both pseudo seq and acineto seq
select sample_identifier, project_name from sample
join sample_source on sample.sample_source_id = sample_source.id
join sample_source_project ssp on sample_source.id = ssp.sample_source_id
join project p on ssp.project_id = p.id
where project_name = any(array['PseudomonasSeq', 'AcinetobacterSeq']);

-- # should be multiple samples for sample source ABS15V and PTS89D
select sample_identifier, sample_source_identifier, project_name from sample
join sample_source ss on sample.sample_source_id = ss.id
join sample_source_project ssp on ss.id = ssp.sample_source_id
join project p on ssp.project_id = p.id
where project_name = any(array['PseudomonasSeq', 'AcinetobacterSeq']);


-- # PTS89D_sample2 should have two extractions, with different extraction identifiers
select readset_identifier, sample_identifier, extraction_identifier, date_extracted, e.id from read_set_nanopore
join read_set rs on rs.id = read_set_nanopore.readset_id
join raw_sequencing r on rs.raw_sequencing_id = r.id
join extraction e on r.extraction_id = e.id
join sample s on e.sample_id = s.id
join sample_source ss on s.sample_source_id = ss.id
join sample_source_project ssp on ss.id = ssp.sample_source_id
join project p on ssp.project_id = p.id
where project_name = any(array['PseudomonasSeq', 'AcinetobacterSeq']);

-- there should be two sets of different readsets associated with the same raw sequencing.

select rs.id, readset_identifier, rsb.name, basecaller from read_set
join read_set_batch rsb on read_set.readset_batch_id = rsb.id
join raw_sequencing rs on read_set.raw_sequencing_id = rs.id;