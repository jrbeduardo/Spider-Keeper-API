from __future__ import unicode_literals

# Nombre de operaciones

LIST_PROJECTS = 'list_projects'
ADD_PROJECT = 'add_project'
LIST_SPIDERS = 'list_spiders'
SPIDER_DETAIL = 'spider_detail'
RUN_SPIDER = 'run_spider'
LIST_JOB_INSTANCE = 'list_job_instance'
ADD_JOB_INSTANCE = 'add_job_instance'
UPDATE_JOB_INSTANCE = 'update_job_instance'
LIST_JOB_EXECUTION_STATUS = 'list_job_execution_status'
STOP_JOB = 'stop_job'


# Recursos de la API de SipderKeeper

RESOURCES = {
    LIST_PROJECTS: '/api/projects',
    ADD_PROJECT: '/api/projects',
    LIST_SPIDERS: '/api/projects/{project_id}/spiders',
    SPIDER_DETAIL: '/api/projects/{project_id}/spiders/{spider_id}',
    RUN_SPIDER: '/api/projects/{project_id}/spiders/{spider_id}',
    LIST_JOB_INSTANCE: '/api/projects/{project_id}/jobs',
    ADD_JOB_INSTANCE: '/api/projects/{project_id}/jobs',
    UPDATE_JOB_INSTANCE: '/api/projects/{project_id}/jobs/{job_id}',
    LIST_JOB_EXECUTION_STATUS: '/api/projects/{project_id}/jobexecs',
    STOP_JOB: '/api/projects/{project_id}/jobexecs/{job_exec_id}'
}


# Prioridad de cada proceso
LOW, NORMAL, HIGH, HIGHEST = range(-1, 3)
PRIORITY = [LOW, NORMAL, HIGH, HIGHEST]


# Frecuencia del proceso

PERIODIC, ONETIME = 'periodic', 'onetime'
RUN_TYPE = [PERIODIC, ONETIME]


# status de los procesos

PENDING, RUNNING, COMPLETED = 'PENDING', 'RUNNING', 'COMPLETED'
STATUS_JOBS = [PENDING, RUNNING, COMPLETED]