class FocusManager:
    def __init__(self):
        self.focus_stack = []

    def push_focus(self, focus_item):
        self.focus_stack.append(focus_item)
        print(f"other pushed: {focus_item}")

    def pop_focus(self):
        if self.focus_stack:
            popped_item = self.focus_stack.pop()
            print(f"other popped: {popped_item}")
            return popped_item
        else:
            print("other stack is empty.")
            return None

    def get_current_focus(self):
        if self.focus_stack:
            return self.focus_stack[-1]
        else:
            print("other stack is empty.")
            return None