from midi2audio import FluidSynth
import os


def is_fsynth_installed():
    """Check to make sure fluidsynth exists in the PATH"""
    for path in os.environ["PATH"].split(os.pathsep):
        f = os.path.join(path, "fluidsynth")
        if os.path.exists(f) and os.access(f, os.X_OK):
            return True

    return False


print(is_fsynth_installed())
cwd = os.getcwd()
# sound font file https://www.musical-artifacts.com/artifacts/3036
filenames = []
fs = FluidSynth(sound_font="sf.sf2")
for file in os.listdir():
    if file.endswith("mid"):
        print(file)
        os.system(
            f"fluidsynth -F {file.replace(".mid", ".wav")} -r 44100 sf.sf2 {file}"
        )  # defintly best code practices!!!
