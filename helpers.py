import sys
import os

def get_files_in_top_dir(file_location):
    '''Return all files in a list in file location in reference to current directory.'''
    sample_files = []

    for (path, dirnames, filenames) in os.walk(file_location):
        # add only '.wav files'
        for filename in filenames:
            if filename.endswith('.wav'):
                sample_files.append(filename)
        break
    return sample_files


def check_par_obj(obj):

    if 'tempo' not in obj:
        print('key "tempo" not found')
        sys.exit()
    check_par(obj, 'tempo')

    if 'length' not in obj:
        print('key "length" not found')
        sys.exit()
    check_par(obj, 'length')

    if 'patterns' not in obj:
        print('key "patterns" not found')
        sys.exit()
    check_pattern_par(obj, 'patterns')

    if 'std' in obj:
        check_par(obj, 'std')



def check_par(obj, par_name):

    if ('start' or 'end' or 'interval') not in obj[par_name]:
        print(par_name, 'dict keys not found')
        sys.exit()

    start = obj[par_name]['start']
    end = obj[par_name]['end']
    interval = obj[par_name]['interval']

    if type(start) is not int or type(end) is not int or type(interval) is not int:
        print(par_name, 'obj parameters must be integers')
        sys.exit()

    if start < 0 or end < 0 or interval < 0:
        print(par_name, 'obj parameters must be positive')
        sys.exit()

    if start >= end:
        print(par_name, 'obj start must be smaller than end')
        sys.exit()

    # input syntax: (1,1,1) possible
    if interval > end - start + 1:
        print(par_name, ' obj interval must fit')
        sys.exit()


def check_pattern_par(obj, par_name):
    possible_patterns = ['whole-note', 'half-note', '4th-note', '8th-note', '16th-note', '32th-note']

    if not ('defined' or 'random') in obj[par_name]:
        print(par_name, 'dict keys not found')
        sys.exit()

    if not ('n' or 'set') in obj[par_name]['random']:
        print(par_name, 'random dict keys not found')
        sys.exit()

    defined = obj[par_name]['defined']
    n = obj[par_name]['random']['n']
    s = obj[par_name]['random']['set']

    for item in defined:
        if item not in possible_patterns:
            print('undefined pattern')
            sys.exit()

    if type(n) is not int or n < 0:
        print('key "n" in random" must be integer and at least 1')
        sys.exit()
    for item in s:
        if item not in possible_patterns:
            print('invalid random set')
            sys.exit()

def write_par_to_file(parameters, dest_folder):
    f = open('{}/parameters.txt'.format(dest_folder), 'w')
    f.write('Test suite name: {}\nParameters used to generate samples:\n{}'.format(dest_folder, parameters))
    f.close()
