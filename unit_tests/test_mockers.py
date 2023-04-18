import pytest

def test_check_readset_fields(mocker):
    # Create mock objects for arguments
    readset_info = {
        'data_storage_device': 'device1',
        'sample_identifier': 'sample1',
        'group_name': 'group1',
        'readset_batch_name': 'batch1',
        'barcode': 'barcode1',
        'path_fastq': '',
        'path_fast5': ''
    }
    nanopore_default = True
    raw_sequencing_batch = mocker.MagicMock()
    raw_sequencing_batch.sequencing_type = 'nanopore'
    covid = False
    
    # Call the function
    with pytest.raises(SystemExit):
        check_readset_fields(readset_info, nanopore_default, raw_sequencing_batch, covid)

    # Test that expected messages were printed and sys.exit() was called
    mocker.patch('builtins.print')
    mocker.patch('sys.exit')
    check_readset_fields(readset_info, nanopore_default, raw_sequencing_batch, covid)
    assert print.call_count == 2
    assert sys.exit.call_count == 1
