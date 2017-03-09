from os.path import join, dirname, exists, isfile
import string
from random import SystemRandom
import environ
from fabric.api import local, task, abort, settings
from fabric.colors import green


@task()
def build_images():
    # if not get_debug_value():
    #     try:
    #         backup_mysql()
    #     except Exception as e:
    #         print("Error occurred: %s" % e)
    #         exit(1)
    django_secret_key = generate_key()
    django_settings_module = get_env_value('DJANGO_SETTINGS_MODULE')
    database_user = get_env_value('DATABASE_USER')
    database_pass = get_env_value('DATABASE_PASSWORD')
    database = get_env_value('DATABASE_NAME')
    pgpassword = get_env_value('PGPASSWORD')
    print("\nDJANGO_SETTINGS_MODULE: ", django_settings_module)
    print("\n==============Building images==============\n")
    build_postgres_image(database_user, database_pass, database, pgpassword)
    build_uwsgi_image(django_secret_key)
    build_nginx_image()


def get_env_value(key):
    env = environ.Env()
    env_file = join(dirname(__file__), "src/mysana/settings/local.env")
    if exists(env_file):
        environ.Env.read_env(str(env_file))

    return env('%s' % key)


@task()
def up():
    web_host = get_env_value('WEB_HOST')
    network = get_env_value('AWS_NETWORK')
    set_env("WEB_HOST", web_host)
    set_env("AWS_NETWORK", network)
    replace_network()
    example_file_conversion("mysana.settings.local.env.example")
    local('docker-compose up -d')
    place_network()


def replace_network():
    local('sed -i.bak "s/{{AWS_NETWORK}}/$AWS_NETWORK/" docker-compose.yml')


def place_network():
    local('sed -i.bak "s/$AWS_NETWORK/{{AWS_NETWORK}}/" docker-compose.yml')


@task()
def status():
    web_host = get_env_value('WEB_HOST')
    network = get_env_value('AWS_NETWORK')
    set_env("WEB_HOST", web_host)
    set_env("AWS_NETWORK", network)
    replace_network()
    local('docker-compose ps')
    place_network()


@task()
def logs(container='mysana-uwsgi'):
    local('docker logs %s' % container)


@task()
def bash(container='mysana-uwsgi', command=""):
    local('docker exec -it %s bash %s' % (container, command))


@task()
def down():
    web_host = get_env_value('WEB_HOST')
    network = get_env_value('AWS_NETWORK')
    set_env("WEB_HOST", web_host)
    set_env("AWS_NETWORK", network)
    replace_network()
    local('docker-compose down')
    place_network()


@task()
def restart():
    print("\n===============Rebooting the containers==============\n")
    print("\n===============Shutting down the container===============\n")
    down()

    print("\n===============Containers are starting up===============\n")
    up()
    # clean()
    print("\n===============The status of the containers===============\n\n   ")
    status()

    # if not get_debug_value():
    #     restore_mysql()


@task()
def clean():
    print("\n===============cleaning the unused containers===============\n")
    try:
        local('docker rmi -f $(docker images -q -f dangling=true)')
    except:
        pass
    try:
        local('docker volume rm $(docker volume ls -qf dangling=true)')
    except:
        pass


@task()
def reboot(container="mysana-uwsgi"):
    local('docker restart %s' % container)


def build_uwsgi_image(django_secret_key):
    if django_secret_key is None:
        abort("Please provide the django_secret_key; Usage: fab build_uwsgi_image:"
              "django_secret_key='^141&epfu9xc1)ou_^qnx$uo4-z*n3a#s=d2lqutulog2o%!yu'"
              "django_settings_module='mysana.settings.development")

    print("\n==============Building mysana-uwsgi image==============\n")

    local("docker build --build-arg DJANGO_SECRET_KEY={key} "
          "-f dockerify/uwsgi/Dockerfile "
          "-t mysana-uwsgi .".format(key=django_secret_key))


def generate_key():
    return "".join([SystemRandom().choice(string.ascii_letters + string.digits)
                    for _ in range(50)])


def example_file_conversion(example_file):
    actual_file = example_file.split(".example")[0]
    if not exists(actual_file):
        return None

    if isfile(actual_file):
        print(green('%s file already exists. Not copying %s to %s \n' % (actual_file, example_file, actual_file)))

        # Doing this because `diff` package returns exit code 1
        # when there are differences, which causes the script
        # to abort.
        with settings(warn_only=True):
            output = local('diff -w -B -u %s %s' % (actual_file, example_file))

            # Return code of diff will be 1 if files differ else it will 0
            # For errors the code will be greater than 1.
            if output.return_code == 1:
                print(green('%s and %s files differ \n') % (actual_file, example_file))

    else:
        local('cp %s %s' % (example_file, actual_file))


def build_nginx_image():
    print("\n==============Building mysana-nginx image==============\n")
    local('docker build -f dockerify/nginx/Dockerfile -t mysana-nginx .')


def get_debug_value():
    debug = get_env_value('DEBUG')
    if debug == 'True':
        return True
    else:
        return False


def build_postgres_image(database_user, database_pass, database_name, pgpassword):
    print("\n==============Building mysana-postgres image==============\n")
    local("docker build --build-arg DATABASE_USER={} --build-arg DATABASE_PASSWORD={} "
          "--build-arg DATABASE_NAME={} --build-arg PGPASSWORD={} "
          "-f dockerify/postgres/Dockerfile -t mysana-postgres .".format(
        database_user, database_pass, database_name, pgpassword
    ))


def set_env(key, value):
    local('export %s=%s' % (key, value))
