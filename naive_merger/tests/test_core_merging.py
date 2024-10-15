
import numpy as np

from naive_merger.modality_merger import merge_probabilities
from naive_merger.HriCommand import HriCommand
from naive_merger.probs_vector import EntropyProbsVector, NaiveProbsVector, ProbsVector

def test_core_merging_1():
    ls = {
        "target_action": np.array([0.5, 0.3, 0.2]), 
        "target_object": np.array([0.6, 0.1, 0.3]), 
    }
    gs = {
        "target_action": np.array([0.5, 0.3, 0.2]), 
        "target_object": np.array([0.6, 0.1, 0.3]), 
    }

    arity_names = ["target_action", "target_object"]

    for magic_function in ["mul", "add"]:
        for thresholding in ["no thresholding", "fixed", "entropy"]:
            p = merge_probabilities(ls, gs, magic_function, thresholding, arity_names)
            print(p)

def test_core_merging_2():
    pv = ProbsVector(p=[0.1,0.2,0.3],template_names=['mark', 'park', 'quark'])
    print(f"{pv}")
    pv = EntropyProbsVector(p=[0.1,0.2,0.3],template_names=['mark', 'park', 'quark'])
    print(f"{pv}")
    pv = NaiveProbsVector(p=[0.1,0.2,0.3],template_names=['mark', 'park', 'quark'])
    print(f"{pv}")

def test_core_merging_3():
    hri_command_nlp = HriCommand.from_dict(
        arity_names = ["target_action", "target_object"],
        data_dict = {
            "target_action_probs": np.array([0.5, 0.3, 0.2]), 
            "target_object_probs": np.array([0.6, 0.1, 0.3]), 
            "target_action": np.array(["pick", "pour", "grab"]), 
            "target_object": np.array(["cube", "cup", "can"]), 
        }, 
        thresholding="entropy",
    )
    hri_command_gs = HriCommand.from_dict(
        arity_names = ["target_action", "target_object"],
        data_dict = {
            "target_action_probs": np.array([0.5, 0.3, 0.2]), 
            "target_object_probs": np.array([0.6, 0.1, 0.3]), 
            "target_action": np.array(["pick", "pour", "grab"]), 
            "target_object": np.array(["cube", "cup", "can"]), 
        }, 
        thresholding="entropy",
    )

    merged_hri_command = hri_command_nlp @ hri_command_gs
    merged_hri_command.applied_thresholding()

if __name__ == "__main__":
    test_core_merging_1()
    test_core_merging_2()
    test_core_merging_3()