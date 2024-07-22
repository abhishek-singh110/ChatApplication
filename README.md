# Interest Messaging and Real-Time Chat Application

This Django application allows users to send interest messages to each other, accept or reject interests, and engage in real-time chat if the interest is accepted. The project utilizes Django Channels for WebSocket communication to enable real-time messaging.

## Features

1. **User Authentication**: Users can register and log in.
2. **Sending Interests**: Logged-in users can browse a list of other users and send interest messages.
3. **Accepting/Rejecting Interests**: Users can view received interest messages and accept or reject them.
4. **Real-Time Chat**: If an interest is accepted, users can chat with each other in real-time.

## Setup

### Prerequisites

- Python 3.12.2
- Django 5.0.7
- Django Channels 4.1.0

### Installation

1. Clone the repository:

   - git clone https://github.com/yourusername/interest-messaging-chat-app.git
   - cd ChatApplication


2. Create and activate the virtual environment:

   - python -m venv venv
   - source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3. Install the required packages:

   - pip install -r requirements.txt
   - install redis on your machine and start the redis-server

4. Run database migrations:

   - python manage.py makemigrations
   - python manage.py migrate

5. Access the application:

   - Open your web browser and navigate to http://127.0.0.1:8000/.

6. Register and log in:

   - Register a new user account.
   - Log in with the newly created account.


7. Send and manage interests:

   - Browse users and send interest messages.
   - View received interests on bell icon and accept or reject them.


8. Chat in real-time:

   - Accept an interest to enable the chat feature.
   - Start chatting in real-time with the other user.


## Notes

 - Currently, when an interest message is sent, notification is displayed on the notification icon. This is    
   intentional and for confirmation purposes and on the notification icon you can perform the Accept/Reject action. But when the user chats then we are not displaying the notification.

 - If you would like additional features or improvements, I am open to making this application much better if necessary.



