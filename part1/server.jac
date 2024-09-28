walker interact {
    can return_message with `root entry {
        report {
            "response": "Hello, world!"
        };
    }
}

walker interact_with_body {
    has name: str;

    can return_message with `root entry {
        report {
            "response": "Hello, " + self.name + "!"
        };
    }
}

walker interact_with_age {
    has name: str;
    has age: int;

    can return_message with `root entry {
        report {
            "response": "Hello, " + self.name + "! You are " + str(self.age) + " years old."
        };
    }
}

walker interact_with_favorites {
    has name: str;
    has favorite_food: str;

    can return_message with `root entry {
        report {
            "response": "Hello, " + self.name + "! Your favorite food is " + self.favorite_food + "."
        };
    }
}