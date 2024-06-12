MemoryLogTemplate = {
  "possible_parameters": [
    {
      "name": "date",
      "type": "datetime",
      "description": "Date the memory occurred"
    },
    {
      "name": "location",
      "type": "str",
      "description": "Physical location or setting"
    },
    {
      "name": "mood",
      "type": "str",
      "description": "Primary emotion or overall mood"
    },
    {
      "name": "people_present",
      "type": "list of str",
      "description": "Names or descriptions of people involved"
    },
    {
      "name": "activities",
      "type": "list of str",
      "description": "Actions, events, or activities that took place"
    },
    {
      "name": "personal_reflection",
      "type": "str",
      "description": "Thoughts, feelings, or insights about the experience"
    },
    {
      "name": "dream_elements",
      "type": "list of str",
      "description": "If part of a dream, key elements or symbols"
    },
    {
      "name": "dream_interpretation",
      "type": "str",
      "description": "Personal thoughts on the dream's meaning"
    },
    {
      "name": "daydream_scenario",
      "type": "str",
      "description": "If a daydream, the imagined situation"
    },
    {
      "name": "fantasy_world",
      "type": "str",
      "description": "Description of a fantastical world associated with the memory"
    },
    {
      "name": "dream_emotions",
      "type": "list of str",
      "description": "Emotions felt within the dream"
    },
    {
      "name": "dream_characters",
      "type": "list of str",
      "description": "Descriptions of characters or entities in the dream"
    },
    {
      "name": "dream_symbolism",
      "type": "list of str",
      "description": "Symbolic meanings or interpretations of dream elements"
    },
    {
      "name": "dream_intensity",
      "type": "int",
      "description": "1-10 rating of how vivid or intense the dream felt"
    },
    {
      "name": "nightmare_severity",
      "type": "int",
      "description": "1-10 rating if the dream was a disturbing nightmare"
    },
    {
      "name": "spiritual_experience",
      "type": "str",
      "description": "Description of any spiritual feelings or insights"
    },
    {
      "name": "existential_thoughts",
      "type": "str",
      "description": "Reflections on life, purpose, or the universe"
    },
    {
      "name": "deja_vu_intensity",
      "type": "int",
      "description": "1-10 rating if the experience felt like d�j? vu"
    },
    {
      "name": "altered_state_of_consciousness",
      "type": "str",
      "description": "Description if in an altered state (meditation, etc.)"
    },
    {
      "name": "religious_context",
      "type": "str",
      "description": "If relevant, the religious/spiritual tradition or belief system"
    },
    {
      "name": "mystical_visions",
      "type": "list of str",
      "description": "Descriptions of mystical or supernatural visions"
    },
    {
      "name": "spiritual_growth",
      "type": "str",
      "description": "How the experience contributed to spiritual development"
    },
    {
      "name": "philosophical_insights",
      "type": "list of str",
      "description": "Deep thoughts or realizations about philosophy"
    },
    {
      "name": "questions_about_existence",
      "type": "list of str",
      "description": "Profound questions that arose about life/reality"
    },
    {
      "name": "physical_state",
      "type": "str",
      "description": "Overall physical health or condition at the time"
    },
    {
      "name": "illnesses",
      "type": "list of str",
      "description": "Any illnesses or physical discomfort experienced"
    },
    {
      "name": "medications_taken",
      "type": "list of str",
      "description": "Medications or substances consumed"
    },
    {
      "name": "energy_levels",
      "type": "str",
      "description": "Level of physical energy (high, low, fluctuating)"
    },
    {
      "name": "physical_sensations",
      "type": "list of str",
      "description": "Detailed descriptions of bodily feelings/sensations"
    },
    {
      "name": "injuries_or_pains",
      "type": "list of str",
      "description": "Any injuries, wounds, aches or pains felt"
    },
    {
      "name": "medical_procedures",
      "type": "list of str",
      "description": "Treatments, exams or procedures undergone"
    },
    {
      "name": "exercise_or_physical_activity",
      "type": "list of str",
      "description": "Types of exercise or movement involved"
    },
    {
      "name": "diet_and_nutrition",
      "type": "str",
      "description": "Dietary patterns, habits or notable foods eaten"
    },
    {
      "name": "meals_consumed",
      "type": "list of str",
      "description": "Specific foods and drinks consumed"
    },
    {
      "name": "hunger_level_before",
      "type": "str",
      "description": "How hungry you were before eating"
    },
    {
      "name": "satisfaction_after",
      "type": "str",
      "description": "Level of satisfaction with the food/drink"
    },
    {
      "name": "culinary_context",
      "type": "str",
      "description": "Atmosphere, company, or cultural significance of the meal"
    },
    {
      "name": "food_preparation",
      "type": "str",
      "description": "How the food was cooked, prepared or presented"
    },
    {
      "name": "food_quality",
      "type": "int",
      "description": "1-10 rating of the taste and quality of the food"
    },
    {
      "name": "alcohol_consumed",
      "type": "list of str",
      "description": "Types and amounts of alcoholic drinks"
    },
    {
      "name": "dining_location",
      "type": "str",
      "description": "The restaurant, home, event, or place where eating occurred"
    },
    {
      "name": "cultural_cuisine",
      "type": "str",
      "description": "If relevant, the cultural or ethnic style of cuisine"
    },
    {
      "name": "food_memories",
      "type": "list of str",
      "description": "Childhood or nostalgic food memories evoked"
    },
    {
      "name": "clothing_worn",
      "type": "list of str",
      "description": "Description of clothes worn by you and others"
    },
    {
      "name": "personal_grooming",
      "type": "str",
      "description": "Hairstyle, makeup, or other aspects of appearance"
    },
    {
      "name": "style_impressions",
      "type": "str",
      "description": "Thoughts on personal style or the style of others"
    },
    {
      "name": "fashion_trends",
      "type": "list of str",
      "description": "Current fashion or style trends reflected"
    },
    {
      "name": "weather_appropriateness",
      "type": "str",
      "description": "How well the clothing suited the weather conditions"
    },
    {
      "name": "outfit_meanings",
      "type": "list of str",
      "description": "Symbolic or sentimental meaning behind clothing choices"
    },
    {
      "name": "costume_or_disguise",
      "type": "str",
      "description": "If dressing up in a costume or disguise"
    },
    {
      "name": "nudity_level",
      "type": "int",
      "description": "1-10 representing how clothed or unclothed you were"
    },
    {
      "name": "attractiveness_perceptions",
      "type": "list of str",
      "description": "Thoughts about physical attractiveness"
    },
    {
      "name": "mode_of_transportation",
      "type": "str",
      "description": "Car, train, plane, walk, etc."
    },
    {
      "name": "travel_route",
      "type": "str",
      "description": "Description or map of the route taken"
    },
    {
      "name": "travel_companions",
      "type": "list of str",
      "description": "People you traveled with"
    },
    {
      "name": "travel_impressions",
      "type": "str",
      "description": "Thoughts on the journey, scenery, or destination"
    },
    {
      "name": "transportation_quality",
      "type": "int",
      "description": "1-10 rating of the transportation experience"
    },
    {
      "name": "travel_mishaps",
      "type": "list of str",
      "description": "Any delays, canceled plans or travel issues"
    },
    {
      "name": "luggage_and_packing",
      "type": "str",
      "description": "What you packed or brought with you"
    },
    {
      "name": "cultural_immersion",
      "type": "str",
      "description": "Experiences with local cultures while traveling"
    },
    {
      "name": "natural_scenery",
      "type": "list of str",
      "description": "Vivid descriptions of landscapes or nature scenes"
    },
    {
      "name": "travel_activities",
      "type": "list of str",
      "description": "Things you did at the destination"
    },
    {
      "name": "new_information_learned",
      "type": "list of str",
      "description": "Facts, concepts, or skills acquired"
    },
    {
      "name": "sources_of_information",
      "type": "list of str",
      "description": "Books, articles, conversations, etc."
    },
    {
      "name": "intellectual_engagement",
      "type": "str",
      "description": "Level of mental stimulation or challenge"
    },
    {
      "name": "insights_gained",
      "type": "list of str",
      "description": "New understandings or perspectives"
    },
    {
      "name": "academic_subjects",
      "type": "list of str",
      "description": "School or academic topics involved"
    },
    {
      "name": "research_processes",
      "type": "list of str",
      "description": "Methods used to study, investigate or learn"
    },
    {
      "name": "knowledge_application",
      "type": "str",
      "description": "How the new knowledge was put into practice"
    },
    {
      "name": "intellectual_discussions",
      "type": "list of str",
      "description": "Key points from debates or discourses"
    },
    {
      "name": "logical_reasoning",
      "type": "list of str",
      "description": "Examples of analytical or rational thinking"
    },
    {
      "name": "unanswered_questions",
      "type": "list of str",
      "description": "Topics you wondered about or still had questions on"
    },
    {
      "name": "artistic_inspirations",
      "type": "list of str",
      "description": "Sources of creative inspiration"
    },
    {
      "name": "artistic_medium",
      "type": "str",
      "description": "Painting, music, writing, etc."
    },
    {
      "name": "creative_process",
      "type": "str",
      "description": "Description of the creative process or techniques used"
    },
    {
      "name": "artistic_outcomes",
      "type": "list of str",
      "description": "Artwork, music, writing, or other creations"
    },
    {
      "name": "creative_challenges",
      "type": "list of str",
      "description": "Obstacles, blocks or difficulties faced"
    },
    {
      "name": "creative_flow",
      "type": "str",
      "description": "Your experience of being 'in the zone' creatively"
    },
    {
      "name": "creative_expression",
      "type": "str",
      "description": "What emotions or ideas you aimed to express"
    },
    {
      "name": "art_interpretation",
      "type": "list of str",
      "description": "Analyzing deeper symbolism or meaning in art"
    },
    {
      "name": "creative_collaboration",
      "type": "list of str",
      "description": "Others you collaborated with artistically"
    },
    {
      "name": "creative_feedback",
      "type": "list of str",
      "description": "Response, critique or feedback received"
    },
    {
      "name": "devices_used",
      "type": "list of str",
      "description": "Phones, computers, cameras, etc."
    },
    {
      "name": "digital_interactions",
      "type": "str",
      "description": "Online activities, social media use, etc."
    },
    {
      "name": "technological_impact",
      "type": "str",
      "description": "How technology influenced the experience"
    },
    {
      "name": "software_applications",
      "type": "list of str",
      "description": "Programs, apps or digital tools utilized"
    },
    {
      "name": "technological_difficulties",
      "type": "list of str",
      "description": "Glitches, failures or issues with technology"
    },
    {
      "name": "futuristic_technology",
      "type": "list of str",
      "description": "Imagined, speculative or bleeding-edge tech"
    },
    {
      "name": "technology_learning",
      "type": "str",
      "description": "Processes of learning or adapting to new technologies"
    },
    {
      "name": "cybersecurity_concerns",
      "type": "list of str",
      "description": "Worries about privacy, hacking or online safety"
    },
    {
      "name": "virtual_reality",
      "type": "str",
      "description": "Experiences involving virtual, augmented or mixed reality"
    },
    {
      "name": "human_robot_interaction",
      "type": "str",
      "description": "Encounters or relationships with robots/AI"
    },
    {
      "name": "expenses",
      "type": "list of str",
      "description": "Money spent and on what"
    },
    {
      "name": "financial_decisions",
      "type": "list of str",
      "description": "Financial choices made"
    },
    {
      "name": "financial_impact",
      "type": "str",
      "description": "How the memory affected your financial situation"
    },
    {
      "name": "income_sources",
      "type": "list of str",
      "description": "Where your money was coming from"
    },
    {
      "name": "charitable_donations",
      "type": "list of str",
      "description": "Money or resources donated to causes"
    },
    {
      "name": "financial_goals",
      "type": "list of str",
      "description": "Savings targets or future money objectives"
    },
    {
      "name": "investment_activities",
      "type": "list of str",
      "description": "Trading, investing, or portfolio management"
    },
    {
      "name": "budgeting_practices",
      "type": "str",
      "description": "How you allocated, tracked or planned spending"
    },
    {
      "name": "financial_education",
      "type": "list of str",
      "description": "What you learned about money management"
    },
    {
      "name": "entrepreneurial_efforts",
      "type": "list of str",
      "description": "Business ideas, startups or money-making ventures"
    },
    {
      "name": "economic_conditions",
      "type": "str",
      "description": "State of the economy and how it impacted you"
    },
    {
      "name": "luxury_experiences",
      "type": "list of str",
      "description": "Extravagant purchases or high-end indulgences"
    },
    {
      "name": "financial_stress",
      "type": "str",
      "description": "Any anxiety, worry or strain related to money"
    },
    {
      "name": "lucky_moments",
      "type": "list of str",
      "description": "Instances of good fortune"
    },
    {
      "name": "unfortunate_events",
      "type": "list of str",
      "description": "Instances of bad luck"
    },
    {
      "name": "coincidences",
      "type": "list of str",
      "description": "Noteworthy coincidences"
    },
    {
      "name": "gut_feelings",
      "type": "str",
      "description": "Intuitive feelings or hunches experienced"
    },
    {
      "name": "gambling_activities",
      "type": "list of str",
      "description": "Games of chance, betting or gambling"
    },
    {
      "name": "risk_taking",
      "type": "list of str",
      "description": "Daring acts or choices involving risk"
    },
    {
      "name": "manifestations",
      "type": "list of str",
      "description": "Things you hoped for that seemed to manifest"
    },
    {
      "name": "near_misses",
      "type": "list of str",
      "description": "Narrow avoidance of accidents or mishaps"
    },
    {
      "name": "karma_reflections",
      "type": "str",
      "description": "Thoughts on cosmic justice or getting what's deserved"
    },
    {
      "name": "opportunity_seized",
      "type": "list of str",
      "description": "Fortunate chances that were capitalized on"
    },
    {
      "name": "jokes_told",
      "type": "list of str",
      "description": "Jokes or funny situations"
    },
    {
      "name": "humor_style",
      "type": "str",
      "description": "Type of humor (satirical, slapstick, witty)"
    },
    {
      "name": "laughter_intensity",
      "type": "str",
      "description": "How much laughter was involved"
    },
    {
      "name": "sources_of_amusement",
      "type": "list of str",
      "description": "What you found funny"
    },
    {
      "name": "comedic_performances",
      "type": "list of str",
      "description": "Descriptions of amusing stunts or skits"
    },
    {
      "name": "inside_jokes",
      "type": "list of str",
      "description": "Humorous references only some would understand"
    },
    {
      "name": "playful_banter",
      "type": "list of str",
      "description": "Examples of witty back-and-forth exchanges"
    },
    {
      "name": "pranks_or_practical_jokes",
      "type": "list of str",
      "description": "Humorous tricks or gags pulled"
    },
    {
      "name": "ridiculous_situations",
      "type": "list of str",
      "description": "Over-the-top, absurd or laughable scenarios"
    },
    {
      "name": "belly_laughs",
      "type": "int",
      "description": "1-10 rating of how hard you belly-laughed"
    },
    {
      "name": "regrets",
      "type": "list of str",
      "description": "Actions not taken or things said/not said"
    },
    {
      "name": "missed_opportunities",
      "type": "list of str",
      "description": "Missed chances or possibilities"
    },
    {
      "name": "lessons_from_regrets",
      "type": "list of str",
      "description": "Insights gained from regrets"
    },
    {
      "name": "hindsight_realizations",
      "type": "list of str",
      "description": "Things you later realized you should have done"
    },
    {
      "name": "guilt_or_remorse",
      "type": "str",
      "description": "Feelings of shame, guilt or remorse"
    },
    {
      "name": "attempts_to_make_amends",
      "type": "list of str",
      "description": "Efforts to rectify mistakes or apologize"
    },
    {
      "name": "rumination",
      "type": "str",
      "description": "How much you dwelled on regrets or what-ifs"
    },
    {
      "name": "accountability_avoidance",
      "type": "list of str",
      "description": "Ways you justified or avoided responsibility"
    },
    {
      "name": "forgiveness_actions",
      "type": "list of str",
      "description": "Steps taken to forgive yourself or others"
    },
    {
      "name": "wisdom_from_experience",
      "type": "list of str",
      "description": "Life lessons to apply going forward"
    },
    {
      "name": "goals_set",
      "type": "list of str",
      "description": "Goals inspired by the memory"
    },
    {
      "name": "future_plans",
      "type": "list of str",
      "description": "Plans made as a result of the memory"
    },
    {
      "name": "aspirations_ignited",
      "type": "list of str",
      "description": "Hopes, dreams, or ambitions sparked"
    },
    {
      "name": "motivation_levels",
      "type": "str",
      "description": "How motivated you felt to pursue your aspirations"
    },
    {
      "name": "potential_roadblocks",
      "type": "list of str",
      "description": "Anticipated challenges or obstacles"
    },
    {
      "name": "skill_development_needs",
      "type": "list of str",
      "description": "Abilities or expertise to be developed"
    },
    {
      "name": "envisioned_lifestyle",
      "type": "str",
      "description": "Your imagined way of life in the future"
    },
    {
      "name": "bucket_list_adventures",
      "type": "list of str",
      "description": "Once-in-a-lifetime experiences desired"
    },
    {
      "name": "legacy_building",
      "type": "str",
      "description": "Thoughts on what you want your life's legacy to be"
    },
    {
      "name": "world_change_ambitions",
      "type": "list of str",
      "description": "Hopes for making the world a better place"
    },
    {
      "name": "actions_taken",
      "type": "list of str",
      "description": "Specific actions you took"
    },
    {
      "name": "goals_achieved",
      "type": "list of str",
      "description": "Goals you successfully completed"
    },
    {
      "name": "failures_experienced",
      "type": "list of str",
      "description": "Instances where you did not reach your goals"
    },
    {
      "name": "lessons_from_failures",
      "type": "list of str",
      "description": "What you learned from setbacks"
    },
    {
      "name": "strategies_for_improvement",
      "type": "list of str",
      "description": "Plans to do things differently in the future"
    },
    {
      "name": "observed_paradoxes",
      "type": "list of str",
      "description": "Situations that seem illogical or contradictory"
    },
    {
      "name": "internal_conflicts",
      "type": "list of str",
      "description": "Conflicting desires, beliefs, or values within yourself"
    },
    {
      "name": "resolution_attempts",
      "type": "list of str",
      "description": "Efforts to make sense of or resolve the paradoxes"
    },
    {
      "name": "puzzling_events",
      "type": "list of str",
      "description": "Events that remain unexplained or mysterious"
    },
    {
      "name": "unanswered_questions",
      "type": "list of str",
      "description": "Questions about the experience you still have"
    },
    {
      "name": "open_possibilities",
      "type": "list of str",
      "description": "Potential future developments or outcomes"
    },
    {
      "name": "internal_contradictions",
      "type": "list of str",
      "description": "Conflicting thoughts or feelings you had about the event"
    },
    {
      "name": "inconsistencies_observed",
      "type": "list of str",
      "description": "Things that did not add up or made you question the experience"
    },
    {
      "name": "emotional_dissonance",
      "type": "list of str",
      "description": "Feelings of confusion, unease, or discomfort"
    },
    {
      "name": "smells_experienced",
      "type": "list of str",
      "description": "Significant or memorable scents"
    },
    {
      "name": "sounds_heard",
      "type": "list of str",
      "description": "Noises or music that stood out"
    },
    {
      "name": "tastes_savored",
      "type": "list of str",
      "description": "Unique or interesting flavors"
    },
    {
      "name": "visual_impressions",
      "type": "list of str",
      "description": "Vivid details about what you saw"
    },
    {
      "name": "physical_touch",
      "type": "list of str",
      "description": "Feelings of touch (softness, roughness, temperature, etc.)"
    },
    {
      "name": "relationship_status",
      "type": "str",
      "description": "Your relationship with the people present"
    },
    {
      "name": "social_interactions",
      "type": "list of str",
      "description": "Detailed descriptions of conversations or interactions"
    },
    {
      "name": "group_dynamics",
      "type": "str",
      "description": "How the group interacted with each other"
    },
    {
      "name": "power_dynamics",
      "type": "str",
      "description": "Who had more influence or authority"
    },
    {
      "name": "conflicts_or_disagreements",
      "type": "list of str",
      "description": "Any arguments or tension"
    },
    {
      "name": "self_awareness_insights",
      "type": "list of str",
      "description": "New things you learned about yourself"
    },
    {
      "name": "personal_challenges",
      "type": "list of str",
      "description": "Obstacles you faced in your own growth"
    },
    {
      "name": "positive_changes_made",
      "type": "list of str",
      "description": "Improvements or changes in your behavior, beliefs, or habits"
    },
    {
      "name": "negative_impacts",
      "type": "list of str",
      "description": "How the experience affected you negatively"
    },
    {
      "name": "growth_opportunities",
      "type": "list of str",
      "description": "Future steps to continue your personal development"
    },
    {
      "name": "ambient_temperature",
      "type": "str",
      "description": "How warm or cold it was"
    },
    {
      "name": "lighting_conditions",
      "type": "str",
      "description": "Brightness, darkness, or specific light sources"
    },
    {
      "name": "architectural_features",
      "type": "str",
      "description": "Significant aspects of the building or space"
    },
    {
      "name": "natural_elements",
      "type": "list of str",
      "description": "Trees, water, animals, etc."
    },
    {
      "name": "atmospheric_conditions",
      "type": "str",
      "description": "Wind, rain, fog, etc."
    },
    {
      "name": "paranormal_occurrences",
      "type": "list of str",
      "description": "Any unexplained or potentially supernatural events"
    },
    {
      "name": "hallucinations_or_delusions",
      "type": "list of str",
      "description": "Experiences that were not real but felt real"
    },
    {
      "name": "altered_states_of_consciousness",
      "type": "str",
      "description": "Meditation, drug use, or other altered states"
    },
    {
      "name": "synchronicity",
      "type": "list of str",
      "description": "Meaningful coincidences or coincidental events"
    },
    {
      "name": "dreams_within_dreams",
      "type": "list of str",
      "description": "Dreams that felt like they were happening within other dreams"
    },
    {
      "name": "time_of_day",
      "type": "str",
      "description": "Morning, afternoon, evening, night"
    },
    {
      "name": "length_of_experience",
      "type": "str",
      "description": "How long the memory lasted"
    },
    {
      "name": "sense_of_time",
      "type": "str",
      "description": "Whether time seemed to move faster or slower"
    },
    {
      "name": "past_life_connections",
      "type": "list of str",
      "description": "Feelings of d�j? vu or being connected to a past life"
    },
    {
      "name": "inspirations_for_art",
      "type": "list of str",
      "description": "How the experience sparked creative ideas"
    },
    {
      "name": "artistic_techniques_used",
      "type": "list of str",
      "description": "Specific methods or styles you used to create art"
    },
    {
      "name": "artworks_created",
      "type": "list of str",
      "description": "Details about the art that resulted from the memory"
    },
    {
      "name": "critical_reception_of_art",
      "type": "list of str",
      "description": "Feedback or reactions to your art"
    },
    {
      "name": "communication_methods_used",
      "type": "list of str",
      "description": "Phone, email, text, etc."
    },
    {
      "name": "social_media_engagement",
      "type": "str",
      "description": "How you used social media"
    },
    {
      "name": "online_platforms_used",
      "type": "list of str",
      "description": "Websites, apps, or online tools"
    },
    {
      "name": "digital_artifacts_created",
      "type": "list of str",
      "description": "Photos, videos, or digital content produced"
    },
    {
      "name": "energy_levels",
      "type": "str",
      "description": "How energized or depleted you felt"
    },
    {
      "name": "mental_clarity",
      "type": "str",
      "description": "Your level of focus and mental sharpness"
    },
    {
      "name": "spiritual_energy",
      "type": "str",
      "description": "Feelings of connection to something beyond the physical"
    },
    {
      "name": "intuitive_insights",
      "type": "list of str",
      "description": "Gut feelings or intuitive understandings"
    },

    {
      "name": "human relationships",
      "type": "list of str",
      "description": "human relationships"
    },

    {
      "name": "actions_reactions",
      "type": "list of str",
      "description": "human relationships"
    },

    {
      "name": "inner_peace",
      "type": "str",
      "description": "Feelings of calmness and serenity"
   },]
}


