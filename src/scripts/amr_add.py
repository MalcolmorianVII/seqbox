import csv

def sanitize_amr_header(amr_dict):
    amr_dict['contig_id'] = amr_dict.pop('Contig id')
    amr_dict['start'] = amr_dict.pop('Start')
    amr_dict['stop'] = amr_dict.pop('Stop')
    amr_dict['strand'] = amr_dict.pop('Strand')
    amr_dict['gene_symbol'] = amr_dict.pop('Gene symbol')
    amr_dict['class'] = amr_dict.pop('Class')
    amr_dict['subclass'] = amr_dict.pop('Subclass')
    amr_dict['sequence_name'] = amr_dict.pop('Sequence name')
    amr_dict['target_length'] = amr_dict.pop('Target length')
    amr_dict['reference_sequence_length'] = amr_dict.pop('Reference sequence length')
    amr_dict['pct_cov_of_ref_seq'] = amr_dict.pop('% Coverage of reference sequence')
    amr_dict['pct_id_to_ref_seq'] = amr_dict.pop('% Identity to reference sequence')
    amr_dict['alignment_length'] = amr_dict.pop('Alignment length')
    amr_dict['accession_of_closest_sequence'] = amr_dict.pop('Accession of closest sequence')

def read_in_as_dict(inhandle,delimiter=','):
    # since csv.DictReader returns a generator rather than an iterator, need to do this fancy business to
    # pull in everything from a generator into an honest to goodness iterable.
    info = csv.DictReader(open(inhandle, encoding='utf-8-sig'),delimiter=delimiter)
    # info is a list of ordered dicts, so convert each one to
    list_of_lines = []
    
    for each_dict in info:
        # print(each_dict)
        # delete data from columns with no header, usually just empty fields
        unwanted = ['Protein identifier','Scope','Element type','Element subtype','Method','HMM id','HMM description','Name of closest sequence']
        change = ['% Coverage of reference sequence','% Identity to reference sequence']
        if None in each_dict:
            del each_dict[None]
        new_info = {x: each_dict[x] for x in each_dict if x not in unwanted}
        sanitize_amr_header(new_info)
        # print(new_info)
        # sometimes excel saves blank lines, so only take lines where the lenght of the set of teh values is > 1
        # it will be 1 where they are all blank i.e. ''
        if len(set(new_info.values())) > 1:
            list_of_lines.append(new_info)
        # because pcr assay only has one value, need to add this check
        elif len(set(new_info.values())) == 1:
            if list(set(new_info.values()))[0] == '':
                pass
            else:
                list_of_lines.append(new_info)
        else:
            pass
            # print(f'This line not being processed - {new_info}')
    return list_of_lines

file = "/home/bkutambe/test_data/bactopia_train/bactopiaResults/CQJ14G/antimicrobial-resistance/CQJ14G-gene-report.txt"
amrs = read_in_as_dict(file)

def get_amrs():
    amrs = read_in_as_dict(file,delimiter="\t")

print(amrs)