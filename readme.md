
Real time subtitles
======


Real time subtitles is for events or conferences with audio or video screenings where translations are prepared as text but not yet time coded or embedded to video.
This application provides functionality for real time syncking and overlaying of subtitles on video screening.

Features:
-------

* Two windows:
  * control window with context view: current subtitle highlighted in the context of previous and upcoming subtitle lines
  * subtitle window which may be overlayed to the bottom of video playing in separate player
* keyboard control forward, backward stepping in subtitle queue, toggling on/off overlay window visibility
* jump to defined subtitle line
* settings for size, color and positioning of overlaying subtitles window

Subtitle files preparation
-------

* encoding: unicode 7 Utf-8 text files with end lines with LF only
* lines separated with line feed (LF)  line breaks

Requirements
-------
* Python 2.7
* PyQt 5

Perhaps easiest to get it running is to install Anaconda python distribution


Potential issue with anaconda and windows:
If error: application failed because could not load qt platform plugin "windows"
 https://github.com/ContinuumIO/anaconda-issues/issues/1270
fix:  "COPY the Continuum\Anaconda3\Library\plugins\platforms
folder to Continuum\Anaconda3
