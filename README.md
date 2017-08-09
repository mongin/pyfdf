# pyfdf
An isometric topographic visualisation and generation toy project, written in python.

![a small mountain over lakes](https://github.com/mongin/pyfdf/blob/master/images/2.png?raw=true)

![a small mountain over lakes](https://github.com/mongin/pyfdf/blob/master/images/4.png?raw=true)

This project offer a vizualizer, `pyfdf.py`, taking as input json-formatted map files, and render them inside a graphical window. The rendering can also be saved to images files, in jpeg, bmp or png format. Map files are generated by a different script, `map_generator.py`, using the improved perlin noise algorithm.

The vizualizer depends on the `pygame` package for image rendering. `pip install pygame` should be all that is needed. The map generator use numpy. If your distribution of python doesn't have it by default, you should install it too.

Usage for the vizualizer:
```
./pyfdf.py -m <map>
```
A few maps are available in the `maps` folder. Note that `hill.json` was done using a bugged version of perlin noise during development.

Usage for the map generator:
```
./map_generator.py > map_file.json
```

There is many more options for the generator and the vizualizer, and a configuration file. Full doc is coming :)