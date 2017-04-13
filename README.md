# SystemAdvisorModel_base
Using NREL's System Advisor Model (SAM), this program provides a basic, generic framework to be used for adapting other scripts. While SAM is written in C, NREL does provide several language wrappers, including a python wrapper which this repository utilizes.

The SAM Simular Core (SSC) SDK is a collection of developer tools for creating renewable energy system models using the SSC library. You can learn more about NREL, SAM and the SAM SDK at: https://sam.nrel.gov/sdk


As this relies on the SAM SDK, which is a custom module, users will need to download and install the SAM SDK from NREL.

NREL provides SDK support at: https://sam.nrel.gov/sdk-support

Output from test1():

('PVWatts V5 Simulation ok, e_net (annual kW) =', 7689.720703125)
Annual energy (year 1) =  7689.72070312
Capacity factor (year 1) =  19.0830879211
Energy yield (year 1) =  1671.6784668
Performance ratio (year 1) =  0.0
Battery efficiency =  0.0
Levelized COE (nominal) =  12.6983346939
Levelized COE (real) =  10.4986534119
Electricity bill without system (year 1) =  423.694641113
Electricity bill with system (year 1) =  12.7737436295
Net savings with system (year 1) =  410.920898438
Net present value =  -6871.05761719
Payback period =  nan
Net capital cost =  10342.4335938
Equity =  10342.4335938
Debt =  0.0

---------------------------------------------------------------------------

('PVWatts V5 Simulation ok, e_net (annual kW) =', 9692.6669921875)
Annual energy (year 1) =  9692.66796875
Capacity factor (year 1) =  17.562997818
Energy yield (year 1) =  1538.51867676
Performance ratio (year 1) =  0.0
Battery efficiency =  0.0
Levelized COE (nominal) =  14.7537298203
Levelized COE (real) =  11.1773824692
Electricity bill without system (year 1) =  246.897720337
Electricity bill with system (year 1) =  -0.0
Net savings with system (year 1) =  246.897720337
Net present value =  -11660.4921875
Payback period =  nan
Net capital cost =  13879.1230469
Equity =  13879.1230469
Debt =  0.0
