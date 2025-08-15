import os
import numpy as np
from scipy.io.wavfile import write

# Ensure directory exists
output_dir = "assets/sounds"
os.makedirs(output_dir, exist_ok=True)

def make_crash_sound():
    """Generates a crash sound and saves it as 'crash.wav'."""
    print("Generating crash sound...")
    sample_rate = 44100
    duration = 0.6
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    noise = np.random.normal(0, 1, t.shape) * np.exp(-6 * t)
    audio = np.int16(noise / np.max(np.abs(noise)) * 32767)
    output_path = os.path.join(output_dir, "crash.wav")
    write(output_path, sample_rate, audio)
    print(f"✅ crash.wav saved to: {output_path}")

def make_laser_sound():
    """Generates a laser sound and saves it as 'laser.wav'."""
    duration = 0.2
    sample_rate = 44100
    start_freq = 1200
    end_freq = 400
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequencies = np.logspace(np.log10(start_freq), np.log10(end_freq), t.size)
    wave = np.sin(2 * np.pi * frequencies * t)
    envelope = np.exp(-10 * t)
    wave *= envelope
    audio = np.int16(wave / np.max(np.abs(wave)) * 32767)
    write(os.path.join(output_dir, "laser.wav"), sample_rate, audio)
    print("✅ laser.wav created!")

def make_explosion_sound():
    """Generates an explosion sound and saves it as 'explosion.wav'."""
    sample_rate = 44100
    duration = 0.8
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    base_freq = 60
    rumble = np.sin(2 * np.pi * base_freq * t)
    noise = np.random.normal(0, 0.5, size=t.shape)
    explosion_wave = rumble + noise
    envelope = np.exp(-4 * t)
    explosion_wave *= envelope
    audio = np.int16(explosion_wave / np.max(np.abs(explosion_wave)) * 32767)
    write(os.path.join(output_dir, "explosion.wav"), sample_rate, audio)
    print("✅ explosion.wav created!")

# ✅ Call functions only after they're defined
if __name__ == "__main__":
    make_laser_sound()
    make_explosion_sound()
    make_crash_sound()
