from src.mission_control.mission_control import MissionControl
from src.mission_control.mission_control import ICommandSender
from src.ui.cli import run_cli

def main():
    command_sender: ICommandSender = MissionControl()
    run_cli(command_sender)

if __name__ == "__main__":
    main()
