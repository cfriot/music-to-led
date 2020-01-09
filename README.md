<!--

  # README AND DOC
    - Faire un helper imprimable sur piano
    - Bel exemple réel en gif
    OK # - Update de la doc pour fiter aux derniers changements

  # VISUAL LANGUAGE
    OK # - définir chaque entitée et stabiliser en fonction

  # BLESSED  GUI
    OK -- Terminer le print de pixels en ajoutant les splits sur pixels
    OK -- encadrer
    OK -- gérer multiline
    OK -- gérer physicalshape
    OK -- gérer inférieur à min_width et resize

  # FINIR MAIN
    OK # Faire le nouveau fichier de conf
    OK # --with-config :  lance le programme suivant le config à lemplacement donné
    OK # Faire le systeme de states
    OK # permettre une modification rapide d'un state
    - Make State system work properly

  # STRESS TEST
   -- macbook
   -- raspi

# OPTIONAL

    # - voir pour mieux gérer les refresh en cas de resize
    # - Courbes d'acceleration sur les propagations type scroll
    # - Permettre l'utilisation sur clavier d'ordi histoire de test
    # Rendre midi et audio inputs comme serial, si port non existant, tentative de connection permanente

    # dmx_lights:
    #   -
    #     name: ""
    #     serial_port_name: ""
    #     number_of_channels: 512

    # SUPER OPTIONNEL
    # Rendre le fire generic à color et speed ?
    # Faire un meteor ?

 -->

<p align="center">
  <a href="https://github.com/tfrere/music-2-led" title="haxe.org"><img src="images/logo.svg" width="400"></a>
</p>
<p align="center">
<a href="https://github.com/tfrere/music-2-led#licence"><img src="https://img.shields.io/badge/licence-MIT-green" alt="Licence"></a>
<a href="https://github.com/tfrere/music-2-led"><img src="https://img.shields.io/badge/platform-osx--64%20%7C%20linux--64-lightgrey" alt="Platform support"></a>
<a href="https://github.com/tfrere/music-2-led"><img src="https://img.shields.io/github/last-commit/tfrere/music-2-led" alt="Last update"></a>
<a href="https://github.com/tfrere/music-2-led"><img src="https://img.shields.io/github/v/tag/tfrere/music-2-led" alt="Current version"></a>
</p>

#

**Music 2 Led** is an **open source program** that allows you to create **real-time audio and midi visualizations on led strips** using Arduino and Python. It was designed for **DJ**'s or **music groups** that want to add some **automated lighting effects** to their shows at lowest cost.

All you need is a **computer** *( works on Raspi 4 )*, an **arduino** and a **led strip**.

### Showcase

...

### How it works ?

![software-architecture](images/archi.png)

### What do i need to do to use it ?

