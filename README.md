Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

# CourseProject CS410Fall2020 
David Tan Sang Tran (davidtt2) { Individual Team }

[David Tran Project Proposal](https://github.com/davidtt2/CourseProject/blob/main/CS410%20Project%20Proposal.pdf)

[David Tran Progress Report](https://github.com/davidtt2/CourseProject/blob/main/CS410%20Project%20Progress%20Report.pdf)

[David Tran Final Report and Documentation](https://github.com/davidtt2/CourseProject/blob/main/CS410%20Project%20Final%20Report.pdf)

## How to Run
1) Clone project (git clone https://github.com/davidtt2/CourseProject.git)
2) Run "CS410 Project Data.py" (keep file structure unchanged)
	- Requires file to be in same directory as cs410-project
	- Requires chromedriver.exe in same directory as py file 
		(also requires Chrome)
		- Different versions can be downloaded at https://chromedriver.chromium.org/downloads
	- Python file will run Selenium webdriver scripts
	- After, it will create a companies.json info file 
	  at root and in Angular project
3) cd to /cs410-project/src
4) Run the Angular script (ng serve -o)
5) UI will open in browser

Modules that may need to be imported/installed to run:
  - npm install @angular/cli
  - ng add @angular/material 
  - pip install pandas
  - pip install selenium
  - others
  
## Description
This project uses a text retrieval method through Python's pandas & Selenium in order to gain information about the top companies in the technology industry. After retrieving that information, the Python file will generate a json file within the Angular project that will be read and displayed in the user interface. From the user interface, the user can search for technology companies by name.

Please contact me for any assistance or comments. 
