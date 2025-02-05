import json
import logging
from datetime import datetime
import schedule
import signal
from logging.handlers import RotatingFileHandler
import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
from discord.ui import Button, View, Select
from collections import defaultdict
import heapq
import asyncio
import os
import sys
from dotenv import load_dotenv
import time

# Setup logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = 'bot_logs.log'
log_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger('BotLogger')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)



# Load environment variables from .env file
load_dotenv()

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents , heartbeat_timeout=120)


# Categorized Tracks
track_categories = {
    "Backend Frameworks": [".net", "node.js", "laravel", "django", "spring"],
    "Cybersecurity Specializations": ["network security", "ethical hacking", "digital forensics"],
    "Data Science Specializations": ["machine learning", "data analysis", "data engineering", "deep learning"],
    "Other Tracks": ["front end", "ui-ux", "flutter", "cloud", "mobile", "embedded systems", "vr", "game development"]
}

universities = [
    "Cairo University",
    "Ain Shams University",
    "Alexandria University",
    "Helwan University",
    "Mansoura University",
    "Assiut University",
    "Zagazig University",
    "Tanta University",
    "Suez Canal University",
    "Benha University",
    "Fayoum University",
    "South Valley University",
    "Menoufia University",
    "Port Said University",
    "Beni Suef University",
    "Kafrelsheikh University",
    "Damietta University",
    "Sohag University",
    "Modern Academy",
    "MSA University",
    "MTI University",
    "Future University",
    "October 6 University",
    "Badr University",
    "New Cairo Academy"
]

