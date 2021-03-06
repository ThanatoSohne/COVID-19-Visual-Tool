# COVID19VisTool: 
## A Web App to Better Visualize the Impact of COVID-19 on Our Lives :earth_americas:

The implementation and overall work for this web app is the byproduct of our 2020 Capstone project in the [CEAS Department](https://www.albany.edu/ceas) here 
at the [University at Albany](https://www.albany.edu), as well as the situation that has arisen due to the virulent spread of COVID-19.

###### Acknowledgement
First, we wish to express our most sincere appreciation to [Dr. ChangHwan Lee](https://www.albany.edu/biology/faculty/changhwan-lee) 
of the [Biological Sciences](https://www.albany.edu/biology) department and [The Lee Lab](https://sites.google.com/view/leelab-ua/home?authuser=0) 
at UAlbany. Dr. Lee has been an exceptional sponsor and mentor thorughout our semester. His expertise, patience, always 
constructive suggestions, and overall enthusiasm was just the right tonic needed to produce a web app to the best of our abilities. 
Dr. Lee was always willing to make time for us and we truly appreciated his generousity.

We also wish to express our gratitude to [Prof. Pradeep Atrey](https://www.albany.edu/ceas/faculty/pradeep-k-atrey) of the CEAS department 
and who serves as both the Director of Undergraduate Programming and as our instructor for the 2020 Capstone project. We truly appreciated
his guidance and suggestions on how best to proceed and develop our project. As well as for allowing us to freely choose a project dealing with 
COVID-19.

Finally, to the makers and maintainers of the Python libraries, outside platforms, and systems that we used in the making of this web app:
**Thank You!**

###### Members of Our Team 
- Jack Angevine
- Mary Ramos
- Mateo Vaquero Benjumea
- Avinash Singh

###### News/ Update Info
As of 6/28/20, the web scraping code is obsolete and will be updated as soon as it has been reworked to better collect information from ever changing data and sites. We are also working on a page within the app to hold a table with info for testing sites based on state. 
As of 09/01/2020, the web app is temporarily down. Trying to move everything over into a Jupyter notebook publication. Code, so far, for the choropleth maps and subplots have been reworked and added to files above (covid19VizProject.py). If you wish to download the Jupyter notebook that has thus far been created, here is the link: https://www.dropbox.com/s/kffn29hm2ffudov/covid19VizProject.ipynb?dl=0 
Will continue to work on this as I get the time. Avi
## Abstract
When it comes to understanding data of any kind, we tend to best conceptualize and understand this data with the 
utilization of visuals. This is not just contained to the fields of computer science or mathematics seeing as its 
interdisciplinary nature lends to success in the communication of hard to grasp concepts or the analyzing of tomes 
of data to a wider audience. 
This project makes use of multiple types of visuals to better describe or showcase the overall spread and impact of COVID-19 around 
the world.

## Reports and Presentations :file_cabinet:
###### :anchor: [Project Requirement Specifications](https://www.dropbox.com/s/mjf9wzc38cqfttg/Project_Requirement_Specifications.pdf?dl=0)
###### :mag: [Use Case Diagram](https://www.dropbox.com/s/fdv2z3it79g38s6/Use_Case_Diagram.pdf?dl=0)
###### :hourglass_flowing_sand: [System/Data Flow Diagram](https://www.dropbox.com/s/caztsjp0ioccnpg/System_Flow.pdf?dl=0)
###### :memo: [System/ Technical Design](https://www.dropbox.com/s/irtyzun17drusgg/System__Technical_Design.pdf?dl=0)
###### :end: [Final Product Presentation](https://drive.google.com/file/d/1V-8RB7o4nKUAnf0npCBY0odmbdREjN3t/view?usp=sharing)
###### :page_with_curl: [Final Product Report](https://www.dropbox.com/s/1k4w0zpmpccoiu6/ICSI499_Report_Team_10.pdf?dl=0)

## Inner Mechanics
There are multiple moving parts to this web app, both behind the scenes and displayed in the app itself.
###### Web Scraping
The web scraping of the datasets used to build the maps, tables, and graphs featured in the app comes from a veritable list of sources
that were picked based on the information they provided, the frequency of updates, and the overall veracity of the information. As well as,
on the basis of the ability to web scrape with the experience of the scraper in mind. Beautiful Soup was employed for majority of the scrapers.

Every state and territory of the United States has an individual scraper within the main scraper program. 
The program is run on a daily basis and alerts the user whether there is a scraper that needs to be fixed 
or whether an exception was passed. The code was written with the idea that even if there is an exception 
the program would not stop running and would only write to file the scrapers that are working and are collecting
the correct information. 

A *pseudo-code* of majority of the scrapers:
```
- request URL content
- parse: soup(url content)
- narrow search (find)
- instantiate list[]
- for f in find:
  - take: f.text
  - list.append(take)
- conditionals in if statement (checks list)
  - file open
  - file.write(list[i], state, fips, values) 
- else print warning to fix
- file.close
...
```
The individual csv files are then git pushed to this repository for use in the web app.

###### US and World Maps
The maps, tables, and graphs utilized within the web app are built using [Plotly's](https://plotly.com/) incredibly diverse and 
powerful graphing libraries. Within our web app, the page dealing with the infection throughout the United States showcases a prominent,
changeable choropleth map that allows the user to choose from a dropdown menu a specific state. Below this is a subplot graph comprised of
a stacked bar graph, a table showing the web scraped information, and a density heat map. 
![Web App Map SubPlot](https://i.imgur.com/HhuEuBD.jpg)
![Global Cluster Map](https://i.imgur.com/0rB9Xio.jpg)

###### 3D Molecular Viewer
Our molecular viewer is Javascript built and allows the user to view two particular types of SARS-CoV-2 proteins whose PDBs were obtained from the [RCSB Protein Data Bank](https://www.rcsb.org/). The two proteins in question are that of [5RE4](https://www.rcsb.org/structure/5RE4) and [6VXX](https://www.rcsb.org/structure/6VXX). The viewer is interactive and allows the user to not only manipulate it but also allows them to render different views after choosing from the options above the viewer.
![3D Molecular Viewer](https://i.imgur.com/EKSeMPr.jpg)
__*Below are the sites that were linked to the app that was built by Mateo.*__
* [Crystal Structure of SARS-CoV-2 main protease in complex with Z1129283193](https://mateov97.github.io/Molecule/)
* [Structure of the SARS-CoV-2 spike glycoprotein](https://mateov97.github.io/Molecule2/)

###### Prediction Model
The prediction models on this page deal with both the US and with particular countries from each one of the continents. The [dataset](https://github.com/datasets/covid-19) used to train these models came from an open source [GitHub Repo](https://github.com/datasets). 
![Prediction Models](https://i.imgur.com/ZvupAar.jpg)




