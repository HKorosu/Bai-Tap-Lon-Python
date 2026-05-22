#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive CLI test with simulated user input
"""
import sys
from io import StringIO
from main import main

# Simulate user input sequence
test_input = """1
1
2
Q
0
"""

# Redirect stdin
sys.stdin = StringIO(test_input)

try:
    print("="*50)
    print("TESTING NEWS AGGREGATOR CLI")
    print("="*50)
    main()
except KeyboardInterrupt:
    print("\n✓ Test interrupted")
except EOFError:
    print("\n✓ Test completed (all input consumed)")
except SystemExit:
    print("\n✓ Application exited normally")
