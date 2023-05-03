## Product design(Cli tool)

we can design a CLI tool for your word-learning software with the following functionalities and interactions:

* User Management:

1. register: Create a new account by providing a username, email, and password.
Example usage: wordly register --username JohnDoe --email john@example.com --password MySecret123

2. login: Authenticate an existing user with their email and password.
Example usage: wordly login --email john@example.com --password MySecret123

3. forgot-password: Send a password reset email to the user.
Example usage: wordly forgot-password --email john@example.com

4. feedback: Submit user feedback on the application.
Example usage: wordly feedback --message "I love this app!"

* Word Learning:

5. learn-next word: Learn a new word, displaying pronunciation, definition, example sentences, and part of speech.
Example usage: wordly learn --word "example"

6. random: Learn a random word from the database.
Example usage: wordly random

* Progress Tracking:

7. progress: Display the number of words learned, completion status, and study duration.
Example usage: wordly progress

8. history: List all the words previously learned by the user.
Example usage: wordly history

9. Example usage: wordly learn --help