import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

st.header("Soil carbon")

st.markdown(
    """

> _A running narrative on measuring below-ground carbon measurement._

"""
)


@st.cache(persist=True)
def load_data(plot=True):
    data = {
        "ocarbon": pd.read_pickle("data/ocarbon.pkl"),
        "soilgrid_corr": pd.read_pickle("data/soilgrid_corr.pkl"),
        "soilgrid_corr_buffered": pd.read_pickle("data/soilgrid_corr_buffered.pkl"),
        "olm_soilgrids_merged": pd.read_pickle("data/olm_soilgrids_merged.pkl"),
    }
    return data


data = load_data()

f = open('intro_framing.md','r')
intro_framing = f.read()
st.markdown(intro_framing)

st.markdown(
    """

	### Data exploration

	The most important datasets in this exploration are *existing* datasets on
	soil carbon.  Our timeline is too short and the funding too small to generate
	totally original data.  Instead, we can add value by assembling global data
	on soil carbon into a form that can be utilized by climate policy and
	decision makers.

	#### [SoilGrids](https://soilgrids.org/)

	SoilGrids uses an array of remotely sensed data sources to geographically
	interpolate the point samples from the [World Soil Information
	Service](https://www.isric.org/explore/wosis/faq-wosis) (WoSIS), a large
	PostgreSQL database developed and maintained by ISRIC, WDC-Soils.
"""
)

image = Image.open("imgs/wosis_points.png")

st.image(
    image,
    caption="Organic Soil Carbon (0-30cm) processed from the WoSIS data",
    use_column_width=True,
)

ocarbon = data["ocarbon"]
nrow, _ = ocarbon.shape
lamb = ocarbon.orgc_value_avg.mean()

st.markdown(
    """

	After some pre-processing, detailed in the associated `clean.ipynb`,  are %s
	point measurements.  The distribtion of organic soil carbon measurements look
	like a Poisson distribution with &lambda;=%s, maybe with a fatter tail.

"""
    % ("{:,d}".format(nrow), np.round(lamb, 1))
)

df = ocarbon[ocarbon.orgc_value_avg < 100]
c = (
    alt.Chart(df)
    .mark_bar(color="#A9BEBE", size=5)
    .encode(
        x=alt.X(
            "orgc_value_avg:Q",
            bin=alt.Bin(step=1),
            title="Organic carbon content (0-30cm)",
        ),
        y=alt.Y("count():Q", title="Frequency"),
    )
)

st.altair_chart(c, use_container_width=True)

st.markdown(
    """

	Now, consider the SoilGrids data.  A sample of the U.S., three square tiles
	at 2 degrees sides is plotted below, where lighter colors indicate higher
	levels of Organic Soil Carbon Stock. *Note that the image is squished due to
	projection being totally ignored &mdash; the image is just for, literally,
	color commentary.*   This area contains 4,095 WoSIS measurements.

"""
)

image = Image.open("imgs/soilgrids_sample.png")

st.image(
    image,
    caption="SoilGrids sample in the U.S. (six degrees across)",
    use_column_width=True,
)

st.markdown(
    """

	The SoilGrid data is a very rough approximation of the ground samples.  Much
	more precise research and coordination has to be done (**Chris, help!!**) to
	ensure that we're comparing apples to apples, but the scatterplot below shows
	that the correlation is positive but weak.

"""
)

soilgrid_corr = data["soilgrid_corr"]

base = (
    alt.Chart(soilgrid_corr)
    .mark_circle(opacity=0.5, color="#A9BEBE")
    .encode(
        alt.X(
            "wosis:Q",
            scale=alt.Scale(domain=[0, 90], clamp=True),
            title="WoSIS measurement",
        ),
        alt.Y("soilgrid:Q", title="SoilGrid pixel (250m) value"),
    )
)


st.altair_chart(base, use_container_width=True)

st.markdown(
    """

	[SoilGrids addresses the uncertainty directly](https://www.isric.org/explore/soilgrids/faq-soilgrids-2017#How_accurate_are_SoilGrids_predictions):

	> The actual mapping accuracy of each targeted soil property and classes is
	still limited: the amount of variation explained by the models ranges between
	30 and 70%. On the other hand, and in comparison to other previous global
	soil databases, SoilGrids provides an objective estimate of the uncertainty
	of mapping.

	In other words, the global estimates are highly uncertain &mdash; maybe not
	even useful &mdash; but at least the uncertainty is open and spatially
	explicit.  Given that the accuracy of SoilGrids is at least as good as any
	other global data source on soil organic carbon, and the precision is
	explicit, a **value added would be to report the uncertainty translates for
	agricultural land and how that uncertainty translates into trends.**

"""
)

