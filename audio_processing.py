from collections import Counter
import time
import traceback
import numpy as np
from scipy.signal import butter, lfilter, find_peaks

class AudioProcessor:
    def __init__(self, app):
        self.SAMPLE_RATE = 44100
        self.NOISE_THRESHOLD = 0.005
        self.app = app

    #Processing Audio
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a
    #Processing Audio   
    def filter_audio(self, audio_buffer, lowcut=40, highcut=3000):
        # Narrower bandpass filtering (40Hz to 3000Hz) to reduce harmonics
        b, a = self.butter_bandpass(lowcut, highcut, self.SAMPLE_RATE)
        filtered_audio = lfilter(b, a, audio_buffer)
        return filtered_audio
    #Processing Audio
    def frequency_to_note(self, frequency):
        if frequency <= 0:
            return None
        # Convert frequency to MIDI note number and map to a note name
        note_number = 12 * np.log2(frequency / 440) + 69
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = int((note_number - 12) / 12)
        note_idx = int(round(note_number)) % 12
        # Include octave number for better identification
        return f"{notes[note_idx]}{octave}"
    #Processing Audio
    def identify_chord(self, notes, include_octave=False):
        if not notes or len(notes) < 2:
            return "No chord detected"

        # Extract base notes without octaves for chord identification
        if include_octave:
            base_notes = [note[:-1] if note and len(note) > 1 and note[-1].isdigit() else note for note in notes]
        else:
            base_notes = notes

        chord_types = {
            'Major': [0, 4, 7],
            'Minor': [0, 3, 7],
            'Diminished': [0, 3, 6],
            'Augmented': [0, 4, 8],
            'Sus2': [0, 2, 7],
            'Sus4': [0, 5, 7],
            '7': [0, 4, 7, 10],
            'Maj7': [0, 4, 7, 11],
            'm7': [0, 3, 7, 10],
            'm7b5': [0, 3, 6, 10],
            '6': [0, 4, 7, 9],
            'm6': [0, 3, 7, 9],
        }
        note_values = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
                       'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}

        numeric_notes = [note_values[note] for note in base_notes if note in note_values]
        if not numeric_notes:
            return "Unknown chord"

        best_match = None
        best_score = 0
        for root in numeric_notes:
            normalized_notes = sorted(list(set([(n - root) % 12 for n in numeric_notes])))
            for chord_name, pattern in chord_types.items():
                common = set(normalized_notes) & set(pattern)
                pattern_coverage = len(common) / len(pattern)
                chord_coverage = len(common) / len(normalized_notes) if normalized_notes else 0
                score = pattern_coverage * 0.7 + chord_coverage * 0.3
                if pattern_coverage >= 0.7 and score > best_score:
                    best_score = score
                    root_note = list(note_values.keys())[list(note_values.values()).index(root)]
                    best_match = f"{root_note} {chord_name}"

        return best_match if best_match else "Unknown chord"
    #Processing Audio
    def yin_pitch(self, signal):
        tau_min = int(self.SAMPLE_RATE / 3000)  # Highest frequency (3000Hz)
        tau_max = int(self.SAMPLE_RATE / 40)    # Lowest frequency (40Hz)
        # Compute difference function
        diff = np.array([np.sum((signal[:len(signal)-tau] - signal[tau:])**2)
                         for tau in range(tau_min, tau_max)])
        # Cumulative mean normalized difference function
        cmndf = np.zeros_like(diff)
        cmndf[0] = 1
        running_sum = 0.0
        for tau in range(1, len(diff)):
            running_sum += diff[tau]
            cmndf[tau] = diff[tau] * (tau + 1) / running_sum if running_sum != 0 else 1

        # Lower threshold for better detection
        yin_threshold = 0.15
        candidates = np.where(cmndf < yin_threshold)[0]
        if candidates.size:
            tau = candidates[0] + tau_min
            return self.SAMPLE_RATE / tau
        else:
            return None
    #Processing Audio
    def process_audio(self, audio_data, sample_rate=None, is_live=True, time_position=0):
        if sample_rate is None:
            sample_rate = self.SAMPLE_RATE
    
        try:
            # Convert to mono if stereo
            if len(audio_data.shape) > 1 and audio_data.shape[1] > 1:
                audio_data = audio_data[:, 0]
    
            # Check if audio is silent using RMS
            rms = np.sqrt(np.mean(audio_data**2))
            if rms < self.NOISE_THRESHOLD:
                result = {"notes": [], "chord": "No notes", "confidence": 0}
                if is_live and self.app.gui_components.result_label.winfo_exists():
                    self.app.root.after(0, lambda: self.app.gui_components.result_label.config(text="No notes"))
                    self.app.log_manager.add_to_log("Live Detection - No notes detected")
                return result
    
            # Apply more aggressive bandpass filtering to reduce subtones
            filtered_audio = self.filter_audio(audio_data, lowcut=55, highcut=2500)
    
            # Enhanced FFT-Based Pitch Detection
            n = len(filtered_audio)
            windowed_audio = filtered_audio * np.blackman(n)
            fft_data = np.fft.rfft(windowed_audio)
            magnitude = np.abs(fft_data)
            freqs = np.fft.rfftfreq(n, 1/sample_rate)
    
            noise_floor = np.percentile(magnitude, 75)
            max_magnitude = np.max(magnitude)
    
            if max_magnitude < self.NOISE_THRESHOLD * 3:
                result = {"notes": [], "chord": "No notes", "confidence": 0}
                if is_live and self.app.gui_components.result_label.winfo_exists():
                    self.app.root.after(0, lambda: self.app.gui_components.result_label.config(text="No notes"))
                    self.app.log_manager.add_to_log("Live Detection - No notes detected")
                return result
    
            peak_threshold = max(noise_floor * 8, max_magnitude * 0.35)
            min_peak_distance = int(30 * (n / sample_rate))
            peaks, _ = find_peaks(magnitude, height=peak_threshold, distance=min_peak_distance)
    
            detected_notes = []
            confidence_score = 0
    
            if len(peaks) > 0:
                peak_freqs = freqs[peaks]
                peak_amps = magnitude[peaks]
    
                sorted_indices = np.argsort(peak_amps)[::-1]
                peak_freqs = peak_freqs[sorted_indices]
                peak_amps = peak_amps[sorted_indices]
    
                valid_peaks = [(f, a) for f, a in zip(peak_freqs, peak_amps) if 55 <= f <= 2500]
    
                if valid_peaks:
                    peak_freqs, peak_amps = zip(*valid_peaks)
                    max_amp = peak_amps[0]
                    norm_amps = [amp/max_amp for amp in peak_amps]
    
                    fundamentals = []
                    harmonic_relations = {}
                    harmonic_tolerance = 0.02
    
                    for i, freq in enumerate(peak_freqs):
                        if norm_amps[i] < 0.15:
                            continue
                        is_harmonic = False
                        for fund in fundamentals:
                            harmonic_ratio = freq / fund
                            if abs(harmonic_ratio - round(harmonic_ratio)) < harmonic_tolerance and harmonic_ratio > 1.2:
                                if fund not in harmonic_relations:
                                    harmonic_relations[fund] = []
                                harmonic_relations[fund].append((freq, norm_amps[i], round(harmonic_ratio)))
                                is_harmonic = True
                                break
                        if not is_harmonic:
                            fundamentals.append(freq)
    
                    ranked_fundamentals = []
                    for fund in fundamentals:
                        fund_amp = next((a for f, a in zip(peak_freqs, norm_amps) if abs(f - fund) < 5), 0)
                        harmonic_bonus = 0.3 if fund in harmonic_relations else 0
                        prominence = fund_amp + harmonic_bonus
                        ranked_fundamentals.append((fund, prominence))
    
                    ranked_fundamentals.sort(key=lambda x: x[1], reverse=True)
                    top_fundamentals = [f for f, _ in ranked_fundamentals[:3]]
    
                    for freq in sorted(top_fundamentals):
                        note = self.frequency_to_note(freq)
                        if note and note not in detected_notes:
                            detected_notes.append(note)
    
                    if ranked_fundamentals:
                        if len(ranked_fundamentals) <= 3:
                            confidence_score = 90
                        else:
                            top_strength = sum(p for _, p in ranked_fundamentals[:3])
                            all_strength = sum(p for _, p in ranked_fundamentals)
                            confidence_score = min(top_strength / all_strength * 100, 100)
    
                # Use YIN fallback
                if len(detected_notes) == 0 and is_live:
                    yin_estimate = self.yin_pitch(filtered_audio)
                    if yin_estimate is not None:
                        yin_note = self.frequency_to_note(yin_estimate)
                        detected_notes = [yin_note]
                        confidence_score = 70
    
            if is_live:
                if not hasattr(self, 'note_history'):
                    self.note_history = []
                    self.detected_chords_history = []
    
                self.note_history.append(detected_notes)
                if len(self.note_history) > 3:
                    self.note_history.pop(0)
    
                if len(self.note_history) >= 2:
                    stable_notes = []
                    for note in detected_notes:
                        if any(note in frame for frame in self.note_history[:-1]):
                            stable_notes.append(note)
                    if stable_notes:
                        detected_notes = stable_notes
    
            if detected_notes and len(detected_notes) >= 2:
                base_notes = [note[:-1] if note and len(note) > 1 and note[-1].isdigit() else note for note in detected_notes]
                chord = self.identify_chord(base_notes)
    
                if is_live:
                    self.detected_chords_history.append(chord)
                    if len(self.detected_chords_history) > 3:
                        self.detected_chords_history.pop(0)
                    chord_counts = Counter(self.detected_chords_history)
                    most_common_chord = chord_counts.most_common(1)
                    if most_common_chord and most_common_chord[0][1] >= 2:
                        chord = most_common_chord[0][0]
            elif detected_notes and len(detected_notes) == 1:
                chord = f"{detected_notes[0][:-1]} note"
            else:
                chord = "No chord detected"
    
            result = {
                "notes": detected_notes,
                "chord": chord,
                "confidence": confidence_score
            }
    
            if is_live:
                if detected_notes:
                    result_text = f"Notes: {', '.join(detected_notes)}\nChord: {chord}"
                    log_text = f"Live Detection - Notes: {', '.join(detected_notes)} - Chord: {chord}"
                else:
                    result_text = "No notes"
                    log_text = "Live Detection - No notes detected"
    
                self.app.root.after(0, lambda: self.app.gui_components.result_label.config(text=result_text))
                self.app.log_manager.add_to_log(log_text)
            else:
                # File mode
                result["time_position"] = time_position
                result["detected_at"] = time.strftime("%H:%M:%S")
                if detected_notes:
                    self.app.log_manager.add_to_log(
                        f"File Analysis at {round(time_position, 2)}s - Notes: {', '.join(detected_notes)} - Chord: {chord}"
                    )
                else:
                    self.app.log_manager.add_to_log(
                        f"File Analysis at {round(time_position, 2)}s - No notes detected"
                    )
    
            return result
    
        except Exception as e:
            print(f"Processing error: {traceback.format_exc()}")
            if is_live:
                self.app.root.after(0, lambda: self.app.gui_components.result_label.config(text=f"Error: {str(e)}"))
            return {"notes": [], "chord": "Error", "confidence": 0, "error": str(e)}
    