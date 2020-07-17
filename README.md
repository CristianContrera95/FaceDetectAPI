# PyAPIPeopleTracker  

### Getting Started
- Para correr la API se debe tener instalado docker en una maquina linux.  
  Luego ejeuctar el archivo: 
  ``` bash
  ./run.sh
  ```

- Si quieren ejecutar la API con conda o virtualenv, deben crear los entornos, instalar los 
paquetes que estan en requirements.txt y ejecutar el script: 
  ``` bash
  python src/run.py
  ```
  
### Usar la API
 - La API tiene dos endpoints:
   - /face_detect: Recibe una imagen y retorna una json con el nombre de la cara reconocida.
   - /face_register: Recibe una imagen y un json con el nombre de la cara, para guardala.

 - La forma de enviar la imagen a la API es en forma de archivo binario, en python eso seria:

``` python 
 import requests

url = 'http://0.0.0.0:5000/api/'

# Guardar una imagen nueva
img_path = 'Webcam_foto_fulano.jpg'
requests.post(url+'face_register', 
              data={'name': 'Cosme Fulanito'},
              files={'image': open(img_path, 'rb')}
             )
# <Response [200]>


# Detectar la persona en un imagen nueva
img_path = 'Webcam_foto_nueva.jpg'
r = requests.post(url+'face_detect',
              files={'image': open(img_path, 'rb')}
             )
# {names: ['Cosme_Fulanito']}
```
