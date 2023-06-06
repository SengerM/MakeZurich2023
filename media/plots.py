import numpy
import plotly.express as px
import pandas

efficiency = numpy.linspace(0,1,99)
T_HOTs = [55]
T_COLDs = [15]
T_SHOWERs = [30,38,42]
shower_time = 14*60
specific_heat_water = 4184 # J kg−1 K−1
Joule_over_kWh = 2.77778e-7**-1
shower_mass_flow_rate = 0.9 # kg/s

data = []
for T_hot in T_HOTs:
	for T_cold in T_COLDs:
		for T_shower in T_SHOWERs:
			_ = pandas.DataFrame(
				{
					'power_ratio': (1-efficiency)*(T_hot-T_cold)/(T_hot-T_cold - efficiency*(T_shower-T_cold)),
				}
			)
			_['efficiency'] = efficiency
			_['T_hot (°C)'] = T_hot
			_['T_cold (°C)'] = T_cold
			_['T_shower (°C)'] = T_shower
			_['Shower energy without heat exchanger (J)'] = shower_mass_flow_rate*shower_time*(T_shower-T_cold)*specific_heat_water
			
			data.append(_)
data = pandas.concat(data)
data['saved_fraction'] = 1-data['power_ratio']
data['saved_fraction_percentage'] = data['saved_fraction']*100
data['Shower energy with heat exchanger (J)'] = data['Shower energy without heat exchanger (J)']*data['power_ratio']
data['Shower energy with heat exchanger (kWh)'] = data['Shower energy with heat exchanger (J)']/Joule_over_kWh

fig = px.line(
	data_frame = data,
	x = 'efficiency',
	y = 'saved_fraction_percentage',
	color = 'T_shower (°C)',
	facet_row = 'T_cold (°C)',
	facet_col = 'T_hot (°C)',
	labels = {
		'efficiency': 'Efficiency of the heat exchanger',
		'saved_fraction_percentage': 'Hot water saved (%)',
		'T_shower (°C)': 'T<sub>shower</sub> (°C)',
		'T_cold (°C)': 'T<sub>cold</sub> (°C)',
		'T_hot (°C)': 'T<sub>hot</sub> (°C)',
	}
)
fig.write_html('fraction_of_savings_vs_exchanger_efficiency.html', include_plotlyjs='cdn')

fig = px.line(
	data_frame = data.query('`T_shower (°C)`==38'),
	x = 'efficiency',
	y = 'Shower energy with heat exchanger (kWh)',
	color = 'T_shower (°C)',
	facet_row = 'T_cold (°C)',
	facet_col = 'T_hot (°C)',
	labels = {
		'efficiency': 'Efficiency of the heat exchanger',
		'saved_fraction_percentage': 'Hot water saved (%)',
		'T_shower (°C)': 'T<sub>shower</sub> (°C)',
		'T_cold (°C)': 'T<sub>cold</sub> (°C)',
		'T_hot (°C)': 'T<sub>hot</sub> (°C)',
	}
)
fig.write_html('shower_energy_vs_exchanger_efficiency.html', include_plotlyjs='cdn')
