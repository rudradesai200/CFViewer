<a href="https://www.buymeacoffee.com/rudradesai200" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

# CFViewer
CFViewer is a project designed to help competetive programmers who use codeforces platform for participating in contests and problem solving. There are many features present on the website, which coders can use to find and explore new problems and contests.

## Recent Updates
<ol>
  <li>A small firefox extension has been made for the suggestions pages. You can search for it on the firefox store or download it from <a href="https://addons.mozilla.org/addon/cfviewer/">here</a>.</li>
  <li>Now you can access site using https too.</li>
</ol>

## Firefox Extension
  ### Instructions to use
  <ul>
    <li>Download it and install it on firefox . Reload firefox if necessary.</li>
    <li> The extension can only be run from the codeforces.com website.</li>
    <li> You need to be logged in on codeforces to use it.</li>
    <li> Click on the logo in your extensions bar</li>
    <li> Select which type of suggestion you want.</li>
    <li> A pop-up will appear containing the suggestion. Press OK to be redirected to that question.</li>
   </ul>

  ### Snapshots
  It can be viewed from this <a href="https://addons.mozilla.org/addon/cfviewer/">page</a>.

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
