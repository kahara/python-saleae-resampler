=============================
python-saleae-resampler
=============================

My "brilliant" desc

Docker
------

For more controlled deployments and to get rid of "works on my computer" -syndrome, we always
make sure our software works under docker.

It's also a quick way to get started with a standard development environment.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"

Creating a development container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build image, create container and start it (switch the 1234 port to the port from src/saleae_resampler/defaultconfig.py)::

    docker build --ssh default --target devel_shell -t saleae_resampler:devel_shell .
    docker create --name saleae_resampler_devel -p 1234:1234 -v `pwd`":/app" -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` saleae_resampler:devel_shell
    docker start -i saleae_resampler_devel

pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i saleae_resampler_devel /bin/bash -c "pre-commit install"
    docker exec -i saleae_resampler_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run -it --rm -v `pwd`":/app" saleae_resampler:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t saleae_resampler:tox .
    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` saleae_resampler:tox

Production docker
^^^^^^^^^^^^^^^^^

There's a "production" target as well for running the application (change the "1234" port and "myconfig.toml" for
config file)::

    docker build --ssh default --target production -t saleae_resampler:latest .
    docker run -it --name saleae_resampler -v myconfig.toml:/app/config.toml -p 1234:1234 -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` saleae_resampler:latest


Local Development
-----------------

TODO: Remove the repo init from this document after you have done it.

TLDR:

- Create and activate a Python 3.7 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p `which python3.7` my_virtualenv

- Init your repo (first create it on-line and make note of the remote URI)::

    git init
    git add .
    git commit -m 'Cookiecutter stubs'
    git remote add origin MYREPOURI
    git push origin master

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    pre-commit install
    pre-commit run --all-files

- Ready to go, try the following::

    saleae_resampler --defaultconfig >config.toml
    saleae_resampler -vv config.toml

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).

Running "pre-commit run --all-files" and "py.test -v" regularly during development and
especially before committing will save you some headache.

Python 3.6
----------

TODO: Remove this section if not using 3.6, reword it for your project if you are.

It's possible to support Python3.6 but unless you absolutely have to, don't: it makes your
code less readable.

See pyproject.toml for the changes you need to do in there, tox.ini and Dockerfile. You will also need
to remove all "from __future__ import annotations" and then all type hints that need said
feature need to be converted into the string format and possibly you need to disable pylint
warnings about unused imports here and there.

Finally remember to use "asyncio.get_event_loop().create_task" instead of "asyncio.create_task"
or preferable just use self.create_task in the service since it handles task tracking.