1. [Install the program](#python-program)
2. [Build an arduino case](#arduino-part)
3. [Update the CONFIG.yml](#configuration)
4. [Setup your show with the effects and mods documentation](#effects---modes)
5. Enjoy !


# Table of contents
- [Installation](#installation)
  * [Python part](#python-part)
  * [Arduino part](#arduino-part)
- [Configuration](#configuration)
  * [Audio channels](#audio-channels)
    + [Virtual audio sources](#virtual-audio-source)
      - [Linux](#linux)
      - [OSX](#osx)
  * [Midi channels](#midi-channels)
    + [Virtual MIDI sources](#virtual-midi-ports)
  * [CONFIG.yml](#configyml)
    + [Sample config file](#sample-config-file)
- [Effects & Modes](#effects---modes)
  * [Effects](#effects)
    + [Sound based](#sound-based)
    + [Midi based](#midi-based)
    + [Time based](#time-based)
    + [Generic](#generic)
  * [Modes](#modes)
- [Credits](#credits)
- [Contribute](#contribute)
- [License](#license)



# Installation

## Python part

The binary file is [here(DEADLINK)](/toto)

```
./music2led --help

-h, --help            show this help message and exit
-l, --list-devices    list available devices
--test-audio-device TEST_AUDIO_DEVICE
                      Test a given audio port.
--test-midi-device TEST_MIDI_DEVICE
                      Test a given midi port.
--test-serial-device TEST_SERIAL_DEVICE
                      Test a given serial port. This will test your arduino / led installation by
                      displaying three ( red green bue ) pixels and make them roll on the strip.
--test-config-file TEST_CONFIG_FILE
                      Test a given config file.
--single-strip SINGLE_STRIP
                      Launch the first strip without gui and multiprocessing.
                      It's for testing purpose.
--with-config-file WITH_CONFIG_FILE
                      Launch with spectific config file. Default one is
                      CONFIG.yml just near the executable.
```

## Arduino part

As each led project has very specific needs, i kept this part as simple as possible.

In case you need a complete packaged product, there is a more advanced version available in the [Arduino folder](/arduino/). You will find 3d printed arduino cases and a more complete electronic scheme.

The arduino code is [here](arduino/serial-case/serial-case.ino).

PS : For now, please consider not using more than 254 leds by arduino.

![electronic-scheme](images/simple-electronic-scheme.png)

# Configuration

This program will use Audio ports, Midi ports and Serial ports.

To help you to configure your CONFIG.yml correctly, there is a little helper that
will list all available ports for each of them.

```
./music2led --list-devices
```

## Audio channels

This program streams audio from the default audio input device (set by the operating system).

Examples of typical audio sources:
- Audio cable connected to the audio input jack (requires USB sound card on Raspberry Pi)
- Webcam microphone, headset, studio recording microphone, etc

On OSX you have the "Built-In Microphone" as a default choice.

### Virtual audio sources
You can use a "virtual audio device" to transfer audio playback from one application to another. This means that you can play music on your computer and connect the playback directly into the program.

#### Linux
Linux users can use [Jack Audio](http://jackaudio.org/) to create a virtual audio device.

#### OSX
On OSX, [Loopback](https://www.rogueamoeba.com/loopback/) can be use to create a virtual audio device.

## Midi channels

...

### Virtual MIDI Sources

On OSX, it's pretty easy to make some virtual MIDI channels.
Here is an example for using them with ableton live.

![osx-midi-settings](images/osx-midi-settings.png)
![ableton-midi-settings](images/ableton-midi-settings.png)

## CONFIG.yml

You can validate the config file with

```
./music2led --test-config-file "./CONFIG.yml"
```

### Sample config file

```yml


---  # document start

# Desired framerate for all the strips

desirated_framerate: 60

# Display the GUI

display_interface: True

# Audio ports
# List of used audio ports
# Available ports can be listed with --list-devices
# Can be changed with the option "Change audio channel"

audio_ports:
  -
    name: Built-in Microphone
    min_frequency: 200
    max_frequency: 12000

# Strips
# They represents independant Arduino cases

strips:
  -
    # Name of the strip
    # Only used in the GUI

    name: Led strip name

    # Name of the associated serial port
    # Available ports can be found with --list-devices

    serial_port_name: /dev/tty.usbserial-14210

    # Midi channels
    # Can be listed with --list-devices
    # midi_ports_for_visualization : used for midi based visualizers
    # midi_ports_for_changing_mode : used for live changing modes

    midi_ports_for_visualization:
      - USB MIDI Interface
    midi_ports_for_changing_mode:
      - LPK25

    # Default state that have to be used on start up

    active_state_index: 0

    # Physical shape
    # Represents the physical shape of the strip
    # Only used in the GUI

    physical_shape:
      - 254

# States
# These are default states for strips
# They contains all the variables that the visualizer need to run properly

states:
  -
    # Name of the strip
    # Only used in the GUI

    name: "Mirrored Energy light blue"

    # Visualizer function
    # These functions can be found in the documentation below

    active_visualizer_effect: energy

    # The propagation curve is used to determine how scroll propagation will
    # work

    active_propagation_curve: ease_in

    # Default audio channel

    active_audio_channel_index: 0

    # Filters

    audio_channel_min_frequency: 200
    audio_channel_max_frequency: 12000

    # Shapes
    # Represents virtual shape that are used by the visualizer
    # Be sure they not contains odd numbers

    shapes:
      -
        - 50
        - 50

    # Active shape index
    # Determine what shape have to be used

    active_shape_index: 0

    # Available color schemes
    # Can be changed via "Change color scheme" function
    #
    # You can call them using hexadecimal notation or using a real name according
    # to the color list that can be found here ->
    # python-app/helpers/color/colorSchemeFormatter.py

    color_schemes:
      -
        - "#FF0000"
        - "#00FF00"
        - "#0000FF"
      -
        - red
        - green
        - blue

    # Active color scheme index
    # Determine what color scheme have to be used

    active_color_scheme_index: 0


    # Maximum allowed brightness
    # Can be used to limit the power consumption
    # Check the Arduino part readme for more informations about it

    max_brightness: 255

    # Reverse and mirror mods

    is_reverse: false
    is_mirror: false

    # Time interval value that is used in time based visualizers

    time_interval: 120

    # Chunk size used in alternate colors

    chunk_size: 5

...  # document end

```


# Effects & Modes

Music To Led has 16 visualization effects and 8 mods.

They can be live changed via dedicated Midi channels. You can choose to use programs like Ableton Live to automate these changes or use a dedicated synthetiser / pad to change them manually during the show.

**Big principle**
You have to send a midi note signal for activating / modifying effects. The table just after will show you the documentation.

## Effects

All the examples are based on a ["red", "green", "blue"] color scheme.

### Sound based

| *Number* | *Midi Note* | *Effect name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 0 | C-2 | **Scroll** | - | ![scroll](images/scroll.gif)
| 1 | C#-2 | **Energy** | - | ![energy](images/energy.gif)
| 2 | D-2 | **ChannelIntensity** | - | ![intensity](images/intensity.gif)
| 3 | D#-2 | **ChannelFlash** | - | ![spectrum](images/envelope.gif)

### Midi based

| *Number* | *Midi Note* | *Effect name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 5 | F-2   | **PianoScroll** | - | ![scroll](images/piano.gif)
| 6 | F#-2  | **PianoNote** | - | TO ADD
| 7 | G-2   | **PitchwheelFlash** | Color intensity based on pitch bend | ![scroll](images/envelope.gif)
| 8 | G#-2  | - | - | ![scroll](images/nothing.gif)

### Time based

| *Number* | *Midi Note* | *Effect name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 10 | A#-2   | **AlternateColorChunks** | Chunk size based on velocity | ![scroll](images/alternate-chunks.gif)
| 11 | B-2    | **AlternateColorShapes** | - | ![scroll](images/alternate-strips.gif)
| 12 | C-1    | **DrawLine** | - | ![scroll](images/nothing.gif)
| 13 | C#-1   | - | - | ![scroll](images/nothing.gif)

### Generic

| *Number* | *Midi Note* | *Effect name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 15 | D#-1  | **Full** | - | ![scroll](images/full.gif)
| 16 | E-1   | **FadeToNothing** | - | ![scroll](images/nothing.gif)
| 17 | F-1  | **Clear** | - | ![scroll](images/nothing.gif)
| 18 | F#-1  | **Fire** | - | ![scroll](images/fire.gif)

## Modes

| *Number* | *Midi Note* | *Mode name* | *Params* | *Example*
|:--|:--|:--|:--|:--
| 20 | G#-1  | **Toggle reverse mode** | - | ![scroll](images/reverse.gif)
| 21 | A-1  | **Toggle mirror mode** | - | ![scroll](images/mirror.gif)
| 22 | A#-1 | **Change shape** | Update based on velocity | ![scroll](images/shape.gif)
| 23 | B-1 | **Change color scheme** | Update based on velocity | ![scroll](images/color.gif)
| 24 | C-0  | **Change time interval in ms** | Update based on velocity | ![scroll](images/nothing.gif)
| 25 | C#-0  | **Change audio channel** | Update based on velocity | ![scroll](images/nothing.gif)
| 26 | D-0 | **Change max Brightness** | Update based on velocity | ![scroll](images/nothing.gif)
| 27 | D#-0 | **Change chunk size** | Update based on velocity | ![scroll](images/nothing.gif)
| 28 | D#-0 | **Change state** | Update based on velocity | ![scroll](images/nothing.gif)


# Credits
This project was a fork of the great [audio-reactive-led-strip](https://github.com/scottlawsonbc/audio-reactive-led-strip). A lot of code has been rewritten since the beginning but it still remains some of the visualizers and audio processing code.

# Contribute
If you have any idea to improve this project or any problem using this, please feel free to upload an [issue](https://github.com/tfrere/music-to-led/issues).

# Future Roadmap

By priority order

- Handle more than the WS2812B led strip
- DMX handling
- Effect mixer
- Electron interface
- Rewrite audio acquisition part
- Beat detection with Aubio

# License
This project was developed by Thibaud FRERE and is released
under the MIT License.
