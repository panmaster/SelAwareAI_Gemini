from collections import defaultdict
from datetime import datetime
memory_templates = {
    "Base": {
        "structure": {
            # --- PERSONAL GROWTH & INSIGHTS  ---
            "Personal Growth & Development": {
                "Milestones": [],
                "Challenges Overcome": [],
                "Lessons Learned": [],
                "Skills Developed": [],
                "Values & Beliefs": [],
                "Goals & Aspirations": [],
                "Significant Decisions": {
                    "Choice Points": [],
                    "Reasons & Reflections": [],
                    "Consequences": [],
                    "What If": []  # Alternative paths not taken
                }
            },

            # --- RELATIONSHIPS & CONNECTIONS ---
            "Relationships & Social Connections": {
                "Family": {
                    "Parents": [],
                    "Siblings": [],
                    "Extended Family": [],
                    "Significant Family Events": []
                },
                "Friendships": {
                    "Close Friends": [],
                    "Circles & Groups": [],
                    "Meaningful Interactions": []
                },
                "Romantic Relationships": {
                    "Partners": [],
                    "Dates & Special Moments": [],
                    "Relationship Milestones": [],
                    "Intimacy & Sexuality": {
                        "Experiences": [],
                        "Reflections": [],
                        "Boundaries": [],
                        "Consent": [],
                        "Values": []
                    }
                },
                "Professional Relationships": {
                    "Colleagues & Peers": [],
                    "Mentors & Role Models": [],
                    "Clients & Collaborators": []
                }
            },

            # --- TRAVEL & EXPLORATION ---
            "Travel & Exploration": {
                "Trips & Journeys": {
                    "By Destination": {},  # Memories organized by place
                    "By Purpose": {}  # Memories grouped by reason for travel
                },
                "Significant Locations": {
                    "Homes": [],
                    "Cities": [],
                    "Natural Places": []
                },
                "Cultures & Experiences": [],
                "Sensory Memories": {
                    "Sights": [],
                    "Sounds": [],
                    "Tastes": [],
                    "Smells": [],
                    "Touch & Textures": []
                }
            },

            # --- HOBBIES, INTERESTS & CREATIVITY ---
            "Hobbies, Interests & Passions": {
                "Creative Pursuits": {
                    "Writing": {
                        "My Writing": [],  # Your own works
                        "Inspirations": []  # Inspiring authors, books, etc.
                    },
                    "Music": {
                        "My Music": [],  # Your compositions, performances
                        "Inspirations": []  # Favorite artists, albums
                    },
                    "Art": {
                        "My Art": [],
                        "Inspirations": []
                    },
                    "Performance": {
                        "My Performances": [],
                        "Inspirations": []
                    },
                    "Crafting": {
                        "My Creations": [],
                        "Inspirations": []
                    }
                    # ... Add other creative outlets
                },
                "Sports & Fitness": {
                    "Individual Sports": [],
                    "Team Sports": [],
                    "Fitness Activities": [],
                    "Competitions & Events": []
                },
                "Learning & Exploration": {
                    "Subjects & Topics": [],
                    "Books & Articles": [],
                    "Courses & Workshops": [],
                    "Documentaries & Films": []
                }
            },

            # --- KNOWLEDGE, LEARNING & RESOURCES ---
            "Knowledge & Education": {
                "Formal Education": {
                    "Schools": [],
                    "Degrees & Certifications": [],
                    "Significant Projects": []
                },
                "Self-Directed Learning": {
                    "Skills Acquired": [],
                    "Areas of Interest": [],
                    "Learning Resources": {
                        "Bookshelf": [],
                        "Online Courses": [],
                        "Mentors & Teachers": []
                    }
                },
                "Knowledge Base": {
                    "Facts & Concepts": [],
                    "Historical Events": [],
                    "Scientific Discoveries": [],
                    "Philosophical Ideas": [],
                    "Artistic Movements": [],
                    "Cultural Insights": []
                },
                "Laws & Regulations": {
                    "Legal Knowledge": [],
                    "Personal Experiences with Laws": [],
                    "Understanding of Legal Systems": []
                }
            },

            # --- WORK & CAREER ---
            "Work & Career": {
                "Jobs & Positions": [],
                "Projects & Accomplishments": [],
                "Skills & Expertise": [],
                "Career Goals": []
            },

            # --- HEALTH & WELLBEING ---
            "Health & Wellbeing": {
                "Physical Health": {
                    "Body Image": [],
                    "Experiences": []
                },
                "Mental & Emotional Health": [],
                "Habits & Routines": [],
                "Pain & Discomfort": {
                    "Physical Pain": [],
                    "Emotional Pain": []
                }
            },

            # --- INTELLECTUAL & CONCEPTUAL ---
            "Intellectual & Conceptual": {
                "Concepts & Ideas": {
                    "Key Concepts": [],
                    "Emerging Ideas": [],
                    "Areas of Interest": []
                },
                "Problems & Challenges": {
                    "Unresolved Problems": [],
                    "Past Challenges": [],
                    "Problem-Solving Strategies": []
                },
                "Contradictions & Paradoxes": [],
                "Unknowns & Mysteries": [],
                "Questions & Inquiries": []
            },

            # --- DREAMS, INTUITIONS & SUBCONSCIOUS ---
            "Dreams & Subconscious": {
                "Dream Journal": [],
                "Intuitions & Insights": [],
                "Recurring Themes": []
            },

            # --- CHALLENGES & SETBACKS ---
            "Challenges & Setbacks": {
                "Significant Mistakes": {
                    "Description": [],
                    "Lessons Learned": [],
                    "How I Grew": []
                },
                "Failures & Disappointments": {
                    "In Personal Projects": [],
                    "In Relationships": [],
                    "In Career": []
                    # ... other relevant areas
                },
                "Difficult Emotions": {
                    "Fear & Anxiety": [],
                    "Anger & Frustration": [],
                    "Sadness & Grief": [],
                    "Shame & Guilt": [],
                    "Jealousy & Envy": [],
                    "Trauma & Abuse": {
                        "Experiences": [],
                        "Impact": [],
                        "Healing Journey": []
                    },
                    # ... other challenging emotions
                },
                "Negative Thought Patterns": [],  # To identify and address
                "Areas for Improvement": []  # Personal growth opportunities
            },

            # --- SENSITIVE EXPERIENCES ---
            "Sensitive Experiences": {
                "Sexuality & Intimacy": {
                    "Experiences": [],
                    "Reflections": [],
                    "Boundaries": [],
                    "Consent": [],
                    "Values": []
                },
                "Trauma & Abuse": {
                    "Physical": [],
                    "Emotional": [],
                    "Sexual": [],
                    "Impact": [],
                    "Healing Journey": []
                },
                "Dangerous Situations": {
                    "Experiences": [],
                    "Impact": [],
                    "Lessons Learned": []
                }
            },

            # --- GOALS, VISIONS & FUTURE ---
            "Goals & Visions": {
                "Life Vision Board": [],  # Big picture aspirations
                "Personal Goals": [],
                "Professional Goals": [],
                "Creative Goals": [],
                "Relationship Goals": [],
                "Health & Wellbeing Goals": [],
                "Learning Goals": [],
                "Action Plans": {}  # Connect plans to specific goals
            },

            # --- SIGNIFICANT EVENTS & MEMORIES ---
            "Significant Events & Memories": {
                "Positive": [],
                "Negative": [],
                "Life-Changing": {
                    "Positive": [],
                    "Negative": []
                }
            }
        }
    },
    "Second": {
        "structure": {
            "Actions and Results": {
                "past": [
                    {"category": "Personal Growth & Development", "items": ["Milestones", "Challenges Overcome", "Significant Decisions.Choice Points", "Significant Decisions.Consequences"]},
                    {"category": "Relationships & Social Connections", "items": ["Family.Significant Family Events", "Friendships.Meaningful Interactions", "Romantic Relationships.Relationship Milestones", "Professional Relationships.Projects & Accomplishments"]},
                    {"category": "Travel & Exploration", "items": ["Trips & Journeys.By Destination", "Trips & Journeys.By Purpose", "Cultures & Experiences"]},
                    {"category": "Hobbies, Interests & Passions", "items": ["Creative Pursuits.My Writing", "Creative Pursuits.My Music", "Creative Pursuits.My Art", "Creative Pursuits.My Performances", "Creative Pursuits.My Creations", "Sports & Fitness.Competitions & Events", "Learning & Exploration.Courses & Workshops", "Learning & Exploration.Documentaries & Films"]},
                    {"category": "Knowledge & Education", "items": ["Formal Education.Schools", "Formal Education.Degrees & Certifications", "Formal Education.Significant Projects", "Self-Directed Learning.Skills Acquired", "Self-Directed Learning.Learning Resources"]},
                    {"category": "Work & Career", "items": ["Jobs & Positions", "Projects & Accomplishments"]},
                    {"category": "Health & Wellbeing", "items": ["Physical Health.Experiences", "Habits & Routines"]},
                    {"category": "Intellectual & Conceptual", "items": ["Concepts & Ideas.Key Concepts", "Problems & Challenges.Past Challenges", "Problems & Challenges.Problem-Solving Strategies"]},
                    {"category": "Dreams & Subconscious", "items": ["Dream Journal", "Intuitions & Insights"]},
                    {"category": "Challenges & Setbacks", "items": ["Significant Mistakes.Description", "Failures & Disappointments", "Difficult Emotions.Experiences", "Negative Thought Patterns"]},
                    {"category": "Sensitive Experiences", "items": ["Sexuality & Intimacy.Experiences", "Trauma & Abuse.Experiences", "Dangerous Situations.Experiences"]},
                    {"category": "Goals & Visions", "items": ["Action Plans"]}
                ],
                "present": [
                    {"category": "Personal Growth & Development", "items": ["Skills Developed", "Goals & Aspirations"]},
                    {"category": "Relationships & Social Connections", "items": ["Family.Parents", "Family.Siblings", "Family.Extended Family", "Friendships.Close Friends", "Friendships.Circles & Groups", "Romantic Relationships.Partners", "Professional Relationships.Colleagues & Peers", "Professional Relationships.Mentors & Role Models", "Professional Relationships.Clients & Collaborators"]},
                    {"category": "Travel & Exploration", "items": ["Significant Locations.Homes", "Significant Locations.Cities", "Significant Locations.Natural Places", "Sensory Memories"]},
                    {"category": "Hobbies, Interests & Passions", "items": ["Creative Pursuits.Inspirations", "Sports & Fitness.Individual Sports", "Sports & Fitness.Team Sports", "Sports & Fitness.Fitness Activities", "Learning & Exploration.Subjects & Topics", "Learning & Exploration.Books & Articles"]},
                    {"category": "Knowledge & Education", "items": ["Knowledge Base", "Laws & Regulations"]},
                    {"category": "Work & Career", "items": ["Skills & Expertise", "Career Goals"]},
                    {"category": "Health & Wellbeing", "items": ["Physical Health.Body Image", "Mental & Emotional Health", "Pain & Discomfort"]},
                    {"category": "Intellectual & Conceptual", "items": ["Concepts & Ideas.Emerging Ideas", "Concepts & Ideas.Areas of Interest", "Problems & Challenges.Unresolved Problems", "Contradictions & Paradoxes", "Unknowns & Mysteries", "Questions & Inquiries"]},
                    {"category": "Challenges & Setbacks", "items": ["Significant Mistakes.Lessons Learned", "Significant Mistakes.How I Grew", "Difficult Emotions.Impact", "Difficult Emotions.Healing Journey", "Areas for Improvement"]},
                    {"category": "Sensitive Experiences", "items": ["Sexuality & Intimacy.Reflections", "Sexuality & Intimacy.Boundaries", "Sexuality & Intimacy.Consent", "Sexuality & Intimacy.Values", "Trauma & Abuse.Impact", "Trauma & Abuse.Healing Journey", "Dangerous Situations.Impact", "Dangerous Situations.Lessons Learned"]},
                    {"category": "Goals & Visions", "items": ["Life Vision Board", "Personal Goals", "Professional Goals", "Creative Goals", "Relationship Goals", "Health & Wellbeing Goals", "Learning Goals"]}
                ],
                "future": [
                    {"category": "Personal Growth & Development", "items": ["Significant Decisions.What If"]},
                    {"category": "Relationships & Social Connections", "items": ["Romantic Relationships.Dates & Special Moments"]},
                    {"category": "Goals & Visions", "items": ["Action Plans.Specific Actions", "Action Plans.Expected Outcomes"]}
                ]
            },
            "Things": {
                "past": [
                    {"category": "Travel & Exploration", "items": ["Trips & Journeys.By Destination", "Significant Locations.Homes", "Significant Locations.Cities", "Significant Locations.Natural Places", "Cultures & Experiences"]},
                    {"category": "Hobbies, Interests & Passions", "items": ["Creative Pursuits.My Writing", "Creative Pursuits.My Music", "Creative Pursuits.My Art", "Creative Pursuits.My Performances", "Creative Pursuits.My Creations", "Learning & Exploration.Books & Articles"]},
                    {"category": "Knowledge & Education", "items": ["Formal Education.Schools", "Formal Education.Degrees & Certifications", "Self-Directed Learning.Learning Resources.Bookshelf", "Self-Directed Learning.Learning Resources.Online Courses", "Knowledge Base", "Laws & Regulations.Legal Knowledge"]},
                    {"category": "Work & Career", "items": ["Jobs & Positions", "Projects & Accomplishments"]},
                    {"category": "Dreams & Subconscious", "items": ["Dream Journal", "Recurring Themes"]},
                    {"category": "Challenges & Setbacks", "items": ["Failures & Disappointments"]}
                ],
                "present": [
                    {"category": "Relationships & Social Connections", "items": ["Family.Parents", "Family.Siblings", "Family.Extended Family", "Friendships.Close Friends", "Friendships.Circles & Groups", "Romantic Relationships.Partners", "Professional Relationships.Colleagues & Peers", "Professional Relationships.Mentors & Role Models", "Professional Relationships.Clients & Collaborators"]},
                    {"category": "Hobbies, Interests & Passions", "items": ["Sports & Fitness.Individual Sports", "Sports & Fitness.Team Sports", "Sports & Fitness.Fitness Activities"]},
                    {"category": "Knowledge & Education", "items": ["Self-Directed Learning.Learning Resources.Mentors & Teachers"]},
                    {"category": "Work & Career", "items": ["Skills & Expertise"]},
                    {"category": "Health & Wellbeing", "items": ["Physical Health.Body Image", "Habits & Routines"]},
                    {"category": "Intellectual & Conceptual", "items": ["Concepts & Ideas.Areas of Interest", "Problems & Challenges.Unresolved Problems", "Contradictions & Paradoxes", "Unknowns & Mysteries", "Questions & Inquiries"]},
                    {"category": "Challenges & Setbacks", "items": ["Significant Mistakes.Description", "Difficult Emotions.Negative Thought Patterns"]}
                ],
                "future": [
                    {"category": "Goals & Visions", "items": ["Life Vision Board", "Personal Goals", "Professional Goals", "Creative Goals", "Relationship Goals", "Health & Wellbeing Goals", "Learning Goals"]}
                ]
            },
            "OwnState": {
                "past": [
                    {"category": "Personal Growth & Development", "items": ["Lessons Learned", "Values & Beliefs"]},
                    {"category": "Relationships & Social Connections", "items": ["Romantic Relationships.Intimacy & Sexuality.Experiences", "Romantic Relationships.Intimacy & Sexuality.Reflections", "Romantic Relationships.Intimacy & Sexuality.Boundaries", "Romantic Relationships.Intimacy & Sexuality.Consent", "Romantic Relationships.Intimacy & Sexuality.Values"]},
                    {"category": "Health & Wellbeing", "items": ["Mental & Emotional Health"]},
                    {"category": "Challenges & Setbacks", "items": ["Significant Mistakes.Lessons Learned", "Significant Mistakes.How I Grew", "Failures & Disappointments", "Difficult Emotions.Impact", "Difficult Emotions.Healing Journey", "Areas for Improvement"]},
                    {"category": "Sensitive Experiences", "items": ["Sexuality & Intimacy.Experiences", "Sexuality & Intimacy.Reflections", "Sexuality & Intimacy.Boundaries", "Sexuality & Intimacy.Consent", "Sexuality & Intimacy.Values", "Trauma & Abuse.Impact", "Trauma & Abuse.Healing Journey", "Dangerous Situations.Impact", "Dangerous Situations.Lessons Learned"]},
                    {"category": "Goals & Visions", "items": ["Life Vision Board"]}
                ],
                "present": [
                    {"category": "Health & Wellbeing", "items": ["Physical Health.Body Image", "Physical Health.Experiences", "Mental & Emotional Health", "Pain & Discomfort"]},
                    {"category": "Challenges & Setbacks", "items": ["Negative Thought Patterns"]}
                ],
                "future": [
                    {"category": "Personal Growth & Development", "items": ["Goals & Aspirations"]},
                    {"category": "Relationships & Social Connections", "items": ["Romantic Relationships.Dates & Special Moments"]},
                    {"category": "Goals & Visions", "items": ["Personal Goals", "Professional Goals", "Creative Goals", "Relationship Goals", "Health & Wellbeing Goals", "Learning Goals"]}
                ]
            },
            "Paradoxes and Contradictions": {
                "past": [
                    {"category": "Intellectual & Conceptual", "items": ["Past Paradoxes", "Past Internal Conflicts", "Past Cognitive Dissonance"]},
                    {"category": "Challenges & Setbacks", "items": ["Significant Mistakes.Description", "Failures & Disappointments", "Difficult Emotions.Impact", "Difficult Emotions.Healing Journey", "Areas for Improvement"]}
                ],
                "present": [
                    {"category": "Intellectual & Conceptual", "items": ["Current Paradoxes", "Ongoing Internal Conflicts", "Current Cognitive Dissonance"]},
                    {"category": "Challenges & Setbacks", "items": ["Negative Thought Patterns"]}
                ],
                "future": [
                    {"category": "Intellectual & Conceptual", "items": ["Potential Paradoxes", "Expected Internal Conflicts", "Strategies to Address Dissonance"]}
                ]
            },
            "Living Things": {
                "past": [
                    {"category": "Relationships & Social Connections", "items": ["Family.Parents", "Family.Siblings", "Family.Extended Family", "Friendships.Close Friends", "Friendships.Circles & Groups", "Romantic Relationships.Partners", "Professional Relationships.Colleagues & Peers", "Professional Relationships.Mentors & Role Models", "Professional Relationships.Clients & Collaborators"]},
                    {"category": "Travel & Exploration", "items": ["Cultures & Experiences"]},
                    {"category": "Challenges & Setbacks", "items": ["Failures & Disappointments.In Relationships"]}
                ],
                "present": [
                    {"category": "Relationships & Social Connections", "items": ["Family.Parents", "Family.Siblings", "Family.Extended Family", "Friendships.Close Friends", "Friendships.Circles & Groups", "Romantic Relationships.Partners", "Professional Relationships.Colleagues & Peers", "Professional Relationships.Mentors & Role Models", "Professional Relationships.Clients & Collaborators"]},
                    {"category": "Travel & Exploration", "items": ["Cultures & Experiences"]},
                    {"category": "Hobbies, Interests & Passions", "items": ["Sports & Fitness.Team Sports"]}
                ],
                "future": [
                    {"category": "Relationships & Social Connections", "items": ["Romantic Relationships.Dates & Special Moments"]},
                    {"category": "Goals & Visions", "items": ["Relationship Goals"]}
                ]
            }
        }
    },
    "Journey": {
        "structure": {
            # --- CORE EXPERIENCES  ---
            "Core Experiences": {
                "Key Moments": {
                    "Significant Events": [],  # Birthdays, graduations, travels, etc.
                    "Life-Changing Events": [],
                    "Turning Points": []  # Moments that shifted your path
                },
                "Recurring Themes": [],  # Patterns in your experiences
                "Challenges Faced": {
                    "External Challenges": [],  # Obstacles from the outside world
                    "Internal Challenges": [],  # Inner conflicts, fears, etc.
                },
                "Triumphs & Accomplishments": {
                    "Personal Achievements": [],
                    "Professional Successes": [],
                    "Creative Wins": []
                }
            },

            # --- EMOTIONAL LANDSCAPE ---
            "Emotional Landscape": {
                "Dominant Emotions": {
                    "Joy & Excitement": [],
                    "Love & Connection": [],
                    "Sadness & Grief": [],
                    "Anger & Frustration": [],
                    "Fear & Anxiety": [],
                    "Other Emotions": []
                },
                "Emotional Triggers": {
                    "Situations": [],  # Events that evoke specific emotions
                    "People": [],
                    "Thoughts": []
                },
                "Emotional Growth": {
                    "Overcoming Negative Patterns": [],
                    "Developing Emotional Intelligence": [],
                    "Building Resilience": []
                }
            },

            # ---  REFLECTIONS & INSIGHTS ---
            "Reflections & Insights": {
                "Personal Values": [],  # What matters most to you
                "Beliefs & Assumptions": [],
                "Lessons Learned": {
                    "From Successes": [],
                    "From Mistakes": [],
                    "From Relationships": []
                },
                "Wisdom & Understanding": [],
                "Self-Discovery": {
                    "Strengths & Talents": [],
                    "Areas for Growth": [],
                    "What I've Learned About Myself": []
                }
            },

            # --- RELATIONSHIPS & CONNECTIONS ---
            "Relationships & Connections": {
                "Family": {
                    "Bonds & Dynamics": [],
                    "Key Moments": [],
                    "Impact on My Life": []
                },
                "Friendships": {
                    "Meaningful Connections": [],
                    "Shared Experiences": [],
                    "Impact on My Life": []
                },
                "Romantic Relationships": {
                    "Significant Partners": [],
                    "Key Moments": [],
                    "Impact on My Life": []
                },
                "Professional Relationships": {
                    "Mentors & Guides": [],
                    "Collaborative Projects": [],
                    "Impact on My Life": []
                }
            },

            # ---  FUTURE ASPIRATIONS ---
            "Future Aspirations": {
                "Personal Goals": [],
                "Professional Goals": [],
                "Creative Goals": [],
                "Relationship Goals": [],
                "Life Vision": []  # Overall direction and aspirations
            }
        }
    },
    "Hierarchical": {
        "structure": {
            # --- LIFE EVENTS & TRANSITIONS ---
            "Life Events & Transitions": {
                "Significant Events": {
                    "Personal": [
                        {"category": "Birthdays", "items": []},
                        {"category": "Graduations", "items": []},
                        {"category": "Weddings", "items": []},
                        {"category": "Other Personal Events", "items": []}
                    ],
                    "Professional": [
                        {"category": "Job Changes", "items": []},
                        {"category": "Promotions", "items": []},
                        {"category": "Project Completions", "items": []},
                        {"category": "Other Professional Events", "items": []}
                    ],
                    "Travel": [
                        {"category": "Trips & Journeys", "items": []},
                        {"category": "Moving Homes", "items": []},
                        {"category": "Other Travel Events", "items": []}
                    ]
                },
                "Life Transitions": {
                    "Personal Growth": [
                        {"category": "Milestones", "items": []},
                        {"category": "Challenges Overcome", "items": []},
                        {"category": "Significant Decisions", "items": []},
                        {"category": "Personal Beliefs & Values", "items": []}
                    ],
                    "Relationships": [
                        {"category": "Family Dynamics", "items": []},
                        {"category": "Friendships", "items": []},
                        {"category": "Romantic Relationships", "items": []},
                        {"category": "Professional Connections", "items": []}
                    ],
                    "Health & Wellbeing": [
                        {"category": "Physical Health", "items": []},
                        {"category": "Mental & Emotional Health", "items": []},
                        {"category": "Habits & Routines", "items": []}
                    ],
                    "Knowledge & Skills": [
                        {"category": "Formal Education", "items": []},
                        {"category": "Self-Directed Learning", "items": []},
                        {"category": "Skills & Expertise", "items": []}
                    ]
                }
            },

            # --- EMOTIONS & REFLECTIONS ---
            "Emotions & Reflections": {
                "Emotional Experiences": {
                    "Dominant Emotions": [
                        {"category": "Joy & Excitement", "items": []},
                        {"category": "Love & Connection", "items": []},
                        {"category": "Sadness & Grief", "items": []},
                        {"category": "Anger & Frustration", "items": []},
                        {"category": "Fear & Anxiety", "items": []},
                        {"category": "Other Emotions", "items": []}
                    ],
                    "Emotional Triggers": [
                        {"category": "Situations", "items": []},
                        {"category": "People", "items": []},
                        {"category": "Thoughts", "items": []}
                    ]
                },
                "Personal Growth & Insights": {
                    "Lessons Learned": [
                        {"category": "From Successes", "items": []},
                        {"category": "From Mistakes", "items": []},
                        {"category": "From Relationships", "items": []}
                    ],
                    "Self-Discovery": [
                        {"category": "Strengths & Talents", "items": []},
                        {"category": "Areas for Growth", "items": []},
                        {"category": "What I've Learned About Myself", "items": []}
                    ]
                }
            },

            # ---  GOALS & ASPIRATIONS ---
            "Goals & Aspirations": {
                "Personal Goals": [
                    {"category": "Health & Wellbeing", "items": []},
                    {"category": "Personal Development", "items": []},
                    {"category": "Relationships", "items": []},
                    {"category": "Creative Pursuits", "items": []},
                    {"category": "Other Personal Goals", "items": []}
                ],
                "Professional Goals": [
                    {"category": "Career Advancement", "items": []},
                    {"category": "Skills & Expertise", "items": []},
                    {"category": "Project Goals", "items": []},
                    {"category": "Other Professional Goals", "items": []}
                ],
                "Life Vision": {
                    "Values & Beliefs", "Aspirations", "Dreams"
                }
            }
        }
    },
    "Emotional Landscapes": {
        "structure": {
            # ---  EMOTIONAL WEATHER ---
            "Emotional Weather": {
                "Dominant Weather Patterns": {
                    "Calm & Serene": {
                        "Description": [],
                        "Triggers": [],
                        "Physical Sensations": []
                    },
                    "Energetic & Excited": {
                        "Description": [],
                        "Triggers": [],
                        "Physical Sensations": []
                    },
                    "Anxious & Worried": {
                        "Description": [],
                        "Triggers": [],
                        "Physical Sensations": []
                    },
                    "Sad & Melancholy": {
                        "Description": [],
                        "Triggers": [],
                        "Physical Sensations": []
                    },
                    "Angry & Frustrated": {
                        "Description": [],
                        "Triggers": [],
                        "Physical Sensations": []
                    },
                    "Other Weather Patterns": []  # Add any additional patterns
                },
                "Weather Shifts": {
                    "Sudden Shifts": [],
                    "Gradual Changes": [],
                    "Factors Influencing Shifts": []
                }
            },

            # ---  EMOTIONAL PALETTE ---
            "Emotional Palette": {
                "Dominant Colors": {
                    "Joy & Happiness": {
                        "Description": [],
                        "Examples": [],
                        "Impact on Life": []
                    },
                    "Love & Connection": {
                        "Description": [],
                        "Examples": [],
                        "Impact on Life": []
                    },
                    "Peace & Tranquility": {
                        "Description": [],
                        "Examples": [],
                        "Impact on Life": []
                    },
                    "Creativity & Inspiration": {
                        "Description": [],
                        "Examples": [],
                        "Impact on Life": []
                    },
                    "Other Colors": []
                },
                "Color Blends": {
                    "Complementary Blends": [],
                    "Contrasting Blends": [],
                    "Impact of Blends": []
                }
            },

            # ---  EMOTIONAL REFLECTIONS ---
            "Emotional Reflections": {
                "Self-Awareness": {
                    "Emotional Triggers": [],
                    "Emotional Responses": [],
                    "Emotional Resilience": []
                },
                "Emotional Growth": {
                    "Learning & Understanding": [],
                    "Managing Emotions": [],
                    "Developing Emotional Intelligence": []
                }
            }
        }
    },
    "Thematic": {
        "structure": {
            # --- CORE THEMES  ---
            "Core Themes": {
                "Love & Connection": {
                    "Memories": [],
                    "Insights & Reflections": [],
                    "Values & Beliefs": []
                },
                "Growth & Transformation": {
                    "Memories": [],
                    "Insights & Reflections": [],
                    "Values & Beliefs": []
                },
                "Adventure & Exploration": {
                    "Memories": [],
                    "Insights & Reflections": [],
                    "Values & Beliefs": []
                },
                "Creativity & Expression": {
                    "Memories": [],
                    "Insights & Reflections": [],
                    "Values & Beliefs": []
                },
                "Purpose & Meaning": {
                    "Memories": [],
                    "Insights & Reflections": [],
                    "Values & Beliefs": []
                },
                "Other Themes": []  # Add more themes as needed
            },

            # ---  KEY LIFE STAGES  ---
            "Life Stages": {
                "Childhood": {
                    "Memories": [],
                    "Significant People": [],
                    "Key Events & Experiences": []
                },
                "Adolescence": {
                    "Memories": [],
                    "Significant People": [],
                    "Key Events & Experiences": []
                },
                "Young Adulthood": {
                    "Memories": [],
                    "Significant People": [],
                    "Key Events & Experiences": []
                },
                "Midlife": {
                    "Memories": [],
                    "Significant People": [],
                    "Key Events & Experiences": []
                },
                "Later Life": {
                    "Memories": [],
                    "Significant People": [],
                    "Key Events & Experiences": []
                }
            },

            # ---  EMOTIONAL LANDSCAPE  ---
            "Emotional Landscape": {
                "Dominant Emotions": {
                    "Joy & Excitement": [],
                    "Love & Connection": [],
                    "Sadness & Grief": [],
                    "Anger & Frustration": [],
                    "Fear & Anxiety": [],
                    "Other Emotions": []
                },
                "Emotional Triggers": {
                    "Situations": [],
                    "People": [],
                    "Thoughts": []
                },
                "Emotional Growth": {
                    "Overcoming Negative Patterns": [],
                    "Developing Emotional Intelligence": [],
                    "Building Resilience": []
                }
            }
        }
    },
    "Thought Threads": {
        "structure": {
            # --- CORE EXPERIENCES ---
            "Core Experiences": {
                "Significant Events": {
                    "Event": [],
                    "Thought Thread": [],
                    "Reflections": []
                },
                "Recurring Themes": {
                    "Theme": [],
                    "Thought Thread": [],
                    "Reflections": []
                },
                "Challenges Faced": {
                    "Challenge": [],
                    "Thought Thread": [],
                    "Reflections": []
                },
                "Triumphs & Accomplishments": {
                    "Accomplishment": [],
                    "Thought Thread": [],
                    "Reflections": []
                }
            },

            # --- RELATIONSHIPS & CONNECTIONS ---
            "Relationships & Connections": {
                "Relationship Type": {
                    "Person/Group": [],
                    "Thought Thread": [],
                    "Reflections": []
                },
                "Key Moments": {
                    "Moment": [],
                    "Thought Thread": [],
                    "Reflections": []
                }
            },

            # --- EMOTIONAL LANDSCAPE ---
            "Emotional Landscape": {
                "Emotions": {
                    "Emotion": [],
                    "Thought Thread": [],
                    "Reflections": []
                },
                "Emotional Triggers": {
                    "Trigger": [],
                    "Thought Thread": [],
                    "Reflections": []
                }
            },

            # ---  REFLECTIONS & INSIGHTS ---
            "Reflections & Insights": {
                "Insights": {
                    "Insight": [],
                    "Thought Thread": [],
                    "Reflections": []
                },
                "Self-Discovery": {
                    "Discovery": [],
                    "Thought Thread": [],
                    "Reflections": []
                }
            },

            # ---  GOALS & ASPIRATIONS ---
            "Goals & Aspirations": {
                "Goals": {
                    "Goal": [],
                    "Thought Thread": [],
                    "Reflections": []
                },
                "Life Vision": {
                    "Vision": [],
                    "Thought Thread": [],
                    "Reflections": []
                }
            }
        }
    },
    "Memory Tree (Environments)": {
        "structure": {
            # --- ENVIRONMENTS ---
            "Environments": {
                "Homes": {
                    "Current Home": {
                        "Memories": [],
                        "Sensory Details": {
                            "Sights": [],
                            "Sounds": [],
                            "Smells": [],
                            "Tastes": [],
                            "Textures": []
                        },
                        "Key Events & Moments": [],
                        "Reflections & Insights": []
                    },
                    "Past Homes": {
                        "Home 1": {
                            "Memories": [],
                            "Sensory Details": {
                                "Sights": [],
                                "Sounds": [],
                                "Smells": [],
                                "Tastes": [],
                                "Textures": []
                            },
                            "Key Events & Moments": [],
                            "Reflections & Insights": []
                        },
                        "Home 2": {
                            "Memories": [],
                            "Sensory Details": {
                                "Sights": [],
                                "Sounds": [],
                                "Smells": [],
                                "Tastes": [],
                                "Textures": []
                            },
                            "Key Events & Moments": [],
                            "Reflections & Insights": []
                        },
                        # ... add more past homes
                    }
                },
                "Cities & Towns": {
                    "Cities": {
                        "Memories": [],
                        "Sensory Details": {
                            "Sights": [],
                            "Sounds": [],
                            "Smells": [],
                            "Tastes": [],
                            "Textures": []
                        },
                        "Key Events & Moments": [],
                        "Reflections & Insights": []
                    },

                },
                "Nature & Outdoors": {
                    "Nature Location 1": {
                        "Memories": [],
                        "Sensory Details": {
                            "Sights": [],
                            "Sounds": [],
                            "Smells": [],
                            "Tastes": [],
                            "Textures": []
                        },
                        "Key Events & Moments": [],
                        "Reflections & Insights": []
                    },
                    "Nature Location 2": {
                        "Memories": [],
                        "Sensory Details": {
                            "Sights": [],
                            "Sounds": [],
                            "Smells": [],
                            "Tastes": [],
                            "Textures": []
                        },
                        "Key Events & Moments": [],
                        "Reflections & Insights": []
                    },
                    # ... add more nature locations
                },
                "Other Environments": {
                    "Environment 1": {
                        "Memories": [],
                        "Sensory Details": {
                            "Sights": [],
                            "Sounds": [],
                            "Smells": [],
                            "Tastes": [],
                            "Textures": []
                        },
                        "Key Events & Moments": [],
                        "Reflections & Insights": []
                    },
                    "Environment 2": {
                        "Memories": [],
                        "Sensory Details": {
                            "Sights": [],
                            "Sounds": [],
                            "Smells": [],
                            "Tastes": [],
                            "Textures": []
                        },
                        "Key Events & Moments": [],
                        "Reflections & Insights": []
                    },
                    # ... add more other environments
                }
            }
        }
    ,
    "Template 10: Memory Tree (Importance Levels)": {
        "structure": {
            # --- IMPORTANCE LEVELS ---
            "Importance Levels": {
                "Life-Changing": {
                    "Events": [],
                    "Reflections": []
                },
                "Significant": {
                    "Events": [],
                    "Reflections": []
                },
                "Memorable": {
                    "Events": [],
                    "Reflections": []
                },
                "Everyday": {
                    "Events": [],
                    "Reflections": []
                }
            }
        }
    }
},
    "Tapestry of Experiences": {
    "structure": {
        "Central Threads": {  # These act like branches in a mind map
            "My Essence": {  # Core values, beliefs, personality
                "Values & Beliefs": [],
                "Strengths & Weaknesses": [],
                "Passions & Interests": [],
                "Sensory Delights": { # Favorite sights, sounds, smells, tastes, textures
                    "Sight": [], "Sound": [], "Smell": [], "Taste": [], "Touch": []
                }
            },
            "Relationships": {
                "Family Tapestry": [],
                "Friendships": [],
                "Romantic Bonds": [],
                "Professional Connections": []
            },
            "Life's Adventures": {
                "Travel & Exploration": [],
                "Creative Pursuits": [],
                "Learning & Growth": []
            },
            "Challenges & Triumphs": { # Story Arc Element
                "Overcoming Adversity": {
                    "Challenges Faced": [],
                    "Lessons Learned": [],
                    "Resilience & Growth": []
                },
                "Celebrating Victories": {
                    "Personal Triumphs": [],
                    "Shared Successes": []
                }
            }
        },
        "Connecting Threads": [] # Use to link memories, themes, and insights across categories
    }
},
    "Technology": {
        "structure": {
            # ---  TECHNOLOGICAL EXPERIENCES ---
            "Technological Experiences": {
                "Personal Devices": {
                    "Computers & Laptops": {
                        "First Computer": [],
                        "Significant Upgrades": [],
                        "Software & Operating Systems": [],
                        "Key Projects & Creations": []
                    },
                    "Mobile Phones & Tablets": {
                        "First Mobile Phone": [],
                        "Significant Upgrades": [],
                        "Apps & Services": [],
                        "Key Projects & Creations": []
                    },
                    "Other Devices": {
                        "Smart Home Devices": [],
                        "Wearables": [],
                        "Gaming Consoles": [],
                        "Other Devices": []
                    }
                },
                "Software & Programming": {
                    "Programming Languages Learned": [],
                    "Key Projects & Applications": [],
                    "Online Communities & Resources": [],
                    "Coding Challenges & Competitions": []
                },
                "Internet & Digital Culture": {
                    "First Internet Experience": [],
                    "Social Media Platforms": {
                        "Favorite Platforms": [],
                        "Key Interactions & Communities": [],
                        "Influential Content": []
                    },
                    "Online Games & Gaming": {
                        "Favorite Games & Genres": [],
                        "Key Achievements & Moments": [],
                        "Gaming Communities": []
                    },
                    "Digital Content Consumption": {
                        "Favorite Websites & Services": [],
                        "Influential Creators & Content": [],
                        "Digital Collections": []
                    },
                    "Other Digital Experiences": []
                },
                "Emerging Technologies": {
                    "Areas of Interest": [],
                    "Concepts & Applications": [],
                    "Predictions & Visions": []
                }
            },

            # --- TECH-RELATED REFLECTIONS ---
            "Tech-Related Reflections": {
                "Impact on Life": {
                    "Positive Impacts": [],
                    "Negative Impacts": [],
                    "Changes in Habits & Behaviors": []
                },
                "Ethics & Values": {
                    "Concerns & Dilemmas": [],
                    "Ethical Principles & Frameworks": [],
                    "Personal Stance on Tech Issues": []
                },
                "Technological Literacy": {
                    "Skills & Knowledge": [],
                    "Areas for Improvement": [],
                    "Future Learning Goals": []
                }
            }
        }
    },
    "Health & Wellness": {
        "structure": {
            # ---  PHYSICAL HEALTH ---
            "Physical Health": {
                "Body Image & Self-Perception": {
                    "Past Experiences": [],
                    "Current Perceptions": [],
                    "Influencing Factors": []
                },
                "Physical Activity & Fitness": {
                    "Past Activities & Routines": [],
                    "Current Activities & Routines": [],
                    "Goals & Aspirations": [],
                    "Challenges & Obstacles": []
                },
                "Nutrition & Diet": {
                    "Past Eating Habits": [],
                    "Current Eating Habits": [],
                    "Food Preferences & Aversions": [],
                    "Dietary Changes & Experiments": [],
                    "Relationship with Food": []
                },
                "Sleep & Rest": {
                    "Past Sleep Patterns": [],
                    "Current Sleep Patterns": [],
                    "Sleep Quality & Challenges": [],
                    "Sleep Habits & Routines": []
                },
                "Medical History": {
                    "Chronic Conditions": [],
                    "Past Injuries & Illnesses": [],
                    "Medical Treatments & Procedures": [],
                    "Family Medical History": []
                }
            },

            # ---  MENTAL & EMOTIONAL WELLBEING ---
            "Mental & Emotional Wellbeing": {
                "Emotional Experiences": {
                    "Dominant Emotions": [],
                    "Emotional Triggers": [],
                    "Emotional Coping Mechanisms": []
                },
                "Mental Health History": {
                    "Mental Health Conditions": [],
                    "Therapy & Counseling": [],
                    "Self-Care Strategies": [],
                    "Impact on Life": []
                },
                "Stress & Anxiety": {
                    "Sources of Stress": [],
                    "Stress Management Techniques": [],
                    "Impact of Stress & Anxiety": []
                },
                "Happiness & Fulfillment": {
                    "Sources of Joy & Happiness": [],
                    "Goals & Aspirations for Fulfillment": [],
                    "Factors Contributing to Happiness": []
                }
            },

            # ---  HEALTH & WELLNESS PRACTICES ---
            "Health & Wellness Practices": {
                "Self-Care Routines": {
                    "Daily Practices": [],
                    "Weekly Practices": [],
                    "Monthly Practices": [],
                    "Impact of Routines": []
                },
                "Alternative Therapies": {
                    "Types of Therapies Used": [],
                    "Experiences & Benefits": [],
                    "Beliefs & Attitudes": []
                },
                "Health & Wellness Goals": {
                    "Short-Term Goals": [],
                    "Long-Term Goals": [],
                    "Action Plans & Strategies": []
                }
            },

            # ---  REFLECTIONS & INSIGHTS ---
            "Reflections & Insights": {
                "Health & Wellness Values": [],
                "Lessons Learned": {
                    "From Health Challenges": [],
                    "From Wellness Practices": []
                },
                "Impact of Health & Wellness on Life": [],
                "Future Goals & Aspirations": []
            }
        }
    },
    "Education & Learning": {
        "structure": {
            # ---  FORMAL EDUCATION ---
            "Formal Education": {
                "Schools & Institutions": {
                    "School 1": {
                        "Years Attended": [],
                        "Key Teachers & Mentors": [],
                        "Significant Experiences": [],
                        "Lessons Learned": []
                    },
                    "School 2": {
                        # ... similar structure as School 1
                    },
                    # ... add more schools as needed
                },
                "Degrees & Certifications": {
                    "Degree 1": {
                        "Field of Study": [],
                        "Thesis/Dissertation": [],
                        "Key Courses & Projects": [],
                        "Impact on Life": []
                    },
                    "Degree 2": {
                        # ... similar structure as Degree 1
                    },
                    # ... add more degrees as needed
                },
                "Extracurricular Activities": {
                    "Clubs & Organizations": [],
                    "Sports & Teams": [],
                    "Key Experiences & Accomplishments": [],
                    "Impact on Life": []
                },
                "Formal Learning Reflections": {
                    "Strengths & Weaknesses in Academia": [],
                    "Learning Styles & Preferences": [],
                    "Impact of Formal Education": []
                }
            },

            # ---  SELF-DIRECTED LEARNING ---
            "Self-Directed Learning": {
                "Areas of Interest": [],
                "Learning Resources": {
                    "Books & Articles": [],
                    "Online Courses & Platforms": [],
                    "Podcasts & Videos": [],
                    "Mentors & Coaches": []
                },
                "Projects & Creations": {
                    "Personal Projects": [],
                    "Creative Works": [],
                    "Skills & Expertise Developed": []
                },
                "Self-Learning Reflections": {
                    "Motivations for Self-Learning": [],
                    "Learning Strategies & Habits": [],
                    "Impact of Self-Learning": []
                }
            },

            # ---  KNOWLEDGE & INSIGHTS ---
            "Knowledge & Insights": {
                "Key Concepts & Theories": [],
                "Areas of Expertise": [],
                "Personal Beliefs & Values Shaped by Learning": [],
                "Unresolved Questions & Curiosity": [],
                "Future Learning Goals": []
            }
        }
    },
    "Actions & Reactions": {
        "structure": {
            # --- ACTIONS ---
            "Actions": {
                "Categories": {
                    "Personal": {
                        "Actions": [],
                        "Motivations": [],
                        "Consequences": [],
                        "Reflections": []
                    },
                    "Professional": {
                        "Actions": [],
                        "Motivations": [],
                        "Consequences": [],
                        "Reflections": []
                    },
                    "Social": {
                        "Actions": [],
                        "Motivations": [],
                        "Consequences": [],
                        "Reflections": []
                    },
                    "Creative": {
                        "Actions": [],
                        "Motivations": [],
                        "Consequences": [],
                        "Reflections": []
                    },
                    "Other": {
                        "Actions": [],
                        "Motivations": [],
                        "Consequences": [],
                        "Reflections": []
                    }
                }
            },

            # --- REACTIONS ---
            "Reactions": {
                "Emotional Reactions": {
                    "Situations": [],
                    "Emotions": [],
                    "Physical Manifestations": [],
                    "Cognitive Responses": [],
                    "Behavioral Responses": []
                },
                "Behavioral Reactions": {
                    "Situations": [],
                    "Actions": [],
                    "Motivations": [],
                    "Consequences": []
                },
                "Cognitive Reactions": {
                    "Situations": [],
                    "Thoughts": [],
                    "Beliefs": [],
                    "Impact on Behavior": []
                }
            },

            # --- PATTERNS & INSIGHTS ---
            "Patterns & Insights": {
                "Recurring Action Patterns": [],
                "Common Reactions": [],
                "Self-Awareness & Growth": [],
                "Action-Reaction Cycle": []
            }
        }
    },
    "Work": {
    "structure": {
      "I. Career Path & Milestones": {
        "Timeline of Roles & Positions": [
          {
            "Company": "Company 1",
            "Role": "Job Title",
            "Time Period": "Start Date - End Date",
            "Key Responsibilities": [],
            "Accomplishments": [],
            "Skills Developed": []
          },
          {
            "Company": "Company 2",
            "Role": "Job Title",
            "Time Period": "Start Date - End Date",
            "Key Responsibilities": [],
            "Accomplishments": [],
            "Skills Developed": []
          }

        ],
        "Significant Career Milestones": [
          {
            "Type": "Promotion/Recognition",
            "Description": ""
          },
          {
            "Type": "Key Project/Achievement",
            "Description": ""
          },
          {
            "Type": "Transition/Change",
            "Description": ""
          }

        ]
      },
      "II. Skillset & Expertise": {
        "Technical Skills": {
          "Areas of Expertise": [],
          "Proficiency Levels": [],
          "Examples of Use": []
        },
        "Soft Skills & Personal Attributes": {
          "Communication & Collaboration": [],
          "Problem-Solving & Critical Thinking": [],
          "Leadership & Teamwork": [],
          "Adaptability & Resilience": [],
          "Other Relevant Soft Skills": []
        },
        "Areas for Continued Development": {
          "Skills to Improve": [],
          "Learning & Development Plans": []
        }
      },
      "III. Work Ethic & Values": {
        "Work Values & Principles": {
          "Guiding Principles": [],
          "How these Values Manifest": []
        },
        "Motivational Factors": {
          "What Drives You": [],
          "Examples of Motivation": []
        },
        "Learning & Growth Mindset": {
          "Approach to Continuous Learning": [],
          "Examples of Growth Mindset in Action": []
        }
      },
      "IV. Career Goals & Aspirations": {
        "Short-Term Goals": {
          "Within the Next Year": [],
          "Action Plan": []
        },
        "Long-Term Goals": {
          "Within the Next 5 Years": [],
          "Within the Next 10 Years": [],
          "Vision for the Future": ""
        },
        "Career Path Exploration": {
          "Industries of Interest": [],
          "Specific Roles": [],
          "Potential Career Paths": []
        }
      },
      "V. Reflections & Insights": {
        "Impact of Work on Life": {
          "Personal Growth": "",
          "Relationship Dynamics": "",
          "Life Choices & Priorities": ""
        },
        "Lessons Learned": {
          "From Successes": [],
          "From Challenges": [],
          "From Mentors & Colleagues": []
        },
        "Future Aspirations & Plans": {
          "Continued Growth & Development": "",
          "Making a Difference": "",
          "Work-Life Balance": ""
        }
      }
    }
  },
    "Template 16: Exploring Sexuality": {
    "structure": {
      "I. Identity & Orientation": {
        "Sexual Identity": {
          "Labels & Terms": [],
          "How You Identify": "",
          "Evolution of Your Identity": ""
        },
        "Sexual Orientation": {
          "Attraction & Desire": "",
          "Romantic Attraction": "",
          "Aromanticism": "",
          "Sexuality Spectrum": "",
          "Fluidity & Change": ""
        },
        "Gender Identity": {
          "Gender Expression": "",
          "How You Express Your Gender": "",
          "Gender Roles & Expectations": "",
          "Gender Non-Conformity": ""
        }
      },
      "II. Experiences & Reflections": {
        "Early Exploration & Curiosity": {
          "Memories & Experiences": [],
          "Influences & Sources of Information": [],
          "Early Thoughts & Feelings": ""
        },
        "Relationships & Intimacy": {
          "Romantic Relationships": {
            "Partners & Experiences": [],
            "Key Moments & Memories": [],
            "Impact on Your Sexuality": ""
          },
          "Non-Romantic Intimacy": {
            "Friendships & Connections": [],
            "Shared Experiences": [],
            "Impact on Your Sexuality": ""
          },
          "Solo Exploration": {
            "Self-Discovery & Pleasure": [],
            "Body Awareness & Sensuality": "",
            "Impact on Your Sexuality": ""
          }
        },
        "Sexuality & Culture": {
          "Cultural Influences": [],
          "Media & Representation": [],
          "Social Norms & Expectations": "",
          "Impact on Your Experiences": ""
        },
        "Sexuality & Spirituality": {
          "Spiritual Beliefs & Practices": [],
          "Connection Between Spirituality & Sexuality": "",
          "Impact on Your Sexuality": ""
        },
        "Sexuality & Mental Health": {
          "Mental Health Conditions & Sexuality": "",
          "Impact on Your Sexuality": "",
          "Support & Resources": []
        }
      },
      "III. Values & Boundaries": {
        "Sexual Values & Beliefs": {
          "Core Values": [],
          "Beliefs About Consent": "",
          "Beliefs About Relationships": "",
          "Beliefs About Pleasure & Intimacy": ""
        },
        "Personal Boundaries": {
          "Physical Boundaries": [],
          "Emotional Boundaries": [],
          "Sexual Boundaries": [],
          "How You Communicate Boundaries": "",
          "Respecting Others' Boundaries": ""
        },
        "Consent & Communication": {
          "Understanding Consent": "",
          "How You Communicate Consent": "",
          "Negotiating & Respecting Consent": "",
          "Consent in Different Situations": ""
        }
      },
      "IV. Goals & Aspirations": {
        "Sexual Exploration & Growth": {
          "Areas of Interest": [],
          "Learning Goals": [],
          "Resources & Support": []
        },
        "Relationship Goals": {
          "Desires & Expectations": [],
          "Openness & Communication": "",
          "Building Healthy Relationships": ""
        },
        "Sexual Health & Wellness": {
          "Goals for Sexual Health": [],
          "Resources & Support": [],
          "Self-Care Practices": []
        },
        "Overall Vision for Your Sexuality": ""
      },
      "V. Reflections & Insights": {
        "Lessons Learned": {
          "From Experiences & Relationships": [],
          "From Learning & Growth": []
        },
        "Impact of Sexuality on Your Life": "",
        "Future Aspirations": "",
        "Continued Exploration & Growth": ""
      }
    }
  },
    "Dangerous Situations": {
    "structure": {
      "I. Experiences & Events": {
        "Significant Events": [
          {
            "Event Description": "",
            "Location & Time": "",
            "People Involved": [],
            "Nature of Danger": "",
            "Immediate Reaction": ""
          }

        ],
        "Recurring Patterns": {
          "Common Themes": [],
          "Situations You Tend to Find Yourself In": [],
          "Triggers for Feeling Unsafe": [],
          "Behavioral Patterns": []
        }
      },
      "II. Emotional & Psychological Impact": {
        "Immediate Reactions": {
          "Fear & Anxiety": "",
          "Anger & Frustration": "",
          "Sadness & Grief": "",
          "Shame & Guilt": "",
          "Other Emotions": []
        },
        "Long-Term Effects": {
          "Trauma & PTSD": "",
          "Anxiety & Fear": "",
          "Trust Issues": "",
          "Self-Esteem & Confidence": "",
          "Other Impacts": []
        },
        "Coping Mechanisms": {
          "Healthy Coping Strategies": [],
          "Unhealthy Coping Strategies": [],
          "Impact of Coping Strategies": ""
        }
      },
      "III. Learning & Growth": {
        "Lessons Learned": {
          "From the Experiences": [],
          "About Yourself": [],
          "About Human Behavior": []
        },
        "Self-Awareness": {
          "Strengths in Difficult Situations": [],
          "Areas for Improvement": [],
          "Triggers & Warning Signs": [],
          "Risk Assessment Skills": ""
        },
        "Building Resilience": {
          "Strategies for Preventing Future Risks": [],
          "Building Support Networks": [],
          "Self-Care Practices": []
        }
      },
      "IV. Seeking Help & Resources": {
        "Support Systems": {
          "Friends & Family": "",
          "Therapists & Counselors": "",
          "Support Groups": "",
          "Other Resources": []
        },
        "Safety Plans": {
          "Steps to Take in Case of Danger": [],
          "Emergency Contacts": [],
          "Safety Measures": [],
          "Escape Routes": ""
        },
        "Legal & Advocacy Resources": {
          "Organizations & Hotlines": [],
          "Legal Options": ""
        }
      },
      "V. Looking Ahead": {
        "Future Goals": {
          "Feeling Safer": "",
          "Building Trust": "",
          "Preventing Future Risks": [],
          "Seeking Support & Empowerment": ""
        },
        "Vision for a Safe & Empowered Future": ""
      }
    }
  },
    "Crime & Justice": {
    "structure": {
      "I. Personal Experiences": {
        "Victims of Crime": {
          "Type of Crime": "",
          "Date & Location": "",
          "Details of the Incident": [],
          "Immediate Reactions": {
            "Emotional Response": [],
            "Physical Response": [],
            "Behavioral Response": []
          },
          "Long-Term Impact": {
            "Emotional Impact": [],
            "Psychological Impact": [],
            "Social Impact": [],
            "Physical Impact": [],
            "Financial Impact": []
          },
          "Support & Resources Accessed": []
        },
        "Witness to Crime": {
          "Type of Crime": "",
          "Date & Location": "",
          "Details of the Incident": [],
          "Actions Taken": {
            "Immediate Actions": [],
            "Later Actions": []
          },
          "Impact on You": {
            "Emotional Impact": [],
            "Psychological Impact": [],
            "Social Impact": []
          },
          "Support & Resources Accessed": []
        },
        "Involvement with the Criminal Justice System": {
          "Role in the System": "",
          "Details of Involvement": [],
          "Experiences with Law Enforcement": {
            "Positive Experiences": [],
            "Negative Experiences": [],
            "Observations of Bias": []
          },
          "Experiences with Legal Professionals": {
            "Positive Experiences": [],
            "Negative Experiences": [],
            "Observations of Inequities": []
          },
          "Impact on Your Life": {
            "Emotional Impact": [],
            "Psychological Impact": [],
            "Social Impact": [],
            "Financial Impact": []
          }
        }
      },
      "II. Understanding Crime": {
        "Types of Crime": {
          "Crimes You're Familiar With": [],
          "Crimes You're Interested in Learning More About": []
        },
        "Causes of Crime": {
          "Social Factors": {
            "Poverty & Inequality": [],
            "Discrimination & Marginalization": [],
            "Lack of Opportunity": [],
            "Social Disorganization": [],
            "Cultural Influences": []
          },
          "Economic Factors": {
            "Unemployment & Underemployment": [],
            "Economic Instability": [],
            "Financial Distress": [],
            "Greed & Corruption": []
          },
          "Psychological Factors": {
            "Mental Health Issues": [],
            "Substance Abuse": [],
            "Personality Disorders": [],
            "Trauma & Abuse": []
          },
          "Other Potential Causes": {
            "Political Instability": [],
            "Environmental Factors": [],
            "Technological Factors": [],
            "Lack of Education": []
          }
        },
        "Impact of Crime": {
          "Individual Impact": {
            "Physical & Emotional Harm": [],
            "Loss of Property & Possessions": [],
            "Financial Loss": [],
            "Psychological Trauma": [],
            "Social Isolation": []
          },
          "Community Impact": {
            "Fear & Anxiety": [],
            "Erosion of Trust": [],
            "Increased Crime Rates": [],
            "Strain on Resources": [],
            "Social Disruption": []
          },
          "Societal Impact": {
            "Erosion of Social Fabric": [],
            "Decreased Quality of Life": [],
            "Economic Strain": [],
            "Political Instability": [],
            "Loss of Public Trust": []
          }
        }
      },
      "III. The Criminal Justice System": {
        "Key Components": {
          "Law Enforcement": {
            "Police Departments": [],
            "Sheriff's Offices": [],
            "State Police": [],
            "Federal Law Enforcement": []
          },
          "Courts": {
            "Trial Courts": [],
            "Appellate Courts": [],
            "Supreme Courts": []
          },
          "Corrections": {
            "Prisons": [],
            "Jails": [],
            "Probation & Parole": [],
            "Community Corrections": []
          },
          "Prosecution & Defense": {
            "Prosecutors": [],
            "Defense Attorneys": [],
            "Public Defenders": []
          },
          "Victim Services": {
            "Victim Advocacy Organizations": [],
            "Victim Assistance Programs": [],
            "Legal Aid": []
          }
        },
        "Your Perspective on the System": {
          "Strengths & Weaknesses": [],
          "Areas for Improvement": {
            "Policing Practices": [],
            "Sentencing & Punishment": [],
            "Rehabilitation & Reintegration": [],
            "Victim Support & Services": [],
            "Equity & Fairness": []
          },
          "Fairness & Justice": "",
          "Rehabilitation & Prevention": ""
        },
        "Experiences with the System": {
          "Positive Experiences": [],
          "Negative Experiences": [],
          "Lessons Learned": []
        }
      },
      "IV.  Social Justice & Criminal Justice Reform": {
        "Issues & Concerns": {
          "Over-Policing & Racial Bias": {
            "Racial Profiling": [],
            "Disproportionate Policing in Communities of Color": [],
            "Police Brutality": [],
            "Systemic Racism": []
          },
          "Mass Incarceration & Prison Reform": {
            "Overcrowding & Poor Conditions": [],
            "Sentencing Disparities": [],
            "Lack of Rehabilitation": [],
            "Reentry Challenges": [],
            "Prison Industrial Complex": []
          },
          "Reentry & Second Chances": {
            "Barriers to Reintegration": [],
            "Support Programs": [],
            "Employment Opportunities": [],
            "Stigma & Discrimination": []
          },
          "Victim Rights & Support": {
            "Access to Justice": [],
            "Trauma-Informed Care": [],
            "Financial Assistance": [],
            "Protection & Safety": []
          },
          "Other Issues": {
            "Mental Health & Substance Abuse in the System": [],
            "Juvenile Justice": [],
            "Cybercrime": [],
            "Human Trafficking": [],
            "Domestic Violence": []
          }
        },
        "Advocacy & Action": {
          "Organizations & Initiatives": [],
          "Your Role in Promoting Justice": "",
          "Potential Actions for Change": {
            "Supporting Reform Organizations": [],
            "Advocating for Policy Changes": [],
            "Educating Others": [],
            "Volunteering & Community Engagement": []
          }
        }
      },
      "V. Reflections & Insights": {
        "Lessons Learned": {
          "About Crime & Justice": [],
          "About Human Behavior": [],
          "About Your Own Values & Beliefs": []
        },
        "Impact of Crime on Your Life": {
          "Personal Impact": "",
          "Societal Impact": ""
        },
        "Future Hopes & Expectations": {
          "For Yourself": "",
          "For Society": ""
        },
        "Vision for a Safer & More Just Society": ""
      }
    }
  },
    "Violence": {
    "structure": {
      "I. Witnessing or Experiencing Violence": {
        "Direct Exposure": {
          "Type of Violence": "",
          "Details of the Incident": [],
          "Location & Time": "",
          "People Involved": [],
          "Immediate Reactions": {
            "Emotional Response": [],
            "Physical Response": [],
            "Behavioral Response": []
          },
          "Long-Term Impact": {
            "Emotional Impact": [],
            "Psychological Impact": [],
            "Social Impact": [],
            "Physical Impact": []
          },
          "Support & Resources Accessed": []
        },
        "Indirect Exposure": {
          "Exposure Through Media": {
            "Types of Media": [],
            "Specific Examples": [],
            "Impact on You": []
          },
          "Exposure Through Stories & Accounts": {
            "Sources of Information": [],
            "Specific Stories": [],
            "Impact on You": []
          }
        },
        "Understanding the Impact": {
          "Personal Impact": "",
          "Societal Impact": "",
          "Global Impact": ""
        }
      },
      "II. Exploring the Causes": {
        "Individual Factors": {
          "Mental Health Issues": [],
          "Substance Abuse": [],
          "Trauma & Abuse": [],
          "Anger Management Issues": [],
          "Personality Disorders": []
        },
        "Social Factors": {
          "Poverty & Inequality": [],
          "Discrimination & Marginalization": [],
          "Lack of Opportunity": [],
          "Social Disorganization": [],
            "Cultural Norms": [],
            "Social Learning": []
        },
        "Environmental Factors": {
            "Exposure to Violence": [],
            "Availability of Weapons": [],
            "Lack of Safe Spaces": [],
            "Neighborhood Conditions": []
        },
        "Other Potential Causes": {
          "Political Instability": [],
          "Economic Crisis": [],
          "Ideological Extremism": [],
          "Media Influence": []
        }
      },
      "III. Addressing Violence & Heinous Acts": {
        "Prevention Strategies": {
          "Early Intervention Programs": [],
          "Trauma-Informed Care": [],
          "Violence Prevention Education": [],
          "Community Building & Empowerment": [],
          "Addressing Root Causes": []
        },
        "Intervention & Response": {
          "Emergency Services": [],
          "Victim Support Services": [],
          "Trauma-Informed Care": [],
          "Legal & Criminal Justice System": [],
          "Mental Health Services": [],
          "Community Support": []
        },
        "Rehabilitation & Healing": {
          "Therapy & Counseling": [],
          "Support Groups": [],
          "Victim Advocacy": [],
          "Reintegration Programs": []
        }
      },


      "IV. Reflections & Insights": {
        "Lessons Learned": {
          "About Human Nature": [],
          "About the Fragility of Life": [],
          "About the Importance of Compassion & Empathy": [],
          "About the Power of Hope & Resilience": []
        },
        "Impact on Your Values & Beliefs": {
          "Beliefs About Humanity": [],
          "Beliefs About Justice & Fairness": [],
          "Beliefs About Safety & Security": []
        },
        "Future Aspirations": {
          "For Yourself": "",
          "For Society": ""
        },
        "Vision for a Safer & More Compassionate World": ""
      }
    }
  },
    "Exploring Non-Normative Sexuality & Intimacy": {
    "structure": {
        "I. Identity & Expression": {
            "Sexual Identity": [
                "Asexual",
                "Bisexual",
                "Pansexual",
                "Demisexual",
                "Polysexual",
                "Graysexual",
                "Sapiosexual",
                "Other Labels"
            ],
            "Sexual Orientation": [
                "Heterosexual",
                "Homosexual",
                "Bisexual",
                "Pansexual",
                "Asexual",
                "Other Orientations"
            ],
            "Gender Identity": [
                "Cisgender",
                "Transgender",
                "Non-Binary",
                "Genderfluid",
                "Agender",
                "Bigender",
                "Other Identities"
            ],
            "Kink & BDSM": {
                "Bondage & Restraint": [
                    "Rope",
                    "Leather",
                    "Silk",
                    "Other Materials"
                ],
                "Domination & Submission": [
                    "Power Exchange",
                    "Discipline & Punishment",
                    "Roleplay",
                    "Other Dynamics"
                ],
                "Sensory Deprivation & Stimulation": [
                    "Blindfolds",
                    "Gagging",
                    "Sensory Deprivation Tanks",
                    "Other Practices"
                ],
                "Roleplay & Fantasy": [
                    "Characters",
                    "Scenarios",
                    "Themes",
                    "Other Elements"
                ],
                "Electroplay": [
                    "Types of Devices",
                    "Intensity Levels",
                    "Safety Precautions"
                ],
                "Waterplay": [
                    "Shower Play",
                    "Bath Play",
                    "Other Water-Related Activities"
                ],
                "Other Practices": [
                    "Flogging",
                    "Spanking",
                    "Foot Fetish",
                    "Age Play",
                    "Other Kink & BDSM Practices"
                ]
            },
            "Personal Values & Beliefs": {
                "Consent": [
                    "Informed Consent",
                    "Enthusiastic Consent",
                    "Negotiating Consent",
                    "Revoking Consent"
                ],
                "Respect": [
                    "Respect for Boundaries",
                    "Respect for Identities",
                    "Respect for Preferences"
                ],
                "Communication": [
                    "Open and Honest Communication",
                    "Active Listening",
                    "Non-Verbal Communication"
                ]
            },
            "Aesthetics & Style": {
                "Clothing & Fashion": [
                    "Fetish Wear",
                    "Leather & Latex",
                    "Underwear & Lingerie",
                    "Specific Styles",
                    "Other Clothing Preferences"
                ],
                "Art & Visuals": [
                    "Photography",
                    "Painting",
                    "Sculpture",
                    "Film & Video",
                    "Other Visual Arts"
                ],
                "Music & Sound": [
                    "Genre Preferences",
                    "Specific Artists & Bands",
                    "Soundscapes & Ambiance",
                    "Music for Specific Practices"
                ],
                "Other Aesthetic Preferences": []
            }
        },
        "II. Sexual Experiences": {
            "Relationships": {
                "Romantic Relationships": [
                    "Initial Attraction",
                    "First Encounters",
                    "Early Exploration",
                    "Memorable Dates",
                    "Shared Experiences",
                    "Turning Points",
                    "Moments of Connection",
                    "First Time Saying 'I Love You'",
                    "Significant Gifts or Gestures",
                    "Conflict Resolution",
                    "Moments of Vulnerability",
                    "Moments of Deep Intimacy",
                    "Communication & Negotiation",
                    "Power Dynamics",
                    "Kink Exploration",
                    "Impact on Self-Discovery",
                    "Challenges & Growth",
                    "Current Relationships"
                ],
                "Non-Romantic Intimacy": [
                    "Platonic Relationships",
                    "Shared Interests",
                    "Open Communication",
                    "Exploring Sexuality Together",
                    "Parties & Events",
                    "Group Activities",
                    "Travel & Adventures",
                    "Moments of Connection",
                    "Impact on Sexuality",
                    "Boundary Setting",
                    "Consent in Non-Romantic Contexts"
                ],
                "Friendships": [],
                "Group Dynamics": [],
                "Online Relationships": []
            },
            "Solo Exploration": {
                "Masturbation": [
                    "Techniques",
                    "Sensations & Preferences",
                    "Impact on Sexuality"
                ],
                "Body Awareness": [
                    "Mindfulness & Meditation",
                    "Massage & Touch",
                    "Sensory Exploration",
                    "Body Image & Self-Acceptance"
                ],
                "Sensory Exploration": [
                    "Visual Stimulation",
                    "Auditory Stimulation",
                    "Olfactory Stimulation",
                    "Tactile Stimulation"
                ],
                "Solo Kink Practices": [
                    "Bondage",
                    "Self-Stimulation",
                    "Sensory Deprivation",
                    "Other Practices"
                ]
            },
            "Sexual Encounters": {
                "Intercourse": {
                    "Vaginal Intercourse": [
                        "Positions & Techniques",
                        "Sensations & Preferences",
                        "Communication & Negotiation",
                        "Impact on Sexuality"
                    ],
                    "Anal Intercourse": [
                        "Positions & Techniques",
                        "Sensations & Preferences",
                        "Communication & Negotiation",
                        "Impact on Sexuality"
                    ],
                    "Oral Intercourse": {
                        "Fellatio (Giving Oral Sex)": [
                            "Techniques",
                            "Sensations & Preferences",
                            "Communication & Negotiation",
                            "Impact on Sexuality"
                        ],
                        "Cunnilingus (Receiving Oral Sex)": [
                            "Techniques",
                            "Sensations & Preferences",
                            "Communication & Negotiation",
                            "Impact on Sexuality"
                        ]
                    },
                    "Other Intercourse": [
                        "Digital Penetration",
                        "Other Practices"
                    ]
                },
                "Oral Sex": {
                    "Fellatio": {
                        "Techniques": [
                            "Classic",
                            "Deepthroat",
                            "Rimjob",
                            "Other Techniques"
                        ],
                        "Sensations & Preferences": [],
                        "Communication & Negotiation": [],
                        "Impact on Sexuality": []
                    },
                    "Cunnilingus": {
                        "Techniques": [
                            "Licking",
                            "Sucking",
                            "Other Techniques"
                        ],
                        "Sensations & Preferences": [],
                        "Communication & Negotiation": [],
                        "Impact on Sexuality": []
                    },
                    "Other Oral Practices": [
                        "French Kissing",
                        "Other Oral Stimulation"
                    ]
                },
                "Anal Sex": {
                    "Preparation & Safety": [
                        "Lubrication",
                        "Communication",
                        "Hygiene",
                        "Relaxation"
                    ],
                    "Positions & Techniques": [
                        "Doggy Style",
                        "Reverse Cowgirl",
                        "Spooning",
                        "Other Positions"
                    ],
                    "Sensations & Preferences": [
                        "Depth",
                        "Pressure",
                        "Intensity",
                        "Other Sensations"
                    ],
                    "Communication & Negotiation": [
                        "Expressing Preferences",
                        "Asking for What You Want",
                        "Negotiating Pace & Intensity",
                        "Open Communication"
                    ]
                },
                "Touching & Stimulation": [
                    "Foreplay",
                    "Erotic Massage",
                    "Focus on Specific Zones"
                ],
                "Sensual Massage": [
                    "Relaxation & Pleasure",
                    "Exploration of Body & Sensations",
                    "Techniques & Preferences"
                ],
                "Exploration of Erotic Zones": [
                    "Clitoris",
                    "Breasts",
                    "Inner Thighs",
                    "Other Zones"
                ],
                "Experiences with Toys & Objects": [
                    "Vibrators",
                    "Dildos",
                    "Anal Beads",
                    "Other Toys"
                ],
                "Other Practices": [
                    "Fetishes & Preferences",
                    "Roleplay & Fantasy"
                ]
            },
            "Community & Culture": {
                "Kink & BDSM Communities": [
                    "Online Forums & Groups",
                    "Local Events & Meetups",
                    "Clubs & Organizations",
                    "Parties",
                    "Workshops",
                    "Conferences",
                    "Other Events"
                ],
                "Social Interactions": [
                    "Building Connections",
                    "Navigating Social Norms",
                    "Finding Support and Resources"
                ],
                "Learning & Resources": [
                    "Books & Articles",
                    "Online Resources",
                    "Workshops & Courses",
                    "Personal Exploration"
                ]
            },
            "III. Safety & Boundaries": {
                "Consent": [
                    "Understanding Consent",
                    "Communication of Consent",
                    "Negotiating Consent",
                    "Consent in Different Situations",
                    "Consent in Kink & BDSM"
                ],
                "Boundaries": [
                    "Physical Boundaries",
                    "Emotional Boundaries",
                    "Sexual Boundaries",
                    "Communication of Boundaries",
                    "Respecting Others' Boundaries",
                    "Negotiating Boundaries in Relationships"
                ],
                "Safety Practices": [
                    "Negotiation & Communication",
                    "Safe Words & Signals",
                    "Aftercare & Debriefing",
                    "Risk Assessment",
                    "Safe Spaces & Environments"
                ],
                "Resources & Support": [
                    "Online Resources",
                    "Local Organizations",
                    "Support Groups",
                    "Therapists & Counselors"
                ]
            },
            "IV. Goals & Aspirations": {
                "Continued Exploration & Growth": [
                    "Areas of Interest",
                    "Learning Goals",
                    "Resources & Support"
                ],
                "Relationship Goals": [
                    "Desires & Expectations",
                    "Openness & Communication",
                    "Building Healthy & Respectful Relationships",
                    "Kink Compatibility"
                ],
                "Sexual Health & Wellness": [
                    "Goals for Sexual Health",
                    "Resources & Support",
                    "Self-Care Practices"
                ],
                "Overall Vision for Your Sexuality": []
            },
            "V. Reflections & Insights": {
                "Lessons Learned": [
                    "From Experiences & Relationships",
                    "From Learning & Growth"
                ],
                "Impact of Sexuality on Your Life": [],
                "Future Aspirations": [],
                "Continued Exploration & Growth": []
            }
        }
    }
  },
    "Animal Encounters": {
    "structure": {
        # ---  ANIMAL ENCOUNTERS ---
        "Animal Encounters": {
            "Vertebrates": {
                "Mammals": {
                    "Pets": {
                        "Dogs": {
                            "Memorable Encounters": [],
                            "Personality Traits": [],
                            "Impact on My Life": []
                        },
                        "Cats": {
                            "Memorable Encounters": [],
                            "Personality Traits": [],
                            "Impact on My Life": []
                        },
                        "Other Mammals": {
                            "Type": {
                                "Memorable Encounters": [],
                                "Personality Traits": [],
                                "Impact on My Life": []
                            }
                        }
                    },
                    "Wildlife": {
                        "Species": {
                            "Memorable Encounters": [],
                            "Observations": [],
                            "Impact on My Life": []
                        }
                    }
                },
                "Birds": {
                    "Pets": {
                        "Parrots": {
                            "Memorable Encounters": [],
                            "Personality Traits": [],
                            "Impact on My Life": []
                        },
                        "Other Birds": {
                            "Type": {
                                "Memorable Encounters": [],
                                "Personality Traits": [],
                                "Impact on My Life": []
                            }
                        }
                    },
                    "Wildlife": {
                        "Species": {
                            "Memorable Encounters": [],
                            "Observations": [],
                            "Impact on My Life": []
                        }
                    }
                },
                "Reptiles": {
                    "Pets": {
                        "Lizards": {
                            "Memorable Encounters": [],
                            "Personality Traits": [],
                            "Impact on My Life": []
                        },
                        "Snakes": {
                            "Memorable Encounters": [],
                            "Personality Traits": [],
                            "Impact on My Life": []
                        },
                        "Turtles": {
                            "Memorable Encounters": [],
                            "Personality Traits": [],
                            "Impact on My Life": []
                        },
                        "Other Reptiles": {
                            "Type": {
                                "Memorable Encounters": [],
                                "Personality Traits": [],
                                "Impact on My Life": []
                            }
                        }
                    },
                    "Wildlife": {
                        "Species": {
                            "Memorable Encounters": [],
                            "Observations": [],
                            "Impact on My Life": []
                        }
                    }
                },
                "Amphibians": {
                    "Pets": {
                        "Frogs": {
                            "Memorable Encounters": [],
                            "Personality Traits": [],
                            "Impact on My Life": []
                        },
                        "Salamanders": {
                            "Memorable Encounters": [],
                            "Personality Traits": [],
                            "Impact on My Life": []
                        },
                        "Other Amphibians": {
                            "Type": {
                                "Memorable Encounters": [],
                                "Personality Traits": [],
                                "Impact on My Life": []
                            }
                        }
                    },
                    "Wildlife": {
                        "Species": {
                            "Memorable Encounters": [],
                            "Observations": [],
                            "Impact on My Life": []
                        }
                    }
                },
                "Fish": {
                    "Pets": {
                        "Aquarium Fish": {
                            "Species": {
                                "Memorable Encounters": [],
                                "Observations": [],
                                "Impact on My Life": []
                            }
                        },
                        "Other Fish": {
                            "Type": {
                                "Memorable Encounters": [],
                                "Personality Traits": [],
                                "Impact on My Life": []
                            }
                        }
                    },
                    "Wildlife": {
                        "Species": {
                            "Memorable Encounters": [],
                            "Observations": [],
                            "Impact on My Life": []
                        }
                    }
                }
            },
            "Invertebrates": {
                "Insects": {
                    "Species": {
                        "Memorable Encounters": [],
                        "Observations": [],
                        "Impact on My Life": []
                    }
                },
                "Arachnids": {
                    "Species": {
                        "Memorable Encounters": [],
                        "Observations": [],
                        "Impact on My Life": []
                    }
                },
                "Mollusks": {
                    "Species": {
                        "Memorable Encounters": [],
                        "Observations": [],
                        "Impact on My Life": []
                    }
                },
                "Other Invertebrates": {
                    "Type": {
                        "Memorable Encounters": [],
                        "Personality Traits": [],
                        "Impact on My Life": []
                    }
                }
            }
        },

        # ---  ANIMAL-RELATED REFLECTIONS ---
        "Animal-Related Reflections": {
            "Lessons Learned from Animals": [],
            "Impact of Animals on My Life": [],
            "Future Aspirations": []
        }
    }
},
    "Illegal Activities": {
    "structure": {
        # ---  ILLEGAL ACTIVITIES  ---
        "Illegal Activities": {
            "Personal Involvement": {
                "Types of Crimes Committed": [],
                "Motivations for Involvement": [],
                "Circumstances Surrounding Involvement": [],
                "Consequences of Involvement": [],
                "Impact on My Life": [],
                "Lessons Learned": []
            },
            "Witnessing Illegal Activities": {
                "Types of Crimes Witnessed": [],
                "Circumstances of Witnessing": [],
                "Impact on My Life": [],
                "Actions Taken": [],
                "Lessons Learned": []
            },
            "Knowledge of Illegal Activities": {
                "Types of Crimes Known About": [],
                "Source of Information": [],
                "Impact on My Life": [],
                "Actions Taken": [],
                "Lessons Learned": []
            },
            "Understanding of the Criminal Justice System": {
                "Perspective on the System": {
                    "Strengths": [],
                    "Weaknesses": [],
                    "Areas for Improvement": []
                },
                "Experiences with Law Enforcement": [],
                "Experiences with Legal Professionals": [],
                "Impact on My Life": []
            },
            "Social Context of Illegal Activities": {
                "Factors Contributing to Crime": {
                    "Poverty & Inequality": [],
                    "Discrimination & Marginalization": [],
                    "Lack of Opportunity": [],
                    "Social Disorganization": [],
                    "Cultural Influences": []
                },
                "Impact of Crime on Communities": [],
                "Impact of Crime on Individuals": [],
                "Impact of Crime on Society": []
            }
        },

        # ---  REFLECTIONS & INSIGHTS ---
        "Reflections & Insights": {
            "Lessons Learned About Crime": [],
            "Lessons Learned About Myself": [],
            "Impact of Illegal Activities on My Life": [],
            "Values & Beliefs about Justice": [],
            "Aspirations for a Safer Future": []
        }
    }
},
    "Crime & Law Disobedience": {
    "structure": {
        # --- PERSONAL EXPERIENCES ---
        "Personal Experiences": {
            "Acts of Law Disobedience": {
                "Type of Disobedience": [],
                "Motivations": [],
                "Circumstances": [],
                "Consequences": [],
                "Impact on My Life": []
            },
            "Witnessing Law Disobedience": {
                "Type of Disobedience": [],
                "Motivations (Observed)": [],
                "Circumstances": [],
                "Consequences (Observed)": [],
                "Impact on My Life": [],
                "Actions Taken (If Any)": []
            },
            "Experiences with Law Enforcement": {
                "Positive Encounters": [],
                "Negative Encounters": [],
                "Observations of Bias": []
            },
            "Experiences with Legal Professionals": {
                "Positive Encounters": [],
                "Negative Encounters": [],
                "Observations of Inequities": []
            }
        },

        # --- REFLECTIONS & UNDERSTANDING ---
        "Reflections & Understanding": {
            "Perspectives on Law and Order": {
                "Beliefs about the Law": [],
                "Views on Law Enforcement": [],
                "Views on Justice": []
            },
            "Ethical Dilemmas": {
                "Situations Where Laws Conflict with Values": [],
                "Personal Approaches to Ethical Dilemmas": []
            },
            "Social Context of Law Disobedience": {
                "Factors Contributing to Disobedience": {
                    "Inequality": [],
                    "Oppression": [],
                    "Lack of Representation": [],
                    "Corruption": []
                },
                "Impact of Law Disobedience on Society": [],
                "Impact of Law Disobedience on Individuals": []
            }
        },

        # ---  ACTION & ADVOCACY ---
        "Action & Advocacy": {
            "Forms of Advocacy": {
                "Supporting Organizations": [],
                "Engaging in Peaceful Protests": [],
                "Educating Others": [],
                "Political Participation": []
            },
            "Personal Commitment to Justice": {
                "Values & Beliefs Guiding My Actions": [],
                "Goals for a Just Society": []
            }
        }
    }
},
    "Pornography": {
    "structure": {
        # ---  PERSONAL EXPERIENCES ---
        "Personal Experiences": {
            "Exposure to Pornography": {
                "First Exposure": {
                    "Age": [],
                    "Context": [],
                    "Impact": []
                },
                "Recurring Exposure": {
                    "Types of Pornography": [],
                    "Frequency": [],
                    "Impact on Sexuality": []
                },
                "Influences & Sources": {
                    "Online Platforms": [],
                    "Friends & Peers": [],
                    "Media & Culture": [],
                    "Other Sources": []
                }
            },
            "Personal Consumption of Pornography": {
                "Motivations": [],
                "Preferences & Aversions": [],
                "Impact on Sexual Experiences": [],
                "Impact on Relationships": []
            },
            "Creating or Sharing Pornography": {
                "Motivations": [],
                "Types of Content": [],
                "Impact on My Life": [],
                "Reflections": []
            }
        },

        # ---  REFLECTIONS & UNDERSTANDING ---
        "Reflections & Understanding": {
            "Impact of Pornography on Society": {
                "Positive Impacts": [],
                "Negative Impacts": [],
                "Cultural Influences": [],
                "Social Norms": []
            },
            "Ethical Considerations": {
                "Consent & Exploitation": [],
                "Representation & Diversity": [],
                "Objectification & Gender Roles": [],
                "Addiction & Compulsive Behavior": [],
                "Other Ethical Concerns": []
            },
            "Pornography & Relationships": {
                "Impact on Romantic Relationships": [],
                "Impact on Communication & Trust": [],
                "Impact on Sexual Expectations": []
            }
        },

        # ---  FUTURE ASPIRATIONS ---
        "Future Aspirations": {
            "Personal Goals": {
                "Understanding My Sexuality": [],
                "Building Healthy Relationships": [],
                "Managing Consumption": [],
                "Other Personal Goals": []
            },
            "Advocacy & Action": {
                "Supporting Organizations": [],
                "Raising Awareness": [],
                "Promoting Positive Change": [],
                "Other Forms of Advocacy": []
            }
        }
    }
},
    "Entertainment & Culture": {
    "structure": {
        # ---  ENTERTAINMENT CONSUMPTION ---
        "Entertainment Consumption": {
            "Movies & TV": {
                "Favorite Genres": [],
                "Favorite Directors": [],
                "Favorite Actors": [],
                "Memorable Films & Shows": [],
                "Impact on My Life": []
            },
            "Music": {
                "Favorite Genres": [],
                "Favorite Artists": [],
                "Favorite Albums": [],
                "Memorable Songs": [],
                "Impact on My Life": []
            },
            "Books": {
                "Favorite Genres": [],
                "Favorite Authors": [],
                "Memorable Books": [],
                "Impact on My Life": []
            },
            "Video Games": {
                "Favorite Genres": [],
                "Favorite Games": [],
                "Memorable Gaming Moments": [],
                "Impact on My Life": []
            },
            "Other Entertainment": {
                "Type": {
                    "Favorite Examples": [],
                    "Impact on My Life": []
                }
            }
        },

        # ---  ENTERTAINMENT & CULTURE ---
        "Entertainment & Culture": {
            "Cultural Influences": {
                "Music": [],
                "Movies & TV": [],
                "Books": [],
                "Video Games": [],
                "Art & Design": [],
                "Fashion": [],
                "Other Cultural Influences": []
            },
            "Personal Values & Beliefs Shaped by Entertainment": [],
            "Impact of Entertainment on My Life": {
                "Positive Impacts": [],
                "Negative Impacts": [],
                "Learning & Growth": []
            },
            "Future Aspirations": {
                "Exploring New Forms of Entertainment": [],
                "Supporting Creative Industries": [],
                "Engaging in Cultural Activities": []
            }
        }
    }
},
    "Politics & Society": {
    "structure": {
        # ---  POLITICAL VIEWS ---
        "Political Views": {
            "Political Identity": {
                "Party Affiliation": [],
                "Ideological Leanings": [],
                "Key Beliefs & Values": []
            },
            "Issues of Importance": {
                "Domestic Issues": [],
                "Foreign Policy Issues": [],
                "Social Justice Issues": [],
                "Environmental Issues": []
            },
            "Political Engagement": {
                "Voting Record": [],
                "Political Activism": [],
                "Engagement with Media & News": [],
                "Discussions with Others": []
            }
        },

        # ---  SOCIAL & POLITICAL EXPERIENCES ---
        "Social & Political Experiences": {
            "Significant Events": {
                "Political Events": [],
                "Social Movements": [],
                "Personal Experiences with Politics": []
            },
            "Impact of Politics on My Life": {
                "Personal Impact": [],
                "Social Impact": [],
                "Economic Impact": []
            },
            "Challenges & Opportunities": {
                "Challenges Faced by Society": [],
                "Opportunities for Change": []
            }
        },

        # ---  REFLECTIONS & INSIGHTS ---
        "Reflections & Insights": {
            "Lessons Learned About Politics": [],
            "Lessons Learned About Society": [],
            "Impact of Politics on My Values & Beliefs": [],
            "Vision for a Better Society": []
        }
    }
},
    "Artificial Intelligence": {"structure": {

        "Personal Experiences": {
            "Interactions with AI": {
                "Personal Assistants": {
                    "Types Used": [],
                    "Memorable Interactions": [],
                    "Impact on My Life": []
                },
                "Social Media & Online Services": {
                    "Personalized Recommendations": [],
                    "AI-Driven Content": [],
                    "Impact on My Online Experiences": []
                },
                "Other AI Interactions": {
                    "Examples": [],
                    "Impact on My Life": []
                }
            },
            "Understanding of AI": {
                "Areas of Knowledge": [],
                "Sources of Information": [],
                "Level of Understanding": []
            },
            "Views on AI Development": {
                "Concerns": [],
                "Hopes & Expectations": [],
                "Personal Stance on AI": []
            }
        },

        # ---  AI & SOCIETY ---
        "AI & Society": {
            "Impact of AI on Various Sectors": {
                "Healthcare": [],
                "Education": [],
                "Transportation": [],
                "Business & Industry": [],
                "Entertainment": [],
                "Other Sectors": []
            },
            "Ethical Considerations": {
                "Bias & Discrimination": [],
                "Job Displacement": [],
                "Privacy & Security": [],
                "Control & Autonomy": [],
                "Other Ethical Concerns": []
            },
            "Future of AI": {
                "Potential Benefits": [],
                "Potential Risks": [],
                "Predictions & Visions": []
            }
        },

        # ---  REFLECTIONS & INSIGHTS ---
        "Reflections & Insights": {
            "Lessons Learned About AI": [],
            "Impact of AI on My Life": [],
            "Impact of AI on Society": [],
            "Values & Beliefs About AI": [],
            "Role in Shaping the Future of AI": []
        }
    },},
    "Death & Loss": {
    "structure": {

        "Personal Experiences": {
            "Deaths of Loved Ones": {
                "Individual": {
                    "Name": "",
                    "Relationship": "",
                    "Date of Death": "",
                    "Circumstances of Death": "",
                    "Immediate Reactions": {
                        "Emotional Response": [],
                        "Physical Response": [],
                        "Behavioral Response": []
                    },
                    "Grief Journey": {
                        "Stages of Grief": [],
                        "Coping Mechanisms": [],
                        "Support Systems": [],
                        "Impact on My Life": []
                    },
                    "Memories & Reflections": [],
                    "How They Influenced Me": []
                }
            },
            "Near-Death Experiences": {
                "Description": "",
                "Impact on My Life": [],
                "Reflections": []
            },
            "Experiences with Dying": {
                "Caring for a Dying Loved One": {
                    "Details of the Experience": [],
                    "Impact on My Life": [],
                    "Reflections": []
                },
                "Witnessing Death": {
                    "Circumstances": [],
                    "Impact on My Life": [],
                    "Reflections": []
                }
            }
        },


        "Reflections & Understanding": {
            "Views on Death & Dying": {
                "Beliefs About the Afterlife": [],
                "Thoughts on Mortality": [],
                "Values & Beliefs Shaped by Loss": []
            },
            "Meaning of Life": {
                "Insights Gained Through Loss": [],
                "Appreciation for Life": [],
                "New Priorities & Goals": []
            },
            "Cultural & Spiritual Perspectives": {
                "Cultural Beliefs & Practices": [],
                "Spiritual Beliefs & Practices": [],
                "Impact of Different Perspectives": []
            }
        },


        "Action & Support": {
            "Support Systems": {
                "Friends & Family": [],
                "Therapists & Counselors": [],
                "Support Groups": [],
                "Other Resources": []
            },
            "Ways I Honor the Deceased": [],
            "Advocacy & Action": {
                "Organizations Supporting Grief & Loss": [],
                "Promoting Awareness of End-of-Life Issues": [],
                "Advocating for End-of-Life Choices": []
            }
        }
    }

},
    "Occupations": {
        "structure": {
            "Occupations": {
                "Occupation 1": {
                    "Name": "",
                    "Description": "",
                    "Skills Required": [],
                    "Education & Training": [],
                    "Work Environment": "",
                    "Typical Tasks": [],
                    "Personal Experiences": [],
                    "Reflections": []
                },
                "Occupation 2": {
                    "Name": "",
                    "Description": "",
                    "Skills Required": [],
                    "Education & Training": [],
                    "Work Environment": "",
                    "Typical Tasks": [],
                    "Personal Experiences": [],
                    "Reflections": []
                },
                # ... Add more occupations as needed
            },
            "Interests & Aspirations": {
                "Career Goals": [],
                "Skills & Knowledge": [],
                "Industry Trends": [],
                "Future Plans": []
            }
        }
    },
    "Family": {"structure":
        {

      "Family Members": {
        "Individual Profiles": {
          "Member Name": {
            "Thought Thread": [],
            "Reflections": []
          }
        }
      },

      # --- FAMILY HISTORY & ROOTS ---
      "Family History & Roots": {
        "Ancestral Origins": {
          "Location": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Significant Events": {
          "Event": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Family Traditions & Values": {
          "Tradition/Value": [],
          "Thought Thread": [],
          "Reflections": []
        }
      },

      # --- FAMILY RELATIONSHIPS ---
      "Family Relationships": {
        "Individual Relationships": {
          "Person": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Family Dynamics": {
          "Dynamic": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Shared Experiences": {
          "Experience": [],
          "Thought Thread": [],
          "Reflections": []
        }
      },

      # --- FAMILY MEMORIES & STORIES ---
      "Family Memories & Stories": {
        "Moments & Events": {
          "Moment/Event": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Family Stories": {
          "Story": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Family Photos & Artifacts": {
          "Photo/Artifact": [],
          "Thought Thread": [],
          "Reflections": []
        }
      },

      # --- FAMILY VALUES & BELIEFS ---
      "Family Values & Beliefs": {
        "Core Values": {
          "Value": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Belief Systems": {
          "Belief": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Family Mission Statement": {
          "Statement": [],
          "Thought Thread": [],
          "Reflections": []
        }
      },

      # --- FAMILY GOALS & ASPIRATIONS ---
      "Family Goals & Aspirations": {
        "Shared Goals": {
          "Goal": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Family Vision": {
          "Vision": [],
          "Thought Thread": [],
          "Reflections": []
        }
      },

      # ---  REFLECTIONS & INSIGHTS ---
      "Reflections & Insights": {
        "Lessons Learned": {
          "Lesson": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Appreciation & Gratitude": {
          "Appreciation": [],
          "Thought Thread": [],
          "Reflections": []
        },
        "Future Aspirations": {
          "Aspiration": [],
          "Thought Thread": [],
          "Reflections": []
        }
      }
    },},
    "Family memberns":{"structure"
    :{
  "Family": {
    "Categories": {
      "Son": {
        "Members": [

        ]
      },
      "Father": {
        "Members": [

        ]
      },
      "Mother": {
        "Members": [

        ]
      },
      "Uncle": {
        "Members": [

        ]
      },
      "Aunt": {
        "Members": [

        ]
      },
      "Granny": {
        "Members": [

        ]
      },
      "Grandpa": {
        "Members": [

        ]
      },
      "Brother": {
        "Members": [

        ]
      },
      "Sister": {
        "Members": [

        ]
      },
      "Cousin": {
        "Members": [

        ]
      },
      "Niece": {
        "Members": [

        ]
      },
      "Nephew": {
        "Members": [

        ]
      }
    }
  }
},},
    "Crime": {
    "structure": {
      "I. Crime Categories": {
        "Violent Crime": {
          "Homicide": {
            "Murder": [],
            "Manslaughter": []
          },
          "Assault": {
            "Aggravated Assault": [],
            "Simple Assault": []
          },
          "Robbery": [],
          "Sexual Assault": {
            "Rape": [],
            "Sexual Battery": [],
            "Sexual Abuse": []
          },
          "Kidnapping": []
        },
        "Property Crime": {
          "Burglary": [],
          "Larceny Theft": {
            "Grand Theft": [],
            "Petit Theft": []
          },
          "Motor Vehicle Theft": [],
          "Arson": []
        },
        "Public Order Crime": {
          "Disorderly Conduct": [],
          "Vandalism": [],
          "Public Intoxication": [],
          "Prostitution": [],
          "Drug Possession": []
        },
        "White Collar Crime": {
          "Fraud": {
            "Wire Fraud": [],
            "Mail Fraud": [],
            "Identity Theft": [],
            "Insurance Fraud": []
          },
          "Embezzlement": [],
          "Money Laundering": [],
          "Tax Evasion": [],
          "Insider Trading": []
        },
        "Organized Crime": {
          "Drug Trafficking": [],
          "Human Trafficking": [],
          "Racketeering": [],
          "Extortion": []
        },
        "Cybercrime": {
          "Hacking": {
            "Data Breaches": [],
            "DDoS Attacks": [],
            "Malware Distribution": []
          },
          "Phishing": [],
          "Cyberstalking": [],
          "Identity Theft": []
        }
      },

      "II. Specific Crimes": {
        "Specific Crime 1": {
          "Name": "",
          "Description": "",
          "Motive": "",
          "Victims": [],
          "Impact": [],
          "Consequences": [],
          "Legal Outcomes": [],
          "Thoughts And Reflections": []
        },
        "Specific Crime 2": {
          "Name": "",
          "Description": "",
          "Motive": "",
          "Victims": [],
          "Impact": [],
          "Consequences": [],
          "Legal Outcomes": [],
          "Thoughts And Reflections": []
        },
        # ... Add more specific crime details as needed
      },

      "III. Reflections And Insights": {
        "Lessons Learned": {
          "About Crime": [],
          "About Criminal Justice System": [],
          "About Human Nature": [],
          "About Society": []
        },
        "Impact On Values And Beliefs": {
          "Beliefs About Justice": [],
          "Beliefs About Human Rights": [],
          "Beliefs About Safety And Security": []
        },
        "Future Aspirations": {
          "For Myself": "",
          "For Society": ""
        },
        "Vision For A Safer World": ""
      }
    }
  },
    "Programming": {
         "structure": {
      "I. Programming Paradigms": {
        "Object-Oriented Programming": {
          "Classes and Objects": [],
          "Inheritance": [],
          "Polymorphism": [],
          "Encapsulation": []
        },
        "Functional Programming": {
          "Functions as First-Class Citizens": [],
          "Immutability": [],
          "Higher-Order Functions": [],
          "Recursion": []
        },
        "Procedural Programming": {
          "Procedures and Functions": [],
          "Control Flow": [],
          "Data Structures": []
        },
        "Logic Programming": {
          "Predicates and Logic": [],
          "Unification": [],
          "Resolution": []
        },
        "Other Paradigms": {
          "Aspect-Oriented Programming": [],
          "Event-Driven Programming": [],
          "Generative Programming": []
        }
      },

      "II. Programming Languages": {
        "Scripting Languages": {
          "Python": [],
          "JavaScript": [],
          "Ruby": [],
          "PHP": []
        },
        "Compiled Languages": {
          "C++": [],
          "Java": [],
          "C#": [],
          "Go": []
        },
        "Markup Languages": {
          "HTML": [],
          "XML": [],
          "Markdown": []
        },
        "Other Languages": {
          "Swift": [],
          "Kotlin": [],
          "Scala": [],
          "Rust": []
        }
      },

      "III. Software Development": {
        "Software Design": {
          "Design Patterns": [],
          "Software Architecture": [],
          "Software Requirements": []
        },
        "Software Testing": {
          "Unit Testing": [],
          "Integration Testing": [],
          "System Testing": []
        },
        "Software Deployment": {
          "Continuous Integration": [],
          "Continuous Delivery": [],
          "DevOps": []
        },
        "Other Aspects": {
          "Version Control": [],
          "Project Management": [],
          "Code Optimization": []
        }
      },

      "IV. Data Structures and Algorithms": {
        "Data Structures": {
          "Arrays": [],
          "Linked Lists": [],
          "Trees": [],
          "Graphs": [],
          "Hash Tables": []
        },
        "Algorithms": {
          "Sorting Algorithms": [],
          "Searching Algorithms": [],
          "Graph Algorithms": [],
          "Dynamic Programming": []
        }
      },

      "V. Computer Science Fundamentals": {
        "Operating Systems": {
          "Processes and Threads": [],
          "Memory Management": [],
          "File Systems": []
        },
        "Computer Networks": {
          "Network Protocols": [],
          "Network Security": [],
          "Network Architecture": []
        },
        "Databases": {
          "SQL": [],
          "NoSQL": [],
          "Database Design": []
        },
        "Other Fundamentals": {
          "Cryptography": [],
          "Artificial Intelligence": [],
          "Machine Learning": []
        }
      }
    },
    "Hacking": {
    "structure": {
      "I. Techniques": {
        "Exploitation": {
          "Vulnerability Analysis": {
            "Code Auditing": [],
            "Fuzzing": [],
            "Static Analysis": [],
            "Dynamic Analysis": []
          },
          "Exploit Development": {
            "Buffer Overflow": [],
            "SQL Injection": [],
            "Cross-Site Scripting (XSS)": [],
            "Remote Code Execution (RCE)": []
          },
          "Post-Exploitation": {
            "Privilege Escalation": [],
            "Lateral Movement": [],
            "Data Exfiltration": [],
            "Persistence": []
          }
        },
        "Social Engineering": {
          "Phishing": {
            "Email Phishing": [],
            "Spear Phishing": [],
            "Whaling": [],
            "Smishing": []
          },
          "Pretexting": [],
          "Baiting": [],
          "Quid Pro Quo": []
        },
        "Reverse Engineering": {
          "Disassembly": [],
          "Decompilation": [],
          "Debugging": [],
          "Malware Analysis": []
        },
        "Other": {
          "Password Cracking": [],
          "Denial of Service (DoS)": [],
          "Network Sniffing": []
        }
      },

      "II. Tools": {
        "Vulnerability Scanners": {
          "Nmap": [],
          "Nessus": [],
          "OpenVAS": []
        },
        "Exploitation Tools": {
          "Metasploit": [],
          "Core Impact": [],
          "Burp Suite": []
        },
        "Reverse Engineering Tools": {
          "IDA Pro": [],
          "Ghidra": [],
          "OllyDbg": []
        },
        "Other Tools": {
          "Wireshark": [],
          "Kali Linux": [],
          "Burp Suite": []
        }
      },

      "III. Ethical Hacking & Security": {
        "Penetration Testing": {
          "Types": [],
          "Methodology": [],
          "Reporting": []
        },
        "Bug Bounty": {
          "Finding & Reporting": [],
          "Rewards": [],
          "Ethics": []
        },
        "Security Awareness": {
          "Threat Identification": [],
          "Best Practices": [],
          "Phishing Awareness": []
        },
        "Other Aspects": {
          "Auditing": [],
          "Incident Response": [],
          "Vulnerability Management": []
        }
      },

      "IV. Legal & Ethical": {
        "Cybercrime Laws": {
          "CFAA": [],
          "DMCA": [],
          "Other": []
        },
        "Ethical vs. Illegal": {
          "Consent": [],
          "Reporting": [],
          "Damage": []
        },
        "Responsible Disclosure": {
          "Best Practices": [],
          "Working with Organizations": [],
          "Legal": []
        }
      },

      "V. Reflections & Insights": {
        "Lessons Learned": {
          "Vulnerabilities": [],
          "Security Awareness": [],
          "Ethics": []
        },
        "Impact": {
          "Cybercrime": [],
          "National Security": [],
          "Privacy": []
        },
        "Future Aspirations": {
          "Personal": [],
          "Community": []
        },
        "Vision": []
      }
    }
  },


},
    "Strangers": {
    "structure": {
      "I. Encounters": {
        "Unexpected Meetings": {
          "Chance Encounters": [],
          "Shared Experiences": [],
          "Unforeseen Connections": []
        },
        "Virtual Interactions": {
          "Online Communities": [],
          "Social Media Connections": [],
          "Digital Encounters": []
        },
        "First Impressions": {
          "Initial Reactions": [],
          "Assumptions and Judgments": [],
          "Breaking the Ice": []
        }
      },

      "II. Perspectives": {
        "Different Worlds": {
          "Cultural Differences": [],
          "Life Experiences": [],
          "Values and Beliefs": []
        },
        "Understanding Others": {
          "Empathy and Compassion": [],
          "Active Listening": [],
          "Open-mindedness": []
        },
        "Challenging Stereotypes": {
          "Preconceived Notions": [],
          "Breaking Down Barriers": [],
          "Diversity and Inclusion": []
        }
      },

      "III. Impact": {
        "Positive Interactions": {
          "Acts of Kindness": [],
          "Inspirational Encounters": [],
          "Personal Growth": []
        },
        "Negative Interactions": {
          "Conflicts and Misunderstandings": [],
          "Unwanted Encounters": [],
          "Dealing with Difficult People": []
        },
        "Transformative Experiences": {
          "Life-Changing Encounters": [],
          "New Perspectives": [],
          "Personal Growth and Evolution": []
        }
      },

      "IV. Reflections": {
        "The Nature of Strangers": {
          "The Unknown": [],
          "Potential and Uncertainty": [],
          "The Power of Connection": []
        },
        "Building Bridges": {
          "Overcoming Fear and Prejudice": [],
          "Promoting Understanding": [],
          "Creating a More Inclusive World": []
        },
        "The Importance of Human Connection": {
          "Connecting with Others": [],
          "Building Relationships": [],
          "The Value of Empathy and Kindness": []
        }
      }
    }
  },
    "Nature & Environment": {
        "structure": {
            "Experiences in Nature": {
                "Outdoor Activities": {
                    "Hiking & Backpacking": [],
                    "Camping": [],
                    "Gardening": [],
                    "Fishing": [],
                    "Other Outdoor Activities": []
                },
                "Wildlife Encounters": {
                    "Memorable Encounters": [],
                    "Observations & Learnings": [],
                    "Impact on My Perspective": []
                },
                "Natural Phenomena": {
                    "Weather Events": [],
                    "Stargazing": [],
                    "Sunrise & Sunset Views": [],
                    "Other Natural Phenomena": []
                },
                "Nature Photography": {
                    "Favorite Images": [],
                    "Techniques & Skills": [],
                    "Impact on My Appreciation for Nature": []
                }
            },
            "Connection to the Natural World": {
                "Environmentalism & Conservation": {
                    "Personal Values & Beliefs": [],
                    "Actions Taken": [],
                    "Organizations Involved with": []
                },
                "Appreciation for Nature": {
                    "Favorite Places & Landscapes": [],
                    "Sensory Experiences": {
                        "Sights": [],
                        "Sounds": [],
                        "Smells": [],
                        "Tastes": [],
                        "Textures": []
                    },
                    "Emotional Responses": [],
                    "Impact on My Well-being": []
                },
                "Spiritual Connection to Nature": {
                    "Beliefs & Practices": [],
                    "Impact on My Spirituality": [],
                    "Meaning & Purpose Found in Nature": []
                }
            },
            "Reflections & Insights": {
                "Lessons Learned from Nature": [],
                "Impact of Nature on My Life": {
                    "Values & Beliefs": [],
                    "Perspective on Life": [],
                    "Creativity & Inspiration": []
                },
                "Future Aspirations": {
                    "Exploring Nature Further": [],
                    "Protecting the Environment": [],
                    "Living in Harmony with Nature": []
                }
            }
        }
    },
    "Faith": {
        "structure": {
            "Religious Beliefs & Practices": {
                "Religious Affiliation": {
                    "Denomination/Tradition": [],
                    "Beliefs & Teachings": [],
                    "Key Texts & Writings": [],
                    "Rituals & Practices": []
                },
                "Spiritual Experiences": {
                    "Memorable Moments": [],
                    "Transformative Events": [],
                    "Insights & Learnings": [],
                    "Impact on My Life": []
                },
                "Religious Community": {
                    "Connections & Relationships": [],
                    "Shared Experiences": [],
                    "Impact on My Faith Journey": []
                }
            },
            "Personal Spirituality": {
                "Spiritual Beliefs": {
                    "Beliefs about God/Higher Power": [],
                    "Beliefs about the Universe": [],
                    "Beliefs about the Afterlife": [],
                    "Beliefs about Purpose & Meaning": []
                },
                "Spiritual Practices": {
                    "Meditation & Mindfulness": [],
                    "Prayer & Contemplation": [],
                    "Yoga & Tai Chi": [],
                    "Other Practices": []
                },
                "Spiritual Growth": {
                    "Personal Journey": [],
                    "Challenges & Obstacles": [],
                    "Insights & Learnings": []
                }
            },
            "Reflections & Insights": {
                "Impact of Spirituality on My Life": {
                    "Values & Beliefs": [],
                    "Decisions & Choices": [],
                    "Relationships & Connections": [],
                    "Overall Perspective on Life": []
                },
                "Lessons Learned": {
                    "From Religious Experiences": [],
                    "From Spiritual Practices": [],
                    "From Challenges & Growth": []
                },
                "Future Aspirations": {
                    "Continuing Spiritual Exploration": [],
                    "Seeking Deeper Understanding": [],
                    "Living a Spiritually Aligned Life": []
                }
            }
        }
    },
    "Visions & Fantasies": {
        "structure": {
            "Fantasies & Imaginary Worlds": {
                "Worlds Created": [],
                "Characters & Stories": [],
                "Emotional Impact": [],
                "Impact on Creativity": []
            },
            "Visions of the Future": {
                "Personal Visions": [],
                "Visions for Society": [],
                "Visions for the World": [],
                "Inspiration & Motivation": []
            },
            "Daydreaming": {
                "Favorite Daydreams": [],
                "Themes & Scenarios": [],
                "Emotional Impact": [],
                "Impact on Creativity": []
            },
            "Reflections & Insights": {
                "Impact of Visions & Fantasies on My Life": {
                    "Inspiration & Creativity": [],
                    "Goals & Aspirations": [],
                    "Perspective on Life": [],
                    "Self-Discovery": []
                },
                "Lessons Learned": {
                    "From Imaginary Worlds": [],
                    "From Visions of the Future": [],
                    "From Daydreaming": []
                },
                "Future Aspirations": {
                    "Continuing to Explore Visions & Fantasies": [],
                    "Using Visions to Shape My Future": [],
                    "Bringing Visions to Life": []
                }
            }
        }
    },
    "Dreams": {
        "structure": {
            "Good Dreams": {
                "Recurring Themes": [],
                "Memorable Dreams": [],
                "Emotional Impact": [],
                "Potential Meanings": []
            },
            "Nightmares": {
                "Recurring Themes": [],
                "Memorable Nightmares": [],
                "Emotional Impact": [],
                "Potential Meanings": []
            },
            "Prophecy Dreams": {
                "Dreams That Came True": [],
                "Dreams That Inspired Action": [],
                "Dreams That Gave Insights": [],
                "Reflections on the Predictive Nature of Dreams": []
            },
            "Dream Journaling": {
                "Methods Used": [],
                "Insights Gained from Journaling": [],
                "Recurring Symbols": [],
                "Patterns & Connections": []
            },
            "Dream Interpretation": {
                "Approaches Used": [],
                "Dream Dictionaries": [],
                "Personal Interpretations": []
            },
            "Reflections & Insights": {
                "Impact of Dreams on My Life": {
                    "Emotions & Feelings": [],
                    "Creativity & Inspiration": [],
                    "Decision-Making": [],
                    "Self-Awareness": []
                },
                "Lessons Learned": {
                    "From Recurring Themes": [],
                    "From Memorable Dreams": [],
                    "From Dream Interpretation": []
                },
                "Future Aspirations": {
                    "Continuing to Explore Dreams": [],
                    "Understanding the Significance of Dreams": [],
                    "Using Dreams for Personal Growth": []
                }
            }
        }
    },
}



