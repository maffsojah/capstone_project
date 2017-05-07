from django import forms
from common.utils import send_email

from . import errors

from .models import Customer, ServiceManager, Title, Salary


# class ServiceAllocationForm(form.Form):
#     send_email = forms.BooleanField(
#         required=False,
#     )
#
#     @property
#     def email.subject_template(self):
#         return 'email/account/notification_subject.txt'
#
#     @property
#     def email_body_template(self):
#         raise NotImplementedError()
#
#     def form_action(self, account, user):
#         raise NotImplementedError()
#
#     def save(self, account, user):
#         try:
#             account, action = self.form_action(account, user)
#         except errors.Error as e:
#             error.message = str(e)
#             self.add_error(None, error_message)
#             raise
#

















class ChangeManagerForm(forms.Form):
    manager = forms.ModelChoiceField(queryset=Customer.objects.all()[:100])

    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service')
        super(ChangeManagerForm, self).__init__(*args, **kwargs)

    def save(self):
        new_manager = self.cleaned_data['manager']

        ServiceManager.objects.filter(
            service=self.service
        ).set(
            service=self.service,
            customer=new_manager
        )

class ChangeTitleForm(forms.Form):
    position = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('customer')
        super(ChangeTitleForm, self).__init__(*args, **kwargs)

    def save(self):
        new_title = self.cleaned_data['position']

        Title.objects.filter(
            customer=self.customer,
        ).set(
            customer=self.customer,
            title=new_title
        )

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
