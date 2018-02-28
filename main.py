import sampler
import helpers
import sys


parameters = {
    'tempo': {
        'start': 100,
        'end': 200,
        'interval': 5},  # (bpm_start, bpm_end, interval)
    'length': {
        'start': 1,
        'end': 2,
        'interval': 1},  # (start, end, interval) note: length in bars not in seconds
    'patterns': {
        'defined': ['4th-note'],
        'random': {
            'n': 0,  # number of samples
            'set': ['half-note', '4th-note', '8th-note', '16th-note']
        }}
    # ('random'), generate 5 random patterns
}


if __name__ == '__main__':
    
    try:
        dest_folder = sys.argv[1]
    except:
        dest_folder = 'samples'
    finally:
        sampler.create_samples(parameters, dest_folder)
        helpers.write_par_to_file(parameters, dest_folder)
