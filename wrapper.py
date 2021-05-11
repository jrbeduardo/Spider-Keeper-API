from __future__ import unicode_literals

from copy import deepcopy

from crontab import CronSlices

from . import constants
from  .client import Client
from .compat import (
    iteritems,
    urljoin
)

class SKeeperAPI(object):

    def __init__(self, target='http://0.0.0.0:5000', auth=('admin', 'admin'),
                 endpoints=None, timeout=None):
        """
        Instancias de KeeperAPI para usar.
        Args:
          target (str): hostname/port .
          auth (str, str): user/pass details. 
          timeout: es el número en segundos que se esperará para que se 
                   establesca la conexión.
        """
        client = Client()
        client.auth = auth
        self.target = target
        self.client = client

        self.timeout = timeout
        '''
        Atributo para los servicios de la API de SpiderKeeper
        '''
        self.resources = deepcopy(constants.RESOURCES)

    def _build_url(self, resource):
        """
        Se contruye la URL absoluta a partir del target y el fin de la url.
        """
        try:
            path = self.resources[resource]
        except KeyError:
            msg = 'Unknown end url `{0}`'
            raise ValueError(msg.format(resource))
        absolute_url = urljoin(self.target, path)
        return absolute_url
    
    def list_projects(self):
        """
        Lista de todos los proyectos agregados. 
        """
        url = self._build_url(constants.LIST_PROJECTS)
        return self.client.get(url, timeout=self.timeout)

    def add_project(self, project_name):
        """
        Se agrega un proyecto dado su nombre  
        """
        url = self._build_url(constants.ADD_PROJECT)
        data = {
            'project_name': project_name
        }
        return self.client.post(url, data=data, timeout=self.timeout)

    def list_spiders(self, project_id):
        """
        lista de todas las arañas de un especifico projecto. 
        """
        params = {
            'project_id': project_id
        }
        url = self._build_url(constants.LIST_SPIDERS).format_map(params)
        
        json = self.client.get(url, timeout=self.timeout)
        return json

    def spider_detail(self, project_id, spider_id):
        """
        Se obtiene la araña a partir del  project_id y su spider_instance_id 
        """
        params = {
            'project_id': project_id, 
            'spider_id': spider_id
        }
        url = self._build_url(constants.SPIDER_DETAIL).format_map(params)
        result = self.client.get(url, timeout=self.timeout)
        return result

    def run_spider(self, project_id, spider_id, spider_arguments = '', 
            priority = constants.NORMAL, tags=None, desc = None):
        """
        Se inicia una araña a partir del project_id y su spider_instance_id
        """
        params = {
            'project_id': project_id, 
            'spider_id': spider_id
        }
        url = self._build_url(constants.RUN_SPIDER).format_map(params)
        data = {
            'project_id': project_id,
            'spider_id': spider_id,
            'spider_arguments': spider_arguments,
            'priority': priority,
            'tags': tags,
            'desc': desc
        }
        return self.client.put(url, data = data, timeout=self.timeout)
     

    def list_job_instance(self, project_id):
        """
        Se obtiene una lista de todos los procesos programados en un proyecto 
        """
        params = {
            'project_id': project_id
        }
        url = self._build_url(constants.LIST_JOB_INSTANCE).format_map(params)        
        return self.client.get(url, timeout=self.timeout)
        
    def add_job_instance(self, project_id, spider_name, cron_expression=None, 
            priority = constants.NORMAL, tags=None, desc = None, enabled=0, 
            run_type = constants.PERIODIC, spider_arguments = ''):        
        """
        Se agrega un trabajo con ciertos parametros.
        Args:
          project_id (int): id del proyecto.
          spider_name (str): nombre de la araña.
          spider_arguments (str): se deben separar por ','
          priority (int): LOW -1, NORMAL 0, HIGH 1, HIGHEST 2
          tags (str): se deben separar por ','
          desc (str): descripción
          cron (str,str,str,str,str): Expersion CRON donde 
            (minutes, hour, day_of_month, day_of_week, cron_month)
          enabled (int): -1, 0
          run_type (str): 
            periodic / onetime ( si se quiere iniciar la araña inmediatamente)
        """
        cron = self.validate_cron(cron_expression)
        self.validate_priority(priority)
        self.validate_run_type(run_type)
        params = {
            'project_id': project_id
            }
        url = self._build_url(constants.ADD_JOB_INSTANCE).format_map(params)
        data = {
            'project_id': project_id,
            'spider_name': spider_name,
            'tags': tags,
            'spider_arguments': spider_arguments,
            'priority': priority,
            'desc': desc,
            'cron_minutes': cron[0],
            'cron_hour': cron[1],
            'cron_day_of_month': cron[2],
            'cron_day_of_week': cron[3],
            'cron_month': cron[4],
            'enabled': enabled,
            'run_type': run_type
        }
        return self.client.post(url, data = data, timeout=self.timeout)

    def update_job_instance(self, project_id, job_id, spider_name, 
            cron_expression=None, spider_arguments = None, priority = None, 
            tags=None, desc = None, enabled=None, run_type = None, status=None):
        """
        Se modifica un proceso de un proyecto a partir del job_id, project_id y
        el nombre de la araña.
        Args:
          project_id (int): id del proyecto.
          job_id (int): id del proceso.
          spider_arguments (str): se deben separar por ',' 
          priority (int): LOW -1, NORMAL 0, HIGH 1, HIGHEST 2
          tags (str): se deben separar por ','
          desc (str): descripción
          cron (str,str,str,str,str): Expersion CRON donde 
            (minutes, hour, day_of_month, day_of_week, cron_month)
          enabled (int): -1 / 0
          run_type (str): periodic/onetime 
          status (str):	si se pone 'run' el proceso de inicia
        """
        cron = self.validate_cron(cron_expression)
        
        params = {
            'project_id': project_id,
            'job_id': job_id
        }
        url = self._build_url(constants.UPDATE_JOB_INSTANCE).format_map(params)
        data = {
            'project_id': project_id,
            'job_id': job_id,
            'spider_name': spider_name,
            'tags': tags,
            'spider_arguments': spider_arguments,
            'priority': priority,
            'desc': desc,
            'cron_minutes': cron[0],
            'cron_hour': cron[1],
            'cron_day_of_month': cron[2],
            'cron_day_of_week': cron[3],
            'cron_month': cron[4],
            'enabled': enabled,
            'run_type': run_type,
            'status': status
        }
        return self.client.put(url, data = data, timeout=self.timeout)


    def validate_cron(self, cron_expression):
        if cron_expression is None:
            return [None]*5 
        else: 
            if not CronSlices.is_valid(cron_expression):
                msg = f'expression {cron_expression} is invalid'
                raise ValueError(msg)
            return cron_expression.split()

    def validate_run_type(self, run_type):
        if run_type not in constants.RUN_TYPE:
            msg = "Run type invalid: onetime/periodic" 
            raise ValueError(msg)

    def validate_priority(self, priority):
        if priority not in constants.PRIORITY:
            msg = f"""Priority invalid: 
            LOW = {constants.LOW}, 
            NORMAL = {constants.NORMAL}, 
            HIGH = {constants.HIGH}, 
            HIGHEST = {constants.HIGHEST} 
            """
            raise ValueError(msg)

    def list_job_execution_status(self, project_id, status=None):
        """
        Se obtiene un diccionario con lo procesos de un especifico proyecto de 
        acuerdo a su status: 
          {'COMPLETED': [], 'PENDING': [], 'RUNNING': []} 
        """
        params = {
            'project_id': project_id
            }
        url = self._build_url(
            constants.LIST_JOB_EXECUTION_STATUS).format_map(params)        
        
        if status is None:
            return self.client.get(url, timeout=self.timeout)
        elif status in constants.STATUS_JOBS:
            return self.client.get(url, timeout=self.timeout)[status]
        else:
            msg = 'status is invalid'
            raise ValueError(msg)

    def stop_job(self, project_id, job_exec_id, signal='KILL'):
        """
        Cancela un trabajo de un especifico projecto.
         Args:
          project_id (int): id del proyecto.
          job_exec_id (int): id del proceso en spiderkeeper.
        """
        params = {
            'project_id': project_id, 
            'job_exec_id': job_exec_id
        }
        post_data = {
            'signal': signal
        }
        url = self._build_url(constants.STOP_JOB).format_map(params)
        result = self.client.put(url, data=post_data, timeout=self.timeout)
        return result