categories = {
    "Actions and Results": {
        "past": ["Actions Taken", "Results Observed"],
        "present": ["Current Actions", "Ongoing Results"],
        "future": ["Planned Actions", "Anticipated Results"]
    },
    "Things": {
        "past": ["Objects Encountered", "Places Visited", "Concepts Learned"],
        "present": ["Current Objects", "Current Location", "Concepts Applied"],
        "future": ["Desired Objects", "Planned Locations", "Future Applications"]
    },
    "OwnState": {
        "past": ["Emotional State", "Physical State", "Mental State", "Spiritual State"],
        "present": ["Current Emotional State", "Current Physical State", "Current Mental State", "Current Spiritual State"],
        "future": ["Anticipated Emotional State", "Desired Physical State", "Expected Mental State", "Spiritual Goals"]
    },
    "Paradoxes and Contradictions": {
        "past": ["Past Paradoxes", "Past Internal Conflicts", "Past Cognitive Dissonance"],
        "present": ["Current Paradoxes", "Ongoing Internal Conflicts", "Current Cognitive Dissonance"],
        "future": ["Potential Paradoxes", "Expected Internal Conflicts", "Strategies to Address Dissonance"]
    },
    "Living Things": {
        "past": ["Past Human Interactions", "Past Animal Encounters", "Past Nature Experiences"],
        "present": ["Current Relationships", "Current Animal Interactions", "Current Nature Experiences"],
        "future": ["Future Relationships", "Anticipated Animal Encounters", "Planned Nature Experiences"]
    }
}


