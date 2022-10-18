import glob
import os
from pathlib import Path

from filesplit.split import Split
from loguru import logger
from sortedcontainers import SortedKeyList


def get_files(dir):
    return {Path(i): os.stat(i).st_size for i in glob.glob(
        '*', root_dir=Path(dir).absolute(), recursive=True) if Path(i).is_file()}


def bin_size(bin: dict):
    return sum(bin.values())


def split_file(file: Path, size: int):
    bins = []
    file.parent.mkdir(f"{file.name}-split")
    folder = file.with_name(f"{file.name}-split")

    # Splitting the files
    Split(
        file.absolute(),
        folder.absolute()
    ).bysize(
        size,
        callback=lambda x, y: bins.append({Path(x): y})
    )

    return bins


def optimize_files(files: dict[Path, int], open_am=5, max_memory=100*(10**6)):
    logger.info("Starting the archive amount optimization")
    # Może warto 2^20 zamiast tego 10^6
    bins = SortedKeyList(key=bin_size)

    for file, memory in files.items():
        logger.debug("Working on {} ({} bytes)", file.name, memory)

        # Iterating through open containers
        for b in bins[:open_am:-1]:
            if bin_size(b)+memory <= max_memory:
                bins.remove(b)
                bins.add(b | {file: memory})
                logger.debug("Adding {} to an existing bin ({} bytes -> {} bytes",
                             file.name, bin_size(b), bin_size(b)+memory)
                break
        else:
            # Adding new container
            bins.extend(split_file(file, max_memory))

    return [list(i.values()) for i in bins]
