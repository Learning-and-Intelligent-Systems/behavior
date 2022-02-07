"""Save checkpoints from a BEHAVIOR demo."""
import inspect
import logging
import os
import sys

import igibson
from igibson.utils.checkpoint_utils import save_checkpoint

import behavior
from behavior.examples.demo_replay_example import safe_replay_demo


def create_checkpoints(demo_file, checkpoint_directory, checkpoint_every_n_steps):
    # Create a step callback function to feed replay steps into checkpoints.
    def step_callback(env, _):
        if not env.task.current_success and env.simulator.frame_count % checkpoint_every_n_steps == 0:
            save_checkpoint(env.simulator, checkpoint_directory)

    logging.info("Replaying demo and saving checkpoints")
    safe_replay_demo(demo_file, mode="headless", step_callbacks=[step_callback])


def main(selection="user", headless=False, short_exec=False):
    """
    Opens a demo and creates checkpoints every N steps
    Checkpoints can be used to initialize the simulation at those states, for example, for RL
    """
    logging.info("*" * 80 + "\nDescription:" + main.__doc__ + "*" * 80)

    demo_file = os.path.join(
        os.path.dirname(inspect.getfile(behavior.examples)),
        "data",
        "cleaning_windows_0_Rs_int_2021-05-23_23-11-46.hdf5",
    )
    checkpoint_directory = "checkpoints"
    if not os.path.exists(checkpoint_directory):
        os.mkdir(checkpoint_directory)

    steps_between_checkpoints = 30 if not short_exec else 300
    create_checkpoints(demo_file, checkpoint_directory, steps_between_checkpoints)


if __name__ == "__main__":
    if sys.argv[1] == "--test":
        main(selection="random", headless=True, short_exec=True)
    else:
        main()