import google.generativeai as genai
import re
import os
import json
from datetime import datetime
from fuzzywuzzy import fuzz  # Import fuzzywuzzy for fuzzy string matching


# ANSI color codes for terminal output
class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Define color codes as dictionary
    COLOR_CODES = {
        "red": FAIL,
        "green": OKGREEN,
        "yellow": WARNING,
        "blue": OKBLUE,
        "magenta": HEADER,

        "reset": ENDC
    }


# Configure the GenAI API
genai.configure(api_key='AIzaSyCltjPhJwWRL3BufxCdz-B4mc-6QdmQKBs')


def print_colored(text, color="white"):
    """Prints text with the specified color."""
    print(f"{TerminalColors.COLOR_CODES.get(color, '')}{text}{TerminalColors.COLOR_CODES['reset']}")


def create_folders_from_structure(structure, base_folder, folder_list):
    """Creates folders from the given structure."""
    for level1_key in structure:
        print(f"    Creating level 1 folder: {level1_key}")
        level1_folder = os.path.join(base_folder, level1_key)
        os.makedirs(level1_folder, exist_ok=True)
        folder_list.append((level1_key, level1_folder))
        print(f"      Added folder {level1_key} to list: {level1_folder}")

        if isinstance(structure[level1_key], dict):
            print(f"      Found nested dictionary for {level1_key}")
            create_folders_from_structure(structure[level1_key], level1_folder, folder_list)


