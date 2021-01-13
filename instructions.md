<p align="left"><img src="https://cdn-images-1.medium.com/max/184/1*2GDcaeYIx_bQAZLxWM4PsQ@2x.png"></p>

# __ih_datamadpt1120_project_m1__

Ironhack Madrid - Data Analytics Part Time - November 2020 - Project Module 1

## **Data:**

There are 3 different datasources involved:

- **Tables (.db).** [Here](http://www.potacho.com/files/ironhack/raw_data_project_m1.db) you can find the `.db` file with the main dataset.

- **API.** We will use the API from the [Open Skills Project](http://dataatwork.org/data/).  

- **Web Scraping.** Finally, we will need to retrieve information about country codes from [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes) website.

---

## **Challenge 1:**

You need to create a **Data Pipeline** that retrieves the following table:

| Country | Job Title      | Gender (*) | Quantity | Percentage |
|---------|----------------|------------|----------|------------|
| Spain   | Data Scientist | Male       | 25       | 5%         |
| Spain   | Data Scientist | Female     | 25       | 5%         |
| ...     | ...            | ...        | ...      | ...        |
> __(*)__ This attribute won't be the same for all students. See distribution bellow in the __Further Information__ section. 


**Your project must meet the following requirements:**

- It must be contained in a GitHub repository which includes a README file that explains the aim and content of your code. You may follow the structure suggested [here](https://github.com/potacho/data-project-template).

- It must create, at least, a `.csv` file including the requested table. Alternatively, you may create an image, pdf, plot or any other output format that you may find convenient. You may also send your output by e-mail, upload it to a cloud repository, etc. 

- It must provide, at least, two options for the final user to select when executing: **(1)** To get the table for every country included in the dataset, **(2)** To get the table for a specific country imputed by the user.

**Additionally:**

- You must prepare a 3 minutes presentation (ppt, canva, etc.) to explain your project (Instructors will provide further details about the content of the presentation).

- The last slide of your presentation must include your candidate for the **'Ironhack Data Code Beauty Pageant'**. 


---

### **Bonus 1:**

| Position | Number of Pro Arguments | Number of Cons Arguments |
|----------|-------------------------|--------------------------|
| In Favor |                         |                          |
| Against  |                         |                          |
> Feel free to decide the criteria to use in order to define the concept of **Number**.

---
### **Bonus 2:**

| Education Level | Top 10 Skills | 
|-----------------|---------------|
| high            |               |                          
| medium          |               |                          
| low             |               |                          
| no education    |               |                          
> Feel free to decide the table's geometry (i.e.: the amount of columns used to show the skills).


---
### **Bonus 3:**

Any other information that you may find interesting and/or relevant!!! 


--- 

## **Further Info**

**Challenge 1 Attribute Distribution:**

- **Gender:** Ale, Basa, Gil, Lewis, Manuel, Mark, Vicky. 

- **Rural:** Castilla, Eloy, Gonzalo, Jaime, Jie, Marina, Raúl, Vázquez. 

- **Age (Dataset was taken in 2016):** Antonio, Álvaro, Clara, Emily, Irene, Miguel, Pablo, Sara.

**References:**

- [SQL Alchemy](https://docs.sqlalchemy.org/en/13/intro.html)

- [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)

- [Requests](https://requests.readthedocs.io/)

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

- [Argparse](https://docs.python.org/3.7/library/argparse.html)












 


 

