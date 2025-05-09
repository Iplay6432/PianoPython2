# PianoPython2: The Awaking of Java
This program is a game where the user plays the Piano using a computer keyboard as accurately as possible. It was coding using the Swing/Graphics library in java and the pyglet library in python.


Piano sounds Steinway Model D274 II by GD CRAFT:
https://www.musical-artifacts.com/artifacts/3036

The Class RoundPolygon.java was made by [Roedy Green at Canadian Mind Products](http://mindprod.com) this class was used because java does not have a built in method for a round Rectangle

[![wakatime](https://wakatime.com/badge/user/5e0929d5-6c04-4390-b85f-6ed88b81a995/project/1544bf01-e84d-4ea5-bfb8-c9f39b50d72d.svg)](https://wakatime.com/badge/user/5e0929d5-6c04-4390-b85f-6ed88b81a995/project/1544bf01-e84d-4ea5-bfb8-c9f39b50d72d)

## Requirements
> [!NOTE]  
> If your using the precompiiled version from the realease tabs at least Java 23 is currently required because it was compiled using Java 23
Tested on Python v3.13.1 and Java 23 but should work with the same requirements for pyglet and swing

## Installation
### To Install Using Git
```bash
git clone https://github.com/Iplay6432/PianoPython2.git
cd PianoPython2
pip install -r requirements.txt
```
### To Run and Install via Releases
Download and extract zip file
Double click both the Main.jar and the PianoPythonApp.exe
You are good to play!!
## Running the program
> [!WARNING]  
> All the commands below wont work if you downloaded from the latest release, all you have to do is run both the .jar and .exe files
### On Windows
```bash
./start.bat
```

> [!WARNING]  
> Code was not tested on other operating systems besides Windows 11
### On Mac and Linux
```bash
chmod +x start.sh #do this first time only
./start.sh
```
If neither of these methods work for you try running these two commands in different terminal windows:
```bash
python Main.py # also try python3 if this doesn't work
```
```bash
java Main.java #if this doesn't work try compiling using javac *.java then running again
```
## Controls
- Navigate with arrow keys, enter, and esc
- Escape &rarr; go back / exit (on title screen)
- Keys s-k &rarr; play in current octave, white notes
- Keys e, r, y, u, i &rarr; play in current octave, black notes
- Keys z-m &rarr; play octave below if not at lowest octave, if it is play octave up, white notes
- Keys 2-6 &rarr; play octave below if not at lowest octave, if it is play octave up, black notes
- Space &rarr; move up 1 octave
- Left alt &rarr; move down 1 octave
- When holding shift and using the alternative notes
    - if octave is 3 than it will play notes two octaves up
    - if octave is 4 than it will play notes an octave up
    - if octave is 5 it will play notes 2 octaves down

## How It Works (Example):
### SettingPanel.java
This Panel holds all the settings and process and saves the data
#### Method Header
```java
public class SettingPanel extends JPanel
```
#### Constructor
Creates a SettingPanel object where the Dimensions of the Screen are supplied. It also creates the different settings and attaches them to the Panel
```java
public SettingPanel(Dimension d)
```

#### Data Fields
```java
private int numOfSettings = 8;
private int state = 0;
private Setting[] settings = new Setting[numOfSettings];
```
#### Methods
```java
public String getState() // returns  the state
```
```java
public void setState(String s) // sets the state
```
#### Focus Class
```java 
private class Focus implements FocusListener
```
##### Methods
```java
public void focusGained(java.awt.event.FocusEvent e) /* method executes when ever focus 
of the panel was lost */
```
```java
public void focusLost(java.awt.event.FocusEvent e) /* runs when ever focus is lost
this method requests focus after it is lost to fix a bug */
```

#### Key Class
```java
private class Key extends KeyAdapter
```
##### Methods
```java
public void keyPressed(KeyEvent e) /* runs whenever a key is pressed, 
if the key is "esc" than asks user if they want to save 
the data and returns to title screen */
```