categories = {
    "Actions and Results": {
        "past": ["Actions Taken", "Results Observed"],
        "present": ["Current Actions", "Ongoing Results"],
        "future": ["Planned Actions", "Anticipated Results"]
    },
    "Things": {
        "past": ["Objects Encountered", "Places Visited", "Concepts Learned"],
        "present": ["Current Objects", "Current Location", "Concepts Applied"],
        "future": ["Desired Objects", "Planned Locations", "Future Applications"]
    },
    "OwnState": {
        "past": ["Emotional State", "Physical State", "Mental State", "Spiritual State"],
        "present": ["Current Emotional State", "Current Physical State", "Current Mental State", "Current Spiritual State"],
        "future": ["Anticipated Emotional State", "Desired Physical State", "Expected Mental State", "Spiritual Goals"]
    },
    "Paradoxes and Contradictions": {
        "past": ["Past Paradoxes", "Past Internal Conflicts", "Past Cognitive Dissonance"],
        "present": ["Current Paradoxes", "Ongoing Internal Conflicts", "Current Cognitive Dissonance"],
        "future": ["Potential Paradoxes", "Expected Internal Conflicts", "Strategies to Address Dissonance"]
    },
    "Living Things": {
        "past": ["Past Human Interactions", "Past Animal Encounters", "Past Nature Experiences"],
        "present": ["Current Relationships", "Current Animal Interactions", "Current Nature Experiences"],
        "future": ["Future Relationships", "Anticipated Animal Encounters", "Planned Nature Experiences"]
    }
}

