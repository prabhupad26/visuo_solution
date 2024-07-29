### Experiment module for testing and evaluating prompts for text-to-SQL generation

#### Prerequisites:
1. Download & Install Docker
2. (Optional) Sign up for [together ai](https://www.together.ai/) account.
3. (Optional) Download the LLama3 70B model from huggingface and run the [llama.cpp server](https://github.com/allenporter/llama-cpp-server) for hosting the LLM locally. Then provide the localhost url in `config.yml`
4. `git clone [https://github.com/prabhupad26/visuo_solution](https://github.com/prabhupad26/visuo_solution.git)`
5. `cd inference`

#### Build and run the application
1. To build the docker image, run the below cmd: `docker build -t q2sql-app-inference .`
Run:
``docker run -p 5001:5001 -e TOGETHER_API_KEY="you llm api key" -e WANDB_API_KEY="your wandb api key" q2sql-app-inference``
2. To debug : 
``docker run -it -p 5001:5001 -e TOGETHER_API_KEY="your llm api key" -e WANDB_API_KEY="your wandb api key" q2sql-app-inference /bin/bash``

Please make sure to provide the correct data path and api tokens in the commands.

Test test use postman or the below curl cmd: 

```
curl -X POST https://api.together.xyz/v1 \
-H "Content-Type: application/json" \
-d '{
  "schema_info": "CREATE TABLE frpm (CDSCode TEXT, Academic Year TEXT, County Code TEXT, District Code TEXT, School Code TEXT, County Name TEXT, District Name TEXT, School Name TEXT, District Type TEXT, School Type TEXT, Educational Option Type TEXT, NSLP Provision Status TEXT, Charter School (Y/N) TEXT, Charter School Number TEXT, Charter Funding Type TEXT, IRC TEXT, Low Grade TEXT, High Grade TEXT, Enrollment (K-12) TEXT, Free Meal Count (K-12) TEXT, Percent (%) Eligible Free (K-12) TEXT, FRPM Count (K-12) TEXT, Percent (%) Eligible FRPM (K-12) TEXT, Enrollment (Ages 5-17) TEXT, Free Meal Count (Ages 5-17) TEXT, Percent (%) Eligible Free (Ages 5-17) TEXT, FRPM Count (Ages 5-17) TEXT, Percent (%) Eligible FRPM (Ages 5-17) TEXT, 2013-14 CALPADS Fall 1 Certification Status TEXT, PRIMARY KEY (['CDSCode']));\nCREATE TABLE satscores (cds TEXT, rtype TEXT, sname TEXT, dname TEXT, cname TEXT, enroll12 TEXT, NumTstTakr TEXT, AvgScrRead TEXT, AvgScrMath TEXT, AvgScrWrite TEXT, NumGE1500 TEXT, PRIMARY KEY (['cds']));\nCREATE TABLE schools (CDSCode TEXT, NCESDist TEXT, NCESSchool TEXT, StatusType TEXT, County TEXT, District TEXT, School TEXT, Street TEXT, StreetAbr TEXT, City TEXT, Zip TEXT, State TEXT, MailStreet TEXT, MailStrAbr TEXT, MailCity TEXT, MailZip TEXT, MailState TEXT, Phone TEXT, Ext TEXT, Website TEXT, OpenDate TEXT, ClosedDate TEXT, Charter TEXT, CharterNum TEXT, FundingType TEXT, DOC TEXT, DOCType TEXT, SOC TEXT, SOCType TEXT, EdOpsCode TEXT, EdOpsName TEXT, EILCode TEXT, EILName TEXT, GSoffered TEXT, GSserved TEXT, Virtual TEXT, Magnet TEXT, Latitude TEXT, Longitude TEXT, AdmFName1 TEXT, AdmLName1 TEXT, AdmEmail1 TEXT, AdmFName2 TEXT, AdmLName2 TEXT, AdmEmail2 TEXT, AdmFName3 TEXT, AdmLName3 TEXT, AdmEmail3 TEXT, LastUpdate TEXT, PRIMARY KEY (['CDSCode']));",
  "question": "What is the highest eligible free rate for K-12 students in the schools in Alameda County?",
  "external_knowledge": "Eligible free rate for K-12 = `Free Meal Count (K-12)` / `Enrollment (K-12)`"
}'

```
#### Some inference results: 

![image](https://github.com/user-attachments/assets/d86f149b-96a1-46b1-ab92-12d72f9f3690)