st.markdown(
    """

	The concordance between the point measurement and the pixel space is still
	unclear.  How does a point measurement relate to an average calculated over a
	continuous area?

	To examine this, we run the same regression, but instead of the SoilGrids
	value of the pixel that the WoSIS measurement falls within, we use the
	average SoilGrids value of all 250m pixels within a 2km radius.

"""
)

soilgrid_corr_buffered = data["soilgrid_corr_buffered"]

buff_c = (
    alt.Chart(soilgrid_corr_buffered)
    .mark_circle(opacity=0.5, color="#A9BEBE")
    .encode(
        alt.X(
            "wosis:Q",
            scale=alt.Scale(domain=[0, 90], clamp=True),
            title="WoSIS measurement",
        ),
        alt.Y("soilgrid:Q", title="SoilGrid value (2km buffer)"),
    )
)

st.altair_chart(buff_c, use_container_width=True)


st.markdown(
    """

	A quick linear regression reveals that the average is slightly more precise,
	probably because some of the noise in the pixel-level analysis was reduced.
	The R-squared value increases from 0.69 to 0.74 for the single-covariate
	regression.  More of the variation in the SoilGrids value is explained by the
	WoSIS measurements.  This doesn't mean much for the predictive or policy
	value of SoilGrids, however, but just that some of the noise has been
	reduced.  Indeed, the variation in SoilGrids measurements drops by 85% when
	averaged over the 2km radius.  The agreement between WoSIS and this
	transformed variable is not convincingly improved.

	It would be more computationally efficient to just throw out "bad" values, or
	those SoilGrid measurements that are zero, rather than averaging over a 2km
	radius.

"""
)

st.markdown(
    """
	#### [OpenLandMap](https://openlandmap.org/)

	The correspondence between Open Land Map and SoilGrids is pretty good over a
	large region.  But still suggests that reporting uncertainty on trends
	(addressing fixed effects and fixed uncertainty effects) is a pretty good
	course of action.

"""
)

olm_soilgrids_merged = data["olm_soilgrids_merged"]

osm_c = (
    alt.Chart(olm_soilgrids_merged)
    .mark_circle(opacity=0.5, color="#A9BEBE")
    .encode(
        alt.X("olm:Q", title="Open Land Map (g/kg)"),
        alt.Y("soilgrids:Q", title="SoilGrid (g/dm3)"),
    )
)

r = osm_c + osm_c.transform_regression("olm", "soilgrids", method="linear").mark_line(
    color="#e45756"
)

st.altair_chart(r, use_container_width=True)

st.markdown(
    """

	#### [Copernicus Global Land Service](https://zenodo.org/record/3938963#.X1q1e5NKgsk)

	#### [Global Soil Organic Carbon Map](http://54.229.242.119/GSOCmap/)

	#### [Rapid Carbon Assessment (RaCA)](https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/?cid=nrcs142p2_054164#methodology)

	### Useful references

	1. [Soil Organic Carbon Mapping Cookbook 2nd Edition](http://www.fao.org/documents/card/en/c/I8895EN)
	2. [Predictive Soil Mapping with R](https://soilmapper.org/PSMwR_lulu.pdf)

"""
)

st.header("Forest Carbon")

