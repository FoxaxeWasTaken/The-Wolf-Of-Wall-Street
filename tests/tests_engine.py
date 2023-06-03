import sys
import os
import subprocess
import json
import random
import tempfile


WRAPPER_PATH = "./tests/bin/match-wrapper-1.4.1.jar"


def get_algo_results(algo_file: str, candles_file: str, result_file: str):
    compet_config = {}
    wrapper_config = {}

    with open("tests/config/competition.json", "r") as compet_file:
        compet_config = json.load(compet_file)
    
    with open("tests/config/wrapper.json", "r") as wrapper_file:
        wrapper_config = json.load(wrapper_file)

    compet_config["dataFile"]["value"] = candles_file
    wrapper_config["match"]["engine"]["configuration"] = compet_config
    wrapper_config["match"]["bots"][0]["command"] = algo_file
    wrapper_config["wrapper"]["resultFile"] = result_file

    cmd = ["java", "-jar", WRAPPER_PATH, json.dumps(wrapper_config)]

    subprocess.run(cmd, timeout=40)


def get_results(result_file: str) -> dict:
    results = {}
    
    with open(result_file, "r") as result:
        json_result = json.load(result)
        results["timeElapsed"] = json_result["timeElapsed"]
        
        response_times = json_result["players"][0]["responseTimes"]
        results["averageResponseTime"] = sum(response_times) / len(response_times)
        results["highestResponseTime"] = max(response_times)
        results["lowestResponseTime"] = min(response_times)
        
        details = json.loads(json_result["details"])
        results["finalBalance"] = details["score"]
    
    return results


def print_results(results_dict: dict):
    print()
    print()
    print("=" * 80)
    print("Wrapper executed in " + str(results_dict["timeElapsed"]) + "ms")
    print("Average response time: " + str(results_dict["averageResponseTime"]) + "ms")
    print("Highest response time: " + str(results_dict["highestResponseTime"]) + "ms")
    print("Lowest response time: " + str(results_dict["lowestResponseTime"]) + "ms")
    print("Final balance: " + str(results_dict["finalBalance"]))
