## Calculate Average Carbon Intensity in gCO2eq/kWh

EmissionFactors.json: [electricitymap-contrib/config/co2eq_parameters_lifecycle.json](https://github.com/electricitymap/electricitymap-contrib/blob/master/config/co2eq_parameters_lifecycle.json)


The configurations below is from: [electricitymap-contrib/parsers/ENTSOE.py](https://github.com/electricitymap/electricitymap-contrib/blob/master/parsers/ENTSOE.py)
```json
ENTSOE_PARAMETER_GROUPS = {
    "production": {
        "biomass": ["B01", "B17"],
        "coal": ["B02", "B05", "B07", "B08"],
        "gas": ["B03", "B04"],
        "geothermal": ["B09"],
        "hydro": ["B11", "B12"],
        "nuclear": ["B14"],
        "oil": ["B06"],
        "solar": ["B16"],
        "wind": ["B18", "B19"],
        "unknown": ["B20", "B13", "B15"],
    },
    "storage": {"hydro storage": ["B10"]},
}
```

```json
ENTSOE_PARAMETER_DESC = {
    "B01": "Biomass", 
    "B02": "Fossil Brown coal/Lignite",
    "B03": "Fossil Coal-derived gas", 
    "B04": "Fossil Gas", 
    "B05": "Fossil Hard coal", 
    "B06": "Fossil Oil",
    "B07": "Fossil Oil shale", 
    "B08": "Fossil Peat", 
    "B09": "Geothermal", 
    "B10": "Hydro Pumped Storage", 
    "B11": "Hydro Run-of-river and poundage", 
    "B12": "Hydro Water Reservoir", 
    "B13": "Marine",
    "B14": "Nuclear",
    "B15": "Other renewable",
    "B16": "Solar",
    "B17": "Waste", 
    "B18": "Wind Offshore",
    "B19": "Wind Onshore",
    "B20": "Other",
}
```