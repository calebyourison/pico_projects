from machine import Pin, PWM

from time import sleep



buzzer_pin = 15
button_pin = 16

buzzer_object = PWM(Pin(buzzer_pin))
button = Pin(button_pin, Pin.IN, Pin.PULL_UP)

# Estimated frequencies of common notes
notes = {
    "C0": 16, "C#0": 17, "Db0": 17, "D0": 18, "D#0": 19, "Eb0": 19,
    "E0": 21, "F0": 22, "F#0": 23, "Gb0": 23, "G0": 25, "G#0": 26,
    "Ab0": 26, "A0": 28, "A#0": 29, "Bb0": 29, "B0": 31,

    "C1": 33, "C#1": 35, "Db1": 35, "D1": 37, "D#1": 39, "Eb1": 39,
    "E1": 41, "F1": 44, "F#1": 46, "Gb1": 46, "G1": 49, "G#1": 52,
    "Ab1": 52, "A1": 55, "A#1": 58, "Bb1": 58, "B1": 62,

    "C2": 65, "C#2": 69, "Db2": 69, "D2": 73, "D#2": 78, "Eb2": 78,
    "E2": 82, "F2": 87, "F#2": 93, "Gb2": 93, "G2": 98, "G#2": 104,
    "Ab2": 104, "A2": 110, "A#2": 117, "Bb2": 117, "B2": 123,

    "C3": 131, "C#3": 139, "Db3": 139, "D3": 147, "D#3": 156, "Eb3": 156,
    "E3": 165, "F3": 175, "F#3": 185, "Gb3": 185, "G3": 196, "G#3": 208,
    "Ab3": 208, "A3": 220, "A#3": 233, "Bb3": 233, "B3": 247,

    "C4": 262, "C#4": 277, "Db4": 277, "D4": 294, "D#4": 311, "Eb4": 311,
    "E4": 330, "F4": 349, "F#4": 370, "Gb4": 370, "G4": 392, "G#4": 415,
    "Ab4": 415, "A4": 440, "A#4": 466, "Bb4": 466, "B4": 494,

    "C5": 523, "C#5": 554, "Db5": 554, "D5": 587, "D#5": 622, "Eb5": 622,
    "E5": 659, "F5": 698, "F#5": 740, "Gb5": 740, "G5": 784, "G#5": 830,
    "Ab5": 830, "A5": 880, "A#5": 932, "Bb5": 932, "B5": 988,

    "C6": 1047, "C#6": 1109, "Db6": 1109, "D6": 1175, "D#6": 1245, "Eb6": 1245,
    "E6": 1319, "F6": 1397, "F#6": 1480, "Gb6": 1480, "G6": 1568, "G#6": 1661,
    "Ab6": 1661, "A6": 1760, "A#6": 1865, "Bb6": 1865, "B6": 1976,

    "C7": 2093, "C#7": 2217, "Db7": 2217, "D7": 2349, "D#7": 2489, "Eb7": 2489,
    "E7": 2637, "F7": 2794, "F#7": 2960, "Gb7": 2960, "G7": 3136, "G#7": 3322,
    "Ab7": 3322, "A7": 3520, "A#7": 3729, "Bb7": 3729, "B7": 3951,

    "C8": 4186
}


def play_note(buzzer: PWM, frequency: int, sound_duration: float, rest_duration: float) -> None:
    """Emit sound from buzzer at given frequency for given duration followed by defined period of rest"""

    buzzer.duty_u16(int(65536 * 0.2))

    buzzer.freq(frequency)

    sleep(sound_duration)

    buzzer.duty_u16(int(65536 * 0))

    sleep(rest_duration)


