import random
import time
import math
import numpy as np
import wave
import struct
import os
import sys
import pysynth_b as psb  # a, b, e, and s variants available
import helpers

def create_samples(parameters_dict, output_folder):

    helpers.check_par_obj(parameters_dict)
    sm = SampleMaker()
    # abbreviate parameters dictionary
    p = parameters_dict

    samples = []

    for length in range(p['length']['start'], p['length']['end'], p['length']['interval']):
        for defined_ptrn in p['patterns']['defined']:
            samples.append(sm.make_sample(length, defined_ptrn))

        for id in range(p['patterns']['random']['n']):
            samples.append(sm.make_random_sample(length, p['patterns']['random']['set'], id))

    #print(len(samples), 'len(samples)')
    #print('samples', samples)
    sm.generate_samples(output_folder, samples, (p['tempo']['start'], p['tempo']['end'], p['tempo']['interval']))

    number_of_samples_without_noise = len(samples) * (p['tempo']['end'] - p['tempo']['start']) / p['tempo']['interval']

    print()  # for better format, too lazy to find the real issue xD
    print(round(number_of_samples_without_noise), 'different samples without noise')
    print()

    number_of_samples_with_noise = 0
    if 'std' in p:
        number_of_samples_with_noise = number_of_samples_without_noise * (p['std']['end'] - p['std']['start'] + p['std']['interval']) / p['std']['interval']
        sm.add_noisy_samples('{}/without_noise/'.format(output_folder), (p['std']['start'], p['std']['end'], p['std']['interval']))

    print('Total', round(number_of_samples_with_noise + number_of_samples_without_noise), 'samples made.')


class Sample:

    def __init__(self, sample, bars, pattern, note):
        self.sample = sample
        self.bars = str(bars)
        self.note_length = str(pattern)
        self.note = str(note)


