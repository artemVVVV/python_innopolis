from django.db import models


#Таблица пользователей стандартная djando, auth_user

"""
Модель для таблицы с данными в файле: 
Автор, Название файла, Общее кол-во и 
кол-во уникальных данных.
Таблица в БД data_sampling_file_statiskincidents
"""

class StatiskIncidents(models.Model):
    user_avtor_file = models.CharField(max_length=150)
    id_avtor_file = models.IntegerField()
    name_file = models.CharField(max_length=150)
    date_file = models.DateField()  #формат "date_file": "2022-08-01"
    gp_all = models.IntegerField()
    gp_unical = models.IntegerField()
    ip_all = models.IntegerField()
    ip_unical = models.IntegerField()
    MAC_all = models.IntegerField()
    MAC_unical = models.IntegerField()
    PROBLEM_all = models.IntegerField()
    PROBLEM_unical = models.IntegerField()

    class Meta:
        ordering = ['-id']


"""
Модель для таблицы с данными ТОП записей: 
инциденты, IP, MAC, проблем,
у одного файла должно быть 5 записей.
Таблица в БД data_sampling_file_topdatafile
"""

class TopDataFile(models.Model):
    top_gp = models.CharField(max_length=250)
    count_top_gp = models.IntegerField()
    top_ip = models.CharField(max_length=250)
    count_top_ip = models.IntegerField()
    top_mac = models.CharField(max_length=250)
    count_top_mac = models.IntegerField()
    top_problems = models.CharField(max_length=250)
    count_top_problems = models.IntegerField()
    #Поле для связки с таблицей data_sampling_file_statiskincidents
    file_incidendy = models.ForeignKey(StatiskIncidents, 
                on_delete=models.SET_DEFAULT, default="1", 
                related_name='file_incidendys')

    def __str__(self):
        return f"""{self.top_gp} {self.count_top_gp} 
                    {self.top_ip} {self.count_top_ip} 
                    {self.top_mac} {self.count_top_mac} 
                    {self.top_problems} {self.count_top_problems} 
                    {self.file_incidendy.user_avtor_file} 
                    {self.file_incidendy.name_file}"""