def create_file_structure(memory_templates):
    """Creates the file structure for storing memories based on the provided templates."""
    script_path = os.path.abspath(os.path.dirname(__file__))
    folder_list = []  # List to store folder names and paths

    for template_name, template_data in memory_templates.items():
        print(f"Processing template: {template_name}")

        template_name_safe = template_name.replace(":", "_")
        print(f"  Safe template name: {template_name_safe}")

        base_folder = os.path.join(script_path, "memories")
        print(f"  Creating base folder: {base_folder}")
        os.makedirs(base_folder, exist_ok=True)
        folder_list.append((template_name_safe, base_folder))

        template_folder = os.path.join(base_folder, template_name_safe)
        print(f"  Creating template folder: {template_folder}")
        os.makedirs(template_folder, exist_ok=True)
        folder_list.append((template_name_safe, template_folder))

        create_folders_from_structure(template_data["structure"], template_folder, folder_list)

    # Compare folder names and create connection map
    similar_folders = find_similar_folders(folder_list)

    # Save connection map to "Memory_connecions_map.txt"
    with open("memories/Memory_connecions_map.txt", "w") as f:
        for folder_name, paths in similar_folders.items():
            f.write(f"**** {folder_name} ****\n")  # Add separator
            for path in paths:
                f.write(f"  Path: {path}\n")
            f.write("\n")


