
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import sys
#sys.path.insert(0, "J:\\SEIA\\SAM\\sam-sdk-2016-3-14-r3\\win64")
import sscapi


# In[2]:

class SAM:
    def __init__(self, fileloc):
        self.ssc = sscapi.PySSC()
        self.data = self.ssc.data_create()
        self.ssc.data_set_string( self.data, 'solar_resource_file', fileloc );

    def pvWatts5(self, pv_terms):
        self.ssc.data_set_number( self.data, 'system_capacity', pv_terms[0])
        self.ssc.data_set_number( self.data, 'module_type', pv_terms[1] )
        self.ssc.data_set_number( self.data, 'array_type', pv_terms[2] )
        self.ssc.data_set_number( self.data, 'losses', pv_terms[3] )
        self.ssc.data_set_number( self.data, 'tilt', pv_terms[4] )
        self.ssc.data_set_number( self.data, 'azimuth', pv_terms[5] )
        self.ssc.data_set_number( self.data, 'adjust:constant', pv_terms[6] )
        mod = self.ssc.module_create("pvwattsv5")
        self.ssc.module_exec_set_print( 0 )
        if self.ssc.module_exec(mod, self.data) == 0:
            print ('PVWatts V5 simulation error')
            idx = 1
            msg = self.ssc.module_log(mod, 0)
            while(msg != None):
                print('\t: ' + msg)
                msg = self.ssc.module_log(mod, idx)
                idx = idx + 1
        else:
            ann = self.ssc.data_get_number(self.data, "ac_annual")
            print("PVWatts V5 Simulation ok, e_net (annual kW) =", ann)
        self.ssc.module_free(mod)
        
    def BELPE(self, load_profile):
        # Enable belpe
        self.ssc.data_set_number( self.data, 'en_belpe', 1 )
        # Get resource file
        
        # House attributes
        self.ssc.data_set_number( self.data, 'floor_area', load_profile[0] )
        self.ssc.data_set_number( self.data, 'stories', load_profile[1] )
        self.ssc.data_set_number( self.data, 'yrbuilt', load_profile[2] )
        self.ssc.data_set_number( self.data, 'retrofits', load_profile[3] )
        self.ssc.data_set_number( self.data, 'occupants', load_profile[4] )

        occ_schedule =[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ];
        self.ssc.data_set_array( self.data, 'occ_schedule',  occ_schedule);
        self.ssc.data_set_number( self.data, 'theat', load_profile[5] )
        self.ssc.data_set_number( self.data, 'tcool', load_profile[6] )
        self.ssc.data_set_number( self.data, 'theatsb', load_profile[7] )
        self.ssc.data_set_number( self.data, 'tcoolsb', load_profile[8] )
        t_sched =[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ];
        self.ssc.data_set_array( self.data, 't_sched',  t_sched);

        # Enable various appliances in the house
        self.ssc.data_set_number( self.data, 'en_heat', load_profile[9] )
        self.ssc.data_set_number( self.data, 'en_cool', load_profile[10] )
        self.ssc.data_set_number( self.data, 'en_fridge', load_profile[11] )
        self.ssc.data_set_number( self.data, 'en_range', load_profile[12] )
        self.ssc.data_set_number( self.data, 'en_dish', load_profile[13] )
        self.ssc.data_set_number( self.data, 'en_wash', load_profile[14] )
        self.ssc.data_set_number( self.data, 'en_dry', load_profile[15] )
        self.ssc.data_set_number( self.data, 'en_mels', load_profile[16] )

        # Monthly utility bill
        monthly_util = load_profile[17]
        self.ssc.data_set_array( self.data, 'monthly_util',  monthly_util);

        module = self.ssc.module_create('belpe')	
        self.ssc.module_exec_set_print( 0 );
        if self.ssc.module_exec(module, self.data) == 0:
            print ('belpe simulation error')
            idx = 1
            msg = self.ssc.module_log(module, 0)
            while (msg != None):
                print ('	: ' + msg)
                msg = self.ssc.module_log(module, idx)
                idx = idx + 1
            SystemExit( "Simulation Error" );
        self.ssc.module_free(module)
        
    def utilityRateV4(self, u_r):
        self.ssc.data_set_number( self.data, 'analysis_period', u_r[0] )
        self.ssc.data_set_number( self.data, 'system_use_lifetime_output', u_r[1] )
        self.ssc.data_set_number( self.data, 'inflation_rate', u_r[2] )
        degradation =[ 0.5 ];
        self.ssc.data_set_array( self.data, 'degradation',  u_r[3]);

        ur_ec_sched_weekend = [[ 6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6 ], [ 6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6 ], [ 6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6 ], [ 6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6 ], [ 6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6 ]];
        self.ssc.data_set_matrix( self.data, 'ur_ec_sched_weekend', ur_ec_sched_weekend );
        ur_ec_tou_mat = [[ 1,   1,   1000,   0,   0.1542000025510788,   0 ], [ 1,   2,   9.9999996802856925e+037,   0,   0.16845999658107758,   0 ], [ 2,   1,   1000,   0,   0.10244999825954437,   0 ], [ 2,   2,   9.9999996802856925e+037,   0,   0.11670999974012375,   0 ], [ 3,   1,   1000,   0,   0.073260001838207245,   0 ], [ 3,   2,   9.9999996802856925e+037,   0,   0.087520003318786621,   0 ], [ 4,   1,   1000,   0,   0.1542000025510788,   0 ], [ 4,   2,   9.9999996802856925e+037,   0,   0.16845999658107758,   0 ], [ 5,   1,   1000,   0,   0.10244999825954437,   0 ], [ 5,   2,   9.9999996802856925e+037,   0,   0.11670999974012375,   0 ], [ 6,   1,   1000,   0,   0.073260001838207245,   0 ], [ 6,   2,   9.9999996802856925e+037,   0,   0.087520003318786621,   0 ]];
        self.ssc.data_set_matrix( self.data, 'ur_ec_tou_mat', ur_ec_tou_mat );
        ur_ec_sched_weekday = [[ 6,   6,   6,   6,   6,   6,   4,   4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   4,   4,   4,   5,   5,   6,   6 ], [ 6,   6,   6,   6,   6,   6,   4,   4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   4,   4,   4,   5,   5,   6,   6 ], [ 6,   6,   6,   6,   6,   6,   4,   4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   4,   4,   4,   5,   5,   6,   6 ], [ 6,   6,   6,   6,   6,   6,   4,   4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   4,   4,   4,   5,   5,   6,   6 ], [ 3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   2,   2,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   2,   2,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   2,   2,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   2,   2,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   2,   2,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   2,   2,   3,   3 ], [ 6,   6,   6,   6,   6,   6,   4,   4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   4,   4,   4,   5,   5,   6,   6 ], [ 6,   6,   6,   6,   6,   6,   4,   4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   4,   4,   4,   5,   5,   6,   6 ]];
        self.ssc.data_set_matrix( self.data, 'ur_ec_sched_weekday', ur_ec_sched_weekday );


        module = self.ssc.module_create('utilityrate4')
        self.ssc.module_exec_set_print( 0 );
        if self.ssc.module_exec(module, self.data) == 0:
            print ('utilityrate4 simulation error')
            idx = 1
            msg = ssc.module_log(module, 0)
            while (msg != None):
                print ('	: ' + msg)
                msg = ssc.module_log(module, idx)
                idx = idx + 1
            SystemExit( "Simulation Error" );
        self.ssc.module_free(module)
        
    def cashloan(self, cl):
        # Set required variables for this module:
        # Note that loan is set to false, making this a cash transaction by default
        self.ssc.data_set_number( self.data, 'federal_tax_rate', cl[0] )
        self.ssc.data_set_number( self.data, 'state_tax_rate', cl[1] )
        self.ssc.data_set_number( self.data, 'real_discount_rate', cl[2] )
        self.ssc.data_set_number( self.data, 'total_installed_cost', cl[3] )
        
        # Create Cashloan module of SAM and run:
        module = self.ssc.module_create('cashloan')
        self.ssc.module_exec_set_print( 0 );
        if self.ssc.module_exec(module, self.data) == 0:
            print ('cashloan simulation error')
            idx = 1
            msg = self.ssc.module_log(module, 0)
            while (msg != None):
                print ('	: ' + msg)
                msg = self.ssc.module_log(module, idx)
                idx = idx + 1
            SystemExit( "Simulation Error" );
        self.ssc.module_free(module)
        
    def report(self):
        annual_energy = self.ssc.data_get_number(self.data, 'annual_energy');
        print 'Annual energy (year 1) = ', annual_energy
        capacity_factor = self.ssc.data_get_number(self.data, 'capacity_factor');
        print 'Capacity factor (year 1) = ', capacity_factor
        kwh_per_kw = self.ssc.data_get_number(self.data, 'kwh_per_kw');
        print 'Energy yield (year 1) = ', kwh_per_kw
        performance_ratio = self.ssc.data_get_number(self.data, 'performance_ratio');
        print 'Performance ratio (year 1) = ', performance_ratio
        average_cycle_efficiency = self.ssc.data_get_number(self.data, 'average_cycle_efficiency');
        print 'Battery efficiency = ', average_cycle_efficiency
        lcoe_nom = self.ssc.data_get_number(self.data, 'lcoe_nom');
        print 'Levelized COE (nominal) = ', lcoe_nom
        lcoe_real = self.ssc.data_get_number(self.data, 'lcoe_real');
        print 'Levelized COE (real) = ', lcoe_real
        elec_cost_without_system_year1 = self.ssc.data_get_number(self.data, 'elec_cost_without_system_year1');
        print 'Electricity bill without system (year 1) = ', elec_cost_without_system_year1
        elec_cost_with_system_year1 = self.ssc.data_get_number(self.data, 'elec_cost_with_system_year1');
        print 'Electricity bill with system (year 1) = ', elec_cost_with_system_year1
        savings_year1 = self.ssc.data_get_number(self.data, 'savings_year1');
        print 'Net savings with system (year 1) = ', savings_year1
        npv = self.ssc.data_get_number(self.data, 'npv');
        print 'Net present value = ', npv
        payback = self.ssc.data_get_number(self.data, 'payback');
        print 'Payback period = ', payback
        adjusted_installed_cost = self.ssc.data_get_number(self.data, 'adjusted_installed_cost');
        print 'Net capital cost = ', adjusted_installed_cost
        first_cost = self.ssc.data_get_number(self.data, 'first_cost');
        print 'Equity = ', first_cost
        loan_amount = self.ssc.data_get_number(self.data, 'loan_amount');
        print 'Debt = ', loan_amount


