from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data_sampling_file.models import StatiskIncidents


"""
Тест запроса к url api 
http://127.0.0.1:8000/data_sampl_file/api/stat_all_file
запись тестовых данных в тестовую зону БД, проверка 
корректности занесения в БД.
"""

class FilesApiTestCase(APITestCase):
    def test_get(self):

        file_1 = StatiskIncidents.objects.create(
            user_avtor_file = "test_voronin_1",
            id_avtor_file = 10,
            name_file = "test name file_1",
            date_file = "2022-08-05",  #формат "date_file": "2022-08-01"
            gp_all = 10,
            gp_unical = 3,
            ip_all = 10,
            ip_unical = 7,
            MAC_all = 10,
            MAC_unical = 4,
            PROBLEM_all = 10,
            PROBLEM_unical = 6
        )
        file_2 = StatiskIncidents.objects.create(
            user_avtor_file = "avoronin",
            id_avtor_file = 1,
            name_file = "test",
            date_file = "2022-08-06",  #формат "date_file": "2022-08-01"
            gp_all = 10,
            gp_unical = 4,
            ip_all = 10,
            ip_unical = 3,
            MAC_all = 10,
            MAC_unical = 5,
            PROBLEM_all = 10,
            PROBLEM_unical = 6
        )
        url = reverse('api/stat_all_file-list')
        response = self.client.get(url)
        len_data = len(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len_data, 2)