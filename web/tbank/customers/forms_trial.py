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


# @operable
# def getAge():
#     age = 0
#     #if customer.Age == '60 +':
#     if customer.Age == Customer.objects.get(Age = "60 +"):
#         age = 0
#     #elif customer.Age == '36 - 59':
#     elif customer.Age == Customer.objects.get(Age = "36 - 59"):
#         age = 1
#     else:
#         age = 2
#     return age
#
# @operable
# def getEducation():
#     education = 0
#     if customer.Education == Customer.objects.get(Education = "Highschool and below"):
#         education = 0
#     else:
#         education = 1
#     return education
#
# @operable
# def getEmployment():
#     employment = 0
#     if customer.Employment == Customer.objects.get(Employment = "Student"):
#         employment = 0
#     elif customer.Employment == Customer.objects.get(Employment = "Contract"):
#         employment = 1
#     else:
#         employment = 2
#     return employment
#
# @operable
# def getStability():
#     stability = 0
#     if customer.Employer_Stability == Customer.objects.get(Employer_Stability = "Unstable"):
#         stability = 0
#     else:
#         stability = 1
#     return stability
#
# @operable
# def getResidential():
#     residential = 0
#     if customer.Residential_Status == Customer.objects.get(Residential_Status = "Rented"):
#         residential = 0
#     else:
#         residential = 1
#     return residential
#
# @operable
# def getSalary():
#     salary = 0
#     if customer.Salary == Customer.objects.get(Salary <= 1000):
#         salary = 0
#     elif customer.Salary == Customer.objects.get(Salary <= 10001 and Salary > 1000):
#         salary = 1
#     else:
#         salary = 2
#     return salary
#
# @operable
# def getLoyalty():
#     loyalty = 0
#     loy = Customer.objects.get(Customer_Loyalty <= 2)
#     #if customer.Customer_Loyalty == Customer.objects.get(Customer_Loyalty <= 2):
#     if customer.Customer_Loyalty == loy.Customer_Loyalty:
#         loyalty = 0
#     else:
#         loyalty = 1
#     return loyalty
#
# @operable
# def getBalance():
#     balance = 0
#     if customer.Balance == Customer.objects.get(Balance <= 2500):
#         balance = 0
#     elif customer.Balance == Customer.objects.get(Balance <= 10001 and Balance > 2500):
#         balance = 1
#     else:
#         balance = 2
#     return balance
#
#
# def feat_list():
#     total = getAge + getEducation + getEmployment + getStability + getResidential + getSalary + getLoyalty + getBalance
#     #print('total:'+ total)
#     return total

#customer = [(Customer.objects.values("Gender", "Account_Type", "Age","Education", "Employment", "Employer_Stability", "Residential_Status", "Salary", "Customer_Loyalty", "Balance").get(pk=customer.Customer_ID))]
#flist = feat_list()
# loyal = getLoyalty
# #a = getAge()
# print(flist)
# print type(flist)
# print(loyal)
# print type(loyal)
#print(a)

# if flist > 15 and flist <= 21:
#     customer.Service_Level = Service.objects.get(service_name = "Platinum Package")
#     platinum_customers.append(customer.Name)
# elif flist > 11 and flist <= 15 :
#         customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
#         gold_customers.append(customer.Name)
# elif flist > 0 and flist <= 11:
#     customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
#     silver_customers.append(customer.Name)


# if feat_list() <= 11:
#     customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
#     silver_customers.append(customer.Name)
# #elif feat_list() > 11 and feat_list() <= 15:
# elif 11 < feat_list() <= 15:
#     # customer.Service_Level = 'Silver Package'
#     customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
#     gold_customers.append(customer.Name)
# elif feat_list() > 15:
#     customer.Service_Level = Service.objects.get(service_name = "Platinum Package")
#     platinum_customers.append(customer.Name)
# else:
#     customer.Service_Level = Service.objects.get(service_name = "No Service Package")
#     non_customers.append(customer.name)



#####  PLAN B ALLOCATION


# def allocate_service(ModelAdmin, request, queryset):
#     platinum_customers = []
#     silver_customers = []
#     gold_customers = []
#     non_customers = []
#     message = ''
#
#
#
#     for customer in queryset:
#         qs = Customer.objects.all()
#         df = qs.to_dataframe(fieldnames=["Age","Education", "Employment", "Employer_Stability", "Residential_Status", "Salary", "Customer_Loyalty", "Balance", "Service_Level"])
#         #df = read_frame(qs)
#
#         df['Age'] = np.where((df['Age']== '60 +'), 0, (np.where((df['Age'] == '36 - 59'), 1, 2)))
#         df['Education'] = np.where((df['Education']== 'Highschool and below'), 0,  1)
#         df['Employment'] = np.where((df['Employment']== 'Student'), 0, (np.where((df['Employment'] == 'Contract'), 1, 0)))
#         df['Employer_Stability'] = np.where((df['Employer_Stability']== 'Unstable'), 0,  1)
#         df['Residential_Status'] = np.where((df['Residential_Status'] == 'Rented'), 0,  1)
#         df['Salary'] = np.where(((df['Salary'] >= 150) & (df['Salary'] <= 1000)), 0, (np.where(((df['Salary'] > 1000) & (df['Salary'] <= 10000)), 1, 2)))
#         df['Customer_Loyalty'] = np.where((df['Customer_Loyalty'] <= 3), 0,  1)
#         df['Balance'] = np.where(((df['Balance'] >= 150) & (df['Balance'] <= 2500)), 0, (np.where(((df['Balance'] > 2500) & (df['Balance'] <= 10000)), 1, 2)))
#
#         added = (df['Age'])+(df['Education'])+(df['Employment'])+(df['Salary'])+(df['Employer_Stability'])+(df['Customer_Loyalty'])+(df['Balance'])+(df['Residential_Status'])
#
#         silver = np.where( added <= 11)
#
#         gold = np.where(( added > 11) & (added <= 15))
#
#         platinum = np.where((added > 15) & (added <= 21))
#
#
#         print (platinum)
#         print(silver)
#         print(gold)
#
#         if silver:
#             customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
#             silver_customers.append(customer.Name)
#         elif gold:
#             customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
#             gold_customers.append(customer.Name)
#         elif platinum:
#             customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
#             platinum_customers.append(customer.Name)
#         else:
#             customer.Service_Level = Service.objects.get(service_name = "No Service Package")
#             non_customers.append(customer.name)
#
#         # else:
#         #      message = "This customer does not meet the required criteria"
#         customer.save()
#
#         if platinum_customers:
#             message = 'The following customers are now Platinum Customers: {}'.format(', '.join(platinum_customers))
#         if silver_customers:
#             message = 'The following customers are now Silver Customers: {}'.format(', '.join(silver_customers))
#         if gold_customers:
#             message = 'The following customers are now Gold Customers: {}'.format(', '.join(gold_customers))
#         if not platinum_customers and not silver_customers and not gold_customers:
#             message = 'No customer changes made!'
#         ModelAdmin.message_user(request, message, level=SUCCESS)
# allocate_service.short_description = 'Allocate Service'
