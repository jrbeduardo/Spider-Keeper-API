# Python-SpiderKeeper-API

Instalar SpiderKepper del repositorio [jrbeduardo/SpiderKeeper](https://github.com/jrbeduardo/SpiderKeeper.git) con el siguiente comando:

~~~
pip install git+https://github.com/jrbeduardo/SpiderKeeper.git
~~~

Este módulo permite trabajar con la API de SpiderKeeper.

# Quick Usage

Conectarse a una instacia de SpiderKeeper. 

```python
from wrapper import SKeeperAPI
sk = SKeeperAPI('http://0.0.0.0:5001', auth=('admin', 'admin'))
```

## **Lista de proyectos**: 
`/api/projects`

```python
sk.list_projects()
```
Salida:
```
[{'project_id': 1, 'project_name': 'web_scrapers'}]
```


## **Agregar un proyecto**: 
`/api/projects`

```python
sk.add_project('My project')
```
Salida:
```
{'project_id': 2, 'project_name': 'My project'}
```

## **Lista de arañas**: 
`/api/projects/{project_id}/spiders`

```python
sk.list_spiders(1)[:3]
```

Salida:

```
[{'project_id': 1,
  'spider_instance_id': 25,
  'spider_name': 'ws_1199_campechehoy'},
 {'project_id': 1,
  'spider_instance_id': 26,
  'spider_name': 'ws_1200_novedadescampeche'},
 {'project_id': 1,
  'spider_instance_id': 27,
  'spider_name': 'ws_1201_comunicacampeche'}]
```


## **Iniciar una araña**: 
`/api/projects/{project_id}/spiders/{spider_id}`


```python
sk.run_spider(1,6)
```
Salida:
```
True
```

## **Lista de trabajos**: 
`/api/projects/{project_id}/jobs`

```python
sk.list_job_instance(1)[:1]
```

Salida:

```
[{'cron_day_of_month': '*',
  'cron_day_of_week': '*',
  'cron_hour': '*',
  'cron_minutes': '*/5',
  'cron_month': '*',
  'desc': None,
  'enabled': True,
  'job_instance_id': 14,
  'priority': 0,
  'project_id': 1,
  'run_type': 'periodic',
  'spider_arguments': '',
  'spider_name': 'quotes',
  'tags': None}]
```


## **Agregar un trabajo**: 
`/api/projects/{project_id}/jobs`

```python
sk.add_job_instance(
    1,     'ws_1201_comunicacampeche',
    cron_expression = '*/5 * * * *'
)
```
Salida:
```
True
```

## **Actualizar un trabajo**: 
`/api/projects/{project_id}/jobs/{job_id}`
```python
sk.update_job_instance(
    2, 
    3,
    'ws_1201_comunicacampeche',
    cron_expression = '*/10 * * * *'
)
```
Salida:
```
True
```
## **Detener un trabajo**: 
`/api/projects/{project_id}/jobexecs/{job_exec_id}`

Cuando el trabajo existe:
```python
sk.stop_job(1,305)
```
Salida:
```
True
```
Si el trabajo no existe o no está iniciado se puede obtener `None` o bien
```
{'code': 500,
 'data': None,
 'msg': "'NoneType' object has no attribute 'project_id'",
 'success': False}
```

## **Status de los trabajos** 
`/api/projects/{project_id}/jobexecs`

```python
sk.list_job_execution_status(1, status='RUNNING')
```
Salida:

```
[{'create_time': '2021-05-08 17:30:00',
  'end_time': None,
  'errors_count': '-',
  'has_errors': False,
  'has_warnings': True,
  'items_count': '-',
  'job_execution_id': 305,
  'job_instance': {'cron_day_of_month': '*',
   'cron_day_of_week': '*',
   'cron_hour': '*',
   'cron_minutes': '*/30',
   'cron_month': '*',
   'desc': None,
   'enabled': True,
   'job_instance_id': 15,
   'priority': 0,
   'project_id': 1,
   'run_type': 'periodic',
   'spider_arguments': '',
   'spider_name': 'ws_1202_campechealdia',
   'tags': None},
  'job_instance_id': 15,
  'project_id': 1,
  'running_on': 'http://localhost:6806',
  'running_status': 1,
  'service_job_execution_id': 'ecb45240b04c11eb867e512199d7e0d3',
  'start_time': '2021-05-08 17:30:01',
  'warnings_count': '-'}]
  ```
