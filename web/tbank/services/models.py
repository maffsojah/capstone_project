# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe

from .managers import TemporalQuerySet


# Create your models here.

# class MyModel(models.Model):
#     name = models.CharField(max_length=250)

#@python_2_unicode_compatible
class ServiceLevel(models.Model):
    SERVICE_LEVELS_CHOICES = (
        (0, 'Silver'),
        (1, 'Gold'),
        (2, 'Platinum'),
    )
    service_name = models.IntegerField(choices=SERVICE_LEVELS_CHOICES)
    description = models.TextField(default='')
    pub_date = models.DateTimeField('date added')

    class Meta:
        db_table = 'service_levels'
        ordering = ['service_name']

    # def __str__(self):
    #     return self.service_name if self.service_name is not None else 'ServiceLevel'

    def __unicode__(self):
        return str(self.service_name)


# class CustomerLoyalty(models.Model):
#     CUSTOMER_LOYALTY_CHOICES = (
#         (0, '0 - 2 years'),
#         (1, '3 - 10 years')
#     )
#
#     customer_loyalty = models.IntegerField(choices=CUSTOMER_LOYALTY_CHOICES)
#
#     class Meta:
#         ordering = ['customer_loyalty']


class Customer(models.Model):
    COUNTRY_CHOICES = (
        ('', 'Country'), (244, 'Aaland Islands'), (1, 'Afghanistan'), (2, 'Albania'), (3, 'Algeria'),
        (4, 'American Samoa'), (5, 'Andorra'), (6, 'Angola'), (7, 'Anguilla'), (8, 'Antarctica'),
        (9, 'Antigua and Barbuda'), (10, 'Argentina'), (11, 'Armenia'), (12, 'Aruba'), (13, 'Australia'),
        (14, 'Austria'), (15, 'Azerbaijan'), (16, 'Bahamas'), (17, 'Bahrain'), (18, 'Bangladesh'),
        (19, 'Barbados'), (20, 'Belarus'), (21, 'Belgium'), (22, 'Belize'), (23, 'Benin'),
        (24, 'Bermuda'), (25, 'Bhutan'), (26, 'Bolivia'), (245, 'Bonaire, Sint Eustatius and Saba'),
        (27, 'Bosnia and Herzegovina'), (28, 'Botswana'), (29, 'Bouvet Island'), (30, 'Brazil'),
        (31, 'British Indian Ocean Territory'), (32, 'Brunei Darussalam'),
        (33, 'Bulgaria'), (34, 'Burkina Faso'), (35, 'Burundi'), (36, 'Cambodia'), (37, 'Cameroon'),
        (38, 'Canada'), (251, 'Canary Islands'), (39, 'Cape Verde'), (40, 'Cayman Islands'), (41, 'Central African Republic'),
        (42, 'Chad'), (43, 'Chile'), (44, 'China'), (45, 'Christmas Island'), (46, 'Cocos (Keeling) Islands'),
        (47, 'Colombia'), (48, 'Comoros'), (49, 'Congo'), (50, 'Cook Islands'), (51, 'Costa Rica'),
        (52, "Cote D'Ivoire"), (53, 'Croatia'), (54, 'Cuba'), (246, 'Curacao'), (55, 'Cyprus'),
        (56, 'Czech Republic'), (237, 'Democratic Republic of Congo'), (57, 'Denmark'), (58, 'Djibouti'), (59, 'Dominica'),
        (60, 'Dominican Republic'), (61, 'East Timor'), (62, 'Ecuador'), (63, 'Egypt'), (64, 'El Salvador'),
        (65, 'Equatorial Guinea'), (66, 'Eritrea'), (67, 'Estonia'), (68, 'Ethiopia'), (69, 'Falkland Islands (Malvinas)'),
        (70, 'Faroe Islands'), (71, 'Fiji'), (72, 'Finland'), (74, 'France, skypolitan'), (75, 'French Guiana'),
        (76, 'French Polynesia'), (77, 'French Southern Territories'), (126, 'FYROM'), (78, 'Gabon'), (79, 'Gambia'),
        (80, 'Georgia'), (81, 'Germany'), (82, 'Ghana'), (83, 'Gibraltar'), (84, 'Greece'),
        (85, 'Greenland'), (86, 'Grenada'), (87, 'Guadeloupe'), (88, 'Guam'), (89, 'Guatemala'),
        (241, 'Guernsey'), (90, 'Guinea'), (91, 'Guinea-Bissau'), (92, 'Guyana'), (93, 'Haiti'),
        (94, 'Heard and Mc Donald Islands'), (95, 'Honduras'), (96, 'Hong Kong'), (97, 'Hungary'), (98, 'Iceland'),
        (99, 'India'), (100, 'Indonesia'), (101, 'Iran (Islamic Republic of)'), (102, 'Iraq'), (103, 'Ireland'),
        (104, 'Israel'), (105, 'Italy'), (106, 'Jamaica'), (107, 'Japan'), (240, 'Jersey'),
        (108, 'Jordan'), (109, 'Kazakhstan'), (110, 'Kenya'), (111, 'Kiribati'), (113, 'Korea, Republic of'),
        (114, 'Kuwait'), (115, 'Kyrgyzstan'), (116, "Lao People's Democratic Republic"), (117, 'Latvia'), (118, 'Lebanon'),
        (119, 'Lesotho'), (120, 'Liberia'), (121, 'Libyan Arab Jamahiriya'), (122, 'Liechtenstein'), (123, 'Lithuania'),
        (124, 'Luxembourg'), (125, 'Macau'), (127, 'Madagascar'), (128, 'Malawi'), (129, 'Malaysia'),
        (130, 'Maldives'), (131, 'Mali'), (132, 'Malta'), (133, 'Marshall Islands'), (134, 'Martinique'),
        (135, 'Mauritania'), (136, 'Mauritius'), (137, 'Mayotte'), (138, 'Mexico'), (139, 'Micronesia, Federated States of'),
        (140, 'Moldova, Republic of'), (141, 'Monaco'), (142, 'Mongolia'), (242, 'Montenegro'), (143, 'Montserrat'),
        (144, 'Morocco'), (145, 'Mozambique'), (146, 'Myanmar'), (147, 'Namibia'), (148, 'Nauru'),
        (149, 'Nepal'), (150, 'Netherlands'), (151, 'Netherlands Antilles'), (152, 'New Caledonia'), (153, 'New Zealand'),
        (154, 'Nicaragua'), (155, 'Niger'), (156, 'Nigeria'), (157, 'Niue'), (158, 'Norfolk Island'),
        (112, 'North Korea'), (159, 'Northern Mariana Islands'), (160, 'Norway'), (161, 'Oman'), (162, 'Pakistan'),
        (163, 'Palau'), (247, 'Palestinian Territory, Occupied'), (164, 'Panama'), (165, 'Papua New Guinea'), (166, 'Paraguay'),
        (167, 'Peru'), (168, 'Philippines'), (169, 'Pitcairn'), (170, 'Poland'), (171, 'Portugal'),
        (172, 'Puerto Rico'), (173, 'Qatar'), (174, 'Reunion'), (175, 'Romania'), (176, 'Russian Federation'),
        (177, 'Rwanda'), (178, 'Saint Kitts and Nevis'), (179, 'Saint Lucia'), (180, 'Saint Vincent and the Grenadines'),
        (181, 'Samoa'), (182, 'San Marino'), (183, 'Sao Tome and Principe'), (184, 'Saudi Arabia'), (185, 'Senegal'),
        (243, 'Serbia'), (186, 'Seychelles'), (187, 'Sierra Leone'), (188, 'Singapore'), (189, 'Slovak Republic'),
        (190, 'Slovenia'), (191, 'Solomon Islands'), (192, 'Somalia'), (193, 'South Africa'),
        (194, 'South Georgia &amp; South Sandwich Islands'), (248, 'South Sudan'), (195, 'Spain'), (196, 'Sri Lanka'),
        (249, 'St. Barthelemy'), (197, 'St. Helena'), (250, 'St. Martin (French part)'), (198, 'St. Pierre and Miquelon'),
        (199, 'Sudan'), (200, 'Suriname'), (201, 'Svalbard and Jan Mayen Islands'), (202, 'Swaziland'),
        (203, 'Sweden'), (204, 'Switzerland'), (205, 'Syrian Arab Republic'), (206, 'Taiwan'), (207, 'Tajikistan'),
        (208, 'Tanzania, United Republic of'), (209, 'Thailand'), (210, 'Togo'), (211, 'Tokelau'), (212, 'Tonga'),
        (213, 'Trinidad and Tobago'), (214, 'Tunisia'), (215, 'Turkey'), (216, 'Turkmenistan'),
        (217, 'Turks and Caicos Islands'), (218, 'Tuvalu'), (219, 'Uganda'), (220, 'Ukraine'), (221, 'United Arab Emirates'),
        (222, 'United Kingdom'), (223, 'United States'), (224, 'United States Minor Outlying Islands'), (225, 'Uruguay'),
        (226, 'Uzbekistan'), (227, 'Vanuatu'), (228, 'Vatican City State (Holy See)'), (229, 'Venezuela'), (230, 'Viet Nam'),
        (231, 'Virgin Islands (British)'), (232, 'Virgin Islands (U.S.)'), (233, 'Wallis and Futuna Islands'),
        (234, 'Western Sahara'), (235, 'Yemen'), (238, 'Zambia'), (239, 'Zimbabwe'),
    )

    GENDER_CHOICES = (
        (0, 'Male'),
        (1, 'Female')
    )

    ACCOUNT_TYPE_CHOICES = (
        (0, 'Current Account'),
        (1, 'Savings Account')
    )

    EDUCATION_CHOICES = (
        (0, 'Highschool and below'),
        (1, 'Tertiary and above')
    )

    EMPLOYMENT_CHOICES = (
        (0, 'Student'),
        (1, 'Contract'),
        (2, 'Permanent')
    )

    EMPLOYER_STABILITY_CHOICES = (
        (0, 'Unstable'),
        (1, 'Stable')
    )

    RESIDENTIAL_STATUS_CHOICES = (
        (0, 'Rented'),
        (1, 'Owned')
    )

    AGE_CHOICES = (
        (0, '60 +'),
        (1, '36 - 59'),
        (2, '18 - 35')
    )

    CUSTOMER_LOYALTY_CHOICES = (
        (0, '0 - 2 years'),
        (1, '3 - 10 years')

    )



    Customer_ID = models.AutoField(primary_key=True)
    Service_Level = models.ForeignKey(ServiceLevel)
    Name = models.CharField(max_length=30)
    Gender = models.IntegerField(choices=GENDER_CHOICES)
    Address = models.CharField(max_length=50)
    Nationality = models.IntegerField(choices=COUNTRY_CHOICES)
    Account_Type = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES)
    Age = models.IntegerField(choices=AGE_CHOICES)
    Education = models.IntegerField(choices=EDUCATION_CHOICES)
    Employment = models.IntegerField(choices=EMPLOYMENT_CHOICES)
    Salary = models.BigIntegerField(help_text=mark_safe('&#36;'))
    Employer_Stability = models.IntegerField(choices=EMPLOYER_STABILITY_CHOICES)
    Customer_Loyalty = models.IntegerField(choices=CUSTOMER_LOYALTY_CHOICES)
    Balance = models.BigIntegerField(help_text=mark_safe('&#36;'))
    Residential_Status = models.IntegerField(choices=RESIDENTIAL_STATUS_CHOICES)

    class Meta:
        db_table = 'clients'

    def __str__(self):
        return self.Name