# In[3]:

def getSAMresults(f, pv_terms, load_profile, utility_info, financials):
    
    # Instantiate a SAM object
    gen = SAM(f)

    # Run through the PV Watts v5 simulator using a submitted weather file
    gen.pvWatts5(pv_terms)

    # Adjust Building/home load profile
    gen.BELPE(load_profile)

    # Run through the Utility rate database
    gen.utilityRateV4(utility_info)

    # Run through the cash/loan financial model from NREL
    gen.cashloan(financials)

    gen.report()
    print("")
    print("---------------------------------------------------------------------------")
    print("")


# In[6]:

def test1():
    f1 = 'C:/SAM/2016.3.14/solar_resource/USA AZ Phoenix Sky Harbor Intl Ap (TMY3).csv'
    f2 = 'C:/SAM/2016.3.14/solar_resource/USA CA Riverside Muni (TMY3).csv'
    files = [f1, f2]
    
    # pvWatts v5 required variables:
    # system capacity, module type (categorical), array type (categorical), losses, tilt, azimuth, adjust:constant
    pv1 = [4.6, 0, 0, 12, 10, 180, 0]
    pv2 = [6.3, 0, 0, 16, 15, 180, 0]
    
    # BELPE (load profile)
    # Sq. ft, stories, yr. built, ... monthly utility bill
    mo_utility1 = [300, 300, 300, 300, 300, 450, 450, 450, 450, 300, 300, 300]
    lp1 = [1700, 2, 2010, 0, 3, 64, 74, 64, 74, 1, 1, 1, 1, 1, 0, 0, 0, mo_utility1]
    
    mo_utility2 = [150, 150, 150, 150, 150, 300, 300, 300, 300, 150, 150, 150]
    lp2 = [1200, 2, 2010, 0, 2, 64, 74, 64, 74, 1, 1, 1, 1, 1, 1, 1, 1, mo_utility2]
    
    # Utility rate database:
    # Analysis period, lifetime or single year of data (categorical), inflation rate, degradation
    ur1 = [25, 0, 2, [0.5]]
    ur2 = [25, 0, 3, [0.5]]
    
    # Cashloan (financial sim) parameters
    # Federal tax rate, state tax rate, real discount rate, installation cost
    cl1 = [30, 8, 5.5, 10342.434]
    cl2 = [25, 8, 5.5, 13879.123]
    
    getSAMresults(f1, pv1, lp1, ur1, cl1)
    getSAMresults(f2, pv2, lp2, ur2, cl2)
    

    return


# In[7]:

if __name__ == '__main__':
    test1()

