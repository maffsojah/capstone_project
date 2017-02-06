# HIT_400: Bank Account Classification System

This repo contains the PySpark code required to run the Bank Account Classification system.  
The system classifies bank customers into suitable bank accounts: Basic, Silver, Gold and Platinum. The resulting classes will be assigned to new customers during account creation.

### Bank Properties

The Bank consists of 3-levels of Customer Accounts;

- **0** Basic account: the basic account with less/no charges, no extra fees and has very few/ limites benefits like (loan amounts, service times e.t.c.)

- **1** Silver account: an upgraded level with high bank charges, extra fees for the higher level of benefits (loans, service times)

- **2** Gold account: an upgraded level  with upgraded charges and extra fees for extended benefits (loans, service times, personal managers), high interest rate

- **3** Platinum account: the highest level of service, with extra fees and the highest level of benefits (loans, service times, personal managers, investement advice), highest interest rates


### Example data
- The Customer Transactions dataset: contains the information about individual customers' transaction history and demographic details

| Field Name 	| Customer ID 	| Name   	| Gender   	| Address	| Account  	| Account Status	|
|---		|---		|------		|---		|---		|---		|			|
| **Type**  	|    Integer   	|     String   	|    Integer  	|     String   	|    Integer   	|			|
| **Example**  	|       234   	|    Terry M. 	|       1	|  10 Albany   	| 	3   	|			|  


The example fields are defined as follows:  

- Customer ID: a unique identifier for a customer
- Name, Gender, Address: the customer's associated information
- Account: this shows the type of account  - 0,1,2,3 for Basic, Silver, Gold and Platinum, respectively
- Account Status: this shows whether the account is active or not (0 = inactive, 1 = active)


