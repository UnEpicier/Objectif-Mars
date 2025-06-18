
from MissionControl import MissionControl
from Rover import Rover


if __name__ == '__main__':
	network = None

	rover = Rover(network)
	missionControl = MissionControl(network)

	missionControl.start()
	