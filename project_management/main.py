import datetime
import plotly.figure_factory as ff

class Task:
    """
    Класс, представляющий задачу в проекте.
    """
    def __init__(self, name, description, duration, dependencies=None):
        """
        Конструктор класса Task.

        Args:
            name (str): Название задачи.
            description (str): Описание задачи.
            duration (int): Длительность задачи в днях.
            dependencies (list, optional): Список задач, от которых зависит
                данная задача. Defaults to None.
        """
        self.name = name
        self.description = description
        self.duration = duration
        self.start_date = None  # Рассчитывается позже
        self.end_date = None    # Рассчитывается позже
        if dependencies is None:
          self.dependencies = []
        else:
          self.dependencies = dependencies
        self.completed = False

    def mark_complete(self):
        """
        Отмечает задачу как выполненную.
        """
        self.completed = True

    def __str__(self):
      return f"Task(name='{self.name}', duration={self.duration}, completed={self.completed})"

    def __repr__(self):
      return self.__str__()


class Project:
    """
    Класс, представляющий проект.
    """
    def __init__(self, name, description, start_date, end_date):
        """
        Конструктор класса Project.

        Args:
            name (str): Название проекта.
            description (str): Описание проекта.
            start_date (datetime.date): Дата начала проекта.
            end_date (datetime.date): Дата окончания проекта.
        """
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = []

    def add_task(self, task):
        """
        Добавляет задачу в проект.

        Args:
            task (Task): Задача, которую нужно добавить.
        """
        self.tasks.append(task)

    def calculate_end_date(self):
      """Вычисляет плановую дату окончания проекта, основываясь на дате
      начала проекта и продолжительности самой долгой цепочки задач.
      """

      # Простая реализация, не учитывающая выходные и праздники
      # и параллельное выполнение задач
      def get_task_chain_duration(task):
        if not task.dependencies:
          return task.duration
        else:
          max_dep_duration = 0
          for dep_task in task.dependencies:
            max_dep_duration = max(max_dep_duration,get_task_chain_duration(dep_task))
          return task.duration + max_dep_duration

      max_duration = 0
      for task in self.tasks:
          max_duration = max(max_duration, get_task_chain_duration(task))

      self.end_date = self.start_date + datetime.timedelta(days=max_duration)
    def get_gantt_data(self):
        """
        Возвращает данные для построения диаграммы Ганта.

        Returns:
            list: Список словарей, каждый из которых представляет собой
                данные для одной полосы на диаграмме Ганта.
        """
        data = []
        for task in self.tasks:
            # Находим самую раннюю дату начала для текущей задачи,
            # основываясь на датах окончания задач-предшественников.
            if task.dependencies:
                start = max([dep.end_date for dep in task.dependencies])
            else:
                start = self.start_date

            # Рассчитываем дату окончания текущей задачи.
            task.start_date = start
            task.end_date = start + datetime.timedelta(days=task.duration)

            data.append(dict(Task=task.name, Start=task.start_date, Finish=task.end_date, Resource=task.name)) #Resource нужен, если раскрашивать по задачам

        return data

    def __str__(self):
      return f"Project(name='{self.name}', start_date={self.start_date}, end_date={self.end_date}, tasks={self.tasks})"
    def __repr__(self):
      return self.__str__()



def create_sample_project():
    """
    Создает тестовый проект с несколькими задачами.

    Returns:
        Project: Тестовый проект.
    """
    # Создаем задачи
    task1 = Task("Подготовка площадки", "Очистка и выравнивание участка", 3)
    task2 = Task("Фундамент", "Заливка фундамента", 5, dependencies=[task1])
    task3 = Task("Стены", "Возведение стен", 10, dependencies=[task2])
    task4 = Task("Крыша", "Монтаж крыши", 7, dependencies=[task3])
    task5 = Task("Отделка", "Внутренняя и внешняя отделка", 15, dependencies=[task3])

    # Создаем проект
    project = Project("Строительство дома", "Одноэтажный дом с мансардой",
                      datetime.date(2024, 1, 15), datetime.date(2024, 5, 15))

    # Добавляем задачи в проект
    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)
    project.add_task(task4)
    project.add_task(task5)

    return project

def create_gantt_chart(project):
    """
    Создает диаграмму Ганта для заданного проекта.

    Args:
        project (Project): Проект, для которого нужно построить диаграмму.

    Returns:
        plotly.figure_factory._gantt.Figure: Объект диаграммы Ганта.
    """
    df = project.get_gantt_data()
    fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True) #Добавлен group_tasks=True
    return fig

if __name__ == "__main__":
    project = create_sample_project()
    # project.calculate_end_date() #Удалено, так как теперь это делается внутри get_gantt_data()
    fig = create_gantt_chart(project)
    fig.show()