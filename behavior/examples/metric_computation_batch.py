import argparse
import inspect
import logging
import os
import sys

from igibson.metrics.agent import RobotMetric
from igibson.metrics.disarrangement import KinematicDisarrangement, LogicalDisarrangement
from igibson.metrics.gaze import GazeMetric
from igibson.metrics.task import TaskMetric

import behavior
from behavior.examples.demo_replay_batch import replay_demo_batch


def parse_args(defaults=False):
    args_dict = dict()
    args_dict["demo_root"] = os.path.join(os.path.dirname(inspect.getfile(behavior.examples)), "data")
    args_dict["log_manifest"] = os.path.join(
        os.path.dirname(inspect.getfile(behavior.examples)), "data", "test_manifest.txt"
    )
    args_dict["out_dir"] = os.path.join(os.path.dirname(inspect.getfile(behavior.examples)), "data")
    if not defaults:
        parser = argparse.ArgumentParser(description="Collect metrics from BEHAVIOR demos in manifest.")
        parser.add_argument("demo_root", type=str, help="Directory containing demos listed in the manifest.")
        parser.add_argument("log_manifest", type=str, help="Plain text file consisting of list of demos to replay.")
        parser.add_argument("out_dir", type=str, help="Directory to store results in.")
        args = parser.parse_args()
        args_dict["demo_root"] = args.demo_root
        args_dict["log_manifest"] = args.log_manifest
        args_dict["out_dir"] = args.out_dir
    return args_dict


def main(selection="user", headless=False, short_exec=False):
    """
    Compute metrics on a batch of previously recorded demos
    Uses a manifest file
    """
    logging.info("*" * 80 + "\nDescription:" + main.__doc__ + "*" * 80)

    defaults = selection == "random" and headless and short_exec
    args_dict = parse_args(defaults=defaults)

    def get_metrics_callbacks(**kwargs):
        metrics = [
            KinematicDisarrangement(),
            LogicalDisarrangement(),
            RobotMetric(),
            GazeMetric(),
            TaskMetric(),
        ]

        return (
            [metric.start_callback for metric in metrics],
            [metric.step_callback for metric in metrics],
            [metric.end_callback for metric in metrics],
            [metric.gather_results for metric in metrics],
        )

    replay_demo_batch(args_dict["demo_root"], args_dict["log_manifest"], args_dict["out_dir"], get_metrics_callbacks)


if __name__ == "__main__":
    if sys.argv[1] == "--test":
        main(selection="random", headless=True, short_exec=True)
    else:
        main()
