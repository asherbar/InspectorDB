# Inspector-D.B.
A database inspector application, focused on applications in the cloud, specifically Cloud Foundry
# Run in Cloud Foundry
1. Clone this repository
1. Create a manifest (see next section for more on how this manifest should look) and put it in the root directory of this repository.
1. Run `cf push`

## Manifest
For the application to run in CF a [manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html) is required. The following manifest.yml is a template for such a manifest:
```
---
applications:
- name: inspector-db
  command: python manage.py collectstatic --noinput && gunicorn project.wsgi:application
  services:
  - <YOUR POSTGRES SERVICE INSTANCE NAME>
  env:
    SECRET_KEY: '<YOUR SECRET KEY>'
  buildpacks:
  - https://github.com/cloudfoundry/python-buildpack#v1.6.25
  ```
Where:
- `<YOUR POSTGRES SERVICE INSTANCE NAME>` is the name of the Postgres instance you want to inspect (optional. You can also [bind](https://docs.cloudfoundry.org/devguide/services/managing-services.html#bind) it to the app later.
- `<YOUR SECRET KEY>` is your secret key. This is [required](https://docs.djangoproject.com/en/2.1/ref/settings/#secret-key) and its value shouldn't be shared. You can generate your own [here](https://www.miniwebtool.com/django-secret-key-generator/).
