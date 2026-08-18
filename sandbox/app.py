import sys
import logging
from typing import Any, Dict, Optional, Union

# Configure logging using standard logger instances
logger = logging.getLogger("SafeExecutor")


def _safe_str(obj: Any) -> str:
    """
    Guarantees string conversion without throwing exceptions even if 
    an object's custom __str__ or __repr__ implementation raises an error.
    """
    try:
        res = str(obj)
        if isinstance(res, str):
            return res
        return repr(obj)
    except Exception:
        try:
            return repr(obj)
        except Exception:
            return f"<{type(obj).__name__} object at {id(obj):#x}>"


def safe_process_input(
    data: Optional[Union[Dict[str, Any], list, tuple, set, str, int, float, bool, bytes, bytearray, memoryview]] = None
) -> Dict[str, Any]:
    """
    Safely handles and processes arbitrary input without crashing.
    Guards against Null/None types, invalid type assumptions, concurrent mutations,
    broken __str__/__repr__ overrides, recursion errors, and unexpected errors.

    :param data: Input data of variable type
    :return: A structured dictionary containing processing status and payload
    """
    try:
        if data is None:
            logger.info("Input data is None. Returning safe default payload.")
            return {
                "success": True,
                "error": None,
                "data": None
            }

        # Handle Dict types safely against concurrent modifications and broken key representations
        if isinstance(data, dict):
            processed_data = {}
            try:
                # Snapshot items to reduce impact of concurrent modification
                items_snapshot = list(data.items())
            except Exception:
                items_snapshot = []

            for k, v in items_snapshot:
                key_str = _safe_str(k)
                processed_data[key_str] = v

        # Handle sequence/collection types safely
        elif isinstance(data, (list, tuple, set, getattr(type, "frozenset", set))):
            try:
                processed_data = list(data)
            except Exception:
                # Safe fallback if iteration fails or collection is modified during iteration
                processed_data = []

        # Handle primitive types
        elif isinstance(data, (bool, int, float, str)):
            processed_data = data

        # Handle binary types safely
        elif isinstance(data, (bytes, bytearray)):
            try:
                processed_data = data.decode("utf-8", errors="replace")
            except Exception:
                processed_data = _safe_str(data)
        elif isinstance(data, memoryview):
            try:
                processed_data = data.tobytes().decode("utf-8", errors="replace")
            except Exception:
                processed_data = _safe_str(data)

        # Fallback for unhandled / custom object types
        else:
            logger.info(f"Unhandled data type received: {type(data).__name__}. Converting to string.")
            processed_data = _safe_str(data)

        return {
            "success": True,
            "error": None,
            "data": processed_data
        }

    except Exception as exc:
        exc_type = type(exc).__name__
        exc_msg = _safe_str(exc)
        logger.error(f"Unexpected runtime failure while processing input: {exc_type} - {exc_msg}", exc_info=True)
        return {
            "success": False,
            "error": f"Internal processing error: {exc_type} - {exc_msg}",
            "data": None
        }


def main() -> int:
    """
    Main execution wrapper providing clean exit codes and top-level exception handling.
    """
    # Setup logger handlers specifically for executable invocation
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    try:
        logger.info("Starting execution safely...")
        response = safe_process_input(data=None)
        
        is_success = isinstance(response, dict) and response.get("success") is True
        logger.info(f"Execution completed with status: {is_success}")
        return 0 if is_success else 1

    except Exception as fatal_error:
        fatal_msg = _safe_str(fatal_error)
        logger.critical(f"Unhandled system crash prevented in main loop: {fatal_msg}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())