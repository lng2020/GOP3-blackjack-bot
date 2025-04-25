import os
import sys
import cv2
from pyscreeze import screenshot


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def safe_imread(file_path, flag=0):
    """Read image with proper path handling"""
    return cv2.imread(resource_path(file_path), flag)


def safe_screenshot(file_path):
    """Take screenshot with proper path handling"""
    os.makedirs(os.path.dirname(resource_path(file_path)), exist_ok=True)
    screenshot(resource_path(file_path))
