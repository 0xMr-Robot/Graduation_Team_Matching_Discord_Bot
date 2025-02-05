# Discord Team Matching Bot

Welcome to the **Discord Team Matching Bot** project! This bot is designed to help students and professionals in various technical fields find the perfect team members or leaders for their projects based on their skills and interests. It automatically matches users based on their track selections, skills, university, and department.

## Features

- **Team Matching**: The bot matches team members with leaders based on their selected track, topics studied, university, and department.
- **Custom Commands**: Users can interact with the bot to register, select their roles, and specify their skills and track.
- **Leader-Member Interaction**: Facilitates team creation where leaders can find members and vice versa.
- **Error Handling**: All commands are protected with error handling to ensure a smooth user experience.
- **Data Persistence**: The bot saves registration data to ensure that no information is lost between bot restarts.

## Installation

### Prerequisites

- Python 3.8+
- `discord.py` library
- `.env` file with your `DISCORD_BOT_TOKEN` for authentication

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/discord-team-matching-bot.git
    cd discord-team-matching-bot
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your Discord bot token:
    ```env
    DISCORD_BOT_TOKEN=your_discord_bot_token_here
    ```

4. Run the bot:
    ```bash
    python bot.py
    ```

## Commands

Here are some of the key commands you can use:

- `!start`: Starts the registration process.
- `!choose_department`: Select your department (e.g., CS, IT, AI).
- `!choose_role`: Choose whether you want to be a Leader or Member.
- `!choose_track`: Choose the track you want to work on (e.g., Web Development, Data Science).
- `!choose_topics`: Select the topics you have studied in your chosen track.
- `!write_comment`: Add a comment about yourself or your team.
- `!helpbot`: Get a list of available commands and their descriptions.

### Example Workflow

1. **Start Registration**: 
    - Use the `!start` command to initiate the registration process.
    - Follow the steps to select your department, role (leader/member), track, topics, and add comments.

2. **Team Matching**:
    - Once you've completed registration, the bot will periodically match leaders with members based on their skills and department. It will notify you of a successful match and share team details.

## Data Handling

- **Data Storage**: All registration data is stored locally in the `bot_data.json` file.
- **Saving Data**: Data is saved automatically after each registration or user update.
- **Error Logging**: All errors are logged to `bot_logs.log` for debugging and issue tracking.

## Contributing

We welcome contributions! If you'd like to contribute to the development of the bot, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add your feature'`).
5. Push to your branch (`git push origin feature/your-feature`).
6. Open a pull request.

## Acknowledgments

- **discord.py**: A Python wrapper for the Discord API used to build the bot.
- **Logging**: The bot uses Python's built-in logging functionality for error handling and data persistence.
- **dotenv**: Environment variables are used to securely store your bot's token.

## Maker

**Eslam Mohamed Abbas ("Mr. Robot")**

Eslam Mohamed Abbas is a skilled **Malware Analyst** and **Cybersecurity Instructor** with extensive experience in threat analysis, reverse engineering, and cybersecurity training. Holding a Bachelor's degree in Computer Science from Mansoura University, Eslam excels in hands-on training and cyber defense techniques. He actively contributes to cybersecurity initiatives, mentors aspiring professionals, and participates in high-level Capture The Flag (CTF) competitions.

You can reach out to Eslam Mohamed Abbas at the following:

- Email: [manwelnueur87@gmail.com](mailto:manwelnueur87@gmail.com)
- Phone: 01022894416
- LinkedIn: [Eslam Mohamed Abbas](https://www.linkedin.com/in/eslam-abbas-20aa64213/)
- GitHub: [0xMr_Robot GitHub](https://github.com/0xMr-Robot)
- Twitter: [@Eslam_Abbas_1](https://twitter.com/Eslam_Abbas_1)
- YouTube: [BlacKSilence12](https://www.youtube.com/@BlacKSilence12)
- Website: [0xmr-robot.github.io](https://0xmr-robot.github.io/)

### Skills & Interests:
- Threat Intelligence & Threat Hunting
- Reverse Engineering & Malware Analysis
- Cybersecurity Education
- Open Source Intelligence (OSINT)
- Capture The Flag (CTF) Competitions

### Projects:
- **Assembly Emulator Spectrum**: [GitHub Link](https://github.com/0xMr-Robot/Assembly-Emu-Spectrum)
- **Automated Malware Collection**: [Blog Post](https://0xmr-robot.github.io/posts/Building-Your-Arsenal-Automated-Malware-Collection/)

For more details on Eslam's work and accomplishments, refer to his [Gitbook](https://mr-robot-1.gitbook.io/mrrobot).

