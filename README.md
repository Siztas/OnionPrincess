# OnionPrincess
This repository is created for the development and collaboration for our 2D RPG Game Codename:OnionPrincess.

## Environment
Python v3.10

Pygame v2.4.0

Numpy v1.23.5

SciPy v1.10.1

PyAudio v0.2.13

Librosa v0.10.0post2


## Code Structure
Main: Main is the base layer for the code to run on, and the game runs on the Game class in Main. The Game class method run reads into the message queue, which provides the basis for the response to events triggered by the keyboard and mouse in the game. 

Level:Level class establishes the hierarchy for switching between multiple maps, and although this hierarchy of multiple containers becomes less significant later in development, Level class was originally developed as a container to enable map switching. The main role of the Level class is to build the map, and the YSortCameraGroup class is called when the Level class is initialised to lay down the map's underlying png map and render the fine structure, although this function was deprecated later in development and replaced by a pre-rendered base map.

Player,Interaction,UI,Enemy,..: These classes are entities that need to be generated on the map during the course of the game or interfaces that need to be rendered, actions, etc. They in fact have a short life cycle or are isolated from the rest of the code.

support,encode,SkeletonMatch,..:These code doesn't actually work on any part of the game, they only play a supporting role, such as the import_folder method in support, which is only used to simplify the step of reading in data, and there are methods written just to facilitate data handling during development (and, apparently, forgetting to remove

To summarize, the code starts from the Game class and enters the command loop, passing the queue of keyboard and mouse operation messages read into Level or responding directly in the Game class. there is always one and only one Level and Player in the Game class, and the event responses for the incoming operations and in-game values are assigned in the Level class. Events such as monster alerts, attacks, deaths etc. are also handled by Level. Game.level will only be re-instantiated when the map is switched, when the archive is read, when a new map and environment is created, and when you die or are transported to a new map.

## Data Structure Usage
Sparse matrix compression by CSR
Use the values, rows and columns arrays to store the location of non--1 values.This speeds up map reading considerably.

Huffman Code
Huffman coding was used for the storage of the archive, an idea that originated from a plan to map an 01 string by short vs. long signals into a wav audio file as an archive, a method that was implemented in bin_to_wav, but the idea was not implemented as the wav playback was far less effective.

KDTree
KDTree is a data structure that organises points in k-dimensional Euclidean space, in this case we use a 2-D Tree, for performing a nearest neighbour search of the input graph with multiple graphs to be matched. It has a structure similar to a balanced binary search tree, and the time complexity of a fold-and-half query is O(log n), which is just right for the requirements.

KMP
（Abandoned）
Rather than using kmp directly, here we take advantage of the idea that kmp keeps the sequence to be matched constant without receding, which matches the real-time incoming we need for audio processing. Using a sliding window, we perform a continuous prefix match of the sequence to be matched against the matching sequence, moving the matching string slightly forward after the match, continuing with the next segment of the matching string, recording the minimum Hemming distance after the mismatch, and returning the minimum Hemming distance during the period as the result of the match at the end of the input or when the Hemming distance is low enough.
(This algorithm has been abandoned due to the time consuming hash algorithm, resulting in the real-time audio not being recognized properly; 6.8,lzc)

## Run
Go to main.py and then have fun!
