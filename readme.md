![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-brightgreen)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue)

# Quiz Game Review

## Overview
The Quiz Game is an interactive and engaging competition designed for fr play and excitement. Participants are randomly selected, asked questions, and must respond within a set time limit. Correct answers are rewarded with a cash prize, adding an element of motivation and fun.

---

## Versions

### Version 1: Without Speech Listening
- Participants press the **"Start Quiz"** button to begin.
- A **random roll number** is selected, and the chosen participant must stand up.
- A question is presented with a **10-second** time limit.
- The participant selects an answer and presses **"Check Answer"** to lock it in.
- If time runs out, the next question is asked automatically.
- Each correct answer earns a **cash prize of Rs. 10** at the end of the game.
- The game continues until all questions are completed.

### Version 2: With Speech Listening
- All features from **Version 1** remn unchanged.
- Voice commands enable key interactions:
  - Saying **"Agent, Start Quiz"** begins the game.
  - Saying **"Agent, Lock Option"** locks in an answer.
- This adds a hands-free experience, making the game more interactive and accessible.

---

## Pros
- **Engaging & Fr:** Randomized participant selection ensures frness.
- **Timed Responses:** The 15-second limit keeps the game dynamic and fast-paced.
- **Reward System:** Monetary prizes encourage participation and excitement.
- **Hands-Free Option (Version 2):** Enhances accessibility through voice commands.

## Areas for Improvement
- **More Reward Tiers:** Different prize amounts based on difficulty could add more excitement.
- **Customization Options:** Allowing hosts to adjust time limits or select question categories.
- **Enhanced Speech Recognition:** Improving accuracy for better user experience in Version 2.

## 📘 How to Use

Follow the steps below to set up and use the Interactive Quiz App:

**Step 1:** Clone the repository to your local working directory using the following command:

```bash
git clone https://github.com/arunsundar2005/Interactive_Quiz_App.git
```
**Step 2:** Install the required dependencies by executing:

```bash
pip install -r requirements.txt
```
**Step 3:** The application uses a predefined set of questions stored in each version file as a Python list of dictionaries. These can be modified to suit individual requirements.

> Note:
If a question includes an image, place the corresponding image file in the images directory. Then, specify the image path in the image key of that question's dictionary. For questions without an image, set the image value to None.

**Step 4:** Select the desired version of the application and run the corresponding Python file to begin the quiz.

## Conclusion
The Quiz Game is a well-designed and engaging experience, ideal for group competitions. The addition of speech listening in Version 2 enhances accessibility, while the core mechanics ensure a fr and fun challenge. Future updates could introduce more customization and refined voice interaction for an even better experience.

