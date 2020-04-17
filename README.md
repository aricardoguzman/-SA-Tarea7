# TAREA 7 -SA- 201010425
## DevOps
Herramientas utilizadas:
  - Github
  - Docker
  - Docker Hub
  - [Circleci.com](https://circleci.com/)
  - Google Compute Engine
## Instalación

Clonar el repositorio
```sh
$ mkdir tarea7 && cd tarea7
$ git clone https://github.com/aricardoguzman/-SA-Tarea7.git .
```
Se debe linkear las credenciales de cada servicio a utilizar
  - Github credentials : Se obtiene al momento de crear el proyecto en Circleci

### Configuración de CircleCI

Generar un par de llaves públicas y privadas en [8wifi.org](https://8gwifi.org/sshfunctions.jsp). Ingresar a [circleci.com/dashboard](https://circleci.com/dashboard), configuración del proyecto a utilizar y luego en SSH Permissions > ADD SSH KEY

![image info](~/Pictures/T7/img1.png)

Hostname será el nombre generado del lado de google cloud.

Además deben generarse las variables de entorno para Docker Hub, donde

  - DOCKER_LOGIN : Docker Hub username
  - DOCKER_PWD : Docker Hub password

![image info](~/Pictures/T7/img2.png)


### Explicación de archivo config.yml

Añade las llaves privadas de github y de la máquina virtual

```sh
- add_ssh_keys:
    fingerprints:
      - bf:51:12:f0:cd:ce:de:ff:d6:be:a9:57:38:46:f2:b5
      - 52:98:bc:12:a7:7b:36:5b:68:09:1c:1c:4f:c0:51:31
```

Crea variables de entorno con valores proporcionados por el software y creamos el entorno virtual necesario para correr python

```sh
  echo 'export TAG=0.1.${CIRCLE_BUILD_NUM}' >> $BASH_ENV
            echo 'export IMAGE_NAME=tarea7-sa' >> $BASH_ENV
            virtualenv helloworld
            . helloworld/bin/activate
            pip install --no-cache-dir -r requirements.txt
```
Si pasan las pruebas se hace un build de la imagen y se guarda en docker hub

```sh
    . helloworld/bin/activate
  pyinstaller -F hello_world.py
  docker build -t $DOCKER_LOGIN/$IMAGE_NAME:$TAG .
  echo $DOCKER_PWD | docker login -u $DOCKER_LOGIN --password-stdin
  docker push $DOCKER_LOGIN/$IMAGE_NAME:$TAG
```

Si todos los pasos pasan exitosamente, conectamos con GCE y corremos un script
```sh
ssh -i ~/.ssh/id_rsa_5298bc12a77b365b68091c1c4fc05131 -o StrictHostKeyChecking=no a.ricardoguzman@35.192.155.141 "/bin/bash ./deploy_app.sh $DOCKER_LOGIN/$IMAGE_NAME:$TAG"
```