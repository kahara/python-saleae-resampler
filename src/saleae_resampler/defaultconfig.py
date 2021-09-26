"""Default configuration file contents"""

# Remember to add tests for keys into test_saleae_resampler.py
DEFAULT_CONFIG_STR = """
[zmq]
pub_sockets = ["ipc:///tmp/saleae_resampler_pub.sock", "tcp://*:52595"]
rep_sockets = ["ipc:///tmp/saleae_resampler_rep.sock", "tcp://*:52596"]

""".lstrip()
