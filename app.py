import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

st.header("Soil carbon")

st.markdown("""

> _A running narrative on measuring below-ground carbon measurement._

""")

@st.cache(persist=True)
def load_data(plot=True):
	data = {
		"ocarbon": pd.read_pickle('data/ocarbon.pkl'),
		"soilgrid_corr": pd.read_pickle('data/soilgrid_corr.pkl')
	}
	return data

data = load_data()

st.markdown("""

	### Introduction and framing

	**Chris** will start on this.

		Quantify and map uncertainty around soil carbon trends

""")

st.markdown("""

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
""")

image = Image.open('imgs/wosis_points.png')

st.image(
	image, 
	caption='Organic Soil Carbon (0-30cm) processed from the WoSIS data',
	use_column_width=True
)

ocarbon = data["ocarbon"]
nrow, _ = ocarbon.shape
lamb = ocarbon.orgc_value_avg.mean()

st.markdown("""
	
	After some pre-processing, detailed in the associated `clean.ipynb`,  are %s
	point measurements.  The distribtion of organic soil carbon measurements look
	like a Poisson distribution with &lambda;=%s, maybe with a fatter tail.

""" % (
		"{:,d}".format(nrow),
		np.round(lamb, 1)
	)
)

df = ocarbon[ocarbon.orgc_value_avg < 100]
c = alt.Chart(df).mark_bar(
		color="#A9BEBE",
		size=5
	).encode(
	    x=alt.X(
	    	'orgc_value_avg:Q',
	    	bin=alt.Bin(step=1),
        	title="Organic carbon content (0-30cm)"
        ),
	    y=alt.Y(
	    	'count():Q',
	    	title="Frequency"
	    )
)

st.altair_chart(c, use_container_width=True)

st.markdown("""

	Now, consider the SoilGrids data.  A sample of the U.S., three square tiles
	at 2 degrees sides is plotted below, where lighter colors indicate higher
	levels of Organic Soil Carbon Stock. *Note that the image is squished due to
	projection being totally ignored &mdash; the image is just for, literally,
	color commentary.*   This area contains 4,095 WoSIS measurements.

""")

image = Image.open('imgs/soilgrids_sample.png')

st.image(
	image, 
	caption='SoilGrids sample in the U.S. (six degrees across)',
	use_column_width=True
)

st.markdown("""
	
	The SoilGrid data is a very rough approximation of the ground samples.  Much
	more precise research and coordination has to be done (**Chris, help!!**) to
	ensure that we're comparing apples to apples, but the scatterplot below shows
	that the correlation is positive but weak.

""")

soilgrid_corr = data["soilgrid_corr"]

base = alt.Chart(soilgrid_corr).mark_circle(
		opacity=0.5,
		color="#A9BEBE"
	).encode(
	    alt.X(
	    	'wosis:Q',
	    	scale=alt.Scale(domain=[0,90], clamp=True),
	    	title="WoSIS measurement"
	    ),
	    alt.Y(
	    	'soilgrid:Q',
	    	title="SoilGrid pixel (250m) value"
	    )
)

st.altair_chart(base, use_container_width=True)

st.markdown("""

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

""")



st.markdown("""
	#### [OpenLandMap](https://openlandmap.org/)

	#### [Copernicus Global Land Service](https://zenodo.org/record/3938963#.X1q1e5NKgsk)

	#### [Global Soil Organic Carbon Map](http://54.229.242.119/GSOCmap/)

	#### [Rapid Carbon Assessment (RaCA)](https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/?cid=nrcs142p2_054164#methodology)

	### Useful references

	1. [Soil Organic Carbon Mapping Cookbook 2nd Edition](http://www.fao.org/documents/card/en/c/I8895EN)
	2. [Predictive Soil Mapping with R](https://soilmapper.org/PSMwR_lulu.pdf)

""")
