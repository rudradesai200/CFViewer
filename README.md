<a href="https://www.buymeacoffee.com/rudradesai200" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

# CFViewer
CFViewer is a project designed to help competetive programmers who use codeforces platform for participating in contests and problem solving. There are many features present on the website, which coders can use to find and explore new problems and contests.

## Recent Updates
  - CFViewer is now available as a docker container. So, users can directly pull cfviewer from DockerHub and use it without any installation. Follow the steps below to use CFViewer.

## Setup
  - First, download `docker` and verify you have properly installed it.
    - This link may help - [https://docs.docker.com/desktop/](Link)
  - Now, pull the cfviewer image using the following commmand (It may take some time depending on your internet connectivity)
    - `docker pull rudradesai200/cfviewer:latest`
  - The setup is complete, now you are ready to run the CFViewer image

## Usage
  - You can start the container by using the following command,
    - `docker run --rm  -dp 8020:8020 rudradesai200/cfviewer:latest --name web`
  - Once the image is run, you can open CFViewer by opening the following url on any browser,
    - `http://localhost:8020` 

## Extras
  - To open the admin console, you need to start the container with following flags
    - DJANGO_SUPERUSER_USERNAME
    - DJANGO_SUPERUSER_PASSWORD
    - DJANGO_SUPERUSER_EMAIL
  - For Ex,
    - `docker run --rm  -dp 8020:8020 -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_PASSWORD=password -e DJANGO_SUPERUSER_EMAIL=admin@example.com rudradesai200/cfviewer`
  - Now to access the admin console, go to
    - `http://localhost:8020/admin`

## Contributing
This platform is completely made using Django-Python Framework. Because, it is hosted on my personal AWS server, I cannot share the complete project on GitHub, So, I have shared just the main app here. Please try to test if it is working or not first, then only open a pull request. Any suggestion and edits are welcome! Thanks in advance for the contribution.

Following is the list of features on the website and how to use it.
## Dashboard
Dashboard contains statistics of coder's perfomance till now on codeforces. It contains 4 different charts - 
1. Problem Category vs Numbers Solved 
2. Rating Changes vs Contests
3. Problems Tag vs Numbers Solved
4. Submission Types vs Total Submissions

Also, some other information like Number of Problems attempted, Contests Attempted , Max Rating on Codeforces and Current Rating.

## Problems Suggestor
Problem Suggestor suggests problems to coders based on the problems they have solved till now. It is a smart algorithm which analyzes the solved problems and its rating and suggests some filters based on it. Also, 10 problems following the same filters are also displayed below it with its link.
![problems_suggestor](https://user-images.githubusercontent.com/44108388/83966373-81f56700-a8d7-11ea-96d8-8224053ef1b2.png)

## Contests Suggestor
Contest Suggestor suggests virtual contests to coders based on the contests they have participated till now. It is a smart algorithm which analyzes the solved contests and suggests some filters based on it. Also, 10 contests following the same filters are also displayed below it along with its link.
![contests_suggestor](https://user-images.githubusercontent.com/44108388/83966376-86218480-a8d7-11ea-8247-14cabfa44886.png)

## Compare and Solve
Just enter the name of a friend and get some detailed statistics comparing the perfomance of your's and your friend's submission history. Also, all of your friend's attempted but unsolved problems are listed in a tabular format along with a link to the problem. So, you can try it and then boast it in front of your friend ;) 

## Problems Page
The main functionality of this page are the filters. You can combine multiple filters to get the problems you want to solve. 
![problem_filters](https://user-images.githubusercontent.com/44108388/83965990-49ed2480-a8d5-11ea-9827-d1ef106cbe47.png)

## Contests Page
It is a simple page which lists all the non-gym contests available on codeforces and displays it in a tabular format.
![Contests_page](https://user-images.githubusercontent.com/44108388/83966272-d815da80-a8d6-11ea-9fa3-8cfd36be0a73.png)

## Books
This page contains the top 10 Books for competitive programming suggested by experts in this field. Also, a link to the amazon page for that book is attached.
![Books_page](https://user-images.githubusercontent.com/44108388/83966271-d6e4ad80-a8d6-11ea-8b77-1f0124869d5a.png)
