# Example
# -------
#
#   hello world

import logging
from pyats import aetest

logger = logging.getLogger(__name__)

class HelloWorld(aetest.Testcase):

    @aetest.test
    def test(self):
        logger.info('Hello World!')

# main()
if __name__ == '__main__':
    # set logger level
    logger.setLevel(logging.INFO)

print("Hello World")
