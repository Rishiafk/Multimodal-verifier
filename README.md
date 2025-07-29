# 🔥 Multimodal Claim-Evidence Verifier

A sophisticated web application that uses AI to verify claims against provided evidence. Built with Flask and powered by Cohere's Command-R model, this tool provides intelligent analysis of claim-evidence relationships with a stunning dark theme UI.

## ✨ Features

- **AI-Powered Verification**: Uses Cohere's Command-R model for intelligent claim analysis
- **Three-Tier Classification**: Supports, Partially Supports, or Not Supported verdicts
- **Detailed Explanations**: Provides clear reasoning for each verification result
- **Beautiful UI**: Dark theme with glowing effects and smooth animations
- **Real-time Processing**: Instant results with responsive design
- **Error Handling**: Graceful error handling with user-friendly messages

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Cohere API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multimodal-verifier.git
   cd multimodal-verifier
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open your browser**
   
   Navigate to `http://127.0.0.1:5000`

## 📖 Usage

1. **Enter a Statement**: Type or paste the statement you want to verify in the "Statement to Verify" field
2. **Provide Evidence**: Enter the evidence that supports or refutes the statement in the "Supporting Evidence" field
3. **Submit for Analysis**: Click the "Check" button to process your submission
4. **Review Results**: View the AI-generated verdict and explanation
5. **Reset**: Use the "Reset" button to clear the form and start over

### Example Usage

**Statement**: "Climate change is primarily caused by human activities"

**Evidence**: "Multiple peer-reviewed studies show that CO2 emissions from fossil fuel burning have increased atmospheric CO2 levels by 40% since pre-industrial times, and climate models consistently attribute recent warming to human activities."

**Expected Result**: The AI would likely classify this as "Supported" with an explanation of how the evidence strongly supports the statement.

## 🏗️ Project Structure

```
multimodal-verifier/
├── run.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── static/
│   └── styles.css        # CSS styling with dark theme
├── templates/
│   └── index.html        # Main HTML template
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

- `COHERE_API_KEY`: Your Cohere API key (required)

### Model Configuration

The application uses Cohere's Command-R model with the following settings:
- **Model**: `command-r`
- **Temperature**: 0.3 (for consistent results)
- **Max Tokens**: 300 (for concise responses)

## 🎨 UI Features

- **Dark Theme**: Elegant dark background with red accents
- **Glowing Effects**: Animated buttons with pulsing effects
- **Responsive Design**: Works on desktop and mobile devices
- **Smooth Animations**: Sparkle effects and hover animations
- **Color-coded Results**: Different colors for different verdict types

## 🛠️ Dependencies

- **Flask**: Web framework for the application
- **Cohere**: AI model for claim verification
- **python-dotenv**: Environment variable management
- **sentence-transformers**: Text processing (if needed for future features)
- **torch**: PyTorch for machine learning capabilities

## 🔍 How It Works

1. **Input Processing**: The application receives claim and evidence text from the user
2. **Prompt Engineering**: Creates a structured prompt for the AI model
3. **AI Analysis**: Sends the prompt to Cohere's Command-R model
4. **Response Parsing**: Extracts verdict and explanation from the AI response
5. **Result Display**: Shows the results with appropriate styling

## 🚧 Error Handling

The application handles various error scenarios:
- **API Errors**: Network issues or invalid API keys
- **Parsing Errors**: Malformed AI responses
- **Missing Input**: Form validation for required fields

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Cohere**: For providing the AI model API
- **Flask**: For the web framework
- **CSS Animations**: For the beautiful UI effects

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/multimodal-verifier/issues) page
2. Create a new issue with detailed information
3. Include your Python version and error messages

## 🔮 Future Enhancements

- [ ] Support for file uploads (PDF, images)
- [ ] Batch processing of multiple claims
- [ ] Export results to PDF/CSV
- [ ] User authentication and history
- [ ] API endpoint for programmatic access
- [ ] Integration with other AI models

---

**Made with ❤️ and ☕ by Rishi Kumar** 
