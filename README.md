# Inspector-D.B.
A database inspector application, focused on applications in the cloud, specifically Cloud Foundry  
![build](https://travis-ci.org/asherbar/InspectorDB.svg?branch=master)
[![codecov](https://codecov.io/gh/asherbar/InspectorDB/branch/master/graph/badge.svg)](https://codecov.io/gh/asherbar/InspectorDB)[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ebad02177e8b423f82dde15521bf9c7e)](https://www.codacy.com/app/asherbar/Inspector-D.B.?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=asherbar/Inspector-D.B.&amp;utm_campaign=Badge_Grade)
## Run in Cloud Foundry
1.  Clone this repository
1.  Create a manifest (see next section for more on how this manifest should look) and put it in the root directory of this repository.
1.  Run `cf push`

## Manifest
For the application to run in CF a [manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html) is required. The following manifest.yml is a template for such a manifest:
```yaml
---
applications:
- name: inspector-db
  command: python manage.py collectstatic --noinput && gunicorn project.wsgi:application
  services:
  -   <YOUR POSTGRES SERVICE INSTANCE NAME>
  env:
    SECRET_KEY: '<YOUR SECRET KEY>'
  buildpacks:
  -   https://github.com/cloudfoundry/python-buildpack#v1.6.25
  ```
Where:
-   `<YOUR POSTGRES SERVICE INSTANCE NAME>` is the name of the Postgres instance you want to inspect (optional. You can also [bind](https://docs.cloudfoundry.org/devguide/services/managing-services.html#bind) it to the app later.
-   `<YOUR SECRET KEY>` is your secret key. This is [required](https://docs.djangoproject.com/en/2.1/ref/settings/#secret-key) and its value shouldn't be shared. You can generate your own [here](https://www.miniwebtool.com/django-secret-key-generator/).
## Options
-   READONLY- when set to 0 (which is read as _false_) allows the user to execute write commands (such as UPDATE, DROP TABLE etc.). If not set the default is 1 which is read as _true_ which limits the user to execute read-only commands (such as SELECT).
