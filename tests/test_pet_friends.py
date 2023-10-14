import os.path

import pytest

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_email1, invalid_password, b

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_add_new_pet(name='gora', animal_type='suslik', age='1', pet_photo='images/images1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet(filter='pet_id'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Giga', 'suslik', '2', 'images/images1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()


def test_put_update_pet(name='Giga', animal_type='nosorog', age=15):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

"""Проверка входа с некорректными данными"""
def test_get_api_key_for_invalid_user_1(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

"""Проверка входа с некорректными данными"""
def test_get_api_key_for_invalid_user_2(email=invalid_email1, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

"""Проверка входа с некорректными данными"""
def test_get_api_key_for_invalid_user_3(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

""" Позволяет добавлять текстовые файлы вместо фото"""
def test_post_add_new_pet_failed_1(name='gora', animal_type='suslik', age='1', pet_photo='images/images1.txt'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


""" и даже видео"""
def test_post_add_new_pet_failed_2(name='gora', animal_type='suslik', age='1', pet_photo='images/images1.3gp'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

""" Длинные имена(>255) и спец символы допустимы"""
def test_post_add_new_pet_failed_3(name=b, animal_type='suslik', age='1', pet_photo='images/images1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

"""Проверка пустых значений"""
def test_post_add_new_pet_failed_4(name='', animal_type='', age='', pet_photo='images/images1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

"""Проверка отрицательных значений поля возраст"""
def test_post_add_new_pet_failed_5(name='', animal_type='', age='-1', pet_photo='images/images1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

"""Проверка граничных значений поля Возраст"""
def test_post_add_new_pet_failed_6(name='', animal_type='', age='1000', pet_photo='images/images1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

"""проверка допустимых значений в полях"""
def test_post_add_new_pet_failed_7(name='1', animal_type='2', age='gl', pet_photo='images/images1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


