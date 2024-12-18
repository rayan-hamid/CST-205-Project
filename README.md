# CST-205-Project
# Climate Awareness Project

Team members: Rayan Hamid, Rian Hasset, Ann Jojo, Esteban Grado

Class: CST-205: Multimedia Design and Programming

Date: December 18, 2024

Project Description: 
This project is a comprehensive web application developed in Flask, aimed at raising awareness about climate change. It provides users with an interactive and educational experience by exploring the causes, effects, and solutions to climate change, as well as resources for taking action. Key features include:

How to Run the Program:
1. git clone <[GitHub repository URL](https://github.com/rayan-hamid/CST-205-Project.git)>
 - cd <CST-205-Project>
2. Activate your virtual environment: source cst205env/bin/activate
3. Install dependencies:
- pip install Flask
- pip install Flask-WTF
- pip install WTForms
- pip install requests
- pip install openmeteo-sdk

4. Run the application: flask --app home --debug run
   - access the application at: http://127.0.0.1:5000/

Key Features:
Causes Page: Displays detailed insights into the primary causes of climate change, such as fossil fuels, deforestation, and urbanization. Users can explore these causes visually and interactively.
Effects Page: Highlights the various consequences of climate change through a visually engaging grid layout, covering topics like rising sea levels, extreme weather, and health impacts.
Carbon Footprint Calculator: A tool that allows users to calculate their carbon footprint based on activities like vehicle use, electricity consumption, flights, and shipping. This feature integrates with the Carbon Interface API to provide accurate estimates of emissions.
Solutions Page: Offers actionable tips and sustainable solutions for reducing individual and collective carbon footprints.
Resources Page: Provides additional educational and actionable resources to empower users to combat climate change.
Quiz: An engaging quiz for testing and improving users' knowledge of climate change, with immediate feedback and scoring.
Weather and Pollution Integration: Allows users to view current weather and air pollution data based on their location, providing localized context for climate change impacts.

Link to GitHub Repository: https://github.com/rayan-hamid/CST-205-Project.git

Link to Trello Board: https://trello.com/b/Ijz5BNCF/team-11485

Future Work: 
User Accounts: Allow users to save their carbon footprint calculations and progress in quizzes.
Advanced Analytics: Provide a dashboard for tracking personal or community-based sustainability metrics.
Gamification: Add badges or rewards for users who engage actively with the application.
Expanded API Integration: Include data from more APIs to provide richer insights into climate change statistics and trends.
