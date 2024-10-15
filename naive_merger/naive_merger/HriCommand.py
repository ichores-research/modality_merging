
import json
from typing import Any, Dict, List

from naive_merger.modality_merger import merge_probabilities
from naive_merger.probs_vector import EntropyProbsVector, NaiveProbsVector, ProbsVector

class HriCommand():
    def __init__(
        self,
        arity_names: List[str],
        pv_dict: Dict[str, Any],
        ):
        self.arity_names = arity_names
        self.pv_dict = pv_dict

    def applied_thresholding(self):
        for arity_type in self.arity_names:
            conclusion = self.pv_dict[arity_type].conclude()
            print(f"arity type {arity_type} conclusion: {conclusion}")

    @property
    def data_dict(self):
        ret = {}
        for arity_type in self.arity_names:
            ret[arity_type] = self.pv_dict[arity_type].p
        return ret
    
    @classmethod
    def from_ros(cls, msg, thresholding):
        msg_dict = json.loads(msg.data)

        arity_names = []
        for k in msg_dict.keys():
            if "_probs" in k:
                arity_names.append(k.split("_probs")[0])

        pv_dict = {}
        for arity_type in arity_names:
            names = msg_dict[arity_type]
            probs = msg_dict[arity_type+"_probs"]

            if thresholding == "no thresholding":
                pv_dict[arity_type] = NaiveProbsVector(probs, names)
            elif thresholding == "fixed":
                pv_dict[arity_type] = ProbsVector(probs, names)
            elif thresholding == "entropy":
                pv_dict[arity_type] = EntropyProbsVector(probs, names)
            else: raise Exception()

        return cls(arity_names, pv_dict)
    
    @classmethod
    def from_dict(cls, arity_names, data_dict, thresholding):
        pv_dict = {}
        for arity_type in arity_names:
            names = data_dict[arity_type]
            probs = data_dict[arity_type+"_probs"]

            if thresholding == "no thresholding":
                pv_dict[arity_type] = NaiveProbsVector(probs, names)
            elif thresholding == "fixed":
                pv_dict[arity_type] = ProbsVector(probs, names)
            elif thresholding == "entropy":
                pv_dict[arity_type] = EntropyProbsVector(probs, names)
            else: raise Exception()

        return cls(arity_names, pv_dict)

    def __matmul__(self, other):
        assert self.arity_names == other.arity_names
        for arity_type in self.arity_names:
            assert (self.pv_dict[arity_type].names == other.pv_dict[arity_type].names).all(), f"{self.pv_dict[arity_type]} != {other.pv_dict[arity_type]}"

        data_dict_new = {}
        data_dict = merge_probabilities(self.data_dict, other.data_dict)
        for arity_type in self.arity_names:
            data_dict_new[arity_type+"_probs"] = data_dict[arity_type]
            data_dict_new[arity_type] = self.pv_dict[arity_type].names
        
        return HriCommand.from_dict(self.arity_names, data_dict_new, thresholding="entropy")
