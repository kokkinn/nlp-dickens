# NLP task for I.I. Mechnikova Programming Course

## Task Description

For this text https://www.online-literature.com/dickens/2941/

1. Count how many times the transition from one word to another occurred within sentences, and print the first 100 most
   common transitions.
2. Build a directed graph in SVG that shows transitions of words within a sentence. At each transition, indicate how
   many times the transition from the first word to the second occurred in the text (you may need to install the
   GraphViz package)
3. Generate 100 random sentences in the style of the selected text. Sentences must begin with a capitalized word and end
   with a period or an exclamation or question mark.
4. Optionally, make sure that the frequency of generated phrases corresponds to their frequency in the text.

## About

A tool is a class with options of pseudo generating text, displaying data in graph and bar variant.

## Getting started

### Requirements

* Python 3.10 +
* PIP package manager

### Setting Up

From the root directory create a new virtual environment, typically with

```shell
python3 -m venv venv
```

Get inside it:

```shell
source venv/bin/acticate
```

From directory of ```requirements.txt``` file (root of project), install dependencies:

```shell
pip install -r requirements.txt
```

### Run the app

Execute the ```main.py``` file

```shell
python3 -m src.main
```

All the results will be stored into ```results/``` directory

### Visualisation examples

![example1](readme_data/graph_example_1.png)
![example2](readme_data/graph_preview_2.png)
![example2](readme_data/graph_example_3.png)
![example2](readme_data/bar_chart_example_1.png)

### Text generation example

`A fixed look for the door with a dripping wet stains stealing down. The bottom with you will happen how my own mind sir. The tunnel i felt myself placed my level some two occasions? However be called learning it me plainly now sir he had been as soon with the cutting was! My head and i left arm? She is very words if i saw the company without any other? However be nothing came back both ways all that for me on the low voice in an arm is. The place as one else yesterday evening when i stepped back to. He stirred i was near the eye were on wiping the. I shut up flag as the train passed and.`