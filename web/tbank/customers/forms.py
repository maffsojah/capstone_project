from django import forms

from .models import Employee, ServiceManager, Title, Salary


class ChangeManagerForm(forms.Form):
    manager = forms.ModelChoiceField(queryset=Employee.objects.all()[:100])

    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service')
        super(ChangeManagerForm, self).__init__(*args, **kwargs)

    def save(self):
        new_manager = self.cleaned_data['manager']

        ServiceManager.objects.filter(
            service=self.service
        ).set(
            service=self.service,
            employee=new_manager
        )


class ChangeTitleForm(forms.Form):
    position = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')
        super(ChangeTitleForm, self).__init__(*args, **kwargs)

    def save(self):
        new_title = self.cleaned_data['position']

        Title.objects.filter(
            employee=self.employee,
        ).set(
            employee=self.employee,
            title=new_title
        )


class ChangeSalaryForm(forms.Form):
    salary = forms.IntegerField(max_value=1000000)

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')
        super(ChangeSalaryForm, self).__init__(*args, **kwargs)

    def save(self):
        new_salary = self.cleaned_data['salary']

        Salary.objects.filter(
            employee=self.employee,
        ).set(
            employee=self.employee,
            salary=new_salary,
        )