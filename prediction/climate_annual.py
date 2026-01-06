import ee

def generate_mat_annual_image(year, scenario):
    dataset = "NASA/GDDP-CMIP6"
    variable = "tas" # Daily Near-Surface Air Temperature in Kelvin
    ic = (
        ee.ImageCollection(dataset)
        .filter(ee.Filter.eq("scenario", scenario))
        .select(variable)
    )
    start = ee.Date.fromYMD(year, 1, 1)
    end = start.advance(1, "year")

    annual = (
        ic.filterDate(start, end)
          # average across time (daily -> annual)
          .mean()
          # average across models
          .reduce(ee.Reducer.mean())
          .rename(f"MAT_{year}_{scenario}")
          .subtract(273.15) # convert kelvin to celsius
          .set({
            "year": year,
            "scenario": scenario,
            "units": "C",
        })
    )

    return annual

# Build monthly mean images
def monthly_mean(month, year, ic):
    month = ee.Number(month)
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, "month")

    return (
        ic.filterDate(start, end)
            .mean()            # daily -> monthly mean
            .set("month", month)
    )

def generate_mwmt_annual_image(year, scenario):
    dataset = "NASA/GDDP-CMIP6"
    variable = "tas"

    # Load and filter dataset
    ic = (
        ee.ImageCollection(dataset)
        .filter(ee.Filter.eq("scenario", scenario))
        .select(variable)
    )

    months = ee.List.sequence(1, 12)
    monthly_ic = ee.ImageCollection(months.map(lambda x: monthly_mean(x, year, ic)))

    # MWMT: warmest monthly mean, ensemble mean across models
    mwmt = (
        monthly_ic
        .max()
        .reduce(ee.Reducer.mean())
        .rename(f"MWMT_{year}_{scenario}")
        .subtract(273.15) # convert kelvin to celsius
        .set({
            "year": year,
            "scenario": scenario,
            "units": "C",
        })
    )

    return mwmt

def generate_mcmt_annual_image(year, scenario):
    dataset = "NASA/GDDP-CMIP6"
    variable = "tas"

    # Load and filter dataset
    ic = (
        ee.ImageCollection(dataset)
        .filter(ee.Filter.eq("scenario", scenario))
        .select(variable)
    )

    months = ee.List.sequence(1, 12)
    monthly_ic = ee.ImageCollection(months.map(lambda x: monthly_mean(x, year, ic)))

    # MCMT: coldest monthly mean, ensemble mean across models
    mcmt = (
        monthly_ic
        .min()
        .reduce(ee.Reducer.mean())
        .rename(f"MCMT_{year}_{scenario}")
        .subtract(273.15) # convert kelvin to celsius
        .set({
            "year": year,
            "scenario": scenario,
            "units": "C",
        })
    )

    return mcmt

def generate_map_annual_image(year, scenario):
    dataset = "NASA/GDDP-CMIP6"
    variable = "pr"  # kg m-2 s-1 (equivalent to mm s-1)

    # Load and filter dataset
    ic = (
        ee.ImageCollection(dataset)
        .filter(ee.Filter.eq("scenario", scenario))
        .select(variable)
    )

    start = ee.Date.fromYMD(year, 1, 1)
    end = start.advance(1, "year")

    # Daily precipitation rate -> annual total (mm/year)
    annual_pr = (
        ic.filterDate(start, end)
          .sum()                       # sum of daily rates
          .multiply(86400)             # seconds/day -> mm/day
    )

    # Ensemble mean across models
    map_img = (
        annual_pr
        .reduce(ee.Reducer.mean())
        .rename(f"MAP_{year}_{scenario}")
        .set({
            "year": year,
            "scenario": scenario,
            "units": "mm/year",
        })
    )

    return map_img