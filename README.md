# Hack The Crisis Sweden 2020

Introduction:

Public health services, especially hospitals, have had a huge increase in demand whilst much of the Swedish workforce have lost their jobs during the Coronavirus pandemic. Our platform solution allows hospitals to find the right people from the population for their growing demand of healthcare work. Hospital staff simply search using the following criteria: Roles & skills & Proximity to hospital
This returns a list of people who match the hospitals skillset and are located nearby to reduce the workers travel thus minimising the spread. This optimises the Swedish workforce by connecting the demand for hospital workers with the increased supply of unemployed / volunteers to save businesses and lives together.

Description:

A dataset is prepared by generating random data which included details about the citizens of the country. Cleaned by pre-processing techniques like removal of special characters, stop words, lemmatization. The data is represented using a word2vec model. [A word-space model is a spatial representation that derives the meaning of words by plotting these words in an n-dimensional geometric space.] Search is performed by performing cosine similarity on the model and the free text entered by the user. Top ten most similar matches are retreived from the dataset.

Tools used: 

Python(Flask), Html, CSS, Bootstrap, Azure DeVops(version control), Azure container registry(Docker), Azure Web App Service.


(Note - This app was originally developed in DevOps, but as that link cannot be accessed outside KPMG repository, I have put the code here.)