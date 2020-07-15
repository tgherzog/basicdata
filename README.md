
## Background ##

This repository contains a handful of datasets I use quite frequently--population,
area and perhaps some others--typically to normalize other data series. Admin1-admin3
are available. Generation scripts are also included as are sources. The data typically
don't need to change more than perhaps once a year, but minor changes to the scripts
are very likely.

### US State Names and Codes ###

This file is maintained by hand. It includes names, FIPS and postal codes
for the 50 states, DC and the 4 major island territories. The level column
can be used to select different feature types.

File Format:

```
fips,code,level,name
```

Hint: some programs will try to convert the fips field to a numeric and you'll lose
the leading 0. Here is a quick fix for pandas, with the only downside being that the 
`level` field is also read as a string:

```
df = pd.read_csv('data/usstates.csv', dtype=str)
```


### Population (latest available year) ###

* Countries: World Bank, https://api.worldbank.org/SP.POP.TOTL
* US States: US Census: https://www2.census.gov/programs-surveys/popest/datasets/
* US Counties: US Census: https://www2.census.gov/programs-surveys/popest/datasets/

File Format:

```
id,name,population[,level-specific fields]
```

Script:  `code/pop.py`

### Surface Area (sq. km, latest available year) ###

* Countries: World Bank, https://data.worldbank.org/indicator/AG.LND.TOTL.K2, https://data.worldbank.org/indicator/AG.SRF.TOTL.K2
* US States: US Census: https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk
* US Counties: US Census: https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk

**NB:** The FactFinder link above provides a user interface to download the state/county data. You need to download it
and extract the CSV to the inputs directory prior to running the build script.

File Format:

```
id,name,surface_area,land_area[,level-specific fields]
```

Script:  `code/area.py`


### Centroids (longitude, latitude) ###

Logical centroids, defined differently at different levels

* Countries: World Bank, https://api.worldbank.org/en/country
* US States: https://www.census.gov/geographies/reference-files/time-series/geo/centers-population.html
* US Counties: https://www.census.gov/geographies/reference-files/time-series/geo/centers-population.html

File Format:

```
id,name,long,lat[,level-specific-fields]
```

Script: `code/centroid.py`
