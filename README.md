# REST API Boilerplate
**A simple REST API developed using [Flask](https://flask.palletsprojects.com/en/1.1.x/):smile:**

&nbsp;
[![instagram](http://img.shields.io/website?label=iamdonmathew&color=green&?&logo=instagram&down_message=follow&up_message=follow&logoColor=white&style=for-the-badge&url=https://www.instagram.com/iamdonmathew)](https://www.instagram.com/iamdonmathew/)
[![linkedin](http://img.shields.io/website?label=iamdonmathew&color=green&?&logo=linkedin&down_message=follow&up_message=follow&logoColor=white&style=for-the-badge&url=https://www.linkedin.com/in/iamdonmathew/)](https://www.linkedin.com/in/iamdonmathew/)

&nbsp;
## Initial Setup

* Clone the repository
```bash
git clone https://github.com/iamdonmathew/Flask-REST-API.git
```
* Install the dependencies
```bash
pip install -r requirements.txt
```
* Create a **.env** file
* Inside the file, create 2 environment variables:
    1. **SQLDATABASE_URI**     _It's a URL for SQL Database eg: sqlite:///data.db_
    2. **TRACK_MODIFICATIONS = True**
    3. **SECRET_KEY**     _It's a secret key for [JWT](https://jwt.io/)._
    4. **CLOUD_NAME**     _It's a storage name on [Cloudinary](https://cloudinary.com/)._
    5. **API_KEY**     _It's a API key of [Cloudinary](https://cloudinary.com/) storage._
    6. **API_SECRET**     _It's a secret key of [Cloudinary](https://cloudinary.com/) storage._
* Thats, it.

&nbsp; 
## To Run

* Commmand
```bash
flask run
```

&nbsp;
**Peace**:v:
