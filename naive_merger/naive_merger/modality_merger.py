
import argparse
from copy import deepcopy
from typing import Dict, List
import numpy as np
from naive_merger.utils import normalized_entropy, diagonal_cross_entropy, is_zeros

PRIOR_CONFIDANCE_NL = 0.99
PRIOR_CONFIDANCE_GS = 0.8

class MagicFuns():
    @staticmethod
    def add(l, g):
        return abs(l + g)/2
    @staticmethod
    def mul(l, g):
        return l * g

def is_merging_needed(ls, gs):
    return True

def merge_probabilities(
        ls: Dict[str, np.ndarray],
        gs: Dict[str, np.ndarray], 
        magic_function: str = "mul",
        thresholding: str = "entropy",
        arity_names: List[str] = ["target_action", "target_object"],
    ) -> Dict[str, np.ndarray]:
    M = {}
    for arity_type in arity_names: # target_action, target_object, ...

        if not is_merging_needed(ls[arity_type], gs[arity_type]):
            M[arity_type] = ls[arity_type] + gs[arity_type]

        lsp=deepcopy(ls[arity_type])
        gsp=deepcopy(gs[arity_type])

        if thresholding == 'no thresholding':
            merged_p = []
            for lp, gp in zip(lsp, gsp):
                merged_p.append(max(lp, gp))

            M[arity_type] = merged_p

        elif thresholding == 'entropy':
            # penalize according to entropy?
            PENALIZE_BY_ENTROPY = True
            DISCARD_ENTROPY_THRESHOLD = 1.01

            if normalized_entropy(lsp) > DISCARD_ENTROPY_THRESHOLD:
                # lsp = np.ones_like(lsp) * np.finfo(lsp.dtype).eps
                msp = gsp
            elif normalized_entropy(gsp) > DISCARD_ENTROPY_THRESHOLD:
                # gsp = np.ones_like(gsp) * np.finfo(gsp.dtype).eps
                msp = lsp
            else:
                if PENALIZE_BY_ENTROPY:
                    # exception for len(1)
                    if len(lsp) == 1:
                        penalization_by_entropy_l = 1.
                    else:
                        penalization_by_entropy_l = diagonal_cross_entropy(lsp)
                    if len(gsp) == 1:
                        penalization_by_entropy_g = 1.
                    else:
                        penalization_by_entropy_g = diagonal_cross_entropy(gsp)
                        
                    lsp /= penalization_by_entropy_l
                    gsp /= penalization_by_entropy_g

                if is_zeros(gsp):
                    msp = lsp
                elif is_zeros(lsp):
                    msp = gsp 
                else:
                    if magic_function == 'mul':
                        msp = lsp * gsp  # "merge"
                    elif magic_function == 'add':
                        msp = lsp + gsp
                    else:
                        raise Exception(f"TODO")

            msp /= np.sum(msp)  # normalize
            M[arity_type] = msp 

        elif thresholding == 'fixed':
            cl, cg = PRIOR_CONFIDANCE_NL * np.array(lsp), PRIOR_CONFIDANCE_GS * np.array(gsp)
            cm = np.zeros(len(cl))
            for n,(l,g) in enumerate(zip(cl, cg)):
                cm[n] = getattr(MagicFuns, magic_function)(l, g)
                #getattr(float(l), self.fun)(g)
            M[arity_type] = cm
                    
        else: raise Exception("Wrong")
    
        # M[arity_type].recompute_ids()
    return M

def main(args):
    ls = {
        "target_action": np.array([0.5, 0.3, 0.2]), 
        "target_object": np.array([0.6, 0.1, 0.3]), 
    }
    gs = {
        "target_action": np.array([0.5, 0.3, 0.2]), 
        "target_object": np.array([0.6, 0.1, 0.3]), 
    }

    p = merge_probabilities(ls, gs, args.magic_function, args.thresholding, args.arity_names)
    
    print(p)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--magic_function", nargs="+", default="mul", choices=["mul", "add"])
    parser.add_argument("--arity_names", nargs="+", default=["target_action", "target_object"])
    parser.add_argument("--thresholding", default="entropy", choices=["no thresholding", "fixed", "entropy"])

    args, _ = parser.parse_known_args()

    main(args)