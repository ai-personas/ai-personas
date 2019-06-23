from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import math
import os.path
import random
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
from tensorflow.python.ops import io_ops
from tensorflow.python.platform import gfile
from tensorflow.python.util import compat

tf.enable_eager_execution()

# download data file
def maybe_download_and_extract_dataset(data_url, dest_directory):
    if not data_url:
        return
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    filename = data_url.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    if not os.path.exists(filepath):

        def _progress(count, block_size, total_size):
            sys.stdout.write(
                '\r>> Downloading %s %.1f%%' %
                (filename, float(count * block_size) / float(total_size) * 100.0))
            sys.stdout.flush()

        try:
            filepath, _ = urllib.request.urlretrieve(data_url, filepath, _progress)
        except:
            tf.logging.error('Failed to download URL: %s to folder: %s', data_url,
                             filepath)
            tf.logging.error('Please make sure you have enough free space and'
                             ' an internet connection')
            raise
        print()
        statinfo = os.stat(filepath)
        tf.logging.info('Successfully downloaded %s (%d bytes)', filename,
                        statinfo.st_size)
        tarfile.open(filepath, 'r:gz').extractall(dest_directory)

def get_data():
    # inital params
    sample_rate = 16000
    window_size_ms = 30.0
    window_stride_ms = 10.0

    # desired samples calc
    sample_rate = 16000
    clip_duration_ms = 1000
    desired_samples = int(sample_rate * clip_duration_ms / 1000)

    # mfcc
    feature_bin_count = 40
    average_window_width = -1
    fingerprint_width = feature_bin_count

    # fingerprint size calc
    window_size_samples = int(sample_rate * window_size_ms / 1000)
    window_stride_samples = int(sample_rate * window_stride_ms / 1000)
    length_minus_window = (desired_samples -window_size_samples)
    if length_minus_window < 0:
        spectrogram_length = 0
    else:
        spectrogram_length = 1 + int(length_minus_window / window_stride_samples)
    fingerprint_size = fingerprint_width * spectrogram_length

    # download google speech file
    data_dir = '/tmp/google/speech'
    maybe_download_and_extract_dataset('http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz', data_dir)

    BACKGROUND_NOISE_DIR_NAME = '_background_noise_'
    SILENCE_LABEL = '_silence_'
    UNKNOWN_WORD_LABEL = '_unknown_'
    # wanted_words = 'yes,no,five,off,six,bed,zero,three'
    wanted_words = 'yes,no'
    label_count = len(wanted_words.split(','))

    wanted_words_index = {}
    for index, wanted_word in enumerate(wanted_words.split(',')):
      wanted_words_index[wanted_word] = index

    label_file = []
    all_words = {}
    # Look through all the subfolders to find audio samples
    search_path = os.path.join(data_dir, '*', '*.wav')
    for wav_path in gfile.Glob(search_path):
      _, word = os.path.split(os.path.dirname(wav_path))
      word = word.lower()
      # Treat the '_background_noise_' folder as a special case, since we expect
      # it to contain long audio samples we mix in to improve training.
      if word == BACKGROUND_NOISE_DIR_NAME:
        continue
      all_words[word] = True
      # If it's a known class, store its detail, otherwise add it to the list
      # we'll use to train the unknown label.
      if word in wanted_words_index:
        label_file.append({'label': word, 'file': wav_path})
    if not all_words:
      raise Exception('No .wavs found at ' + search_path)

    print("label_file len", len(label_file))
    sample_count = len(label_file)


    audio = np.zeros((sample_count, fingerprint_size))
    labels = np.zeros(sample_count)

    input_wav_files = [f['file'] for f in label_file]
    input_labels = [l['label'] for l in label_file]
    unique_labels = list(set(input_labels))

    print(unique_labels)
    print(input_labels)


    # Use the processing graph we created earlier to repeatedly to generate the
    # final output sample data we'll use in training.
    for i in xrange(0, sample_count):
      # Pick which audio sample to use.
      sample_index = np.random.randint(len(input_wav_files))
      sample = label_file[sample_index]
      time_shift_amount = 0
      time_shift_padding = [[0, -time_shift_amount], [0, 0]]
      time_shift_offset = [-time_shift_amount, 0]

      foreground_volume = 1
      if sample['label'] == '_silence_':
        foreground_volume = 0

      # Run the graph to produce the output audio.
      data_tensor = get_audio_output(sample['file'],foreground_volume,time_shift_padding,time_shift_offset)
      audio[i, :] = data_tensor.numpy()[0].flatten()
      labels[i] = unique_labels.index(sample['label'])

    print(np.shape(data))
    return data, labels.astype(int)

def get_audio_output(wav_filename, foreground_volume, time_shift_padding, time_shift_offset):
  wav_loader = io_ops.read_file(wav_filename)
  wav_decoder = contrib_audio.decode_wav(wav_loader, desired_channels=1, desired_samples=desired_samples)

  # Allow the audio sample's volume to be adjusted.
  scaled_foreground = tf.multiply(wav_decoder.audio, foreground_volume)

  # Shift the sample's start position, and pad any gaps with zeros.
  padded_foreground = tf.pad(
      scaled_foreground,
      time_shift_padding,
      mode='CONSTANT')
  sliced_foreground = tf.slice(padded_foreground,
                               time_shift_offset,
                               [desired_samples, -1])


  # Run the spectrogram and MFCC ops to get a 2D 'fingerprint' of the audio.
  spectrogram = contrib_audio.audio_spectrogram(
      sliced_foreground,
      window_size=window_size_samples,
      stride=window_stride_samples,
      magnitude_squared=True)

  # The number of buckets in each FFT row in the spectrogram will depend on
  # how many input samples there are in each window. This can be quite
  # large, with a 160 sample window producing 127 buckets for example. We
  # don't need this level of detail for classification, so we often want to
  # shrink them down to produce a smaller result. That's what this section
  # implements. One method is to use average pooling to merge adjacent
  # buckets, but a more sophisticated approach is to apply the MFCC
  # algorithm to shrink the representation.
  output_ = contrib_audio.mfcc(
      spectrogram,
      wav_decoder.sample_rate,
      dct_coefficient_count= fingerprint_width)
  return output_


