# Correlation-Analysis-Amazon-Customer-Reviews

## Project Overview

### General Description
I performed correlation analysis on whether vine reviews had an impact on the star rating of a product from a [Kaggle Amazon Customer Review Dataset](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset). Amazon vine is an invitation-only program that selects the most insightful reviewers to allow them to order items free of charge and share their product experiences with Amazon customers. I wanted to determine if there was a bias in vine reviews due to getting items for free by looking at the star rating given. 

### Motivation
This project was a group project assigned in my Data Mining class at my university. My teammates and I divided the project by each doing different data mining tasks on the Amazon Customer Review Dataset. I chose to do correlation analysis becauese while my group members and I were going through the dataset we discovered the attribute known as [_vine_](https://www.amazon.com/vine/about). We decided to look into what vine was and we realized that we could maybe find some interesting correlation between whether a review was written by a vine member were given higher ratings in their reviews of a product than non-vine members. 

## Installation 

### Prerequisites
***IDE*** -  You will need a program to view and edit code. We recommend Visual Studio Code.
- Download from the [Visual Studio Website](https://code.visualstudio.com/download)
- Unzip the files and run the installation

***PYTHON*** - This program is written in Python and uses libraries such as pandas, numpy, matplotlib, seaborn, scipy, and duckdb. 
- Download from the [Python Website](https://www.python.org/downloads/)
- Unzip the files and run the installation
- Make sure to add Python as a PATH variable. [Link on how?](https://realpython.com/add-python-to-path/)

***DATASET*** - The dataset is available for download on Kaggle which is linked [here](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset). I recommend importing it to a duckdb database which is what we did for our project. The DuckDB documentation link is provided down below. Make sure to have the database file in the amazon_reviews folder along with the correlation.py file.

### Quick Startup
  - Clone the repository:
    ```
    git clone https://github.com/joshua-frey-wsu/Correlation-Analysis-Amazon-  
    Customer-Reviews.git
    ```
  - Navigate to the root directory of the project.
  - Change into the amazon_reviews directory.
  - Add database file in the directory.
  - Type to following command to run the code:
    ```python3 correlation.py```
    
### Manual Startup/Manual Recreation
If you prefer to explore manually or recreate this project on your own.

1. Install pip (Windows):
   Terminal:
   ```python get-pip.py```
   [Link on how for different Operating Systems of installation methods]      (https://pip.pypa.io/en/stable/installation/)

2. Create Virtual Environment:
    - Using Terminal:
      ```
      python3 -m venv venv
      source venv/bin/activate
      ```
    - Using VSCode:
      [Link on How](https://code.visualstudio.com/docs/python/environments)
      
3. Install Python Libraries in Virtual Environment:
     - Pandas:
       ```pip install pandas```
     - NumPy:
       ```pip install numpy```
     - matplotlib:
       ```
       python -m pip install -U pip
       python -m pip install -U matplotlib
       ```
     - seaborn:
       ```pip install seaborn```
     - SciPy:
       ```python -m pip install scipy```
     - DuckDB:
       ```pip install duckdb --upgrade```
  4. DuckDB:
     
     My group member imported the dataset from Kaggle as a single DuckDB database.   
     DuckDB can be used to retrieve subsets of data using SQL commands in the language 
     of our choice. If Python is the language of choice then the link to the     
     documentation is [here]  (https://duckdb.org/docs/api/python/overview).
     If you want to use a different programming language or just want to know more then      the link is [here](https://duckdb.org/docs/). 

## Contributing 
- Fork it!

Through the terminal: 
- Create your feature branch: `git checkout -b my-new-feature`
- Commit your changes: `git commit -am 'Add some feature'`
- Push to the branch: `git push origin my-new-feature`
- Submit a pull request :D

Through VS code IDE:
- At the bottom left select the branch icon (it should say "main")
- Choose to "create new branch"
- Name the branch according to the feature you will be working on
- Press enter, and then ensure you are checked out to ths new branch you made at the bottom left

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.