# Shared Subcategories (Universal)

shared_subcategories = [
    "Intensity",
    "Duration",
    "Frequency",
    "Significance",
    "Emotional Impact",
    "Triggers",
    "Connections",
    "Lessons Learned",
    "Actions Taken",
    "Future Implications"
]


categories = [
    "Events", "Actions", "Concepts", "People", "Places",
    "Emotions", "Relationships", "Objects", "Time", "Space",
    "Sounds", "Colors", "Tastes", "Smells", "Textures",
    "Body Parts", "Animals", "Plants", "Materials", "Tools",
    "Buildings", "Transportation", "Food", "Clothing", "Technology",
    "Arts", "Sports", "Games", "Education", "Health",
    "Nature", "Weather", "Geography", "History", "Culture",
    "Politics", "Economics", "Science", "Technology", "Society",
    "Language", "Communication", "Logic", "Mathematics", "Philosophy",
    "Religion", "Spirituality", "Mythology", "Literature", "Music",
    "Art", "Design", "Fashion", "Entertainment", "Media",
    "Law", "Justice", "Crime", "War", "Peace",
    "Love", "Hate", "Fear", "Joy", "Sadness",
    "Family", "Friendship", "Community", "Society", "World",

    # Expanding upon the original categories
    "Personal Events", "Social Events", "Natural Events", "Historical Events", "Cultural Events",
    "Physical Actions", "Mental Actions", "Social Actions", "Work Actions", "Travel Actions",
    "Abstract Concepts", "Social Concepts", "Philosophical Concepts", "Scientific Concepts", "Technological Concepts",
    "Family Members", "Friends", "Professionals", "Community Members", "Historical Figures",
    "Cities", "Countries", "Continents", "Landforms", "Bodies of Water",
    "Happiness", "Anger", "Surprise", "Disgust", "Shame",
    "Romantic Relationships", "Family Relationships", "Friendships", "Professional Relationships",
    "Social Relationships",
    "Furniture", "Electronics", "Vehicles", "Clothing", "Jewelry",
    "Past", "Present", "Future", "Seasons", "Time Periods",
    "Direction", "Distance", "Location", "Dimensions", "Coordinates",
    "Music Genres", "Musical Instruments", "Music Theory", "Composers", "Musicians",
    "Painting", "Sculpture", "Photography", "Film", "Architecture",
    "Sports Teams", "Sports Rules", "Sports Equipment", "Athletes", "Coaches",
    "Board Games", "Card Games", "Video Games", "Puzzles", "Role-Playing Games",
    "Schools", "Universities", "Libraries", "Museums", "Research Institutions",
    "Medicine", "Nutrition", "Fitness", "Mental Health", "Wellness",
    "Forests", "Deserts", "Oceans", "Mountains", "Rivers",
    "Weather Patterns", "Climate Change", "Natural Disasters", "Environmental Issues", "Sustainability",
    "Ancient History", "Medieval History", "Modern History", "Contemporary History", "World History",
    "Culinary Traditions", "Art Forms", "Festivals", "Belief Systems", "Social Customs",
    "Political Systems", "Government", "Laws", "Politics", "Ideologies",
    "Economy", "Business", "Finance", "Trade", "Globalization",
    "Biology", "Chemistry", "Physics", "Astronomy", "Mathematics",
    "Software", "Hardware", "Artificial Intelligence", "Robotics", "Nanotechnology",
    "Social Issues", "Inequality", "Poverty", "Racism", "Gender Equality",
    "Grammar", "Vocabulary", "Phonology", "Morphology", "Syntax",
    "Communication Skills", "Public Speaking", "Writing", "Negotiation", "Conflict Resolution",
    "Reasoning", "Deduction", "Induction", "Critical Thinking", "Problem Solving",
    "Numbers", "Equations", "Geometry", "Algebra", "Calculus",
    "Ethics", "Morality", "Values", "Meaning", "Purpose",
    "Theism", "Atheism", "Agnosticism", "Spirituality", "Mysticism",
    "Myths", "Legends", "Folklore", "Fairy Tales", "Epic Poems",
    "Novels", "Short Stories", "Poetry", "Drama", "Nonfiction",
    "Classical Music", "Jazz", "Rock", "Pop", "Electronic Music",
    "Painting Styles", "Sculpture Styles", "Architectural Styles", "Design Trends", "Fashion Trends",
    "Movies", "TV Shows", "Music Videos", "Video Games", "Theater",
    "Legal Systems", "Crimes", "Punishments", "Justice", "Law Enforcement",
    "Warfare", "Peacekeeping", "Conflict Resolution", "Human Rights", "International Relations",
    "Friendship", "Love", "Marriage", "Family", "Community",
    "Happiness", "Sadness", "Anger", "Fear", "Anxiety",
    "Culture", "Society", "Community", "Identity", "Values",
    "Global Issues", "Climate Change", "Poverty", "Disease", "Conflict",

    # Expanding on specific areas
    "Types of Events", "Event Planning", "Event Management",
    "Types of Actions", "Action Verbs", "Action Phrases",
    "Types of Concepts", "Conceptual Thinking", "Abstract Reasoning",
    "Types of People", "Personality Traits", "Human Behavior",
    "Types of Places", "Geography", "Urban Planning",
    "Types of Emotions", "Emotional Intelligence", "Emotional Regulation",
    "Types of Relationships", "Relationship Dynamics", "Communication Skills",
    "Types of Objects", "Material Science", "Design",
    "Types of Time", "Chronology", "Time Management",
    "Types of Space", "Dimensions", "Coordinate Systems",
    "Types of Sounds", "Acoustics", "Music Theory",
    "Types of Colors", "Color Theory", "Color Psychology",
    "Types of Tastes", "Culinary Arts", "Food Science",
    "Types of Smells", "Aromatherapy", "Perfume",
    "Types of Textures", "Material Science", "Sensory Perception",
    "Types of Body Parts", "Anatomy", "Physiology",
    "Types of Animals", "Zoology", "Animal Behavior",
    "Types of Plants", "Botany", "Plant Ecology",
    "Types of Materials", "Material Science", "Engineering",
    "Types of Tools", "Technology", "Engineering",
    "Types of Buildings", "Architecture", "Urban Design",
    "Types of Transportation", "Automotive Engineering", "Aerospace Engineering",
    "Types of Food", "Culinary Arts", "Nutrition",
    "Types of Clothing", "Fashion Design", "Textile Industry",
    "Types of Technology", "Computer Science", "Engineering",
    "Types of Arts", "Art History", "Art Theory",
    "Types of Sports", "Sports Science", "Exercise Physiology",
    "Types of Games", "Game Design", "Game Theory",
    "Types of Education", "Educational Psychology", "Curriculum Development",
    "Types of Health", "Medicine", "Public Health",
    "Types of Nature", "Ecology", "Environmental Science",
    "Types of Weather", "Meteorology", "Climate Science",
    "Types of Geography", "Cartography", "Geographic Information Systems",
    "Types of History", "Historiography", "Historical Research",
    "Types of Culture", "Anthropology", "Sociology",
    "Types of Politics", "Political Science", "International Relations",
    "Types of Economics", "Microeconomics", "Macroeconomics",
    "Types of Science", "Scientific Method", "Research",
    "Types of Technology", "Computer Science", "Engineering",
    "Types of Society", "Sociology", "Social Psychology",
    "Types of Language", "Linguistics", "Language Acquisition",
    "Types of Communication", "Communication Theory", "Interpersonal Communication",
    "Types of Logic", "Formal Logic", "Informal Logic",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Theology", "Religious Studies",
    "Types of Spirituality", "Mysticism", "Meditation",
    "Types of Mythology", "Mythology", "Folklore",
    "Types of Literature", "Literary Theory", "Critical Analysis",
    "Types of Music", "Music Theory", "Music History",
    "Types of Art", "Art History", "Art Criticism",
    "Types of Design", "Design Thinking", "User Experience Design",
    "Types of Fashion", "Fashion History", "Fashion Design",
    "Types of Entertainment", "Media Studies", "Entertainment Industry",
    "Types of Media", "Journalism", "Public Relations",
    "Types of Law", "Legal Studies", "Jurisprudence",
    "Types of Justice", "Criminal Justice", "Social Justice",
    "Types of Crime", "Criminology", "Forensic Science",
    "Types of War", "Military History", "International Relations",
    "Types of Peace", "Peace Studies", "Conflict Resolution",
    "Types of Love", "Romantic Love", "Platonic Love",
    "Types of Hate", "Prejudice", "Discrimination",
    "Types of Fear", "Phobias", "Anxiety Disorders",
    "Types of Joy", "Happiness", "Well-being",
    "Types of Sadness", "Grief", "Depression",
    "Types of Family", "Family Dynamics", "Parenting",
    "Types of Friendship", "Friendship Dynamics", "Social Support",
    "Types of Community", "Community Development", "Social Networks",
    "Types of Society", "Sociology", "Social Stratification",
    "Types of World", "Global Issues", "International Relations",

    # More specific examples
    "Sports Leagues", "Sports Championships", "Sports Records",
    "Types of Music", "Music Genres", "Musical Instruments",
    "Types of Art", "Art Styles", "Art Movements",
    "Types of Food", "Cuisine", "Recipes",
    "Types of Technology", "Gadgets", "Software",
    "Types of Buildings", "Architecture Styles", "City Planning",
    "Types of Vehicles", "Cars", "Airplanes", "Trains",
    "Types of Clothing", "Fashion Trends", "Textile Production",
    "Types of Animals", "Wildlife", "Domesticated Animals",
    "Types of Plants", "Flowers", "Trees", "Vegetables",
    "Types of Weather", "Climate Change", "Natural Disasters",
    "Types of History", "Ancient History", "Medieval History", "Modern History",
    "Types of Culture", "Traditions", "Customs", "Festivals",
    "Types of Politics", "Political Systems", "Ideologies",
    "Types of Economics", "Markets", "Trade", "Finance",
    "Types of Science", "Physics", "Chemistry", "Biology",
    "Types of Technology", "Computers", "Internet", "Artificial Intelligence",
    "Types of Society", "Social Class", "Culture", "Values",
    "Types of Language", "Grammar", "Vocabulary", "Phonology",
    "Types of Communication", "Verbal Communication", "Nonverbal Communication",
    "Types of Logic", "Deductive Reasoning", "Inductive Reasoning",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Christianity", "Islam", "Buddhism",
    "Types of Spirituality", "Meditation", "Yoga", "Mysticism",
    "Types of Mythology", "Greek Mythology", "Roman Mythology", "Norse Mythology",
    "Types of Literature", "Poetry", "Fiction", "Nonfiction",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Art", "Painting", "Sculpture", "Photography", "Film",
    "Types of Design", "Graphic Design", "Web Design", "Industrial Design",
    "Types of Fashion", "Streetwear", "High Fashion", "Couture",
    "Types of Entertainment", "Movies", "TV Shows", "Video Games",
    "Types of Media", "News", "Social Media", "Advertising",
    "Types of Law", "Criminal Law", "Civil Law", "International Law",
    "Types of Justice", "Criminal Justice", "Social Justice",
    "Types of Crime", "Violent Crime", "Property Crime", "White-Collar Crime",
    "Types of War", "World War II", "Cold War", "Civil Wars",
    "Types of Peace", "Peace Treaties", "Peace Movements", "Nonviolent Resistance",
    "Types of Love", "Romantic Love", "Platonic Love", "Familial Love",
    "Types of Hate", "Racism", "Sexism", "Homophobia",
    "Types of Fear", "Phobias", "Anxiety", "Panic Attacks",
    "Types of Joy", "Happiness", "Gratitude", "Contentment",
    "Types of Sadness", "Grief", "Depression", "Loneliness",
    "Types of Family", "Nuclear Family", "Extended Family", "Blended Family",
    "Types of Friendship", "Casual Friendships", "Close Friendships", "Best Friends",
    "Types of Community", "Rural Communities", "Urban Communities", "Online Communities",
    "Types of Society", "Capitalist Societies", "Socialist Societies", "Communist Societies",
    "Types of World", "Global Issues", "Climate Change", "Poverty", "Disease",
    "Types of Jobs", "Professions", "Careers", "Industries", "Occupations",
    "Types of Education", "Formal Education", "Informal Education", "Higher Education",
    "Types of Health", "Physical Health", "Mental Health", "Social Health",
    "Types of Nature", "Ecosystems", "Biodiversity", "Conservation",
    "Types of Weather", "Temperature", "Precipitation", "Wind",
    "Types of Geography", "Landforms", "Bodies of Water", "Climate Zones",
    "Types of History", "Ancient History", "Medieval History", "Modern History",
    "Types of Culture", "Art", "Music", "Literature", "Food",
    "Types of Politics", "Democracy", "Republic", "Monarchy",
    "Types of Economics", "Capitalism", "Socialism", "Communism",
    "Types of Science", "Physics", "Chemistry", "Biology", "Astronomy",
    "Types of Technology", "Computers", "Internet", "Artificial Intelligence",
    "Types of Society", "Social Class", "Culture", "Values",
    "Types of Language", "Grammar", "Vocabulary", "Phonology",
    "Types of Communication", "Verbal Communication", "Nonverbal Communication",
    "Types of Logic", "Deductive Reasoning", "Inductive Reasoning",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Christianity", "Islam", "Buddhism",
    "Types of Spirituality", "Meditation", "Yoga", "Mysticism",
    "Types of Mythology", "Greek Mythology", "Roman Mythology", "Norse Mythology",
    "Types of Literature", "Poetry", "Fiction", "Nonfiction",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Art", "Painting", "Sculpture", "Photography", "Film",
    "Types of Design", "Graphic Design", "Web Design", "Industrial Design",
    "Types of Fashion", "Streetwear", "High Fashion", "Couture",
    "Types of Entertainment", "Movies", "TV Shows", "Video Games",
    "Types of Media", "News", "Social Media", "Advertising",
    "Types of Law", "Criminal Law", "Civil Law", "International Law",
    "Types of Justice", "Criminal Justice", "Social Justice",
    "Types of Crime", "Violent Crime", "Property Crime", "White-Collar Crime",
    "Types of War", "World War II", "Cold War", "Civil Wars",
    "Types of Peace", "Peace Treaties", "Peace Movements", "Nonviolent Resistance",
    "Types of Love", "Romantic Love", "Platonic Love", "Familial Love",
    "Types of Hate", "Racism", "Sexism", "Homophobia",
    "Types of Fear", "Phobias", "Anxiety", "Panic Attacks",
    "Types of Joy", "Happiness", "Gratitude", "Contentment",
    "Types of Sadness", "Grief", "Depression", "Loneliness",
    "Types of Family", "Nuclear Family", "Extended Family", "Blended Family",
    "Types of Friendship", "Casual Friendships", "Close Friendships", "Best Friends",
    "Types of Community", "Rural Communities", "Urban Communities", "Online Communities",
    "Types of Society", "Capitalist Societies", "Socialist Societies", "Communist Societies",
    "Types of World", "Global Issues", "Climate Change", "Poverty", "Disease",
    "Types of Travel", "Adventure Travel", "Luxury Travel", "Backpacking",
    "Types of Cuisine", "Italian Cuisine", "French Cuisine", "Indian Cuisine",
    "Types of Art", "Abstract Art", "Surrealism", "Impressionism",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Sports", "Team Sports", "Individual Sports", "Extreme Sports",
    "Types of Technology", "Computers", "Mobile Devices", "Artificial Intelligence",
    "Types of Science", "Biology", "Chemistry", "Physics", "Astronomy",
    "Types of History", "Ancient History", "Medieval History", "Modern History",
    "Types of Culture", "Art", "Music", "Literature", "Food", "Religion",
    "Types of Politics", "Democracy", "Republic", "Monarchy",
    "Types of Economics", "Capitalism", "Socialism", "Communism",
    "Types of Society", "Social Class", "Culture", "Values",
    "Types of Language", "Grammar", "Vocabulary", "Phonology",
    "Types of Communication", "Verbal Communication", "Nonverbal Communication",
    "Types of Logic", "Deductive Reasoning", "Inductive Reasoning",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Christianity", "Islam", "Buddhism",
    "Types of Spirituality", "Meditation", "Yoga", "Mysticism",
    "Types of Mythology", "Greek Mythology", "Roman Mythology", "Norse Mythology",
    "Types of Literature", "Poetry", "Fiction", "Nonfiction",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Art", "Painting", "Sculpture", "Photography", "Film",
    "Types of Design", "Graphic Design", "Web Design", "Industrial Design",
    "Types of Fashion", "Streetwear", "High Fashion", "Couture",
    "Types of Entertainment", "Movies", "TV Shows", "Video Games",
    "Types of Media", "News", "Social Media", "Advertising",
    "Types of Law", "Criminal Law", "Civil Law", "International Law",
    "Types of Justice", "Criminal Justice", "Social Justice",
    "Types of Crime", "Violent Crime", "Property Crime", "White-Collar Crime",
    "Types of War", "World War II", "Cold War", "Civil Wars",
    "Types of Peace", "Peace Treaties", "Peace Movements", "Nonviolent Resistance",
    "Types of Love", "Romantic Love", "Platonic Love", "Familial Love",
    "Types of Hate", "Racism", "Sexism", "Homophobia",
    "Types of Fear", "Phobias", "Anxiety", "Panic Attacks",
    "Types of Joy", "Happiness", "Gratitude", "Contentment",
    "Types of Sadness", "Grief", "Depression", "Loneliness",
    "Types of Family", "Nuclear Family", "Extended Family", "Blended Family",
    "Types of Friendship", "Casual Friendships", "Close Friendships", "Best Friends",
    "Types of Community", "Rural Communities", "Urban Communities", "Online Communities",
    "Types of Society", "Capitalist Societies", "Socialist Societies", "Communist Societies",
    "Types of World", "Global Issues", "Climate Change", "Poverty", "Disease",
    "Types of Jobs", "Professions", "Careers", "Industries", "Occupations",
    "Types of Education", "Formal Education", "Informal Education", "Higher Education",
    "Types of Health", "Physical Health", "Mental Health", "Social Health",
    "Types of Nature", "Ecosystems", "Biodiversity", "Conservation",
    "Types of Weather", "Temperature", "Precipitation", "Wind",
    "Types of Geography", "Landforms", "Bodies of Water", "Climate Zones",
    "Types of History", "Ancient History", "Medieval History", "Modern History",
    "Types of Culture", "Art", "Music", "Literature", "Food", "Religion",
    "Types of Politics", "Democracy", "Republic", "Monarchy",
    "Types of Economics", "Capitalism", "Socialism", "Communism",
    "Types of Society", "Social Class", "Culture", "Values",
    "Types of Language", "Grammar", "Vocabulary", "Phonology",
    "Types of Communication", "Verbal Communication", "Nonverbal Communication",
    "Types of Logic", "Deductive Reasoning", "Inductive Reasoning",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Christianity", "Islam", "Buddhism",
    "Types of Spirituality", "Meditation", "Yoga", "Mysticism",
    "Types of Mythology", "Greek Mythology", "Roman Mythology", "Norse Mythology",
    "Types of Literature", "Poetry", "Fiction", "Nonfiction",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Art", "Painting", "Sculpture", "Photography", "Film",
    "Types of Design", "Graphic Design", "Web Design", "Industrial Design",
    "Types of Fashion", "Streetwear", "High Fashion", "Couture",
    "Types of Entertainment", "Movies", "TV Shows", "Video Games",
    "Types of Media", "News", "Social Media", "Advertising",
    "Types of Law", "Criminal Law", "Civil Law", "International Law",
    "Types of Justice", "Criminal Justice", "Social Justice",
    "Types of Crime", "Violent Crime", "Property Crime", "White-Collar Crime",
    "Types of War", "World War II", "Cold War", "Civil Wars",
    "Types of Peace", "Peace Treaties", "Peace Movements", "Nonviolent Resistance",
    "Types of Love", "Romantic Love", "Platonic Love", "Familial Love",
    "Types of Hate", "Racism", "Sexism", "Homophobia",
    "Types of Fear", "Phobias", "Anxiety", "Panic Attacks",
    "Types of Joy", "Happiness", "Gratitude", "Contentment",
    "Types of Sadness", "Grief", "Depression", "Loneliness",
    "Types of Family", "Nuclear Family", "Extended Family", "Blended Family",
    "Types of Friendship", "Casual Friendships", "Close Friendships", "Best Friends",
    "Types of Community", "Rural Communities", "Urban Communities", "Online Communities",
    "Types of Society", "Capitalist Societies", "Socialist Societies", "Communist Societies",
    "Types of World", "Global Issues", "Climate Change", "Poverty", "Disease",
    "Types of Jobs", "Professions", "Careers", "Industries", "Occupations",
    "Types of Education", "Formal Education", "Informal Education", "Higher Education",
    "Types of Health", "Physical Health", "Mental Health", "Social Health",
    "Types of Nature", "Ecosystems", "Biodiversity", "Conservation",
    "Types of Weather", "Temperature", "Precipitation", "Wind",
    "Types of Geography", "Landforms", "Bodies of Water", "Climate Zones",
    "Types of History", "Ancient History", "Medieval History", "Modern History",
    "Types of Culture", "Art", "Music", "Literature", "Food", "Religion",
    "Types of Politics", "Democracy", "Republic", "Monarchy",
    "Types of Economics", "Capitalism", "Socialism", "Communism",
    "Types of Society", "Social Class", "Culture", "Values",
    "Types of Language", "Grammar", "Vocabulary", "Phonology",
    "Types of Communication", "Verbal Communication", "Nonverbal Communication",
    "Types of Logic", "Deductive Reasoning", "Inductive Reasoning",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Christianity", "Islam", "Buddhism",
    "Types of Spirituality", "Meditation", "Yoga", "Mysticism",
    "Types of Mythology", "Greek Mythology", "Roman Mythology", "Norse Mythology",
    "Types of Literature", "Poetry", "Fiction", "Nonfiction",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Art", "Painting", "Sculpture", "Photography", "Film",
    "Types of Design", "Graphic Design", "Web Design", "Industrial Design",
    "Types of Fashion", "Streetwear", "High Fashion", "Couture",
    "Types of Entertainment", "Movies", "TV Shows", "Video Games",
    "Types of Media", "News", "Social Media", "Advertising",
    "Types of Law", "Criminal Law", "Civil Law", "International Law",
    "Types of Justice", "Criminal Justice", "Social Justice",
    "Types of Crime", "Violent Crime", "Property Crime", "White-Collar Crime",
    "Types of War", "World War II", "Cold War", "Civil Wars",
    "Types of Peace", "Peace Treaties", "Peace Movements", "Nonviolent Resistance",
    "Types of Love", "Romantic Love", "Platonic Love", "Familial Love",
    "Types of Hate", "Racism", "Sexism", "Homophobia",
    "Types of Fear", "Phobias", "Anxiety", "Panic Attacks",
    "Types of Joy", "Happiness", "Gratitude", "Contentment",
    "Types of Sadness", "Grief", "Depression", "Loneliness",
    "Types of Family", "Nuclear Family", "Extended Family", "Blended Family",
    "Types of Friendship", "Casual Friendships", "Close Friendships", "Best Friends",
    "Types of Community", "Rural Communities", "Urban Communities", "Online Communities",
    "Types of Society", "Capitalist Societies", "Socialist Societies", "Communist Societies",
    "Types of World", "Global Issues", "Climate Change", "Poverty", "Disease",
    "Types of Jobs", "Professions", "Careers", "Industries", "Occupations",
    "Types of Education", "Formal Education", "Informal Education", "Higher Education",
    "Types of Health", "Physical Health", "Mental Health", "Social Health",
    "Types of Nature", "Ecosystems", "Biodiversity", "Conservation",
    "Types of Weather", "Temperature", "Precipitation", "Wind",
    "Types of Geography", "Landforms", "Bodies of Water", "Climate Zones",
    "Types of History", "Ancient History", "Medieval History", "Modern History",
    "Types of Culture", "Art", "Music", "Literature", "Food", "Religion",
    "Types of Politics", "Democracy", "Republic", "Monarchy",
    "Types of Economics", "Capitalism", "Socialism", "Communism",
    "Types of Society", "Social Class", "Culture", "Values",
    "Types of Language", "Grammar", "Vocabulary", "Phonology",
    "Types of Communication", "Verbal Communication", "Nonverbal Communication",
    "Types of Logic", "Deductive Reasoning", "Inductive Reasoning",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Christianity", "Islam", "Buddhism",
    "Types of Spirituality", "Meditation", "Yoga", "Mysticism",
    "Types of Mythology", "Greek Mythology", "Roman Mythology", "Norse Mythology",
    "Types of Literature", "Poetry", "Fiction", "Nonfiction",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Art", "Painting", "Sculpture", "Photography", "Film",
    "Types of Design", "Graphic Design", "Web Design", "Industrial Design",
    "Types of Fashion", "Streetwear", "High Fashion", "Couture",
    "Types of Entertainment", "Movies", "TV Shows", "Video Games",
    "Types of Media", "News", "Social Media", "Advertising",
    "Types of Law", "Criminal Law", "Civil Law", "International Law",
    "Types of Justice", "Criminal Justice", "Social Justice",
    "Types of Crime", "Violent Crime", "Property Crime", "White-Collar Crime",
    "Types of War", "World War II", "Cold War", "Civil Wars",
    "Types of Peace", "Peace Treaties", "Peace Movements", "Nonviolent Resistance",
    "Types of Love", "Romantic Love", "Platonic Love", "Familial Love",
    "Types of Hate", "Racism", "Sexism", "Homophobia",
    "Types of Fear", "Phobias", "Anxiety", "Panic Attacks",
    "Types of Joy", "Happiness", "Gratitude", "Contentment",
    "Types of Sadness", "Grief", "Depression", "Loneliness",
    "Types of Family", "Nuclear Family", "Extended Family", "Blended Family",
    "Types of Friendship", "Casual Friendships", "Close Friendships", "Best Friends",
    "Types of Community", "Rural Communities", "Urban Communities", "Online Communities",
    "Types of Society", "Capitalist Societies", "Socialist Societies", "Communist Societies",
    "Types of World", "Global Issues", "Climate Change", "Poverty", "Disease",
    "Types of Jobs", "Professions", "Careers", "Industries", "Occupations",
    "Types of Education", "Formal Education", "Informal Education", "Higher Education",
    "Types of Health", "Physical Health", "Mental Health", "Social Health",
    "Types of Nature", "Ecosystems", "Biodiversity", "Conservation",
    "Types of Weather", "Temperature", "Precipitation", "Wind",
    "Types of Geography", "Landforms", "Bodies of Water", "Climate Zones",
    "Types of History", "Ancient History", "Medieval History", "Modern History",
    "Types of Culture", "Art", "Music", "Literature", "Food", "Religion",
    "Types of Politics", "Democracy", "Republic", "Monarchy",
    "Types of Economics", "Capitalism", "Socialism", "Communism",
    "Types of Society", "Social Class", "Culture", "Values",
    "Types of Language", "Grammar", "Vocabulary", "Phonology",
    "Types of Communication", "Verbal Communication", "Nonverbal Communication",
    "Types of Logic", "Deductive Reasoning", "Inductive Reasoning",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Christianity", "Islam", "Buddhism",
    "Types of Spirituality", "Meditation", "Yoga", "Mysticism",
    "Types of Mythology", "Greek Mythology", "Roman Mythology", "Norse Mythology",
    "Types of Literature", "Poetry", "Fiction", "Nonfiction",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Art", "Painting", "Sculpture", "Photography", "Film",
    "Types of Design", "Graphic Design", "Web Design", "Industrial Design",
    "Types of Fashion", "Streetwear", "High Fashion", "Couture",
    "Types of Entertainment", "Movies", "TV Shows", "Video Games",
    "Types of Media", "News", "Social Media", "Advertising",
    "Types of Law", "Criminal Law", "Civil Law", "International Law",
    "Types of Justice", "Criminal Justice", "Social Justice",
    "Types of Crime", "Violent Crime", "Property Crime", "White-Collar Crime",
    "Types of War", "World War II", "Cold War", "Civil Wars",
    "Types of Peace", "Peace Treaties", "Peace Movements", "Nonviolent Resistance",
    "Types of Love", "Romantic Love", "Platonic Love", "Familial Love",
    "Types of Hate", "Racism", "Sexism", "Homophobia",
    "Types of Fear", "Phobias", "Anxiety", "Panic Attacks",
    "Types of Joy", "Happiness", "Gratitude", "Contentment",
    "Types of Sadness", "Grief", "Depression", "Loneliness",
    "Types of Family", "Nuclear Family", "Extended Family", "Blended Family",
    "Types of Friendship", "Casual Friendships", "Close Friendships", "Best Friends",
    "Types of Community", "Rural Communities", "Urban Communities", "Online Communities",
    "Types of Society", "Capitalist Societies", "Socialist Societies", "Communist Societies",
    "Types of World", "Global Issues", "Climate Change", "Poverty", "Disease",
    "Types of Jobs", "Professions", "Careers", "Industries", "Occupations",
    "Types of Education", "Formal Education", "Informal Education", "Higher Education",
    "Types of Health", "Physical Health", "Mental Health", "Social Health",
    "Types of Nature", "Ecosystems", "Biodiversity", "Conservation",
    "Types of Weather", "Temperature", "Precipitation", "Wind",
    "Types of Geography", "Landforms", "Bodies of Water", "Climate Zones",
    "Types of History", "Ancient History", "Medieval History", "Modern History",
    "Types of Culture", "Art", "Music", "Literature", "Food", "Religion",
    "Types of Politics", "Democracy", "Republic", "Monarchy",
    "Types of Economics", "Capitalism", "Socialism", "Communism",
    "Types of Society", "Social Class", "Culture", "Values",
    "Types of Language", "Grammar", "Vocabulary", "Phonology",
    "Types of Communication", "Verbal Communication", "Nonverbal Communication",
    "Types of Logic", "Deductive Reasoning", "Inductive Reasoning",
    "Types of Mathematics", "Algebra", "Geometry", "Calculus",
    "Types of Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Types of Religion", "Christianity", "Islam", "Buddhism",
    "Types of Spirituality", "Meditation", "Yoga", "Mysticism",
    "Types of Mythology", "Greek Mythology", "Roman Mythology", "Norse Mythology",
    "Types of Literature", "Poetry", "Fiction", "Nonfiction",
    "Types of Music", "Classical Music", "Jazz", "Rock", "Pop",
    "Types of Art", "Painting", "Sculpture", "Photography", "Film",
    "Types of Design", "Graphic Design", "Web Design", "Industrial Design",
    "Types of Fashion", "Streetwear", "High Fashion", "Couture",
    "Types of Entertainment", "Movies", "TV Shows", "Video Games",
    "Types of Media", "News", "Social Media", "Advertising"]