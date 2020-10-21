# Hackrithmitic 2020 (Best Use of Google Cloud), HackTheU 2020 (Best Use of Google Cloud)
## Inspiration
The COVID-19 pandemic has affected educational systems worldwide, leading to the near-total closures of schools, universities and colleges. Most governments around the world have temporarily closed educational institutions in an attempt to reduce the spread of COVID-19. As of 30 September 2020, approximately **1.077 billion** learners are currently affected due to school closures in response to the pandemic. According to UNICEF monitoring, **53 countries** are currently implementing nationwide closures and **27** are implementing local closures, impacting about **61.6 percent** of the world's student population. **72 countries'** schools are currently open.

![data](https://assets.weforum.org/editor/35ZTVoUUKZ8R135jMCnLB3YirWPKRy49J6fKpf7q2ek.jpeg)

A crucial aspect of schoolwork that's missing due to the pandemic is group studying. Effective study groups can help students learn course material in a deeper, more concrete way. Solving challenging problems together allow students to tackle their courseload better and view the material from various different perspectives. Due to the pandemic, it is difficult to tackle problems and compare answers with each other as efficiently.

That's where ***EduSource*** looks to provide an effective solution.
## What it does
There are two specific features that ***EduSource*** specializes in:
### Crowdsourcing answers
***EduSource*** allows users to subscribe to courses in their universities, create Problem Sets that include difficult problems from past assignments, quizzes and exams, and invite other students to collaborate with them in solving those Problem Sets. By allowing students to add their own answers, or award a **Kudos** to other answers that match theirs, ***EduSource*** provides a platform where students can verify their solutions with others. The number of **Kudos** an answer has represents its reliability.
### Scientific Equation Recognition
Using ***EduSource***, students may also upload pictures of their handwritten notes and obtain a list of scientific equations in their notes with detailed descriptions. This is extremely useful for math/science students who deal with countless formulae and equations and will allow them to better understand the relationship between all the different identities.  
  
Click image below for demo video (or click [here](https://youtu.be/-2_g7Y_6jL8))
[![Video_Thumbnail](http://i3.ytimg.com/vi/-2_g7Y_6jL8/maxresdefault.jpg)](https://youtu.be/-2_g7Y_6jL8)
## How I built it
The web application is built using **Flask** in **Python**, along with **HTML** and **CSS** for markup and styling. **Flask SQLAlchemy** is used as a database to store information about Users, Problem Sets, Questions and Answers. The Equation Tool is built using the **Google Cloud Vision** Client Library for Python. This is done by implementing **OCR (Optical Character Recognition)** to identify equations.
## Challenges I ran into
This is one of the first few websites I have built. The most challenging part was visualizing all the database components and their relationships with each other.
## Accomplishments that I'm proud of and what I learned
As a non-web developer and the sole contributor to this project, I am glad that I could produce a finished product. This experience allowed me to get a better grasp on HTML, CSS and database management. I'm happy to think that this application may help someone someday in this pandemic.
## What's next for ***EduSource***
There are several features I would like to add to ***EduSource***:
- Video call group studies
- Support for LaTeX
- Incorporate AI-based math and science problem solving solving APIs