def find_similar_folders(folder_list):
    """Finds similar folder names in the list using Levenshtein distance."""
    similar_folders = {}

    total_comparisons = len(folder_list) * (len(folder_list) - 1) // 2  # Calculate total comparisons
    comparisons_left = total_comparisons

    for i in range(len(folder_list)):
        folder_name_1, path_1 = folder_list[i]

        if folder_name_1 not in similar_folders:
            similar_folders[folder_name_1] = [path_1]

        for j in range(i + 1, len(folder_list)):
            folder_name_2, path_2 = folder_list[j]

            similarity_score = fuzz.ratio(folder_name_1, folder_name_2)

            print(f"Comparing '{folder_name_1}' and '{folder_name_2}': Score = {similarity_score}")
            print_colored(f"Comparisons left: {comparisons_left}", "yellow")  # Print remaining comparisons in yellow
            comparisons_left -= 1

            # Adjust threshold as needed
            if similarity_score >= 80:  # Example threshold adjusted to 80
                print(f"   Found similar folders: '{folder_name_1}' and '{folder_name_2}'")
                if folder_name_1 in similar_folders:
                    similar_folders[folder_name_1].append(path_2)
                else:
                    similar_folders[folder_name_1] = [path_1, path_2]

    return similar_folders


def categorize_memory(summary, categories):
    """Categorizes a memory frame based on keywords in the summary."""
    for category, subcategories in categories.items():
        for time_period, keyword_list in subcategories.items():
            for keyword in keyword_list:
                if re.search(rf"\b{keyword}\b", summary, re.IGNORECASE):
                    return category, time_period, keyword

    return "uncategorized", "unknown", "unknown"


