#!/usr/bin/env python3
import unittest

# Discover all the tests
tests = unittest.TestLoader().discover('tests')

# Run the tests
unittest.TextTestRunner(verbosity=2).run(tests)
