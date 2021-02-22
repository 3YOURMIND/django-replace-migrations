# django-replace-migrations

This package is an extension to djangos `makemigrations.py`.
It can be used to get rid of old migrations as an alternative to djangos `squashmigration` command.

## Reasoning

In big django projects, migration files easily pile up and get an increasing problem.
Django comes with the squashmigration command - however, it is hard to handle because of multiple reasons.
Especially, it can not handle circular dependencies - they must be resolved [manually and with great care](https://stackoverflow.com/questions/37711402/circular-dependency-when-squashing-django-migrations).

One possible solution is to:

* Delete all existing migrations
* Run `./manage.py makemigrations`, so that it creates new initial migrations
* Run `./manage.py migrate --fake [new migrations]` or `./manage.py migrate --fake-initail` on all servers.

This workflow might work fine, if you have only few (production) servers - however, it becomes hard, when you have many environments with different versions of your application.

With django-replace-migrations also creates new initial migrations, but also, additionally, adds the already existing migrations to the `replace` list of the new migration
(That list is used by `squashmigrations` as well). By doing that, faking migrations is not needed anymore.

## Warning

The new replacing migrations will not consider any `RunPython` or `RunSQL` operations.
That might be acceptable depending on your use of those operations and if you need those to prepare a fresh database.


## Installation

Run

```
pip install django-replace-migrations
```

and add `django_replace_migrations` to your list of installed apps.


## Simple Workflow

If your apps are not depending on each other, you can use django-replace-migrations like this:

```
./manage.py makemigratons --replace-all --name replace [app1, app2, ...]
```
Note, that you will need to [list all of your apps](https://stackoverflow.com/questions/4111244/get-a-list-of-all-installed-applications-in-django-and-their-attributes) explicitly - otherwise django will also try to replace migrations from dependencies.
While `--name` could be omitted, it is highly recommended to use it so that you can easily recognize the new migrations.

If for any of your apps there are not one but two or more migrations created, your apps are depending on each other (see below).

You can leave your old migrations in the codebase. Old versions will continue to use the old migrations, while fresh installations will use the newly created replace migration instead.

If you remove the old migrations later, you will need to update the dependencies in your other migrations and replace all occurrences of the old migration with the new replace migration. You can easily do that with try-and-error (`migrate` will fail and tell you which dependency is missing)


## Workflow for depending apps

Due to the way django resolves the `replace` list, it can not handle circular dependencies within apps. To prevent an error during migration, you must delete the old migrations that you replaced.

If you have your application deployed on multiple servers, you must define down to which version, you will support upgrading and only replace those migrations.

Let’s assume that our current version of the application is 3.0 and we want to get rid of all migrations prior to 2.0.

The workflow for this would be:

* `git checkout 2.0`
* create a new branch `git checkout -b 2-0-delete-migrations`
* [delete all existing migrations in your apps](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html)
* commit and note the commit hash
* `git checkout 2.0`
* create a new branch `git checkout -b 2-0-replace-migrations`
* run `./manage.py makemigrations --replace-all --name replace_2_0 [app1, app2, ...]` ([How to get all apps](https://stackoverflow.com/questions/4111244/get-a-list-of-all-installed-applications-in-django-and-their-attributes))
* commit and note the commit hash
* `git checkout [your main/feature branch]`
* `git cherry-pick [commit-hash from 2-0-delete-migrations]`
* `git cherry-pick [commit-hash from 2-0-replace-migrations]`

Now you have all migrations prior to 2.0 removed and replaced with new migrations.

That means that:

* Server database is prior 2.0 -> Migrations will not work
* Server database is after 2.0 -> Newly created replacement migrations will not run because all migrations they replace are already applied
* Server database is fresh -> Newly created replacement migrations will run.

## `makemigration.py` compatibility

This package requires deep integration into `makemigrations.py` so that I needed to copy the whole `makemigrations.py` here. Currently the version of `makemigrations.py` is copied from Django 2.1, however it is also tested with Django 3.0 and works there as well. If you encounter problems, please write what version of Django you are using.