def convert_note_values(note: tuple[str, float, float], bpm: int = 60, octave_shift: int | float | None = None) -> \
tuple[int, float, float]:
    """
    Convert string name to frequency, convert note and rest values to seconds based on BPM

    Assumes a quarter note/rest is one second in length given 60 BPM

    Octave shift in either direction +/- values
    """
    note_name, note_length, rest_length = note

    frequency = notes.get(note_name, 5000)  # Likely a discordant note if not properly defined name

    # Each single octave shift essentially doubles or halves the frequency
    if octave_shift:
        frequency *= 2 ** octave_shift
        # Final value must be a whole number
        frequency = round(frequency)

    note_length_seconds = (60 / bpm) * 4 * note_length

    rest_length_seconds = (60 / bpm) * 4 * rest_length

    return frequency, note_length_seconds, rest_length_seconds


def play_song(song: list[tuple[str, float, float]], bpm: int = 60, octave_shift: int | float | None = None) -> None:
    """Play a simple melody given a list of notes, durations, and rests.  Increase tempo and modify pitch if designated"""

    converted_song_values = [convert_note_values(note=note, bpm=bpm, octave_shift=octave_shift) for note in song]

    for (freq, duration, rest) in converted_song_values:
        play_note(buzzer=buzzer_object, frequency=freq, sound_duration=duration, rest_duration=rest)


daisy_bell = [
    # Dai-sy
    ("G6", 0.75, 0),
    ("E6", 0.75, 0),
    # Dai-sy
    ("C6", 0.75, 0),
    ("A5", 0.5, 0.25),  # Quarter Rest
    # Give
    ("A5", 0.25, 0),
    # Me
    ("B5", 0.25, 0),
    # Your
    ("C6", 0.25, 0),
    # An-swer
    ("A5", 0.5, 0),
    ("C6", 0.25, 0),
    # Do
    ("G5", 1.25, 0.25),  # Quarter Rest

    # I'm
    ("C6", 0.75, 0),
    # Half
    ("G6", 0.75, 0),
    # Cra-zy
    ("E6", 0.75, 0),
    ("C6", 0.5, 0),
    # All
    ("A5", 0.25, 0),
    # For
    ("B5", 0.25, 0),
    # The
    ("C6", 0.25, 0),
    # Love
    ("D6", 0.5, 0),
    # Of
    ("E6", 0.25, 0),
    # You
    ("D6", 1.0, 0.25),  # Quarter Rest

    # It
    ("E6", 0.25, 0),
    # Won't
    ("F6", 0.25, 0),
    # Be
    ("E6", 0.25, 0),
    # A
    ("D6", 0.25, 0),
    # Sty-lish
    ("G6", 0.5, 0),
    ("E6", 0.25, 0),
    # Mar-riage
    ("D6", 0.25, 0),
    ("C6", 1.0, 0),
    # I
    ("D6", 0.25, 0),
    # Can't
    ("E6", 0.5, 0),
    # Af-ford
    ("C6", 0.25, 0),
    ("A5", 0.5, 0),
    # A
    ("C6", 0.25, 0),
    # Car-riage
    ("A5", 0.25, 0),
    ("G5", 0.75, 0.25),  # Quarter Rest

    # But
    ("G5", 0.25, 0),
    # You'll
    ("C6", 0.5, 0),
    # Look
    ("E6", 0.25, 0),
    # Sweet
    ("D6", 0.5, 0.25),  # Should be Half Rest, Quarter sounds more natural
    # On
    ("C6", 0.5, 0),
    # The
    ("E6", 0.25, 0),
    # Seat
    ("D6", 0.25, 0.25),  # Quarter Rest
    # Of
    ("E6", 0.125, 0),
    # A
    ("F6", 0.125, 0),
    # Bi-cy-cle
    ("G6", 0.25, 0),
    ("E6", 0.25, 0),
    ("C6", 0.25, 0),
    # Built
    ("D6", 0.5, 0),
    # For
    ("G5", 0.25, 0),
    # Two
    ("C6", 1.0, 0),
]

