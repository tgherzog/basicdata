
## Background ##

This repository contains a handful of datasets I use quite frequently--population,
area and perhaps some others--typically to normalize other data series. Admin1-admin3
are available. Generation scripts are also included as are sources. The data typically
don't need to change more than perhaps once a year, but minor changes to the scripts
are very likely.

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
and extract the CSV to the inputs directory prior to running the build script

File Format:

```
id,name,surface_area,land_area[,level-specific fields]
```

Script:  `code/area.py`
