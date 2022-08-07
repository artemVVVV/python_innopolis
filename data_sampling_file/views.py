from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.core.paginator import Paginator
from .forms import LoginUserForm
from .models import StatiskIncidents, TopDataFile
from .serializers import MyStatistickSerializer, MyTopSerializer
from datetime import datetime, date
from rest_framework import viewsets


"""
Класс для обработки загруженного файла
выбор ТОП популярных записей
"""

class FileAnalize():

    #Получение кол-ва строк, уникальных данных в строках и ТОП записей
    def count_top_data(data_text, line):
        list_data_text = [(i_gp.decode("utf-8")).split(',')[line] for i_gp in data_text]
        data_unical_count=dict((x, list_data_text.count(x)) for x in set(list_data_text) if list_data_text.count(x) > 0)
        top_gp = (sorted(data_unical_count.items(), key=lambda item: -item[1]))[:5]
        return len(list_data_text), len(data_unical_count), top_gp
    
    #Выборка нужных данных из файла
    def count_all(data_dano, request, name_file):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        GP_len, GP_unical, list_GP_top = FileAnalize.count_top_data(data_dano, 0)
        IP_len, IP_unical, list_IP_top = FileAnalize.count_top_data(data_dano, 1)
        MAC_len, MAC_unical, list_MAC_top = FileAnalize.count_top_data(data_dano, 2)
        PROBLEM_len, PROBLEM_unical, list_PROBLEM_top = FileAnalize.count_top_data(data_dano, 3)
        return  [
                request.user.username, request.user.id, 
                name_file, today, GP_len, GP_unical, 
                IP_len, IP_unical, MAC_len, MAC_unical, 
                PROBLEM_len, PROBLEM_unical,
                list_GP_top, list_IP_top, list_MAC_top, 
                list_PROBLEM_top
                ]


"""
Класс для добавления данных из файла в БД
данные добавляются в 2 таблицы 
data_sampling_file_statiskincidents и
data_sampling_file_topdatafile
"""

class FileToDB():

    #Получение обработанных данных, запись в БД data_sampling_file_statiskincidents
    def add_db_top(text):

        """
        Так как из text приходят списки с вложенными списками,
        то на данном этапе реализованно обращение к лементам по
        расположению элемента в списке. Списки формируются в
        классе FileAlize()
        """

        for i in range(len(text[13])):
            TopDataFile.objects.create(
                    top_gp = text[12][i][0],
                    count_top_gp = text[12][i][1],
                    top_ip = text[13][i][0],
                    count_top_ip = text[13][i][1],
                    top_mac = text[14][i][0],
                    count_top_mac = text[14][i][1],
                    top_problems = text[15][i][0],
                    count_top_problems = text[15][i][1],
                    file_incidendy = StatiskIncidents.objects.get(
                        pk=StatiskIncidents.objects.first().id)).save()
            """
            .first() Берется первый элемент из таблицы, так как
            В Модели class StatiskIncidents(models.Model) 
            сортировка по убыванию id
            """
    
    #Получение обработанных данных, запись в БД data_sampling_file_statiskincidents
    def add_db(text):

        """
        Так как из text приходит список, то на данном этапе реализованно
        обращение к элементам по расположению элемента в списке. 
        Списки формируются в классе FileAlize()
        """

        StatiskIncidents.objects.create(user_avtor_file = text[0], 
        id_avtor_file = text[1], name_file = text[2], 
        date_file = text[3], gp_all = text[4], 
        gp_unical = text[5], ip_all = text[6], 
        ip_unical = text[7], MAC_all = text[8], 
        MAC_unical = text[9], PROBLEM_all = text[10],
        PROBLEM_unical = text[11]).save()
        FileToDB.add_db_top(text)


#Обработка запроса к странице "Список всех файлов"
def all_files(request):
    contact_list = StatiskIncidents.objects.all()
    paginator = Paginator(contact_list, 5)
    page_number = request.GET.get('page')
    page_onj = paginator.get_page(page_number)

    rezult_out = {
        "paginator": paginator,
        "page_obj" : page_onj,
        "allfiles" : StatiskIncidents.objects.all().count
    }
    return render(request, "data_sampling_file/all_files.html", rezult_out)
    

"""
Класс для обработки запроса к вкладке
"Мои файлы", принимает POST запросы с 
кнопки Изменить и Удалить
"""

class MyFileStranicty(View):

    def rezult(self, dano):
        contact_list = StatiskIncidents.objects.filter(id_avtor_file=dano.user.id)
        paginator = Paginator(contact_list, 3)
        page_number = dano.GET.get('page')
        page_obj = paginator.get_page(page_number)

        rezult_out = {
                "paginator": paginator,
                "page_obj": page_obj,
                "allfiles" : StatiskIncidents.objects.all().count
            }

        return rezult_out

    def get(self, request):
        retern_out =render(request, "data_sampling_file/my_files.html", 
                                MyFileStranicty().rezult(request))
        return retern_out
    
    def post(self, request):
        new_name_file = request.POST.get("rename_new")
        id_file = request.POST.get("id_file")

        #Для изменения файла
        if new_name_file and request.POST.get("check_btn") == "update":
            rename_file = StatiskIncidents.objects.get(id=id_file)
            rename_file.name_file = new_name_file
            rename_file.save()

        #Для удаления файла
        elif id_file and request.POST.get("check_btn") == "delete":

            #Удаление файлов из БД data_sampling_file_topdatafile
            TopDataFile.objects.filter(file_incidendy_id=id_file).delete()

            #Удаление файлов из БД data_sampling_file_statiskincidents
            StatiskIncidents.objects.get(id=id_file).delete()

        retern_out = render(request, "data_sampling_file/my_files.html", 
                            MyFileStranicty().rezult(request))
        return retern_out


