# Django File Sharing System

A simple and efficient file sharing system built with Django and Tailwind CSS that allows users to upload multiple files and share them via a generated zip file download link.

## Features

- 📤 Multiple file upload support
- 🔗 Automatic shareable link generation
- 📦 Automatic ZIP file creation
- 📱 Responsive UI with Tailwind CSS
- 🔄 Real-time upload progress
- 📋 One-click link copying

## Security Features

- User Authentication Required for Uploads
- Secure File Handling
- Automatic File Cleanup
- Short UIDs for Privacy
- CSRF Protection
- Protected Download Links


## Tech Stack

- Django 
- Django REST Framework
- Tailwind CSS
- Python

## Installation and Setup

1. Clone the repository
```bash
git clone https://github.com/yogeshsharma11/File-Sharing-System.git
cd File-Sharing-System
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create necessary directories
```bash
mkdir -p public/static
```

5. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to start using the application.

## Usage

1. **Upload Files**
   - Drag and drop files or click to select files
   - Click "Upload Files" button
   - Copy the generated sharing link

2. **Download Files**
   - Open the shared link
   - Click "Download ZIP" to get all files

## Project Structure

```
File-Sharing-System/
├── app/
│   ├── migrations/
│   │   └── __init__.py
│   ├── management/
│   │   └── commands/
│   │       └── cleanup_folders.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── Fileshare/
│   
```

## Security Features

- User Authentication Required for Uploads
- Secure File Handling
- Automatic File Cleanup
- Short UIDs for Privacy
- CSRF Protection
- Protected Download Links

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository.