# Track Topics with Difficulty Scores
track_topics = {
    ".net": [
        {"name": "C# Basics", "difficulty": "beginner", "score": 15},
        {"name": ".NET Core Fundamentals", "difficulty": "beginner", "score": 15},
        {"name": "Basic Web API", "difficulty": "intermediate", "score": 25},
        {"name": ".NET MVC", "difficulty": "intermediate", "score": 25},
        {"name": "Entity Framework", "difficulty": "advanced", "score": 40},
        {"name": "Dependency Injection", "difficulty": "advanced", "score": 40},
        {"name": "Microservices with .NET", "difficulty": "advanced", "score": 40},
        {"name": "Advanced ORM", "difficulty": "advanced", "score": 40},
        {"name": "Performance Optimization", "difficulty": "advanced", "score": 40}
    ],
    "node.js": [
        {"name": "JavaScript Basics", "difficulty": "beginner", "score": 15},
        {"name": "Node.js Fundamentals", "difficulty": "beginner", "score": 15},
        {"name": "Express.js Basics", "difficulty": "intermediate", "score": 25},
        {"name": "Async Programming", "difficulty": "intermediate", "score": 25},
        {"name": "RESTful API Design", "difficulty": "advanced", "score": 40},
        {"name": "Authentication", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Express", "difficulty": "advanced", "score": 40},
        {"name": "Microservices", "difficulty": "advanced", "score": 40},
        {"name": "Performance Tuning", "difficulty": "advanced", "score": 40}
    ],
    "laravel": [
        {"name": "PHP Basics", "difficulty": "beginner", "score": 15},
        {"name": "Laravel Installation", "difficulty": "beginner", "score": 15},
        {"name": "Routing Fundamentals", "difficulty": "intermediate", "score": 25},
        {"name": "Eloquent ORM", "difficulty": "intermediate", "score": 25},
        {"name": "Authentication", "difficulty": "advanced", "score": 40},
        {"name": "Blade Templates", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Eloquent", "difficulty": "advanced", "score": 40},
        {"name": "Laravel Microservices", "difficulty": "advanced", "score": 40},
        {"name": "Performance Optimization", "difficulty": "advanced", "score": 40}
    ],
    "django": [
        {"name": "Python Basics", "difficulty": "beginner", "score": 15},
        {"name": "Django Setup", "difficulty": "beginner", "score": 15},
        {"name": "Basic Models", "difficulty": "intermediate", "score": 25},
        {"name": "Django ORM", "difficulty": "intermediate", "score": 25},
        {"name": "Authentication", "difficulty": "advanced", "score": 40},
        {"name": "REST Framework", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Querying", "difficulty": "advanced", "score": 40},
        {"name": "Microservices", "difficulty": "advanced", "score": 40},
        {"name": "Performance Optimization", "difficulty": "advanced", "score": 40}
    ],
    "spring": [
        {"name": "Java Basics", "difficulty": "beginner", "score": 15},
        {"name": "Spring Boot Fundamentals", "difficulty": "beginner", "score": 15},
        {"name": "Dependency Injection", "difficulty": "intermediate", "score": 25},
        {"name": "Spring MVC", "difficulty": "intermediate", "score": 25},
        {"name": "JPA", "difficulty": "advanced", "score": 40},
        {"name": "Security Configuration", "difficulty": "advanced", "score": 40},
        {"name": "Microservices", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Caching", "difficulty": "advanced", "score": 40},
        {"name": "Performance Tuning", "difficulty": "advanced", "score": 40}
    ],
    "network security": [
        {"name": "Network Basics", "difficulty": "beginner", "score": 15},
        {"name": "TCP/IP", "difficulty": "beginner", "score": 15},
        {"name": "Firewall Concepts", "difficulty": "intermediate", "score": 25},
        {"name": "Intrusion Detection", "difficulty": "intermediate", "score": 25},
        {"name": "Network Protocols", "difficulty": "advanced", "score": 40},
        {"name": "Packet Analysis", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Threat Detection", "difficulty": "advanced", "score": 40},
        {"name": "Network Forensics", "difficulty": "advanced", "score": 40},
        {"name": "Secure Network Design", "difficulty": "advanced", "score": 40}
    ],
    "ethical hacking": [
        {"name": "Security Fundamentals", "difficulty": "beginner", "score": 15},
        {"name": "Basic Networking", "difficulty": "beginner", "score": 15},
        {"name": "Linux Basics", "difficulty": "intermediate", "score": 25},
        {"name": "Penetration Testing Basics", "difficulty": "intermediate", "score": 25},
        {"name": "Vulnerability Assessment", "difficulty": "advanced", "score": 40},
        {"name": "Exploit Techniques", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Penetration Testing", "difficulty": "advanced", "score": 40},
        {"name": "Red Team Tactics", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Exploit Development", "difficulty": "advanced", "score": 40}
    ],
    "digital forensics": [
        {"name": "Computer Forensics Basics", "difficulty": "beginner", "score": 15},
        {"name": "Evidence Preservation", "difficulty": "beginner", "score": 15},
        {"name": "Basic Tools", "difficulty": "intermediate", "score": 25},
        {"name": "Forensic Analysis Techniques", "difficulty": "intermediate", "score": 25},
        {"name": "Disk Forensics", "difficulty": "advanced", "score": 40},
        {"name": "Memory Forensics", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Forensic Tools", "difficulty": "advanced", "score": 40},
        {"name": "Malware Analysis", "difficulty": "advanced", "score": 40},
        {"name": "Complex Investigation Techniques", "difficulty": "advanced", "score": 40}
    ],
    "machine learning": [
        {"name": "Python Basics", "difficulty": "beginner", "score": 15},
        {"name": "Statistics Fundamentals", "difficulty": "beginner", "score": 15},
        {"name": "Basic ML Algorithms", "difficulty": "intermediate", "score": 25},
        {"name": "Scikit-learn", "difficulty": "intermediate", "score": 25},
        {"name": "Supervised Learning", "difficulty": "advanced", "score": 40},
        {"name": "Feature Engineering", "difficulty": "advanced", "score": 40},
        {"name": "Deep Learning", "difficulty": "advanced", "score": 40},
        {"name": "Advanced ML Algorithms", "difficulty": "advanced", "score": 40},
        {"name": "Model Deployment", "difficulty": "advanced", "score": 40}
    ],
    "data analysis": [
        {"name": "Python Basics", "difficulty": "beginner", "score": 15},
        {"name": "Excel Fundamentals", "difficulty": "beginner", "score": 15},
        {"name": "Basic Statistics", "difficulty": "intermediate", "score": 25},
        {"name": "Pandas", "difficulty": "intermediate", "score": 25},
        {"name": "NumPy", "difficulty": "advanced", "score": 40},
        {"name": "Data Visualization", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Analytics", "difficulty": "advanced", "score": 40},
        {"name": "Predictive Modeling", "difficulty": "advanced", "score": 40},
        {"name": "Big Data Tools", "difficulty": "advanced", "score": 40}
    ],
    "data engineering": [
        {"name": "SQL Basics", "difficulty": "beginner", "score": 15},
        {"name": "Data Warehousing Concepts", "difficulty": "beginner", "score": 15},
        {"name": "ETL Fundamentals", "difficulty": "intermediate", "score": 25},
        {"name": "Apache Spark", "difficulty": "intermediate", "score": 25},
        {"name": "Big Data Technologies", "difficulty": "advanced", "score": 40},
        {"name": "Data Pipeline Design", "difficulty": "advanced", "score": 40},
        {"name": "Distributed Computing", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Data Modeling", "difficulty": "advanced", "score": 40},
        {"name": "Real-time Data Processing", "difficulty": "advanced", "score": 40}
    ],
    "deep learning": [
        {"name": "Neural Network Basics", "difficulty": "beginner", "score": 15},
        {"name": "Python for AI", "difficulty": "beginner", "score": 15},
        {"name": "Basic Deep Learning Concepts", "difficulty": "intermediate", "score": 25},
        {"name": "TensorFlow", "difficulty": "intermediate", "score": 25},
        {"name": "Keras", "difficulty": "advanced", "score": 40},
        {"name": "Neural Network Architectures", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Neural Networks", "difficulty": "advanced", "score": 40},
        {"name": "Computer Vision", "difficulty": "advanced", "score": 40},
        {"name": "NLP Techniques", "difficulty": "advanced", "score": 40}
    ],
    "front end": [
        {"name": "HTML Basics", "difficulty": "beginner", "score": 15},
        {"name": "CSS Fundamentals", "difficulty": "beginner", "score": 15},
        {"name": "JavaScript Basics", "difficulty": "intermediate", "score": 25},
        {"name": "Responsive Design", "difficulty": "intermediate", "score": 25},
        {"name": "Bootstrap", "difficulty": "advanced", "score": 40},
        {"name": "JavaScript ES6+", "difficulty": "advanced", "score": 40},
        {"name": "React", "difficulty": "advanced", "score": 40},
        {"name": "Vue.js", "difficulty": "advanced", "score": 40},
        {"name": "State Management", "difficulty": "advanced", "score": 40}
    ],
    "ui-ux": [
        {"name": "Design Principles", "difficulty": "beginner", "score": 15},
        {"name": "Color Theory", "difficulty": "beginner", "score": 15},
        {"name": "Typography Basics", "difficulty": "intermediate", "score": 25},
        {"name": "Wireframing", "difficulty": "intermediate", "score": 25},
        {"name": "Prototyping", "difficulty": "advanced", "score": 40},
        {"name": "User Research", "difficulty": "advanced", "score": 40},
        {"name": "Figma", "difficulty": "advanced", "score": 40},
        {"name": "Adobe XD", "difficulty": "advanced", "score": 40},
        {"name": "Advanced UX Strategy", "difficulty": "advanced", "score": 40}
    ],
    "flutter": [
        {"name": "Dart Basics", "difficulty": "beginner", "score": 15},
        {"name": "Flutter Installation", "difficulty": "beginner", "score": 15},
        {"name": "Basic Widgets", "difficulty": "intermediate", "score": 25},
        {"name": "State Management", "difficulty": "intermediate", "score": 25},
        {"name": "Navigation", "difficulty": "advanced", "score": 40},
        {"name": "API Integration", "difficulty": "advanced", "score": 40},
        {"name": "Custom Widgets", "difficulty": "advanced", "score": 40},
        {"name": "Performance Optimization", "difficulty": "advanced", "score": 40},
        {"name": "Advanced State Solutions", "difficulty": "advanced", "score": 40}
    ],
    "cloud": [
        {"name": "Cloud Computing Basics", "difficulty": "beginner", "score": 15},
        {"name": "Basic Networking", "difficulty": "beginner", "score": 15},
        {"name": "Virtual Machines", "difficulty": "intermediate", "score": 25},
        {"name": "AWS Basics", "difficulty": "intermediate", "score": 25},
        {"name": "Azure Fundamentals", "difficulty": "advanced", "score": 40},
        {"name": "Docker Basics", "difficulty": "advanced", "score": 40},
        {"name": "Kubernetes", "difficulty": "advanced", "score": 40},
        {"name": "Cloud Security", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Deployment Strategies", "difficulty": "advanced", "score": 40}
    ],
    "mobile": [
        {"name": "Mobile Development Basics", "difficulty": "beginner", "score": 15},
        {"name": "UI Design for Mobile", "difficulty": "beginner", "score": 15},
        {"name": "Android Development", "difficulty": "intermediate", "score": 25},
        {"name": "iOS Development", "difficulty": "intermediate", "score": 25},
        {"name": "React Native Basics", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Mobile Architectures", "difficulty": "advanced", "score": 40},
        {"name": "Performance Optimization", "difficulty": "advanced", "score": 40},
        {"name": "Cross-Platform Development", "difficulty": "advanced", "score": 40}
    ],
    "embedded systems": [
        {"name": "Electronics Basics", "difficulty": "beginner", "score": 15},
        {"name": "Microcontroller Fundamentals", "difficulty": "beginner", "score": 15},
        {"name": "C Programming", "difficulty": "intermediate", "score": 25},
        {"name": "Arduino Programming", "difficulty": "intermediate", "score": 25},
        {"name": "Raspberry Pi", "difficulty": "advanced", "score": 40},
        {"name": "Sensor Integration", "difficulty": "advanced", "score": 40},
        {"name": "IoT Protocols", "difficulty": "advanced", "score": 40},
        {"name": "Advanced Embedded Programming", "difficulty":"advanced", "score": 40},
        {"name": "Real-Time Systems", "difficulty": "advanced", "score": 40}
    ],
    "vr": [
        {"name": "3D Basics", "difficulty": "beginner", "score": 15},
        {"name": "Virtual Reality Concepts", "difficulty": "beginner", "score": 15},
        {"name": "Basic Game Design", "difficulty": "intermediate", "score": 25},
        {"name": "Unity Basics", "difficulty": "intermediate", "score": 25},
        {"name": "3D Modeling", "difficulty": "advanced", "score": 40},
        {"name": "Basic VR Interactions", "difficulty": "advanced", "score": 40},
        {"name": "Advanced VR Development", "difficulty": "advanced", "score": 40},
        {"name": "Unreal Engine", "difficulty": "advanced", "score": 40},
        {"name": "VR Performance Optimization", "difficulty": "advanced", "score": 40}
    ],
    "game development": [
        {"name": "Game Design Basics", "difficulty": "beginner", "score": 15},
        {"name": "Unity Basics", "difficulty": "beginner", "score": 15},
        {"name": "Unreal Engine Basics", "difficulty": "intermediate", "score": 25},
        {"name": "2D Game Development", "difficulty": "intermediate", "score": 25},
        {"name": "3D Game Development", "difficulty": "advanced", "score": 40},
        {"name": "Game Physics", "difficulty": "advanced", "score": 40},
        {"name": "AI in Games", "difficulty": "advanced", "score": 40},
        {"name": "Multiplayer Game Development", "difficulty": "advanced", "score": 40},
        {"name": "VR Game Development", "difficulty": "advanced", "score": 40}
    ]
}

# Data structures to store members and leaders
members = defaultdict(list)
leaders = defaultdict(list)
user_data = {}
registered_users = set()
user_track_registrations = {}
matched_members = set()  # New set to track matched members
leader_departments = {}  # New dictionary to store leaders' departments

# Data storage functions
def save_data():
    try:
        # Convert member tuples to serializable format
        serialized_members = {}
        for track, member_list in members.items():
            serialized_members[track] = []
            for rating, reg_time, member in member_list:
                # Store user ID and name instead of User object
                serialized_member = {
                    'user_id': member.get('user_id') or member['user'].id,  # Handle both new and old format
                    'user_name': member.get('user_name') or member['user'].name,  # Handle both new and old format
                    'track': member['track'],
                    'rating': member['rating'],
                    'comment': member['comment'],
                    'department': member['department'],
                    'university': member['university'],
                    'selected_topics': member['selected_topics'],
                    'registration_time': member['registration_time']
                }
                serialized_members[track].append((rating, reg_time, serialized_member))

        # Convert leaders to serializable format
        serialized_leaders = {}
        for track, leader_list in leaders.items():
            serialized_leaders[track] = []
            for leader in leader_list:
                # Store user ID and name instead of User object
                serialized_leader = {
                    'user_id': leader.get('user_id') or leader['user'].id,  # Handle both new and old format
                    'user_name': leader.get('user_name') or leader['user'].name,  # Handle both new and old format
                    'team_name': leader['team_name'],
                    'track': leader['track'],
                    'team_comment': leader['team_comment'],
                    'department': leader['department'],
                    'university': leader['university']
                }
                serialized_leaders[track].append(serialized_leader)

        data = {
            'members': serialized_members,
            'leaders': serialized_leaders,
            'user_data': user_data,
            'registered_users': list(registered_users),
            'matched_members': list(matched_members),
            'leader_departments': leader_departments
        }
        
        with open('bot_data.json', 'w') as f:
            json.dump(data, f, default=str)
        logger.info("Data saved successfully")

    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")

def load_data():
    try:
        if os.path.exists('bot_data.json'):
            with open('bot_data.json', 'r') as f:
                data = json.load(f)
            
            # Restore data structures
            global members, leaders, user_data, registered_users, matched_members, leader_departments
            
            # Restore members
            members = defaultdict(list)
            for track, member_list in data['members'].items():
                for rating, reg_time, member_dict in member_list:
                    # Store just the raw data - we'll get the User object when needed
                    member = {
                        'user_id': member_dict['user_id'],
                        'user_name': member_dict['user_name'],
                        'track': member_dict['track'],
                        'rating': member_dict['rating'],
                        'comment': member_dict['comment'],
                        'department': member_dict['department'],
                        'university': member_dict['university'],
                        'selected_topics': member_dict['selected_topics'],
                        'registration_time': member_dict['registration_time']
                    }
                    members[track].append((rating, reg_time, member))
            
            # Restore leaders
            leaders = defaultdict(list)
            for track, leader_list in data['leaders'].items():
                for leader_dict in leader_list:
                    # Store just the raw data
                    leader = {
                        'user_id': leader_dict['user_id'],
                        'user_name': leader_dict['user_name'],
                        'team_name': leader_dict['team_name'],
                        'track': leader_dict['track'],
                        'team_comment': leader_dict['team_comment'],
                        'department': leader_dict['department'],
                        'university': leader_dict['university']
                    }
                    leaders[track].append(leader)
            
            user_data = data['user_data']
            registered_users = set(data['registered_users'])
            matched_members = set(data['matched_members'])
            leader_departments = data['leader_departments']
            
            logger.info("Data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")

# Automatic restart function
def schedule_restart():
    save_data()
    logger.info("Initiating scheduled restart")
    
    python_executable = sys.executable  # Get Python executable path
    script_path = os.path.abspath(sys.argv[0])  # Get absolute path of script

    # Ensure proper quoting of file paths (handles spaces correctly)
    command = [python_executable, script_path]
    os.execv(python_executable, command)

# Error handling decorator
def error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            ctx = args[0] if args else None
            error_msg = f"Error in {func.__name__}: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.send(f"An error occurred. Please try again or contact support.\nError: {str(e)}")
    return wrapper

# Use these in your command responses, for example:
@bot.command(name="helpbot")
async def helpbot(ctx):
    help_title = "Discord Team Matching Bot Commands"
    help_description = (
        "Welcome to the Team Matching Bot! Here are the available commands:"
    )
    
    fields = [
        ("🔹 Registration Process", "`!start` - Complete entire registration process", False),
        ("🔹 Commands", 
         "`!choose_department` - Select department\n"
         "`!choose_role` - Choose Leader/Member\n"
         "`!choose_track` - Select track\n"
         "`!choose_topics` - Select topics\n"
         "`!write_comment` - Add comment", False),
        ("📌 Registration Flow",
         "1. Choose Department\n"
         "2. Choose Role\n"
         "3. Select Track Category\n"
         "4. Select Specific Track\n"
         "5. Choose Topics\n"
         "6. Write Comment", False)
    ]
    
    embed = format_embed_message(help_title, help_description, fields)
    await ctx.send(embed=embed)

# Helper function to calculate rating based on difficulty scores
def calculate_rating(user_id):
    track = user_data[user_id]['track']
    selected_topics = user_data[user_id].get('selected_topics', [])
    
    total_score = 0
    # Calculate total points from selected topics
    for topic_name in selected_topics:
        for topic in track_topics[track]:
            if topic['name'] == topic_name:
                total_score += topic['score']
    
    # Calculate total possible points across all topics
    total_possible_score = sum(topic['score'] for topic in track_topics[track])
    
    # Calculate rating as percentage
    return 0 if total_possible_score == 0 else min(int((total_score / total_possible_score) * 100), 100)

# Update the departments in choose_department command
@bot.command(name="choose_department")
async def choose_department(ctx):
    user_id = ctx.author.id
    role = user_data.get(user_id, {}).get('role')
    university = user_data.get(user_id, {}).get('university')

    # Check if the user is a leader and already has registered before
    if role == "leader" and user_id in leader_departments:
        stored_dept = leader_departments[user_id]['department']
        stored_univ = leader_departments[user_id]['university']
        
        # If university doesn't match previous registration
        if university != stored_univ:
            await ctx.send(f"You must register with your original university: {stored_univ}")
            user_data[user_id]["university"] = stored_univ
            await ctx.invoke(bot.get_command("choose_department"))
            return
            
        # Use the stored department and prevent changes
        user_data[user_id]["department"] = stored_dept
        await ctx.send(f"Your department is already set to {stored_dept.upper()} and cannot be changed.")
        await ctx.invoke(bot.get_command("choose_role"))
        return

    # If the leader doesn't have a department yet or is a member, allow them to choose
    select = Select(
        placeholder="Choose your department",
        options=[
            discord.SelectOption(label="CS", value="cs"),
            discord.SelectOption(label="IT", value="it"),
            discord.SelectOption(label="IS", value="is"),
            discord.SelectOption(label="AI", value="ai"),
            discord.SelectOption(label="SW", value="sw"),
            discord.SelectOption(label="BIO", value="bio")
        ]
    )

    async def callback(interaction):
        user_data[user_id]["department"] = select.values[0]
        
        # If the user is a leader, store their department and university permanently
        if role == "leader":
            leader_departments[user_id] = {
                'department': select.values[0],
                'university': user_data[user_id].get('university')
            }
        
        await interaction.response.send_message(f"You have chosen {select.values[0].upper()} department.")
        await ctx.invoke(bot.get_command("choose_role"))

    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.send("Please choose your department:", view=view)


# Add new command for university selection
@bot.command(name="choose_university")
async def choose_university(ctx):
    user_id = ctx.author.id
    role = user_data.get(user_id, {}).get('role')

    # Check if leader already registered
    if role == "leader" and user_id in leader_departments:
        stored_univ = leader_departments[user_id]['university']
        user_data[user_id]["university"] = stored_univ
        await ctx.send(f"Your university is already set to {stored_univ} and cannot be changed.")
        await ctx.invoke(bot.get_command("choose_department"))
        return

    # Create select menu with universities
    select = Select(
        placeholder="Choose your university",
        options=[discord.SelectOption(label=univ, value=univ) for univ in universities]
    )

    async def callback(interaction):
        user_data[user_id] = {"university": select.values[0]}
        await interaction.response.send_message(f"You have chosen {select.values[0]}.")
        await ctx.invoke(bot.get_command("choose_department"))

    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.send("Please choose your university:", view=view)

# Role Selection Command
@bot.command(name="choose_role")
async def choose_role(ctx):
    user_id = ctx.author.id
    
    select = Select(
        placeholder="Choose your role",
        options=[
            discord.SelectOption(label="Leader", value="leader"),
            discord.SelectOption(label="Member", value="member")
        ]
    )

    async def callback(interaction):
        selected_role = select.values[0]
        
        # Check if user is choosing to be a leader and has registered before
        if selected_role == "leader" and user_id in leader_departments:
            stored_univ = leader_departments[user_id]['university']
            stored_dept = leader_departments[user_id]['department']
            current_univ = user_data[user_id].get('university')
            current_dept = user_data[user_id].get('department')
            
            # Verify university and department match previous registration
            if current_univ != stored_univ or current_dept != stored_dept:
                await interaction.response.send_message(
                    f"⚠️ You must register with your original university ({stored_univ}) "
                    f"and department ({stored_dept.upper()}). Please start over with !start"
                )
                return
        
        user_data[user_id]["role"] = selected_role
        
        if selected_role == "leader":
            await interaction.response.send_message("You have chosen to be a Leader.")
            await ctx.send("Please enter your team name:")
            
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            
            try:
                msg = await bot.wait_for("message", check=check, timeout=60)
                team_name = msg.content
                user_data[user_id]["team_name"] = team_name
                await ctx.send(f"Your team name is {team_name}.")
                
                # Store leader's information if this is their first registration
                if user_id not in leader_departments:
                    leader_departments[user_id] = {
                        'university': user_data[user_id]['university'],
                        'department': user_data[user_id]['department']
                    }
                
                await ctx.invoke(bot.get_command("choose_track"))
            except asyncio.TimeoutError:
                await ctx.send("Team name selection timed out. Please try again.")
        
        else:  # Member
            await interaction.response.send_message("You have chosen to be a Member.")
            await ctx.invoke(bot.get_command("choose_track"))

    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.send("Choose your role:", view=view)

# Track Selection Command
@bot.command(name="choose_track")
async def choose_track(ctx):
    role = user_data.get(ctx.author.id, {}).get('role')
    
    select = Select(
        placeholder="Choose track category",
        options=[discord.SelectOption(label=category, value=category) for category in track_categories.keys()]
    )

    async def category_callback(interaction):
        category = select.values[0]
        track_options = [
            discord.SelectOption(label=track, value=track) 
            for track in track_categories[category]
        ]
        
        track_select = Select(
            placeholder=f"Choose track in {category}",
            options=track_options
        )

        async def track_callback(track_interaction):
            selected_track = track_select.values[0]
            
            # Remove previous track restrictions for leaders
            user_data[ctx.author.id]['track'] = selected_track
            await track_interaction.response.send_message(f"You have chosen {selected_track}.")
            
            # Different flow for leader and member
            if role == "leader":
                await ctx.invoke(bot.get_command("write_comment"))
            else:
                await ctx.invoke(bot.get_command("choose_topics"))

        track_select.callback = track_callback
        track_view = View()
        track_view.add_item(track_select)
        await interaction.response.send_message(f"Choose a track in {category}:", view=track_view)

    select.callback = category_callback
    view = View()
    view.add_item(select)
    await ctx.send("Choose a track category:", view=view)

# Topic Selection Command
@bot.command(name="choose_topics")
async def choose_topics(ctx):
    track = user_data[ctx.author.id]["track"]
    topics = [topic['name'] for topic in track_topics[track]]
    
    select = Select(
        placeholder="Choose topics you've studied",
        options=[discord.SelectOption(label=topic, value=topic) for topic in topics],
        max_values=len(topics)
    )

    async def callback(interaction):
        selected_topics = select.values
        user_data[ctx.author.id]["selected_topics"] = selected_topics
        rating = calculate_rating(ctx.author.id)
        user_data[ctx.author.id]["rating"] = rating
        
        await interaction.response.send_message(f"You have selected: {', '.join(selected_topics)}. Your rating is {rating}%.")
        await ctx.invoke(bot.get_command("write_comment"))

    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.send("Please select topics you've studied:", view=view)

# Write Comment Command
@bot.command(name="write_comment")
async def write_comment(ctx):
    role = user_data[ctx.author.id]["role"]
    
    if role == "member" and ctx.author.id in registered_users:
        await ctx.send("You have already registered. Wait for matching.")
        return

    comment_prompt = (
        "Write A Comment About Your Team Like Members In It And Your Project Idea.." 
        if role == "leader" else 
        "Write A Comment About Yourself Like What You Have Studied And What You Will Study In The Future.."
    )
    
    await ctx.send(comment_prompt)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
        comment = msg.content
        user_data[ctx.author.id]["comment"] = comment
        registration_time = time.time()
        
        track = user_data[ctx.author.id]["track"]
        department = user_data[ctx.author.id]["department"]
        university = user_data[ctx.author.id]["university"]
        
        if role == "member":
            member = {
                "user_id": ctx.author.id,  # Store ID instead of User object
                "user_name": ctx.author.name,  # Store name separately
                "track": track,
                "rating": user_data[ctx.author.id]["rating"],
                "comment": comment,
                "department": department,
                "university": university,
                "selected_topics": user_data[ctx.author.id].get("selected_topics", []),
                "registration_time": registration_time
            }
            heapq.heappush(members[track], (-member["rating"], registration_time, member))
            registered_users.add(ctx.author.id)
        else:
            leader = {
                "user_id": ctx.author.id,  # Store ID instead of User object
                "user_name": ctx.author.name,  # Store name separately
                "team_name": user_data[ctx.author.id]["team_name"],
                "track": track,
                "team_comment": comment,
                "department": department,
                "university": university
            }
            leaders[track].append(leader)
        
        await ctx.send("Your registration is complete. You've been added to the matching queue.")
        await ctx.invoke(bot.get_command("match"))
        
    except asyncio.TimeoutError:
        await ctx.send("Comment submission timed out. Please try again.")

# Update the start command to begin with university selection
# Add error handling to existing commands
@bot.command(name="start")
@error_handler
@commands.cooldown(1, 15, BucketType.user)
async def start(ctx):
    user_id = ctx.author.id
    
    # If user is already registered as a leader, verify their status
    if user_id in leader_departments:
        stored_data = leader_departments[user_id]
        await ctx.send(
            f"⚠️ You have previously registered as a leader for:\n"
            f"University: {stored_data['university']}\n"
            f"Department: {stored_data['department'].upper()}\n\n"
            f"You must use these same details to register again."
        )
    
    # Check if the member is already registered and not matched
    if user_id in registered_users:
        await ctx.send("You have already registered. Wait for matching.")
        return

    # Clear any existing data for the user
    if user_id in user_data:
        del user_data[user_id]
    
    await ctx.invoke(bot.get_command("choose_university"))
    save_data()

#Perform_Matching Process Function
async def perform_matching():
    try:
        matching_track_count = 0
        
        for category, tracks in track_categories.items():
            for track in tracks:
                track_leaders = leaders.get(track, []).copy()
                track_members = members.get(track, [])
                
                while track_leaders and track_members:
                    try:
                        leader = track_leaders[0]  # Don't pop yet, wait until match is confirmed
                        matching_member = None
                        temp_members = []
                        
                        while track_members:
                            rating, reg_time, member = heapq.heappop(track_members)
                            
                            # Check if member is still in registered_users
                            if (member['user_id'] in registered_users and 
                                leader["university"] == member["university"] and 
                                leader["department"] == member["department"]):
                                matching_member = member
                                break
                            else:
                                temp_members.append((rating, reg_time, member))
                        
                        # Restore unmatched members back to the heap
                        for m in temp_members:
                            heapq.heappush(track_members, m)
                        
                        if not matching_member:
                            track_leaders.pop(0)  # Remove leader if no match found
                            continue

                        # Get the actual Discord User objects
                        try:
                            leader_user = await bot.fetch_user(leader['user_id'])
                            member_user = await bot.fetch_user(matching_member['user_id'])
                            
                            if not leader_user or not member_user:
                                logger.error("Could not fetch user objects")
                                continue
                                
                            leader_channel = await leader_user.create_dm()
                            member_channel = await member_user.create_dm()
                        except discord.HTTPException as e:
                            logger.error(f"Failed to create DM channels: {e}")
                            continue

                        # Format messages
                        success_header = "```ansi\n\u001b[1;32m🎉 MATCHING SUCCESS! 🎉\u001b[0m\n```"
                        
                        leader_match_info = (
                            f"{success_header}\n"
                            f"**📋 Match Details**\n"
                            f"```yml\n"
                            f"Member Name   : {member_user.name}\n"
                            f"University    : {matching_member['university']}\n"
                            f"Department    : {matching_member['department'].upper()}\n"
                            f"Track         : {matching_member['track']}\n"
                            f"Team          : {leader['team_name']}\n"
                            f"```\n"
                        )

                        member_match_info = (
                            f"{success_header}\n"
                            f"**📋 Match Details**\n"
                            f"```yml\n"
                            f"Team Leader   : {leader_user.name}\n"
                            f"University    : {leader['university']}\n"
                            f"Department    : {leader['department'].upper()}\n"
                            f"Track         : {leader['track']}\n"
                            f"Team          : {leader['team_name']}\n"
                            f"```\n"
                        )

                        team_info = (
                            f"**🏢 Team Information**\n"
                            f"```ansi\n"
                            f"\u001b[1;34m── Team Leader's Message ──\u001b[0m\n"
                            f"{leader['team_comment']}\n"
                            f"```"
                        )

                        topics_str = ", ".join(matching_member["selected_topics"])
                        member_profile = (
                            f"**👤 Member Profile**\n"
                            f"```ansi\n"
                            f"\u001b[1;33m── Technical Background ──\u001b[0m\n"
                            f"• Track: {matching_member['track']}\n"
                            f"• Rating: {matching_member['rating']}%\n\n"
                            f"\u001b[1;33m── Topics Studied ──\u001b[0m\n"
                            f"{topics_str}\n\n"
                            f"\u001b[1;33m── Personal Note ──\u001b[0m\n"
                            f"{matching_member['comment']}\n"
                            f"```"
                        )

                        contact_info = (
                            f"**📱 Next Steps**\n"
                            f"```ansi\n"
                            f"\u001b[1;35mYou can now communicate directly through Discord!\u001b[0m\n"
                            f"Feel free to discuss project details and next steps.\n"
                            f"```"
                        )

                        # Send all messages with error handling
                        try:
                            await leader_channel.send(leader_match_info)
                            await leader_channel.send(team_info)
                            await leader_channel.send(member_profile)
                            await leader_channel.send(contact_info)
                            
                            await member_channel.send(member_match_info)
                            await member_channel.send(team_info)
                            await member_channel.send(member_profile)
                            await member_channel.send(contact_info)
                            
                            # Only proceed with cleanup if messages were sent successfully
                            # Clean up after successful match
                            leader_id = leader['user_id']
                            member_id = matching_member['user_id']
                            
                            track_leaders.pop(0)  # Now safe to remove the leader
                            leaders[track] = [l for l in leaders[track] if l['user_id'] != leader_id]
                            
                            if leader_id in user_data:
                                del user_data[leader_id]
                            if member_id in user_data:
                                del user_data[member_id]
                            
                            registered_users.discard(member_id)
                            matched_members.add(member_id)
                            
                            if leader_id in leader_departments:
                                del leader_departments[leader_id]
                            
                            matching_track_count += 1
                            logger.info(f"Successful match in track {track}: Leader {leader_id} with Member {member_id}")
                            
                        except discord.HTTPException as e:
                            logger.error(f"Failed to send match messages: {e}")
                            continue
                        except Exception as e:
                            logger.error(f"Error during match cleanup: {e}")
                            continue
                        
                    except Exception as e:
                        logger.error(f"Error in matching process for track {track}: {str(e)}")
                        continue
        
        # Save data after all matches are complete
        try:
            save_data()
        except Exception as e:
            logger.error(f"Error saving data after matching: {str(e)}")
        
        return matching_track_count
        
    except Exception as e:
        logger.error(f"Error in perform_matching: {str(e)}")
        return 0


# Add these helper functions for improved message formatting
def format_section_header(title, emoji=""):
    return f"```ansi\n\u001b[1;36m{emoji} {title} {emoji}\u001b[0m\n```"

def format_field(label, value):
    return f"{label:<12}: {value}"

# Message formatting functions
def format_embed_message(title, description, fields=None, color=0x3498db):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    
    return embed

def format_success_message(message):
    return f"```ansi\n\u001b[1;32m✅ {message}\u001b[0m\n```"

def format_error_message(message):
    return f"```ansi\n\u001b[1;31m❌ {message}\u001b[0m\n```"

def format_info_message(message):
    return f"```ansi\n\u001b[1;34mℹ️ {message}\u001b[0m\n```"

def format_warning_message(message):
    return f"```ansi\n\u001b[1;33m⚠️ {message}\u001b[0m\n```"

# Match Command with Enhanced Matching and Communication
@bot.command(name="match")
async def match(ctx):
    bot.loop.create_task(perform_matching())
    await ctx.send("Matching process started in the background.")


# Automatic Matching Task
@tasks.loop(seconds=30)
async def auto_match():
    await perform_matching()

# Start the auto-match task when the bot is ready
# Update the bot's event handlers
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    logger.info(f'Bot logged in as {bot.user}')
    load_data()  # Load saved data
    auto_match.start()
    
    # Schedule restart every hour
    schedule.every(45).minutes.do(schedule_restart)
    
    # Start schedule checker
    while True:
        schedule.run_pending()
        await asyncio.sleep(30)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("```❌ Invalid command. Use `!helpbot` for a list of commands.```")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("```❌ Missing required argument. Please check the command usage.```")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"```⏳ Please wait {error.retry_after:.2f}s before using this command again.```")
    else:
        error_msg = f"Command error: {str(error)}"
        logger.error(error_msg)
        await ctx.send(f"```❌ An error occurred. Please try again later.\nError: {str(error)}```")
    

# Run the bot
# write this if you use terminal or cmd : set DISCORD_BOT_TOKEN=your_bot_token_here
# write this if you use powershell : $env:DISCORD_BOT_TOKEN="your_bot_token_here"
# Update the main function
async def main():
    try:
        # Handle shutdown gracefully
        def signal_handler(sig, frame):
            logger.info("Shutdown signal received")
            save_data()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        async with bot:
            await bot.start(os.getenv("DISCORD_BOT_TOKEN"))
    except Exception as e:
        logger.error(f"Main function error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())