"""
Класс для обработки запроса при добавлении файла
GET и POST запросы
"""

class AddFile(View):
    def __init__(self):
        self.rezult_out = {"allfiles" : StatiskIncidents.objects.all().count}

    def get(self, request):
            return render(request, "data_sampling_file/add_file.html", 
                                                        self.rezult_out)


    def post(self, request):
        try:
            card_text = request.FILES['document']
            list_text = card_text.readlines()
            count = FileAnalize.count_all(list_text, request, card_text.name)
            FileToDB.add_db(count)
                    
            return render(request, "data_sampling_file/add_file.html", 
                            self.rezult_out)

        except:
            return render(request, "data_sampling_file/add_file.html", 
                            self.rezult_out)


"""
Класс для обработки запросов к странице "Отчет за период"
за период фильтруется с помощью метода 
.filter(date_file__range=(date_old, date_new))
"""

class FileToDate(View):

    def get(self, request):

        rezult_out = {
                "allfiles" : StatiskIncidents.objects.all().count,
            }

        return render(request, "data_sampling_file/file_for_date.html", 
                        rezult_out)
            

    def post(self, request):
        date_old = request.POST.get("date_old")
        date_new = request.POST.get("date_new")

        if date_old == "" or date_new == "":
            date_old = date(2005, 1, 1)
            date_new = date(2005, 3, 31)

        rezult_out = {
                "file_to_date" : StatiskIncidents.objects.filter(
                            date_file__range=(date_old, 
                            date_new)),
                "allfiles" : StatiskIncidents.objects.all().count,
            }
        return render(request, "data_sampling_file/file_for_date.html", 
                        rezult_out)


""""
Класс для обработки текста на странице "Работа с текстом"
Выборка ТОП записей, общее кол-во записей.
"""

class ViborkaText():

    #подсчет количества записей всего.
    def count_line(text_data):
        list_data_text = text_data.split('\n')

        try:
            while '' in list_data_text:
                list_data_text.remove('')
        except:
            pass

        #Вбрать ТОП 5 повторяющихся
        list_data_count=dict((x, list_data_text.count(x)) 
                            for x in set(list_data_text) 
                            if list_data_text.count(x) > 0)

        list_data_sort = (sorted(list_data_count.items(), 
                            key = lambda item: -item[1]))[:5]

        return list_data_sort, len(list_data_text)

    def unical_line(text_data):
        text_unical = text_data.split('\n')

        #Убрать повтор. эл. из списка
        unique = []
        [unique.append(text_unical) for text_unical in text_unical if 
        text_unical not in unique and text_unical != '']
        unique_len = len(unique)
        unique = '\n'.join(unique)

        return unique, unique_len
        

"""
Класс для обработки запросов на страницу 
"Работа с текстом", POST запрос выполняет из
worktotext.js с помощью Ajax
"""

class WorkToText(View):

    def get(self, request):
        rezult_out = {
                "allfiles" : StatiskIncidents.objects.all().count,
            }
        return render(request, "data_sampling_file/work_to_text.html", rezult_out)

    def post(self, request):

        data_text = request.POST.get("text_data")
        data_text_obrabotka,  all_text_len = (ViborkaText.count_line(data_text))
        data_text_unical, unical_text_len = (ViborkaText.unical_line(data_text))

        if all_text_len > 0 :

            data_text_list = ["Количество всего записей: " + 
                                str(all_text_len) +  "\n\nТОП 5 записей: "]
            for i in data_text_obrabotka:
                data_text_list.append((i[0]).replace('\r', '') + 
                " Количество повторений: "+  str(i[1]))
            data_text_list.append("\nКоличество уникальных записей: " + 
                                str(unical_text_len) + 
                                "\nВсе уникальные записи: \n" + 
                                data_text_unical)

            data_text_list = '\n'.join(data_text_list)

        else:
            data_text_list = "Нет данных"

        rezult_out = {"text_itog" : data_text_list}

        return render(request, "data_sampling_file/work_to_text.html", rezult_out)
            
            

"""
API для работы с БД
Для проекта ViewSet MyStatistickSerializer
"""

#Класс для всех запросов к файлам
class MyStatistickViewSetAdmin(viewsets.ModelViewSet):
    queryset = StatiskIncidents.objects.all()
    serializer_class = MyStatistickSerializer

#Класс для только GET запросов 
class MyStatistickViewSet(MyStatistickViewSetAdmin):
    http_method_names = ['get']

#Класс для всех запросов к ТОП инцидентам
class MyTopViewSetAdmin(viewsets.ModelViewSet):
    queryset = TopDataFile.objects.all()
    serializer_class = MyTopSerializer

#Класс для только GET запросов 
class MyTopViewSet(MyTopViewSetAdmin):
    http_method_names = ['get']

#Класс для обработки входа
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'data_sampling_file/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('my_files')

#Функционал для выхода
def logout_user(request):
    logout(request)
    return redirect('login')