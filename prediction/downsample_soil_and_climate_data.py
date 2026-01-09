import ee
ee.Authenticate()
ee.Initialize(project="data-481404")
from climate_annual import *

k_image = ee.Image("ISDASOIL/Africa/v1/potassium_extractable").select('mean_0_20').rename(['Potassium_g_kg_0-20_m'])
p_image = ee.Image("ISDASOIL/Africa/v1/phosphorus_extractable").select('mean_0_20').rename(['Phosphorus_g_kg_0-20_m'])
n_image = ee.Image("ISDASOIL/Africa/v1/nitrogen_total").select('mean_0_20').rename(['Nitrogen_g_kg_0-20_m'])
soc_image = ee.Image("ISDASOIL/Africa/v1/carbon_organic").select('mean_0_20').rename(['OrganicCarbon_g_kg_0-20_m'])

region = k_image.geometry()
scale = 100_000

grid_proj = ee.Projection("EPSG:4326").atScale(scale)

years = [2020, 2030, 2040, 2050]
scenarios = ["ssp245", "ssp585"]
climate_images = []

for year in years:
    for scenario in scenarios:
        climate_images.append(generate_mat_annual_image(year, scenario))
        climate_images.append(generate_mwmt_annual_image(year, scenario))
        climate_images.append(generate_mcmt_annual_image(year, scenario))
        climate_images.append(generate_map_annual_image(year, scenario))

combined_image = k_image

for img in [p_image, n_image, soc_image] + climate_images:
    combined_image = combined_image.addBands(img)

combined_image = combined_image.reproject(crs=grid_proj)

pixel_fc = region.coveringGrid(grid_proj)

# compute means of soil variables over each grid cell
reduced = combined_image.reduceRegions(
    collection=pixel_fc,
    reducer=ee.Reducer.mean(),
    crs=grid_proj
)

task = ee.batch.Export.table.toDrive(
    collection=reduced,
    description="downsampled_soil_and_climate_data_raw",
    fileFormat="CSV"
)
task.start()