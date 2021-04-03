from background_task import background
from logging import getLogger
logger = getLogger(__name__)

@background(schedule=1)
def demo_task(message):
    print('demo_task. message={0}'.format(message))
