#####  PLAN B ALLOCATION
def age(ModelAdmin, request, queryset):
    if customer.Age == '60 +':
        customer.Age = 0
    elif customer.Age == '36 - 59':
        customer.Age = 1
    else:
        customer.Age = 2
    return customer.Age

def education(ModelAdmin, request, queryset):
    if customer.Education == 'Highschool and below':
        customer.Education = 0
    else:
        customer.Education = 1
    return customer.Education

def employment(ModelAdmin, request, queryset):
    if customer.Employment == 'Student':
        customer.Employment = 0
    elif customer.Employment == 'Contract':
        customer.Employment = 1
    else:
        customer.Employment = 2
    return customer.Employment

def stability(ModelAdmin, request, queryset):
    if customer.Employer_Stability == 'Unstable':
        customer.Employer_Stability = 0
    else:
        customer.Employer_Stability = 1
    return customer.Employer_Stability

def residential(ModelAdmin, request, queryset):
    if customer.Residential_Status == 'Rented':
        customer.Residential_Status = 0
    else:
        customer.Residential_Status = 1
    return customer.Residential_Status

def salary(ModelAdmin, request, queryset):
    if customer.Salary <= 1000:
        customer.Salary = 0
    elif 1000 < customer.Salary <= 10001:
        customer.Salary = 1
    else:
        customer.Salary = 2
    return customer.Salary

def loyalty(ModelAdmin, request, queryset):
    if customer.Customer_Loyalty <= 2:
        customer.Customer_Loyalty = 0
    else:
        customer.Customer_Loyalty = 1
    return customer.Customer_Loyalty

def balance(ModelAdmin, request, queryset):
    if customer.Balance <= 2500:
        customer.Balance = 0
    elif 2500 < customer.Balance <= 10001:
        customer.Balance = 1
    else:
        customer.Balance = 2
    return customer.Balance

feat_list = age + education + employment + stability + residential + salary + loyalty + balance

def allocate_service(ModelAdmin, request, queryset):
    platinum_customers = []
    silver_customers = []
    message = ''

    for customer in queryset:
        if feat_list <= 11:
            customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
            silver_customers.append(customer.Name)
        elif feat_list > 11 and feat_list <= 15:
            # customer.Service_Level = 'Silver Package'
            customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            gold_customers.append(customer.Name)
        else:
             customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
             platinum_customers.append(customer.Name)
        customer.save()

        if platinum_customers:
            message = 'The following customers are now Platinum Customers: {}'.format(', '.join(platinum_customers))
        if silver_customers:
            message = 'The following customers are now Silver Customers: {}'.format(', '.join(silver_customers))
        if gold_customers:
            message = 'The following customers are now Gold Customers: {}'.format(', '.join(gold_customers))
        if not platinum_customers and not silver_customers and not gold_customers:
            message = 'No customer changes made!'
        ModelAdmin.message_user(request, message, level=SUCCESS)
allocate_service.short_description = 'Allocate Service'
