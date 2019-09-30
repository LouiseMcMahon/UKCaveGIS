# UK Caves GIS
The aim of this project is to provide GIS files for each caving region which contain the entrances of every known cave programtically.

The aim is to provide:

* KML
* JSON
* GPX

For the following registrys:
- [x] [Derbyshire](https://registry.thedca.org.uk/])
- [ ] [North Yorkshire](https://cncc.org.uk/caving/caves/index.php?keyword=&sort=last_updated%20DESC)
- [ ] [Wales and related areas](http://www.cambriancavingcouncil.org.uk/registry/ccr_registry.php?reg=All+Wales+and+the+Marches&nam=)
- [x] [Mendip](http://www.mcra.org.uk/registry/)
- [x] [Scotland](http://registry.gsg.org.uk/sr/registrysearch.php)
- [ ] [Ireland](http://www.ubss.org.uk/search_irishcaves.php)

# Download
To download the output from this repository go to the releases page and download the KML or JSON file for the region you are interested in.

## Accuracy
All efforts have been made to ensure accuracy of the output files but not every registry entry is acurate to begin with. Not every registry entry lists WGS84 or NGR which means it has to be derived from the other if availaible which can introduce an error. If you chose to use this data for navigation its not my fault if you end up wandering around on leck fell lost in the mist!

# Developing
Pull requests welcome but please read the contribution guidelines first [here](.github/contributing.md)

The tool is written in python 3.4 using [scrapy](https://scrapy.org/) the output is released by commits to master via travis CI
Docker is used manage the python enviroment.

## Running
1. First build the docker image `docker-compose build`
1. Then run the spiders with `docker-compose up`

To run scrapy commands run `docker-compose run scrapy scrapy <command>`.

To have access to the containers shell run `docker-compose run scrapy /bin/bash`

You may need to reset the owner and permissions of files created by docker/scrapy using `sudo chmod` & `sudo chown`
