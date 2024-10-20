from dataclasses import dataclass
from abc import ABC
from typing import Dict, Literal, Optional

from datasets import load_dataset

from .utils import RawDatasetPreprocessor

@dataclass
class ALMARDPBase(RawDatasetPreprocessor, ABC):
    dimension: Literal["xcomet", "kiwi", "fluency"] = "xcomet"

    def _dataset_to_preference_formatter(self, example) -> Dict[str, str]:
        chosen_idx = example[f"{self.dimension}_best_response_id"]
        rejected_idx = example[f"{self.dimension}_worst_response_id"]
        return {
            "raw_prompt": example["prompt"],
            "prompt":   self.prompt_template.format(raw_prompt=example["prompt"]),
            "chosen":   example[f"response_{chosen_idx}"],
            "rejected": example[f"response_{rejected_idx}"],
        }


@dataclass
class ALMARDP(ALMARDPBase):
    path: Optional[str] = "marulyanova/PKU-SafeRLHF-10K-Modified"

    def _get_raw_dataset(self, split):
        if split == "train":
            return load_dataset(self.path, split="train").train_test_split(test_size=0.1, seed=0)["train"]
        elif split == "validation":
            return load_dataset(self.path, split="train").train_test_split(test_size=0.1, seed=0)["test"]
        elif split == "test":
            raise NotImplementedError("marulyanova/PKU-SafeRLHF-10K-Modified is for development, no test set available.")
        else:
            raise NotImplementedError


if __name__ == '__main__':
    safer10k_train_dataset = ALAMRDP(dimension="safer").get_preference_dataset(split="train")
    better10k_train_dataset = ALAMRDP(dimension="better").get_preference_dataset(split="train")
    breakpoint()