st.markdown("""

	### Data Sources

	#### [Global Ecosystem Dynamics Investigation](https://gedi.umd.edu) (GEDI)

	GEDI is high resolution laser ranging of Earth’s forests and topography from
	the International Space Station (ISS).  The first major paper published based
	on these data was the Popotov (2020) [dataset on global tree
	height](https://glad.umd.edu/dataset/gedi).  There are dozens of additional
	derived datasets on the three-dimensional structure of forests, and
	calibration of existing optical imagery. (e.g., *Highly Local Model
	Calibration with a New GEDI LiDAR Asset on Google Earth Engine Reduces
	Landsat Forest Height Signal Saturation*, [Healy
	(2020)](https://www.mdpi.com/2072-4292/12/17/2840)).

	#### [Harmonized global maps of above and belowground biomass carbon density in the year 2010](https://www.nature.com/articles/s41597-020-0444-4)

	This dataset provides temporally consistent and harmonized global maps of
	aboveground and belowground biomass carbon density for the year 2010 at a
	300-m spatial resolution. The aboveground biomass map integrates land-cover
	specific, remotely sensed maps of woody, grassland, cropland, and tundra
	biomass. Input maps were amassed from the published literature and, where
	necessary, updated to cover the focal extent or time period. The belowground
	biomass map similarly integrates matching maps derived from each aboveground
	biomass map and land-cover specific empirical models. Aboveground and
	belowground maps were then integrated separately using ancillary maps of
	percent tree cover and landcover and a rule-based decision tree. Maps
	reporting the accumulated uncertainty of pixel-level estimates are also
	provided.

	#### [UNEP-WCMC Biomass Dataset](https://royalsocietypublishing.org/doi/10.1098/rstb.2019.0128)

	This dataset represents above- and below-ground terrestrial carbon storage
	(tonnes (t) of C per hectare (ha)) for circa 2010. The dataset was
	constructed by combining the most reliable publicly available datasets and
	overlaying them with the ESA CCI landcover map for the year 2010 (ESA, 2017),
	assigning to each grid cell the corresponding above-ground biomass value from
	the biomass map that was most appropriate for the grid cell's landcover type.
	Input carbon datasets were identified through a literature review of existing
	datasets on biomass carbon in terrestrial ecosystems published in
	peer-reviewed literature. To determine which datasets to combine to produce
	the global carbon density map, identified datasets were evaluated based on
	resolution, accuracy, biomass definition and reference date (see Table 1 in
	paper cited for further information on datasets selected). After aggregating
	each selected dataset to a nominal scale of 300 m resolution, forest
	categories in the CCI ESA 2010 landcover dataset were used to extract
	above-ground biomass from Santoro et al. 2018 for forest areas. Woodland and
	savanna biomass were then incorporated for Africa from Bouvet et al. 2018.,
	and from Santoro et al. 2018 for areas outside of Africa and outside of
	forest. Biomass from croplands, sparse vegetation and grassland landcover
	classes from CCI ESA, in addition to shrubland areas outside Africa missing
	from Santoro et al. 2018, were extracted from were extracted from Xia et al.
	2014. and Spawn et al. 2017 averaged by ecological zone for each landcover
	type. Below-ground biomass were added using root-to-shoot ratios from the
	2006 IPCC guidelines for National Greenhouse Gas Inventories (IPCC, 2006). No
	below-ground values were assigned to croplands as ratios were unavailable.
	Above-and-below-ground biomass were then summed together and multiplied by
	0.5 to convert to carbon, generating a single above-and-below-ground biomass
	carbon layer. This dataset has not been validated.

	#### [Global, 30-m resolution continuous fields of tree cover](https://www.tandfonline.com/doi/full/10.1080/17538947.2013.786146)

	The Landsat Vegetation Continuous Fields (VCF) tree cover layers contain
	estimates of the percentage of horizontal ground in each 30-m pixel covered
	by woody vegetation greater than 5 meters in height. The dataset is available
	for four epochs centered on the years 2000, 2005, 2010 and 2015. The dataset
	is derived from the GFCC Surface Reflectance product (GFCC30SR), which is
	based on enhanced Global Land Survey (GLS) datasets. The GLS datasets are
	composed of high-resolution Landsat 5 Thematic Mapper (TM) and Landsat 7
	Enhanced Thematic Mapper Plus (ETM+) images at 30 meter resolution.

	Tree cover, the proportional, vertically projected area of vegetation
	(including leaves, stems, branches, etc.) of woody plants above a given
	height, affects terrestrial energy and water exchanges, photosynthesis and
	transpiration, net primary production, and carbon and nutrient fluxes. Tree
	cover also affects habitat quality and movements of wildlife, residential
	property value for humans, and other ecosystem services. The continuous
	classification scheme of the VCF product enables better depiction of land
	cover gradients than traditional discrete classification schemes. Importantly
	for detection and monitoring of forest changes (e.g., deforestation and
	degradation), tree cover provides a measurable attribute upon which to define
	forest cover and its changes. Changes in tree cover over time can be used to
	monitor and retrieve site-specific histories of forest change.

	#### [High-Resolution Global Maps of 21st-Century Forest Cover Change](https://science.sciencemag.org/content/342/6160/850)

	Results from time-series analysis of Landsat images in characterizing global
	forest extent and change from 2000 through 2019. Trees are defined as
	vegetation taller than 5m in height and are expressed as a percentage per
	output grid cell as ‘2000 Percent Tree Cover’. ‘Forest Cover Loss’ is defined
	as a stand-replacement disturbance, or a change from a forest to non-forest
	state, during the period 2000–2019. ‘Forest Cover Gain’ is defined as the
	inverse of loss, or a non-forest to forest change entirely within the period
	2000–2012. ‘Forest Loss Year’ is a disaggregation of total ‘Forest Loss’ to
	annual time scales. Reference 2000 and 2019 imagery are median observations
	from a set of quality assessment-passed growing season observations.

	#### [Costa Rica National Inventory of Greenhouse Gases (INGEI)](http://sinamecc.opendata.junar.com/dashboards/21151/inventario-nacional-de-gases-de-efecto-invernadero-ingei/)

	The National Inventory of Greenhouse Gases (INGEI) counts the gases emitted
	and absorbed from the atmosphere during a calendar year for the Costa Rican
	territory, according to the guidelines established by the Intergovernmental
	Group of Experts on Climate Change (IPCC).  Note; The inventories for 1990,
	1996 and 2000 are not comparable as they were calculated with a different
	methodology than the recent inventories. They are currently being
	recalculated to be comparable. Privileged access is available through the
	current Ministry of the Environment.

""")