class SampleMaker:

    def make_random_sample(self, bars, pattern, id):
        ''' Length is approximated
        :param bars: bar integer multiple
        :return:
        '''
        song = []

        time_length_choices = []

        # convert pattern to number and add also pysynth negative values aka dotted half notes
        for i in range(len(pattern)):
            if pattern[i] == 'whole-note':
                time_length_choices.extend([-1, 1])
            elif pattern[i] == 'half-note':
                time_length_choices.extend([-2, 2])
            elif pattern[i] == '4th-note':
                time_length_choices.extend([-4, 4])
            elif pattern[i] == '8th-note':
                time_length_choices.extend([-8, 8])
            elif pattern[i] == '16th-note':
                time_length_choices.extend([-16, 16])
            elif pattern[i] == '32th-note':
                time_length_choices.extend([-32, 32])


        note_choices = ['a0', 'a#0', 'bb0', 'b0', 'cb0', 'c1', 'b#1', 'c#1', 'db1', 'd1', 'd#1', 'eb1', 'e1', 'fb1',
                        'f1',
                        'e#1', 'f#1', 'gb1', 'g1', 'g#1', 'ab1', 'a1', 'a#1', 'bb1', 'b1', 'cb1', 'c2', 'b#2', 'c#2',
                        'db2',
                        'd2', 'd#2', 'eb2', 'e2', 'fb2', 'f2', 'e#2', 'f#2', 'gb2', 'g2', 'g#2', 'ab2', 'a2', 'a#2',
                        'bb2',
                        'b2', 'cb2', 'c3', 'b#3', 'c#3', 'db3', 'd3', 'd#3', 'eb3', 'e3', 'fb3', 'f3', 'e#3', 'f#3',
                        'gb3',
                        'g3', 'g#3', 'ab3', 'a3', 'a#3', 'bb3', 'b3', 'cb3', 'c4', 'b#4', 'c#4', 'db4', 'd4', 'd#4',
                        'eb4',
                        'e4', 'fb4', 'f4', 'e#4', 'f#4', 'gb4', 'g4', 'g#4', 'ab4', 'a4', 'a#4', 'bb4', 'b4', 'cb4',
                        'c5',
                        'b#5', 'c#5', 'db5', 'd5', 'd#5', 'eb5', 'e5', 'fb5', 'f5', 'e#5', 'f#5', 'gb5', 'g5', 'g#5',
                        'ab5',
                        'a5', 'a#5', 'bb5', 'b5', 'cb5', 'c6', 'b#6', 'c#6', 'db6', 'd6', 'd#6', 'eb6', 'e6', 'fb6',
                        'f6',
                        'e#6', 'f#6', 'gb6', 'g6', 'g#6', 'ab6', 'a6', 'a#6', 'bb6', 'b6', 'cb6', 'c7', 'b#7', 'c#7',
                        'db7',
                        'd7', 'd#7', 'eb7', 'e7', 'fb7', 'f7', 'e#7', 'f#7', 'gb7', 'g7', 'g#7', 'ab7', 'a7', 'a#7',
                        'bb7',
                        'b7', 'cb7', 'c8', 'b#8']
        current_length = 0
        while current_length < bars:
            random.shuffle(time_length_choices)
            random.shuffle(note_choices)
            note_length = random.choice(time_length_choices)
            note = random.choice(note_choices)

            current_length = current_length + 1 / abs(note_length)
            song.append((note, note_length))
        #print(id, ' : ', song)
        #print()

        return Sample(song, bars, 'random{}'.format(id), 'all')


    def make_sample(self, bars, pattern, note = 'c'):
        ''' Generate a sample wave. Make random if pattern='random' '''

        # convert pattern to number
        if pattern == 'whole-note':
            pattern = 1
        elif pattern == 'half-note':
            pattern = 2
        elif pattern == '4th-note':
            pattern = 4
        elif pattern == '8th-note':
            pattern = 8
        elif pattern == '16th-note':
            pattern = 16
        elif pattern == '32th-note':
            pattern = 32

        sample = []
        current_length = 0

        while current_length < bars:
            sample.append((note, pattern))
            current_length = current_length + 1 / pattern

        return Sample(sample, bars, pattern, note)


    def generate_samples(self, output_folder, sample_list, tempo):
        '''
        Generates .wav-s for every given tempo from the sample.
        :param sample_list: Sample list
        :param tempo:
        :param output_folder:
        :return:
        '''

        start = tempo[0]
        end = tempo[1]
        interval = tempo[2]

        for sample in sample_list:
            for t in range(start, end, interval):
                # remove the '/' if it exists
                if output_folder.endswith('/'):
                    output_folder = output_folder[:-1]

                # if random samples add custom identifier not to override other random patterns
                filename = '{}bpm_{}bars_{}ptrn.wav'.format(t, sample.bars, sample.note_length)
                file_location = '{}/without_noise/{}'.format(output_folder, filename)

                # make directories if they don't exist
                if not os.path.exists(os.path.dirname(file_location)):
                    os.makedirs(os.path.dirname(file_location))
                psb.make_wav(sample.sample, fn=file_location, leg_stac=.7, bpm=t, silent=True)

                print('Created:', file_location)




    def add_noisy_samples(self, source_dir, std):
        '''Generates noisy files with given parameters from every .wav file in the source_dir.
        Output files are written to source_dir/../std<std>'''

        sample_files = helpers.get_files_in_top_dir(source_dir)

        start = std[0]
        end = std[1]
        interval = std[2]
        for standard_deviation in range(start, end, interval):
            for sample in sample_files:
                self.make_some_noise(source_dir + sample, std=standard_deviation)


    def make_some_noise(self, file_location, mean = 0, std = 100, silent=True):
        ''' Add gaussian noise to wav file. '''

        CHUNK_SIZE = 1024
        # noise is always white => mean zero

        input_wave = wave.open(file_location, 'rb')

        if not silent:
            print('format', input_wave.getparams())

        noisy_sample = np.array([])

        data = input_wave.readframes(CHUNK_SIZE)

        while len(data) > 0:

            data_chunk = np.fromstring(data, 'int16') # one channels sampwidth = 2 => 2* 8 = 16

            noise = np.random.normal(mean, std, size=len(data_chunk))
            noisy_sample = np.concatenate((noisy_sample, data_chunk + noise))

            data = input_wave.readframes(CHUNK_SIZE)

        if not silent:
            print('Max noisy sample:', max(noisy_sample))
            print('Min noisy sample:', min(noisy_sample))


        filename = os.path.split(file_location)[1]

        output_dir = '{}/../std{}/'.format(os.path.dirname(file_location), std)

        output_file_location = '{}{}_noisy_{}.wav'.format(output_dir, filename.rsplit('.wav')[0], std)

        # create folders if they don't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # create file with noise
        output_wave = wave.open(output_file_location, 'wb')
        output_wave.setnchannels(input_wave.getnchannels())
        output_wave.setsampwidth(input_wave.getsampwidth())
        output_wave.setframerate(input_wave.getframerate())

        noisy_sample = noisy_sample.astype(int)
        noisy_sample = noisy_sample.tolist()

        # if int16 limits broken, add zero
        noisy_sample_in_bytes = []
        for item in noisy_sample:
            if -32768 <= item <= 32767:
                noisy_sample_in_bytes.append(struct.pack('<h', item))
            else:
                noisy_sample_in_bytes.append(b'\x00\x00')

        if not silent:
            print('b''.join(noisy_sample_in_bytes', len(b''.join(noisy_sample_in_bytes)))

        output_wave.writeframes(b''.join(noisy_sample_in_bytes))
        print('Created:', output_file_location, '\n')

        output_wave.close()
