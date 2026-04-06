from dataclasses import dataclass

class AFSM:
    # Атрибуты класса (общие для всех экземпляров)
    admin_states = {}
    all_states = ["default", "add_category", "add_product_text", "add_product_photo",
                  "add_product_link", "add_video", "add_video_category", "add_video_title",
                  "add_video_description", "add_recipe_category", "add_recipe_title",
                  "add_recipe_description", "add_recipe_video", "enter_text_message",
                  "add_photo_messages", "add_raffle_text", "add_raffle_photo", "set_video_ds", "set_video_name","set_recipe_ds", "set_recipe_name",
                  "add_vcategoryy", "add_rcategoryy"]
    ddict = {}

    def __init__(self):
        # Ничего не переопределяем, используем классовые атрибуты
        pass

    def new_admin(self, admin_id):
        self.__class__.admin_states[admin_id] = "default"
        self.__class__.ddict[admin_id] = {}

    def set_state(self, admin_id, new_state):
        if new_state in self.__class__.all_states:
            self.__class__.admin_states[admin_id] = new_state

    def get_state(self, admin_id):
        return self.__class__.admin_states.get(admin_id, "default")

    def append_dict(self, admin_id, key, value):
        if admin_id not in self.__class__.ddict:
            self.__class__.ddict[admin_id] = {}
        self.__class__.ddict[admin_id][key] = value

    def get_dict(self, admin_id):
        return self.__class__.ddict.get(admin_id, {})

    def clear_dict(self, admin_id):
        if admin_id in self.__class__.ddict:
            self.__class__.ddict[admin_id] = {}

class UFSM:
    # Атрибуты класса (общие для всех экземпляров)
    user_states = {}
    all_states = ["default", "input_weight", "input_height", "input_age", "input_srid"]
    ddict = {}

    def __init__(self):
        pass

    def new_user(self, user_id):
        self.__class__.user_states[user_id] = "default"
        self.__class__.ddict[user_id] = {}

    def set_state(self, user_id, new_state):
        if new_state in self.__class__.all_states:
            self.__class__.user_states[user_id] = new_state

    def get_state(self, user_id):
        return self.__class__.user_states.get(user_id, "default")

    def append_dict(self, user_id, key, value):
        if user_id not in self.__class__.ddict:
            self.__class__.ddict[user_id] = {}
        self.__class__.ddict[user_id][key] = value

    def get_dict(self, user_id):
        return self.__class__.ddict.get(user_id, {})

    def clear_dict(self, user_id):
        if user_id in self.__class__.ddict:
            self.__class__.ddict[user_id] = {}