def search_memories(query, category=None, time_period=None):
    """Searches for memories based on the given criteria."""
    matching_memories = []
    for root, _, files in os.walk("memories"):
        for file in files:
            print("checking")
            if file.endswith(".txt"):
                filepath = os.path.join(root, file)
                # Check if the category and time_period match (if provided)
                if category and category not in filepath:
                    continue
                if time_period and time_period not in filepath:
                    continue
                # Search within the file content
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        matching_memories.append(filepath)
    return matching_memories


def retrieve_memories(phrase, log_filepath):
    """Retrieves memory frames based on phrase matching, folder traversal, and temporal sorting."""
    phrase_parts = re.findall(r'\w+', phrase)  # Example: simple word splitting
    candidate_frames = []

    for root, _, files in os.walk("memories"):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                for part in phrase_parts:
                    if part.lower() in filepath.lower():
                        # Load the memory frame from the file
                        with open(filepath, 'r') as f:
                            frame_data = json.load(f)
                            frame_data["Path"] = filepath  # Add filepath to data
                            candidate_frames.append(frame_data)
                        break  # Move to next file after finding a match

    # Sort by timestamp and group by session
    sorted_frames = sorted(candidate_frames, key=lambda x: x["Time"], reverse=True)
    sessions = {}
    for frame in sorted_frames:
        session_id = frame["Session"]
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append(frame)

    # Create sets of frames based on the session and time
    all_frames = sorted_frames  # All frames, sorted by time

    # Example: Create a contextual set of frames
    contextual_sets = {}  # Store multiple contextual sets
    for session_id, frames in sessions.items():
        for i, frame in enumerate(frames):
            contextual_set = []
            contextual_set.append(frame)

            # Add frames before the current frame
            for j in range(i - 1, -1, -1):
                contextual_set.append(frames[j])

            # Add frames after the current frame
            for j in range(i + 1, len(frames)):
                contextual_set.append(frames[j])

            contextual_sets[f"{session_id}_{frame['Time']}"] = contextual_set






