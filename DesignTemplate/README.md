# 🎨 Code Playground - Social Snippet Sharing Platform

A Django-based web platform for creating, sharing, and discovering HTML/CSS/JavaScript code snippets with a focus on social interaction and learning.

## 📋 Table of Contents
- [Overview](#overview)
- [Current Features](#current-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## 🎯 Overview

Code Playground is a **social platform for web developers** to:
- Create and edit HTML, CSS, and JavaScript snippets in a Monaco-powered editor
- Share their work with the community through a public feed
- Discover and fork snippets from other developers
- Build a portfolio of code snippets with social engagement metrics
- Learn from others through code inspection and remixing

**Think of it as:** CodePen meets GitHub for quick web experiments and social learning.

## ✨ Current Features

### 🖊️ Code Editor
- **Monaco Editor Integration**: Full-featured code editor with syntax highlighting
- **Live Preview**: Real-time rendering of HTML/CSS/JS output
- **Multi-Language Support**: Separate editors for HTML, CSS, and JavaScript
- **Environment Support**: 2D web and 3D (Three.js) rendering environments
- **Auto-Save**: Snippets saved via AJAX to prevent data loss

### 👤 User Management
- **Authentication**: Sign up, login, and Google OAuth integration
- **User Profiles**: Personal profile pages with activity tracking
- **Activity Dashboard**: Track daily snippet creation and engagement
- **Avatar Support**: Custom user avatars and bio information

### 📱 Social Features
- **Public Feed**: Discover latest snippets from the community
- **Like System**: Like snippets to show appreciation
- **Fork Functionality**: Clone and remix other users' code
- **View Tracking**: Analytics for snippet popularity
- **Comments**: [Implemented in backend, UI pending]
- **Copy Code**: Easy one-click copy for HTML, CSS, and JS tabs

### 🎨 Snippet Management
- **CRUD Operations**: Create, Read, Update, and Delete your snippets
- **Slug Generation**: SEO-friendly URLs auto-generated from titles
- **Tagging System**: Categorize snippets with custom tags
- **Privacy Controls**: Public/private visibility settings
- **Fork Lineage**: Track which snippets were forked from others
- **Code Display**: Tabbed interface showing HTML, CSS, and JavaScript source

### 🔍 Discovery & Search
- **Feed Filtering**: Filter by environment (2D/3D) and tags
- **Popular Tags**: Quick access to trending categories
- **User Profiles**: Browse all snippets by a specific creator

## 🛠️ Tech Stack

### Backend
- **Django 5.x**: Python web framework
- **SQLite/PostgreSQL**: Database (SQLite for dev, PostgreSQL for production)
- **Django Authentication**: Built-in auth with custom user model
- **Django REST Framework**: [Potential for API expansion]

### Frontend
- **HTML5 + CSS3**: Core markup and styling
- **JavaScript (ES6+)**: Client-side interactivity
- **Monaco Editor**: VSCode's editor for the web
- **Fetch API**: AJAX requests for dynamic updates
- **Three.js** (optional): 3D rendering support

### Styling
- **Custom CSS**: Hand-crafted dark theme
- **GitHub-inspired Dark Mode**: Professional, modern UI
- **Responsive Design**: Mobile-friendly layouts
- **Glassmorphism Effects**: Modern visual aesthetics

## 📁 Project Structure

```
DesignTemplate/
├── accounts/               # User authentication & profiles
│   ├── models.py          # Custom User model, Activity tracking
│   ├── views.py           # Login, signup, profile views
│   ├── forms.py           # Custom auth forms
│   └── templates/         # Auth & profile templates
├── playground/            # Core snippet functionality
│   ├── models.py          # Snippet, Like, View, Comment models
│   ├── views.py           # Editor, feed, detail views
│   ├── urls.py            # URL routing
│   ├── static/            # CSS, JS, images
│   └── templates/         # Editor, feed, detail templates
├── static/                # Collected static files
├── media/                 # User uploads (avatars, thumbnails)
├── templates/             # Base templates
├── manage.py              # Django management script
└── db.sqlite3             # Development database
```

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DesignTemplate
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver 4000
   ```

8. **Access the application**
   - Homepage: `http://localhost:4000/`
   - Admin: `http://localhost:4000/admin/`

## 💡 Usage

### Creating a Snippet
1. Sign up or log in
2. Click "Create" in the navigation bar
3. Write your HTML, CSS, and JavaScript code
4. Preview updates in real-time
5. Add a title and tags
6. Click "Save" to publish

### Editing a Snippet
1. Navigate to your snippet's detail page
2. Click the "Edit" button (visible only to owner)
3. Make your changes in the editor
4. Click "Save" to update

### Deleting a Snippet
1. Go to your snippet's detail page
2. Click the red "Delete" button
3. Confirm the deletion in the dialog
4. Snippet is permanently removed

### Forking a Snippet
1. Find a snippet you like
2. Click the "Fork" button
3. Snippet is cloned to your account
4. Make your modifications in the editor

### Copying Code
1. View any snippet detail page
2. Use the tabs (HTML/CSS/JavaScript) to switch between code
3. Click the "Copy" button for the code you want
4. Paste into your own editor

## 🔮 Future Enhancements

### Planned Features
- [ ] **Search Functionality**: Full-text search across snippets
- [ ] **Collections**: Group related snippets into collections
- [ ] **Embed Snippets**: Share snippets via iframe embeds
- [ ] **Code Templates**: Starter templates for common patterns
- [ ] **Syntax Themes**: Customizable editor color schemes
- [ ] **Keyboard Shortcuts**: Power-user editor shortcuts
- [ ] **Version History**: Track changes to snippets over time
- [ ] **Collaboration**: Real-time collaborative editing
- [ ] **Competitions**: Weekly coding challenges
- [ ] **Badges & Achievements**: Gamification for engagement

### Technical Improvements
- [ ] **REST API**: Full API for third-party integrations
- [ ] **CDN Integration**: Faster static asset delivery
- [ ] **Caching**: Redis for performance optimization
- [ ] **Auto-Thumbnails**: Screenshot generation for snippets
- [ ] **Code Linting**: Real-time error detection
- [ ] **Testing Suite**: Unit and integration tests
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **PostgreSQL Migration**: Production-ready database
- [ ] **Docker Support**: Containerized deployment

### UI/UX Enhancements
- [ ] **Comment System UI**: Frontend for existing comment backend
- [ ] **Notification System**: Real-time alerts for likes, forks, comments
- [ ] **Advanced Filtering**: Sort by popularity, date, environment
- [ ] **Infinite Scroll**: Smoother feed browsing
- [ ] **Dark/Light Mode Toggle**: User preference for themes
- [ ] **Accessibility**: WCAG 2.1 AA compliance
- [ ] **Mobile App**: React Native companion app

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue describing the problem
2. **Suggest Features**: Share your ideas in the issues
3. **Submit Pull Requests**: Fork, create a branch, and submit PR
4. **Improve Documentation**: Help make the docs clearer
5. **Write Tests**: Add test coverage for existing features

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Comment complex logic
- Test your changes before submitting
- Keep commits atomic and well-described

## 📝 License

[Specify your license - e.g., MIT, GPL, etc.]

## 👨‍💻 Author

Created with ❤️ by [Your Name]

## 🙏 Acknowledgments

- Monaco Editor by Microsoft
- Django Framework by Django Software Foundation
- Three.js by Mr.doob and contributors
- Inspiration from CodePen, JSFiddle, and GitHub

---

**Status**: 🚀 Active Development  
**Version**: 1.0.0  
**Last Updated**: December 2025
