# Downsample iSDAsoil data on to 0.5deg resolution grid
import ee
ee.Authenticate()
ee.Initialize(project="data-481404")

k_image = ee.Image("ISDASOIL/Africa/v1/potassium_extractable").select('mean_0_20')
p_image = ee.Image("ISDASOIL/Africa/v1/phosphorus_extractable").select('mean_0_20')
n_image = ee.Image("ISDASOIL/Africa/v1/nitrogen_total").select('mean_0_20')
soc_image = ee.Image("ISDASOIL/Africa/v1/carbon_organic").select('mean_0_20')

grid_proj = ee.Projection("EPSG:4326").atScale(50000)

downsampled_k_image = k_image.reduceResolution(ee.Reducer.mean(), bestEffort=True).reproject(crs=grid_proj)

task = ee.batch.Export.image.toDrive(
    image=downsampled_k_image,
    description="ISDAsoil_0_5deg",
    scale=50000,
    region=k_image.geometry(),
    crs="EPSG:4326",
    maxPixels=1e13
)
task.start()