# Definir la imagen Base
FROM python:3.9-slim

# actualizar pip e instalar Jupiter notebook
RUN pip3 install --upgrade pip && \
    pip3 install notebook==6.5.6

#Se define el directorio.
WORKDIR /workspace    

# Se crea el directorio donde se guardara las configuraciones
RUN mkdir -p /root/.jupyter

# Agregar las configuraciones basicas
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py

# Puerto de exposicion
EXPOSE 8888

#Inicio del contenedor
CMD [ "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root" ]