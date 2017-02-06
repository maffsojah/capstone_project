# HIT_400: Bank Customer Classification System

This repo contains the PySpark code required to run the Bank Customer Classification system.  
The system classifies bank customers into 3 distinct service levels: Silver, Gold and Platinum.


### Bank Properties

The purpose of the system is for the bank to make use of customer data to enhance its marketing strategies through selling other services outside normal-banking to its customers.

#### Services Offered

0. Personal Loans
1. Money markets (Unit trusts)
2. Stocks
3. Junior Accounts: Fixed Deposit Accounts for kids
4. Fixed Deposit Accounts
5. Mortgages
6. Insurance
7. Safety Deposit
8. Offshore Banking

#### Service Levels

|   Silver (0)	| Gold (1)   	| Platinum (2)   	|
|---		|---		|---			|
|  0 - 3 	| 0 - 6   	| 0  - 8   		|


### Example data

- The Customer  dataset: contains the information about individual customers as shown;


| Field Name   	| Customer ID  	| Name  	| Gender  	| Address  	| Service  Level 	| Account Type  	|
|---		|---		|---		|---		|---		|---			|---			|
| **Type**  	| Integer  	|  String  	| Integer   	| String   	| Integer   		| Integer	  	|
| **Example**  	| 234	  	|  Terry M. 	|  1	 	| 10 Albany  	|  3	 		|   1			|


The fields are defined as follows:  

- Customer ID: a unique identifier for a customer
- Name, Gender, Address, Nationality, Account Type: the customer's associated information
- Age: the age of the customer
- Education: the customer's level of education (0 = Highschool and less, 1 = Tertiary ++)
- Employment: the customer's employment status - Permanent, Contract, Student
- Monthly Salary:
- Employer Stability: indicates the financial state of the employer - *1* Do salaries come on time? (0 = No, 1 = Yes) **AND** *2* Are the offices rented or owned? (0 = Rented, 1 = Owned )
- Consistency:  indicates how long the customer has been using the bank
- Balance: indicates the recurring bank balance of the customer - $( 20 - 2500 ), $( 2501 - 10000 ), $( 10001 ++ )
- Residential status: customer residential status (0 = rented, 1 = owned)
- Service Level: indicates the level of service - 0, 1, 2 for Silver, Gold and Platinum, respectively.


