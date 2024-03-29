import os
import shutil
from datetime import datetime
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from opservatory.app import update_containers_info, update_fleet_facts
from opservatory.infrastructure.kornet_comm import KornetCommunicator
from opservatory.state.json_repo import JsonStateRepository

sched = BackgroundScheduler()

TEMP_FILES_PATH = Path(os.path.dirname(__file__)) / "infrastructure" / "ansible" / "tmp"
PROJECT_PATH = Path(os.path.dirname(__file__))
STATE_DUMP_PATH = PROJECT_PATH / "volumes" / "state.json"


@sched.scheduled_job(
    id="facts_update",
    trigger=CronTrigger.from_crontab("*/1 * * * *"),
    next_run_time=datetime.now(),
)
def update_fleet():
    logger.info("Updating fleet facts...")
    comm = KornetCommunicator()
    repo = JsonStateRepository(path=STATE_DUMP_PATH)
    fleet = update_fleet_facts(comm, repo)

    shutil.rmtree(TEMP_FILES_PATH)
    TEMP_FILES_PATH.mkdir()

    logger.info("Machines updated:", len(fleet.machines))


@sched.scheduled_job(
    id="containers_update",
    trigger=CronTrigger.from_crontab("* * * * *"),
    next_run_time=datetime.now(),
)
def update_docker_images():
    logger.info("Updating fleet business state...")
    comm = KornetCommunicator()
    repo = JsonStateRepository(path=STATE_DUMP_PATH)
    fleet = update_containers_info(comm, repo)
    logger.info("Machines updated:", len(fleet.machines))


# update_fleet()
# update_docker_images()