close_to_you = [
    # Why
    ("G5", 0.375, 0),
    # Do
    ("B5", 0.375, 0),
    # Birds
    ("G6", 0.25, 0.375),  # Quarter rest x 1.5
    # Sud-den-ly
    ("G6", 0.25, 0),
    ("F6", 0.125, 0),
    ("G6", 0.25, 0),
    # Ap-pear
    ("A6", 0.375, 0),
    ("E6", 0.5, 0.375),  # Quarter rest x 1.5
    # Ev-ry
    ("E6", 0.125, 0),
    ("G6", 0.125, 0),
    # Time
    ("B6", 0.375, 0.625),  # Quarter rest x 1.5 + Quarter Rest
    # You
    ("E6", 0.125, 0),
    # Are
    ("G6", 0.25, 0),
    # Near
    ("C7", 0.75, 0.75),  # Half rest X 1.5

    # Just
    ("G5", 0.25, 0),
    # Like
    ("B5", 0.375, 0),
    # Me
    ("G6", 0.5, 0.375),  # Quarter rest x 1.5
    # They
    ("G5", 0.25, 0),
    # Long
    ("B5", 0.375, 0),
    # To
    ("A6", 0.125, 0),
    # Be
    ("G6", 0.375, 0.375),  # Quarter rest x 1.5
    # Close
    ("G5", 0.25, 0),
    # To
    ("B5", 0.375, 0),
    # You
    ("G6", 1.0, 0.375),  # Quarter rest x 1.5
]

you_are_my_sunshine = [
    # You
    ("G5", 0.25, 0.01),
    # Are
    ("G5", 0.25, 0.01),
    # My
    ("A5", 0.25, 0.01),
    # Sun-shine
    ("B5", 0.5, 0.01),
    ("B5", 0.5, 0.25),  # Quarter Rest
    # My
    ("B5", 0.25, 0.01),
    # On-ly
    ("A5", 0.25, 0.01),
    ("B5", 0.25, 0.01),
    # Sun-shine
    ("G5", 0.5, 0.01),
    ("G5", 0.5, 0.25),  # Quarter Rest

    # You
    ("G5", 0.25, 0.01),
    # Make
    ("A5", 0.25, 0.01),
    # Me
    ("B5", 0.25, 0.01),
    # Hap-py
    ("C6", 0.5, 0.01),
    ("E6", 0.5, 0.25),  # Quarter Rest
    # When
    ("E6", 0.25, 0.01),
    # Skies
    ("D6", 0.25, 0.01),
    # Are
    ("C6", 0.25, 0.01),
    # Grey
    ("B5", 1.0, 0.25),  # Quarter Rest

    # You'll
    ("G5", 0.25, 0.01),
    # Ne-ver
    ("A5", 0.25, 0.01),
    ("B5", 0.25, 0.01),
    # Know
    ("C6", 0.5, 0.01),
    # Dear
    ("E6", 0.5, 0.25),  # Quarter Rest
    # How
    ("E6", 0.25, 0.01),
    # Much
    ("D6", 0.25, 0.01),
    # I
    ("C6", 0.25, 0.01),
    # Love
    ("B5", 0.5, 0.01),
    # You
    ("G5", 0.5, 0.5),  # Half Rest

    # Please
    ("G5", 0.25, 0.01),
    # Don't
    ("A5", 0.25, 0.01),
    # Take
    ("B5", 0.75, 0.01),
    # My
    ("C6", 0.25, 0.01),
    # Sun-shine
    ("A5", 0.5, 0.01),
    ("A5", 0.25, 0.01),
    # A-way
    ("B5", 0.25, 0.01),
    ("G5", 1.0, 0.25)  # Quarter Rest

]



songs = [
    (you_are_my_sunshine, 210, -0.5),
    (daisy_bell, 240, -1),
    (close_to_you, 150, -1.5)
]

# Start from the first song
song_index = 0

while True:

    if button.value() == 0:  # Button pressed

        selected_song = songs[song_index]
        play_song(song=selected_song[0], bpm=selected_song[1], octave_shift=selected_song[2])
        song_index = (song_index + 1) % len(songs)  # start over
