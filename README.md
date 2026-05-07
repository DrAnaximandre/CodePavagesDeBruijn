# Readme:
A simple implementation of the deBuijn method for non periodic tilings of the plane.

Bruijn, de, N. G. (1981). Algebraic theory of Penrose's non-periodic tilings of the plane.
Indagationes Mathematicae, 43(1), 39-66.

See also
  https://github.com/neozhaoliang/pywonderland/blob/master/src/aperiodic-tilings/debruijn.py
  for another implementation, much more "professional" and pythonic,
  but with a different display style.

 Another valuable site : https://www.mathpages.com/home/kmath621/kmath621.htm


## Preferred installation 

```
source .venv/bin/activate
pip install -r requirements.txt
```


## Usage

To run the script, use the following command:

```sh
python main.py -c <config_file_path> -g <function_name>
```

### Arguments
- `-c`, `--config`: Path to the configuration file (default: `configs/config_polo.json`).
- `-g`, `--go`: Name of the function to run (default: `goAllDefaults`).
- `-N`, `--N`: lenght of gamma (default: `5`).

### Example

To run the script with a different configuration file and function, use the following command:

```sh
python main.py -c configs/config_mike.json -g goVerySmall
```

## The demo

The following code:
```sh
python main.py -g goDemo
``` 
returns the following graph:


![Example Glyph](images/go_demo.png)


## Glyphs

An example of function calling is:

```sh
python main.py -g goGlyphs
```

This will read the default config file. With a little trial and error, one can get this kind of graphs:


![Example Glyph](images/example_glyphs_2.png)
![Example Glyph](images/example_glyphs_1.png)

## Neighbours

### Neighbours, descriptions and parameters

Building on the precedent stream of work, the graph is extracted from the tiling.
For each vertex of the graph, one draws a polygon that join, for each edge from the vertex, a point on this edge at distance `k` from the vertex.

By default, edges between the polygons are plotted.
This can be changed with the `"draw_edges"` key in the config file.

By default, the distance `k` is 0.333. 
This can be changed with the `"k"` key in the config file.

See `go_neighbours.py` for implementation details.

### Examples

An example of function calling is:

```sh
python main.py -g goNeighbours -c configs/config_polo_neighbours.json
```

![Example neighbours](images/example_neighbours_1.png)

Note that on the example above, there is no edge between the polygons.
This is because in the config called, the key `"draw_edges"` is at `"False"`.


One can also change the N via command line, for example:

```sh
python main.py -g goNeighbours -N 6 
```

![Example neighbours](images/example_neighbours_2.png)

Supports alpha modification per polygon.

## Splines
Does not work yet. See `go_splines.py`.

## Zoomed Neighbours

Experimental.
Generate three files: 
  - one large png figure inspired by  the Neighbours stream of work above
  - one other png that represent the first image where some zooming inserts are diplayed
  - a `.tif` file that can be used to print the second png


This stream of work is intented to show a disjoint graph at high DMAX (50+) and potentially high N (10+).
The figure is saved at a first `dpi` that can also be high (2000+). Increasing that number will lead to a bigger first png, but the second image will not show the pixelisation produced by the demo.

The demo be started with `python main.py -g goZoomedNeighbours -N 5 -c configs/config_polo_zoomed_neighbours_demo.json`

![Example zoomed neighbours](images/example_zoomed_neighbours.png)