def response_interpreter_for_function_calling(response):
    """Interprets the AI's response and executes function calls
       (excluding memory storage).
    """
    outcome = []
    try:
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call'):
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = function_call.args

                    if function_name in FUNCTION_MAPPING:
                        function_to_call = FUNCTION_MAPPING[function_name]
                        if function_args is not None:
                            try:
                                outcome = function_to_call(**function_args)
                            except Exception as e:
                                print_colored(
                                    f"Error executing function {function_name}: {e}",
                                    "blue"
                                )
                        else:
                            print_colored(
                                "Warning: Function call arguments are missing.", "red"
                            )
                    else:
                        print(response)
                        print_colored(
                            f"Error: Unknown function: {function_name}", "red"
                        )
                else:
                    print_colored(
                        "No function call found in the response.", "blue"
                    )
    except Exception as E:
        print(E)
    if outcome is None:
        outcome = ""
    return outcome


FUNCTION_MAPPING = {
    # Example:
    # "play_music": play_music,
}


def STORE_MEMORY_Frame(current_time, user_input, ai_response, ai_response2, memory_data):
    """Stores structured memory data and the conversation frame across multiple templates SIMULTANEOUSLY."""
    # Define color codes
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    magenta = "\033[95m"
    cyan = "\033[96m"
    white = "\033[97m"
    reset = "\033[0m"
    import json
    from collections import defaultdict
    from typing import List, Dict

    # --- Load Connection Map ---
    script_path = os.path.abspath(os.path.dirname(__file__))
    connection_map_path = os.path.join(script_path, "memories", "Memory_connecions_map.txt")
    with open(connection_map_path, 'r', encoding='utf-8') as f:
        connection_map_data = f.read()

    # --- Process Connection Map Data ---
    connection_map = defaultdict(list)
    for line in connection_map_data.splitlines():
        if "****" in line:
            current_folder_name = line.strip("****").strip()
        elif "  Path:" in line:
            path = line.strip("  Path:").strip()
            connection_map[current_folder_name].append(path)

    print(f"{yellow}Connection Map: {connection_map}{reset}")

    def extract_entries_smart(response_message):

        entries = []
        print(f"{magenta}extract_entries_smart{reset}")

        # Use regex to find the JSON block
        json_match = re.search(r"```json\n(.*?)\n```", response_message, re.DOTALL)

        # If JSON block is found, extract the JSON data
        if json_match:
            try:
                json_data = json_match.group(1)  # Extract JSON string
                response_data = json.loads(json_data)
                print(f"{green}Successfully loaded JSON data:{reset}")
                print(json.dumps(response_data, indent=4))  # Print the loaded JSON data

                # --- Extract data using matching rules ---
                entry = defaultdict(list)

                # Define a set of single-value fields
                single_value_fields = {
                    "concise_summary",
                    "main_topic",
                    "problem_solved",
                    "concept_definition",
                    "category",
                    "subcategory",
                    "memory_about",
                    "interaction_type",  # Handle potential lists
                    "positive_impact",
                    "negative_impact",
                    "expectations",
                    "object_states",
                    "short_description",
                    "description",
                    "strength_of_experience",
                    "personal_information",
                    "obtained_knowledge"
                }

                # Define a set of list-type fields
                list_type_fields = {
                    "keywords",
                    "entities",
                    "actions",
                    "facts",
                    "contradictions_paradoxes",
                    "people",
                    "objects",
                    "animals",
                    "scientific_data",
                    "tags",
                    "tools_and_technologies",
                    "example_projects",
                    "best_practices",
                    "common_challenges",
                    "debugging_tips",
                    "related_concepts",
                    "visualizations",
                    "implementation_steps",  # Handle lists of dictionaries
                    "resources",  # Handle lists of dictionaries
                    "code_examples"  # Handle lists of dictionaries
                }

                # Direct Matching:
                for key, value in response_data.items():
                    if key in single_value_fields:
                        if isinstance(value, list):
                            entry[key].extend(value)  # Handle potential list values
                        else:
                            entry[key] = value
                        print(f"{blue}Direct match: {key} = {value}{reset}")
                    elif key in list_type_fields:
                        if isinstance(value, list):
                            if value and isinstance(value[0], dict):
                                entry[key].extend(value)  # Handle lists of dictionaries
                            else:
                                entry[key].extend(value)  # Handle lists of simple values
                        else:
                            entry[key].append(value)  # Handle single value
                        print(f"{blue}List match: {key} = {value}{reset}")

                # Keyword-Based Mapping:
                for key, value in response_data.items():
                    if "keyword" in key.lower() and isinstance(value, list):
                        entry["keywords"].extend(value)
                        print(f"{blue}Keyword match: {key} = {value}{reset}")
                    elif "description" in key.lower():
                        entry["description"] = value
                        print(f"{blue}Description match: {key} = {value}{reset}")
                    elif "summary" in key.lower():
                        entry["concise_summary"] = value
                        print(f"{blue}Summary match: {key} = {value}{reset}")
                    elif "step" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["implementation_steps"].extend(value)
                        print(f"{blue}Step match: {key} = {value}{reset}")
                    elif "resource" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["resources"].extend(value)
                        print(f"{blue}Resource match: {key} = {value}{reset}")
                    elif "code" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["code_examples"].extend(value)
                        print(f"{blue}Code match: {key} = {value}{reset}")

                # Additional Matching:
                for key, value in response_data.items():
                    if "interaction_type" in key.lower() and isinstance(value, list):
                        entry["interaction_type"].extend(value)
                        print(f"{blue}Interaction type match: {key} = {value}{reset}")
                    elif "category" in key.lower():
                        entry["category"] = value
                        print(f"{blue}Category match: {key} = {value}{reset}")
                    elif "subcategory" in key.lower():
                        entry["subcategory"] = value
                        print(f"{blue}Subcategory match: {key} = {value}{reset}")

                # --- Store 'storage' information ---
                entry["storage"] = {
                    "storage_method": "",  # Placeholder - You might extract this from the AI response
                    "location": "",  # Placeholder - You might extract this from the AI response
                    "memory_folders_storage": [],  # These will be set later
                    "strenght of matching memory to given folder": []  # These will be set later
                }

                # Append the entry to the list
                entries.append(dict(entry))  # Convert back to regular dict
                print(f"{green}Extracted entry: {entry}{reset}")  # Print the extracted entry
                print(f"{yellow}{'-' * 30}{reset}")  # Separator for better readability

            except json.JSONDecodeError:
                print(f"{red}Error: Invalid JSON in response message.{reset}")
            except Exception as e:
                print(f"{red}Error extracting entry: {e}{reset}")

        return entries

    extracted_entries = extract_entries_smart(ai_response2)

    if extracted_entries:
        # --- Analyze and Categorize ---
        for entry in extracted_entries:
            print(f"{yellow}Analyzing entry: {entry}{reset}")
            # --- Find Matching Folders ---
            matching_folders = []
            print(f"{magenta}Matching Folders: {matching_folders}{reset}")

            category, time_period, keyword = categorize_memory(entry["concise_summary"], connection_map)

            if category and time_period:
                print(f"{green}Memory categorized as {category} - {time_period} - {keyword}{reset}")
                # Retrieve potential folders for the memory based on the connection map
                matching_folders = connection_map.get(f"{category} - {time_period}", [])
            else:
                print(f"{yellow}Memory categorization: Uncategorized, Unknown, Unknown{reset}")

            if matching_folders:
                print(f"{green}Matching Folders found: {matching_folders}{reset}")

                # --- Calculate matching scores ---
                matching_scores = []
                for folder in matching_folders:
                    # Extract category and time_period from the folder name
                    parts = folder.split("\\")[-2:]  # Get last two parts of the path
                    category = parts[0]
                    time_period = parts[1]

                    # Calculate similarity scores
                    similarity_score = fuzz.ratio(entry["concise_summary"], f"{category} {time_period}")
                    matching_scores.append((folder, similarity_score))

                # --- Update memory frame ---
                entry["storage"]["memory_folders_storage"] = matching_folders
                entry["storage"]["strenght of matching memory to given folder"] = matching_scores
                print(f"{green}Updated memory frame: {entry}{reset}")

                # --- Store Memory Frame ---
                script_path = os.path.abspath(os.path.dirname(__file__))
                memory_frame_number = memory_data.get('MEMORY_FRAME_NUMBER', 1)
                edit_number = memory_data.get('EDIT_NUMBER', 0)
                timestamp_format = "%Y-%m-%d_%H-%M-%S"
                timestamp = current_time.strftime(timestamp_format)
                for folder, similarity_score in matching_scores:  # Iterate using folder and score
                    # Add strength score to file name if it's not "unknown"
                    file_name_suffix = ""
                    if similarity_score != "unknown":
                        file_name_suffix = f"_strenght_{similarity_score}"

                    memory_frame_filepath = os.path.join(script_path, folder,
                                                         f"MemoryFrame_{memory_frame_number}_{edit_number}_{timestamp}{file_name_suffix}.json")
                    os.makedirs(os.path.join(script_path, folder), exist_ok=True)
                    with open(memory_frame_filepath, "w") as f:
                        json.dump(entry, f, indent=4)

                    # --- Update Memory Frame Log ---
                    os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
                    memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")
                    with open(memory_log_filepath, 'a', encoding='utf-8') as f:
                        f.write(
                            f"MemoryFrame: {memory_frame_number}, Edit: {edit_number}, Type: JSON, path: {memory_frame_filepath}, time: {timestamp}, session: {memory_frame_number}_{edit_number}\n"
                        )  # Log the file path
                    print(f"Memory frame log updated: {memory_log_filepath}")
                    print(f"{green}Memory frame saved in: {memory_frame_filepath}{reset}")

            else:
                print(f"{yellow}No matching folders found for this memory frame{reset}")
    else:
        print(f"{yellow}No JSON data found in the AI response{reset}")

    # --- Store Conversation Frame ---
    separator = "######$######"
    conversation_filename = f"MemoryFrame_{timestamp}.txt"
    conversation_filepath = os.path.join(script_path, "conversation_logs", conversation_filename)

    readable_timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    frame_content = (
        f"{separator} Memory Frame {memory_frame_number}, Edit {edit_number} - {readable_timestamp} {separator}\n"
        f"USER_INPUT: {user_input}\n"
        f"AI_RESPONSE: {ai_response}\n"
        f"AI_RESPONSE_SUMMARY: {ai_response2}\n"
        f"{separator} Memory Frame End {memory_frame_number}, Edit {edit_number} {separator}\n\n"
    )

    with open(conversation_filepath, 'a', encoding='utf-8') as f:
        f.write(frame_content)
    print(f"Conversation frame saved in: {conversation_filepath}")

    # Increment memory frame number
    memory_data['MEMORY_FRAME_NUMBER'] += 1

    # --- Update Memory Frame Log ---
    os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
    memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")
    with open(memory_log_filepath, 'a', encoding='utf-8') as f:
        f.write(
            f"MemoryFrame: {memory_frame_number - 1}, Edit: {edit_number}, Type: Text, path: {memory_frame_filepath}, time: {timestamp}, session: {memory_frame_number - 1}_{edit_number}\n"
        )  # Log the file path
    print(f"Memory frame log updated: {memory_log_filepath}")


