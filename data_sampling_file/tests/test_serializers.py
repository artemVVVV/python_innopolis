from django.test import TestCase
from data_sampling_file.models import StatiskIncidents
from data_sampling_file.serializers import MyStatistickSerializer


"""
Тест Сериализатора, при изменении StatiskIncidents, 
прохождение теста будет с ошибкой.
"""

class StatiskIncidentsSerializerTestCase(TestCase):
    def test_ok(self):
        file_1 = StatiskIncidents.objects.create(
            user_avtor_file = "test_voronin",
            id_avtor_file = 10,
            name_file = "test name file",
            date_file = "2022-08-05",  #формат "date_file": "2022-08-01"
            gp_all = 10,
            gp_unical = 3,
            ip_all = 10,
            ip_unical = 7,
            MAC_all = 10,
            MAC_unical = 4,
            PROBLEM_all = 10,
            PROBLEM_unical = 6,
        )
        file_2 = StatiskIncidents.objects.create(
            user_avtor_file = "test_voronin_2",
            id_avtor_file = 5,
            name_file = "test name file_2",
            date_file = "2022-08-06",  #формат "date_file": "2022-08-01"
            gp_all = 10,
            gp_unical = 4,
            ip_all = 10,
            ip_unical = 3,
            MAC_all = 10,
            MAC_unical = 5,
            PROBLEM_all = 10,
            PROBLEM_unical = 6,
        )
        data = MyStatistickSerializer([file_1, file_2], many=True).data
        expected_data = [
            {
                "id" : file_1.id,
                "user_avtor_file" : "test_voronin",
                "id_avtor_file" : 10,
                "name_file" : "test name file",
                "date_file" : "2022-08-05",  #формат "date_file": "2022-08-01"
                "gp_all" : 10,
                "gp_unical" : 3,
                "ip_all" : 10,
                "ip_unical" : 7,
                "MAC_all" : 10,
                "MAC_unical" : 4,
                "PROBLEM_all" : 10,
                "PROBLEM_unical" : 6,
            }, 
            {
                "id" : file_2.id,
                "user_avtor_file" : "test_voronin_2",
                "id_avtor_file" : 5,
                "name_file" : "test name file_2",
                "date_file" : "2022-08-06",  #формат "date_file": "2022-08-01"
                "gp_all" : 10,
                "gp_unical" : 4,
                "ip_all" : 10,
                "ip_unical" : 3,
                "MAC_all" : 10,
                "MAC_unical" : 5,
                "PROBLEM_all" : 10,
                "PROBLEM_unical" : 6,
            }
        ]
        self.assertEqual(expected_data, data)