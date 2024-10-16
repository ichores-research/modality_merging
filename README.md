# Modality Merging

Naive modality merger is limited now to 2 modalities. 

## Install

Install ROS2 and use as ROS package.
```Shell
cd <ichores_ws>
colcon build --symlink-install
cd <ichores_ws>/merging_modalities/naive_merger
pip install -e .

```

- [ ] change to ROS1 or ZMQ bridge to Tiago?

## Usage:

```
source <ichores_ws>/install/setup.bash
ros2 run naive_merger mm_node
```
This sets listening `--topics` for inputs Hand outputs `/mm/solution`. Both input and output are format of type `HRICommand.msg` (see *hri_msgs*).


## Notes

- [ ] Entropy is not using PRIOR_CONFIDANCE


## Hyperparameters

- Tune Thresholding in `probs_vector.py`
```
MATCH_THRESHOLD = 0.4
CLEAR_THRESHOLD = 0.4
UNSURE_THRESHOLD = 0.11
DIFFS_THRESHOLD = 0.01
DISCARD_TWO_MAXES_ENABLED = False
UNIFORM_ENTROPY_TH = 0
UNIFORM_ENTROPY_TH_LEN_1 = 1.1
NOISE_TH = 0.05
```
- Tune merging in `modality_merger.py`:
```
PRIOR_CONFIDANCE_NL = 0.99
PRIOR_CONFIDANCE_GS = 0.8
# penalize according to entropy?
PENALIZE_BY_ENTROPY = True
DISCARD_ENTROPY_THRESHOLD = 1.01 # no discarding
MAGIC_FUNCTION = "mul"
ARITY_NAMES = ["action", "object"]
```
- Tune thresholding approach in `HriCommand.py`:
```
THRESHOLDING = "entropy"
```
- Tune input modalities in `modality_merger_node.py`
```
--topics ["gg", "nlp"] # listening to topics
```
