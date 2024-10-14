# AI-Generated Guided Meditation Web App

## Project Overview

The AI-Generated Guided Meditation Web App is a SaaS-based platform designed to provide personalized meditation experiences. Utilizing AI-generated content, the app allows users to select meditation categories, receive dynamic scripts, and listen to them. Additionally, it features an admin interface for managing meditations and categories, ensuring a comprehensive and customizable meditation experience.

## Features

- **User Dashboard**: 
  - Modify your profile to tailor the meditation experience.
  - View and review your previous meditation history.
  - Replay past sessions and visualize your meditation sessions via heatmaps.

- **Gamification**: 
  - Earn badges as rewards for staying engaged, enhancing user retention and motivation.

- **Meditation Options**: 
  - Access both AI-generated meditations and static meditations for a diverse experience.

- **Feedback System**: 
  - Provide feedback after sessions to help improve the app and personalize future content.

- **Chatbot**: 
  - Interact with a chatbot that offers predefined questions for guidance and support.

- **Monetization**: 
  - Support the app by tipping or buying a coffee through the "Buy Me a Coffee" feature.

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/meditation-app.git
   cd meditation-app
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key and Google Cloud credentials:
     ```
     OPENAI_API_KEY=your_openai_api_key
     GOOGLE_APPLICATION_CREDENTIALS=path_to_your_google_credentials.json
     ```

## Database Setup

- Ensure you have a MySQL database set up.
- Import the provided SQL schema to set up the necessary tables.

## Usage

1. **Run the Application**:
   ```bash
   flask run
   ```

2. **Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:5000`.

3. **Admin Access**:
   - Navigate to `/admin` to access the admin dashboard.
   - Manage meditations and categories through the admin interface.

## API Information

- **AI Content Generation**: Utilizes OpenAI's GPT-3.5 for generating meditation scripts.
- **Text-to-Speech Conversion**: Uses Google Cloud Text-to-Speech for audio synthesis.

## Monetization Feature

- **Buy Me a Coffee**: Users can support the app financially by buying a coffee, helping sustain and improve the service.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to OpenAI for providing the GPT-3.5 model.
- Google Cloud for Text-to-Speech services.
- All contributors who have helped improve the app.

