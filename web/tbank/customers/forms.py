from django import forms

from .models import Customer #Salary # Title, ServiceManager


# class ChangeManagerForm(forms.Form):
#     manager = forms.ModelChoiceField(queryset=Customer.objects.all()[:100])
#
#     def __init__(self, *args, **kwargs):
#         self.service = kwargs.pop('service')
#         super(ChangeManagerForm, self).__init__(*args, **kwargs)
#
#     def save(self):
#         new_manager = self.cleaned_data['manager']
#
#         ServiceManager.objects.filter(
#             service=self.service
#         ).set(
#             service=self.service,
#             customer=new_manager
#         )

# class ChangeTitleForm(forms.Form):
#     position = forms.CharField()
#
#     def __init__(self, *args, **kwargs):
#         self.employee = kwargs.pop('customer')
#         super(ChangeTitleForm, self).__init__(*args, **kwargs)
#
#     def save(self):
#         new_title = self.cleaned_data['position']
#
#         Title.objects.filter(
#             customer=self.customer,
#         ).set(
#             customer=self.customer,
#             title=new_title
#         )

class ChangeSalaryForm(forms.Form):
    salary = forms.IntegerField(max_value=1000000)

    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer')
        super(ChangeSalaryForm, self).__init__(*args, **kwargs)

    def save(self):
        new_salary = self.cleaned_data['salary']

        Salary.objects.filter(
            customer=self.customer,
        ).set(
            customer=self.customer,
            salary=new_salary,
        )
