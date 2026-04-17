#Definir la imagen base
from ubuntu:20.04

#Activar una ariable de entorno del sistema operativo:
ENV DEBIAN_FRONTEND=noninteractive

#Generar actualizaciones del sistema y se instalan algunos paquetes
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    wget && \
    apt-get clean


#actualizar pip e instalar Jupiter notebook
RUN pip3 install --upgrade pip && \
    pip3 install notebook==6.5.6

#se define
WORKDIR /workspace


#Se crea el directorio donde se guardaran las configuraciones de jupiter notebook
RUN mkdir -p /root/.jupyter

#Configuraciones de entorno jupiter
run echo "c.NotebookApp.token =''">> /root/.jupyter/jupyter_notebook_config.py \
    echo "c.NotebookApp.password =''">> /root/.jupyter/jupyter_notebook_config.py \
    echo "c.NotebookApp.open_browser =False">> /root/.jupyter/jupyter_notebook_config.py \
    echo "c.NotebookApp.allow_root =True">> /root/.jupyter/jupyter_notebook_config.py 

#Puerto de exposicion
expose 8888

#Inicia el contenedor
CMD ["jupyter", "notebook", "--ip=0.0.0.0"."--port=8888", "--no-browser","--allow-root"]