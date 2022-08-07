from django.test import TestCase
from data_sampling_file.views import ViborkaText


#Тест для проверки функций из модуля views.py
class FilesViborkaTextTestCase(TestCase):
    #Проверка функции подсчета кол-ва повторений
    def test_count(self):
        test_text = "Тест1\nТест2\nТест1\nТест4\nТест2\nТест1"
        rezult_text_in = ViborkaText.count_line(test_text)
        rezult_text = ([('Тест1', 3), ('Тест2', 2), ('Тест4', 1)], 6)
        self.assertEqual(rezult_text_in, rezult_text)

    #Проверка функции подсчета уникальных
    def test_unical(self):
        test_text = "Тест1\nТест2\nТест1\nТест4\nТест2\nТест1"
        rezult_text_in = ViborkaText.unical_line(test_text)
        rezult_text = ('Тест1\nТест2\nТест4', 3)
        self.assertEqual(rezult_text_in, rezult_text)