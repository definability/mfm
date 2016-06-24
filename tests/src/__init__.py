from .Face import FaceTest
from .MFM import MFMTest
from . import fitter

test_cases = [FaceTest, MFMTest] + fitter.test_cases
