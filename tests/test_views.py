'''
this file is part of "El Botadero"
copyright 2018 Rodrigo Garcia <rgarcia@laotra.red>
AGPL liberated.
'''
import pytest
import os
from botadero import create_app
from botadero import shared
from flask import current_app

@pytest.fixture
def app():
    app = create_app()
    return app

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

# def test_downloadNotExists(client):
#     response = client.get('/almacen/NonExistent/j8j13j4128934804jvn1FJ.nnah')
#     assert response.status_code == 404

def test_uploadFile(client):
    from botadero.utils import borrarArchivo, existeArchivo
    # armando peticion de subida de archivo de prueba
    url = '/Misc/upload_file_a'
    nombreArchivo = 'amL7c891712721799999cn1u923412341234.cv' # nombre extraño
    headers = {
        'Content-Type': 'multipart/form-data; boundary=---------------------------67471868316984729031353498406',
        'Accept:': '*/*'
    }
    # body = '-----------------------------67471868316984729031353498406\r\nContent-Disposition: form-data; name=\"file\"; filename=\"rstup.c\"\r\nContent-Type: text/x-csrc\r\n\r\n/* rstup.c\n * - Functions for initialization in ices\n * Copyright (c) 2020 testing.-----------------------------67471868316984729031353498406\r\nContent-Disposition: form-data; name=\"__ajax\"\r\n\r\ntrue\r\n-----------------------------67471868316984729031353498406--\r\n","mode":"application/json'
    body = '-----------------------------67471868316984729031353498406\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{nombreArchivo}\"\r\nContent-Type: text/x-csrc\r\n\r\n/* {nombreArchivo}\n * - Testing\n * Copyright (c) 2020 testing.-----------------------------67471868316984729031353498406\r\nContent-Disposition: form-data; name=\"__ajax\"\r\n\r\ntrue\r\n-----------------------------67471868316984729031353498406--\r\n","mode":"application/json'.format(nombreArchivo=nombreArchivo)
    response = client.post(url,
                           headers=headers,
                           data=body)
    assert response.status_code == 200
    nombreYRuta = os.path.join('./', shared.globalParams.uploadDirectory, nombreArchivo)
    # TODO: Agregar comprobacion de cuerpo de respuesta JSON
    assert borrarArchivo(nombreYRuta) is True
    assert existeArchivo(nombreYRuta) is None
    
# def test_downloadExists(client):
#     response = client.get('/almacen/Misc/.gitkeep')
#     print('==================================')
#     print(response.__dict__)
#     print('==================================')
#     assert response.status_code == 200


