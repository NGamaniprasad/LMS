"""
Data translation management layer. Handles raw system transactions,
file configurations, and storage mutations cleanly.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from utilities import log_execution, LibraryException

class FileStoreManager:
    """Manages raw serialization reads and system flush operations safely."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Maintains clean local storage setups on disk pools."""
        if not self.file_path.exists():
            try:
                with open(self.file_path, "w", encoding="utf-8") as target_file:
                    json.dump([], target_file, indent=4)
            except IOError as io_error:
                raise LibraryException(f"Failed handling base directory provisioning vectors for disk storage target: {str(io_error)}")

    @log_execution
    def read_records(self) -> List[Dict[str, Any]]:
        """Extracts text structures out of physical text targets into operational tracking buffers."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as target_file:
                return json.load(target_file)
        except json.JSONDecodeError:
            return []
        except FileNotFoundError:
            return []
        except Exception as error:
            raise LibraryException(f"Fatal exception reading flat state datasets from disk segments: {str(error)}")

    @log_execution
    def write_records(self, dataset: List[Dict[str, Any]]) -> None:
        """Flushes in-memory structural lists straight out into target data structures safely."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as target_file:
                json.dump(dataset, target_file, indent=4)
        except IOError as io_error:
            raise LibraryException(f"Failed updating production state configurations onto storage nodes: {str(io_error)}")
        except Exception as general_err:
            raise LibraryException(f"Unexpected operational crash inside lower runtime storage modules: {str(general_err)}")