def summarise_memory_folder_structure(folder_path, file_path="directory_structure.txt", include_files=True):


    ignore_files = [".\\directory_structure.txt", ".\\Memory_connecions_map.txt"]

    with open(file_path, 'w') as f:
        f.write(f"Directory structure for: {folder_path}\n\n")
        for root, dirs, files in os.walk(folder_path):
            # Write folder path to file
            f.write(f"{root}\n")

            if include_files:
                # Write file names to file, ignoring specified files
                for file in files:
                    full_path = os.path.join(root, file)
                    if full_path not in ignore_files:
                        f.write(f"{full_path}\n")


# --- Load Memory Templates ---
with open("memories/memory_templates.json", "r") as f:
    memory_templates = json.load(f)

# --- Create File Structure and Connection Map ---
create_file_structure(memory_templates)
directory_structure = summarise_memory_folder_structure(folder_path="./memories",
                                                        file_path="./memories/directory_structure.txt")
memory_data = {
    'MEMORY_FRAME_NUMBER': 1,  # Initialize memory frame number
    'EDIT_NUMBER': 0  # Initialize edit number
}

while True:
    try:
        user_input = input("Enter input: ")

        interaction_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            safety_settings={'HARASSMENT': 'block_none'},
            system_instruction='You follow orders and generate creative text interactions'
        )

        current_time = datetime.now()

        # Format timestamp outside the prompt
        formatted_timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')

        chat1 = interaction_model.start_chat(history=[])
        prompt = f"currentTime:  {formatted_timestamp}  create {user_input} "
        chat1 = interaction_model.start_chat(history=[])
        prompt = f"currentTime:  {current_time}  create {user_input} "
        print(f"Prompt:  {prompt}")
        response1 = chat1.send_message(prompt)
        try:
            print_colored(f"AI Response: {response1.text}", "green")
        except Exception as e:
            print(e)

        # --- Memory Processing with Gemini ---
        memory_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            safety_settings={'HARASSMENT': 'block_none'},
            system_instruction="""You are a sophisticated AI assistant helping to organize memories. 
                    Analyze and summarize the above user-AI conversation, focusing on elements that would be most useful for storing and retrieving this memory later. Don't hallucinate.
                    use provided schema  for  response
                    Provide the following information in a structured format using JSON:  you  have  2 Templates to choose form

                    you can also  cut  out entries  if  they  dont  seem  approparate for  memory storage and would be  empty
                    never  crose  out   "Memory Folder storage entry": 
                    """,

        )
        print(
            f" *****************************************************************************************************")
        schema_for_chat2 = """   
                                if  the memory  does  not  fit  into schema  you can  reduce  entries  and  focues  on most  important entries:
                                but  always  use  "memory_folders_storage": as  suggestion  in what  folders  that   memor should be saved.

                                Template  to use:          
                                         {
                              "metadata": {
                                "creation_date": "", // Date and time the memory was created.
                                "source": "", // Origin of the memory (e.g., conversation, website, book).
                                "author": "" // Author or source of the memory.
                              },
                              "type": "conversation" // OR "technical_concept"  (This field designates the memory type)
                              "core": {
                                "main_topic": "",  // Core theme or subject of the memory.
                                "category": "",  // General category (e.g., "Technology", "History", "Science").
                                "subcategory": "", // More specific category (e.g., "Programming", "World War II", "Biology").
                                "memory_about": "" // Brief description of what the memory is about.
                              },
                              "summary": {
                                "concise_summary": "", // Brief overview of the memory's content.
                                "description": "" //  Detailed explanation of the memory.
                              },
                              "content": {
                                "keywords": [], // Key terms related to the memory.
                                "entities": [], // People, places, things mentioned.
                                "tags": [], // User-defined tags for retrieval.
                                "observations": [], //  Interesting observations or insights made.
                                "facts": [], //  Statements of fact in the memory.
                                "contradictions": [], //  Contradictions or conflicting statements. 
                                "paradoxes": [], //  Paradoxes or seemingly contradictory ideas. 
                                "scientific_data": [], //  Scientific data or observations.
                                "visualizations": [], //  Visualizations or diagrams related to the memory.
                              },
                              "interaction": {
                                "interaction_type": [], // Type of interaction that occurred (e.g., "Question-Answer", "Discussion", "Instruction-Following"). 
                                "people": [], //  People involved in the memory.
                                "objects": [], //  Objects involved in the memory.
                                "animals": [], //  Animals involved in the memory. 
                                "actions": [], // Actions or events described in the memory. 
                                "observed_interactions": [], //  Additional interactions observed.
                              },
                              "impact": {
                                "obtained_knowledge": "", //  New knowledge or insights gained.
                                "positive_impact": "", // Positive outcomes of the memory.
                                "negative_impact": "", //  Negative outcomes of the memory.
                                "expectations": "", //  User expectations before the interaction.
                                "strength_of_experience": "" // Significance of the memory for the user.
                              },
                              "importance": {
                                "reason": "", //  Why this memory is significant or important. 
                                "potential_uses": [] //  How this memory might be used or applied in the future.
                              },
                              "technical_details": { 
                                 "problem_solved": "", // (For technical concepts)  The problem being addressed.
                                 "concept_definition": "", // (For technical concepts) A clear definition of the term. 
                                 "implementation_steps": [
                                   {
                                     "step": "",
                                     "code_snippet": "",
                                     "notes": ""
                                   }
                                 ], //  Implementation steps for a technical concept. 
                                 "tools_and_technologies": [], //  Tools or technologies used for implementation.
                                 "example_projects": [], //  Examples of real-world projects using the concept.
                                 "best_practices": [], //  Best practices for implementation.
                                 "common_challenges": [], //  Common difficulties encountered.
                                 "debugging_tips": [], //  Tips for troubleshooting.
                                 "related_concepts": [], //  Other related concepts. 
                                 "resources": [
                                   {
                                     "type": "",
                                     "url": "",
                                     "title": ""
                                   }
                                 ], // Relevant resources (articles, books, videos).
                                 "code_examples": [
                                   {
                                     "name": "",
                                     "description": "",
                                     "code": "",
                                     "notes": ""
                                   }
                                 ], // Code examples relevant to the memory. 
                              },
                              "storage": {
                                "storage_method": "", //  How the memory is stored (e.g., database, file system).
                                "location": "", //  The location where the memory is stored.
                                "memory_folders_storage": [] //  Suggested folders for storage.
                                "strenght of matching memory to given folder": [] //  from scale 0-10
                              }
                            }

            """

        chat_2 = memory_model.start_chat(history=[])
        create_memory_prompt = f"""User: {user_input}
                                    AI: {response1.text}
                                    Schema:
                                    {schema_for_chat2}"""

        print(create_memory_prompt)

        response2 = chat_2.send_message(create_memory_prompt)
        print("-----------------------------------------------------------------------------------")
        print(f"  Memory Data: {response2.text}")
        print(f"  ******---->STORE_MEMORY_Frame *******")

        # --- Function Execution ---
        response_interpreter_for_function_calling(response2)
        try:
            STORE_MEMORY_Frame(
                current_time,  # Pass current_time as the first argument
                user_input,
                response1.text,
                response2.text,
                memory_data
            )
        except Exception as e:
            print(e);

    except Exception as e:
        print_colored(f"Error in the main loop: {e}", "red")