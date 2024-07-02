## creative_loop.py

class CreativeLoop():
    def __init__(self, ai_system):
        super().__init__(ai_system)

    def execute(self, current_state):
        print("Creative Loop executing...")
        creative_model = self.ai_system.models['creative'] 

        prompt = "Give me a story idea about a time traveler who meets their younger self."
        response = creative_model.send_message({"role":"user", "content": prompt}).last_message().text
        print("Story Idea:", response)



