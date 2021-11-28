import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


filepath = 'Cash_Cash_-_Overtime.ogg'

def mp3_to_hpss_spectrogram():
    x, sr = librosa.load(filepath, duration = 60)
    D = librosa.stft(x)
    D_harmonic, D_percussive = librosa.decompose.hpss(D)
    rp = np.max(np.abs(D))
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=rp), y_axis='log')
    plt.colorbar()
    plt.title('Original spectrogram')
    plt.subplot(3, 1, 2)
    librosa.display.specshow(librosa.amplitude_to_db(D_harmonic, ref=rp), y_axis='log')
    plt.colorbar()
    plt.title('Harmonic spectrogram')
    plt.subplot(3, 1, 3)
    librosa.display.specshow(librosa.amplitude_to_db(D_percussive, ref=rp), y_axis='log', x_axis='time')
    plt.colorbar()
    plt.title('Percussive spectrogram')
    plt.tight_layout()

def mp3_to_hpss_waveplot():
    fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True)
    y, sr = librosa.load(filepath, duration=60)
    librosa.display.waveplot(y, sr=sr, ax=ax[0])
    ax[0].set(title='Original waveform')
    ax[0].label_outer()
    harm, perc = librosa.effects.hpss(y)
    librosa.display.waveplot(harm, sr=sr, alpha=0.5, ax=ax[1])
    ax[1].set(title='Harmonic waveform')
    librosa.display.waveplot(perc, sr=sr, color='r', alpha=0.5, ax=ax[2])
    ax[2].set(title='Percussive waveform')

def mp3_to_hpss():
    y, sr = librosa.load(filepath, duration=60, sr=None)
    D = librosa.stft(y)
    D_harmonic, D_percussive = librosa.decompose.hpss(D)
    h = librosa.istft(D_harmonic)
    p = librosa.istft(D_percussive)
    import soundfile as sf
    filename = filepath + "_percussive.wav"
    sf.write(filename, p, 44100)

def mp3_to_txt():
    file_path = filepath + "_percussive.wav"
    x, sr = librosa.load(file_path, duration=60)
    onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    # onset_frames = librosa.onset.onset_detect(x, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames)
    output_name = "beat_timeframe.txt"
    with open(output_name, 'wt') as f:
        f.write('\n'.join(['%.1f' % onset_time for onset_time in onset_times]))

def txt_to_note():
    pass

mp3_to_hpss()
mp3_to_txt()

# Visualisation
# mp3_hpss_visualise()
# mp3_to_hpss_waveplot()