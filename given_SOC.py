import numpy as np
import pybamm


# 1st calculation ###################
model = pybamm.lithium_ion.DFN()
chemistry = pybamm.parameter_sets.Chen2020
parameter_values = pybamm.ParameterValues(chemistry=chemistry)

experiment = pybamm.Experiment(
[("Discharge at C/3 until 3.703 V",
 "Hold at 3.703 V until 5 mA",
 "Rest for 48 hours")], period="1 hours"
)

sim = pybamm.Simulation(model, experiment=experiment, parameter_values=parameter_values)
sim.solve()
sim.plot()

solution = sim.solution
c_s_n = solution["Average negative particle concentration [mol.m-3]"]
c_s_p = solution["Average positive particle concentration [mol.m-3]"]
# print(c_s_n.entries[-1])
# print(c_s_p.entries[-1])
#####################

# validation #######################
model_SOC = pybamm.lithium_ion.DFN()
chemistry = pybamm.parameter_sets.Chen2020
parameter_values = pybamm.ParameterValues(chemistry=chemistry)

# set parameters as initial voltage = 3.703 V (might be other good ways)
parameter_values["Initial concentration in negative electrode [mol.m-3]"] = c_s_n.entries[-1].round(0)
parameter_values["Initial concentration in positive electrode [mol.m-3]"] = c_s_p.entries[-1].round(0)
parameter_values["Initial concentration in electrolyte [mol.m-3]"] = 1100.0

experiment = pybamm.Experiment(
[("Rest for 10 seconds",
 "Discharge at 10C for 10 seconds",
 "Rest for 10 seconds")], 
    period="0.1 seconds"
)

sim_SOC = pybamm.Simulation(model_SOC, experiment=experiment, parameter_values=parameter_values)
sim_SOC.solve()
sim_SOC.plot()
