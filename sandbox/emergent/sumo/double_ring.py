"""Double ring version of sugiyama experiment.

This example consists of 41 IDM cars on a double ring creating shockwaves.
"""

from flow.controllers import IDMController, ContinuousRouter
from flow.core.experiment import Experiment
from flow.core.params import SumoParams, EnvParams, \
    InitialConfig, NetParams, SumoLaneChangeParams
from flow.core.vehicles import Vehicles
from flow.scenarios.loop import LoopScenario, ADDITIONAL_NET_PARAMS
from flow.envs.loop.lane_changing import LaneChangeAccelEnv, \
    ADDITIONAL_ENV_PARAMS


def example(render=None):
    """
    Perform a simulation of vehicles on a double ring road.

    Parameters
    ----------
    render : bool, optional
        specifies whether to use sumo's gui during execution

    Returns
    -------
    exp: flow.core.experiment.Experiment
        A non-rl experiment demonstrating the performance of human-driven
        vehicles on a ring road.
    """
    sumo_params = SumoParams(sim_step=0.1, render=True)

    if render is not None:
        sumo_params.render = render

    vehicles = Vehicles()
    # Permit lane changing of human drivers
    lane_change_params = SumoLaneChangeParams(
        lane_change_mode="strategic")
    vehicles.add(
        veh_id="idm",
        acceleration_controller=(IDMController, {}),
        sumo_lc_params=lane_change_params,  # enables lane changing
        routing_controller=(ContinuousRouter, {}),
        num_vehicles=41)

    env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

    net_params = NetParams(
        additional_params={
            "length": 260,
            "lanes": 2,  # double ring
            "speed_limit": 30,
            "resolution": 40,
        }
    )

    # Vehicle initial placement: random positions
    initial_config = InitialConfig(bunching=20, spacing="random")

    scenario = LoopScenario(
        name="double_ring",
        vehicles=vehicles,
        net_params=net_params,
        initial_config=initial_config)

    # No AVs, so doesn't matter if it's a lane change env or not
    env = LaneChangeAccelEnv(env_params, sumo_params, scenario)

    return Experiment(env)


if __name__ == "__main__":
    # import the experiment variable
    exp = example()

    # run for a set number of rollouts / time steps
    exp.run(1, 1500)
