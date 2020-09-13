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
	ocarbon = pd.read_pickle('data/ocarbon.pkl')
	return ocarbon

ocarbon = load_data()

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
	#### [OpenLandMap](https://openlandmap.org/)

	#### [Copernicus Global Land Service](https://zenodo.org/record/3938963#.X1q1e5NKgsk)

	#### [Global Soil Organic Carbon Map](http://54.229.242.119/GSOCmap/)

	#### [Rapid Carbon Assessment (RaCA)](https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/?cid=nrcs142p2_054164#methodology)

	### Useful references

	1. [Soil Organic Carbon Mapping Cookbook 2nd Edition](http://www.fao.org/documents/card/en/c/I8895EN)
	2. [Predictive Soil Mapping with R](https://soilmapper.org/PSMwR_lulu.pdf)

""")
